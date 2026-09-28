# -*- coding: utf-8 -*-
"""线下做题拍照交卷 —— 自测脚本

子命令：
  order [ps_id]                    校验「题号顺序」是否与打印出来的 PDF 一致
  fill  [ps_id] [out.png]          在练习集 PDF 上模拟手写作答，生成"线下做题照片"
  recog [ps_id] [out.png]          直接调 paper_ocr 识别照片，打印识别结果
  e2e   [ps_id] [out.png] [base]   走 HTTP：上传识别 → 自动交卷，打印结果

用法（在项目根目录）：
  .venv\\Scripts\\python.exe tools\\paper_ocr_e2e.py fill
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND = os.path.join(ROOT, "backend")
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

import urllib.request  # noqa: E402
import urllib.error  # noqa: E402

FAKE_HAND_FONT = "C:/Windows/Fonts/Inkfree.ttf"
MM = 72.0 / 25.4  # 1mm = 2.834pt


def get_db():
    from app.database import SessionLocal
    return SessionLocal()


def abs_pdf_path(ps):
    p = ps.pdf_path or ""
    if not p:
        return None
    p = p.replace("\\", "/")
    from app.config import get_settings
    upload_dir = get_settings().UPLOAD_DIR
    cand = [
        os.path.join(BACKEND, p),
        os.path.join(BACKEND, upload_dir, p),
        os.path.join(BACKEND, "uploads", p.lstrip("/")),
        p,
    ]
    for c in cand:
        if os.path.exists(c):
            return os.path.abspath(c)
    return None


def pick_practice_set(db, ps_id=None):
    from app.models import PracticeSet
    q = db.query(PracticeSet).filter(PracticeSet.deleted == False)  # noqa: E712
    if ps_id:
        return q.filter(PracticeSet.id == ps_id).first()
    sets = [s for s in q.order_by(PracticeSet.id.desc()).limit(30).all() if s.pdf_path]
    return sets[0] if sets else None


def fake_answer(no, qtype, idx_in_type):
    """造一个「学生写下的答案」"""
    t = qtype or "choice"
    if t == "choice":
        return "ABCD"[idx_in_type % 4]
    if t == "judge":
        return "√" if idx_in_type % 2 == 0 else "×"
    if t == "fill":
        opts = ["am", "is", "are", "a", "12", "30", "1/2", "0.5"]
        return opts[idx_in_type % len(opts)]
    if t == "calc":
        return f"{idx_in_type + 1}2+8=20"
    if t == "application":
        return "3+2=5，5个"
    if t in ("operation", "writing"):
        return "如图所示，画出一条线段"
    return "答案"


def cmd_order(ps_id=None):
    from app.routers.practice_set import load_practice_questions
    from app.services import paper_ocr
    import fitz

    db = get_db()
    ps = pick_practice_set(db, ps_id)
    if not ps:
        print("!! 没有找到带 PDF 的练习集")
        return
    pairs = load_practice_questions(db, ps.id)
    qs = [
        {"id": q.id, "parsed_question": q.parsed_question, "original_text": q.original_text,
         "question_type": q.question_type, "option_a": q.option_a, "option_b": q.option_b,
         "option_c": q.option_c, "option_d": q.option_d}
        for _psq, q in pairs
    ]
    ordered = paper_ocr.printed_order(qs)
    print(f"练习集 #{ps.id} {ps.name}  共 {len(pairs)} 题")

    pdf = abs_pdf_path(ps)
    if not pdf:
        print("!! 未找到 PDF 文件，跳过顺序校验")
        return
    doc = fitz.open(pdf)
    print(f"PDF: {os.path.basename(pdf)}  页数 {doc.page_count}")

    # 提取每个题号 "N." 的实际位置（左边距处的题号）
    positions = {}
    for pno in range(doc.page_count):
        for w in doc[pno].get_text("words"):
            x0, y0, x1, y1, text = w[0], w[1], w[2], w[3], w[4]
            t = text.strip()
            if t.endswith(".") and t[:-1].isdigit() and x0 < 60:
                n = int(t[:-1])
                if n not in positions:
                    positions[n] = (pno, round(y0, 1))
    doc.close()

    ok = True
    for idx, q in enumerate(ordered, 1):
        stem = (q["parsed_question"] or q["original_text"] or "")[:34].replace("\n", " ")
        pos = positions.get(idx)
        flag = ""
        if pos is None:
            flag = "  ← PDF 中未找到该题号"
            ok = False
        elif idx > 1 and positions.get(idx - 1) and pos < positions[idx - 1]:
            flag = "  ← 题号位置倒退"
            ok = False
        print(f"  {idx:>3}. [{q['question_type']}] {stem}{flag}")
    print("题号顺序校验：", "OK 一致" if ok else "FAIL 不一致")
    return ok


def render_and_fill(ps, out_png, mode="fake"):
    """渲染 PDF 并用"手写体"写上答案，返回 (图片路径, 造的答案 {no: text})"""
    import fitz
    from PIL import Image, ImageDraw, ImageFont
    from app.routers.practice_set import load_practice_questions
    from app.services import paper_ocr

    db = get_db()
    pairs = load_practice_questions(db, ps.id)
    qs = [
        {"id": q.id, "parsed_question": q.parsed_question, "original_text": q.original_text,
         "question_type": q.question_type, "option_a": q.option_a, "option_b": q.option_b,
         "option_c": q.option_c, "option_d": q.option_d}
        for _psq, q in pairs
    ]
    ordered = paper_ocr.printed_order(qs)
    pdf = abs_pdf_path(ps)
    if not pdf:
        raise SystemExit("!! 未找到 PDF")

    zoom = 2.0
    doc = fitz.open(pdf)
    pages = []
    for pno in range(doc.page_count):
        pix = doc[pno].get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        words = doc[pno].get_text("words")
        # 题号位置
        pos = {}
        for w in words:
            x0, y0, x1, y1, text = w[0], w[1], w[2], w[3], w[4]
            t = text.strip()
            if t.endswith(".") and t[:-1].isdigit() and x0 < 60:
                n = int(t[:-1])
                if n not in pos:
                    pos[n] = (x0, y0, y1)
        # 每题「题干最后一行的行尾」位置：答案就写在那儿（填空/选择在括号，主观题在书写区）
        ends = {}
        for n, (_x0, y0, _y1) in pos.items():
            later = [yy for yy in [v[1] for v in pos.values()] if yy > y0 + 1]
            band_end = min(later) if later else 1e9
            band = [w for w in words if y0 - 1 <= w[1] < band_end - 1 and w[0] > 60]
            if not band:
                ends[n] = (60.0, y0 + 14)
                continue
            max_y = max(w[3] for w in band)
            last = [w for w in band if w[3] >= max_y - 2]
            ends[n] = (max(w[2] for w in last), max_y)
        pages.append((img, pos, ends))
    doc.close()

    font = ImageFont.truetype(FAKE_HAND_FONT, int(13 * MM * zoom / 2.0) + 6)
    made = {}
    idx_in_type = {}
    for img, pos, ends in pages:
        draw = ImageDraw.Draw(img)
        for idx, q in enumerate(ordered, 1):
            if idx not in pos:
                continue
            t = q["question_type"] or "choice"
            idx_in_type[t] = idx_in_type.get(t, 0)
            ans = fake_answer(idx, t, idx_in_type[t])
            idx_in_type[t] += 1
            ex_pt, ey_pt = ends[idx]
            px = ex_pt * zoom + 6          # 题干末行行尾右侧
            py = ey_pt * zoom - 16         # 与末行同一行
            if px > 480 * zoom:            # 太靠右就换到下一行（书写区）
                px = 70 * zoom
                py = ey_pt * zoom + 14
            if mode == "fake":
                draw.text((px, py), ans, fill=(20, 30, 160), font=font)
                made[idx] = ans
    pages[0][0].save(out_png)
    if len(pages) > 1:
        pages[1][0].save(out_png.replace(".png", "_p2.png"))
    return out_png, made


def cmd_fill(ps_id=None, out="uploads/images/_e2e_filled.png"):
    db = get_db()
    ps = pick_practice_set(db, ps_id)
    path, made = render_and_fill(ps, out)
    print("已生成模拟手写照片:", path)
    print("造的答案:", json.dumps(made, ensure_ascii=False))


def cmd_recog(ps_id=None, img=None):
    from app.routers.practice_set import load_practice_questions
    from app.services import paper_ocr

    db = get_db()
    ps = pick_practice_set(db, ps_id)
    pairs = load_practice_questions(db, ps.id)
    qs = [
        {"id": q.id, "parsed_question": q.parsed_question, "original_text": q.original_text,
         "question_type": q.question_type, "option_a": q.option_a, "option_b": q.option_b,
         "option_c": q.option_c, "option_d": q.option_d}
        for _psq, q in pairs
    ]
    img = img or "uploads/images/_e2e_filled.png"
    res = paper_ocr.recognize_answers([os.path.abspath(img)], qs)
    print("provider:", res.get("provider"), res.get("model"))
    print("pages:", json.dumps(res.get("pages"), ensure_ascii=False))
    print("notes:", json.dumps(res.get("notes"), ensure_ascii=False))
    print("识别结果:")
    for a in res.get("answers", []):
        print(f"  no={a['no']:>3} qid={a['question_id']:>4} [{a['confidence']}] {a['answer']}")
    print("empty nos:", res.get("empty"))
    return res


def cmd_e2e(ps_id=None, img=None, base="http://127.0.0.1:8016", kid=None):
    img = os.path.abspath(img or "uploads/images/_e2e_filled.png")
    db = get_db()
    ps = pick_practice_set(db, ps_id)
    base = base.rstrip("/")

    # 1) 识别（multipart 上传）
    boundary = "----qwpboundary9x"
    with open(img, "rb") as f:
        content = f.read()
    body = b""
    body += f"--{boundary}\r\n".encode()
    body += b'Content-Disposition: form-data; name="files"; filename="paper.png"\r\n'
    body += b"Content-Type: image/png\r\n\r\n" + content + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        f"{base}/api/practice-sets/{ps.id}/recognize-paper", data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        rec = json.loads(r.read().decode())
    print(f"[识别] {rec['message']}")
    for q in rec["questions"]:
        print(f"  {q['no']:>3}. [{q.get('question_type')}] 识别={q['recognized_answer']!r} "
              f"({q.get('confidence')}) 题干={(q.get('question_text') or '')[:30]}")

    # 2) 交卷
    payload = {
        "answers": [{"question_id": q["question_id"], "answer": q["recognized_answer"]}
                    for q in rec["questions"] if q["recognized_answer"]],
        "images": rec.get("images", []),
        "auto_grade": True,
    }
    req = urllib.request.Request(
        f"{base}/api/practice-sets/{ps.id}/photo-submit",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=600) as r:
        sub = json.loads(r.read().decode())
    print(f"[交卷] {sub['message']} 批改 {sub['graded']}/{sub['total']} 题，"
          f"对 {sub['correct']} 错 {sub['wrong']}，正确率 {sub['accuracy']}%（{sub['graded_by']}）")
    for r_ in sub.get("results", []):
        print(f"  qid={r_.get('question_id')} is_correct={r_.get('is_correct')} "
              f"comment={(r_.get('comment') or '')[:40]}")
    if sub.get("unsupported"):
        print("  跳过:", json.dumps(sub["unsupported"], ensure_ascii=False))
    return rec, sub


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "order"
    a = sys.argv[2] if len(sys.argv) > 2 else None
    b = sys.argv[3] if len(sys.argv) > 3 else None
    c = sys.argv[4] if len(sys.argv) > 4 else None
    if cmd == "order":
        cmd_order(int(a) if a else None)
    elif cmd == "fill":
        cmd_fill(int(a) if a else None, b or "uploads/images/_e2e_filled.png")
    elif cmd == "recog":
        cmd_recog(int(a) if a else None, b)
    elif cmd == "e2e":
        cmd_e2e(int(a) if a else None, b, c or "http://127.0.0.1:8016")
    else:
        print(__doc__)
