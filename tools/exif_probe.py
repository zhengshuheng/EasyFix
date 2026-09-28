# -*- coding: utf-8 -*-
"""验证手机照片的两个坑：EXIF 方向 + 超大尺寸（normalize_image 是否处理正确）

用法（项目根目录）：.venv\\Scripts\\python.exe tools\\exif_probe.py [练习集id]
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND = os.path.join(ROOT, "backend")
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from PIL import Image  # noqa: E402


def main():
    from app.services.paper_ocr import normalize_image, recognize_answers
    from app.routers.practice_set import load_practice_questions
    from app.database import SessionLocal
    from app.models import PracticeSet

    ps_id = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    db = SessionLocal()
    ps = db.query(PracticeSet).get(ps_id)
    pairs = load_practice_questions(db, ps_id)
    qs = [
        {"id": q.id, "parsed_question": q.parsed_question, "original_text": q.original_text,
         "question_type": q.question_type, "option_a": q.option_a, "option_b": q.option_b,
         "option_c": q.option_c, "option_d": q.option_d}
        for _psq, q in pairs
    ]

    src = "uploads/images/_e2e_filled.png"
    base = Image.open(src).convert("RGB")
    print(f"原图（基准）尺寸: {base.size}")

    # 模拟手机竖拍：像素转 90°，长边放大到 4032，EXIF Orientation=6（显示时需顺时针转回）
    pixels = base.rotate(90, expand=True)  # 逆时针转 90°，模拟"躺着存"的像素
    scale = 4032 / max(pixels.size)
    pixels = pixels.resize((int(pixels.width * scale), int(pixels.height * scale)), Image.LANCZOS)
    phone = "uploads/images/_e2e_phone.jpg"
    exif = Image.Exif()
    exif[274] = 6  # Orientation: Rotate 90 CW
    pixels.save(phone, "JPEG", quality=95, exif=exif, dpi=(72, 72))
    print(f"手机照片: {phone}  {os.path.getsize(phone)//1024} KB  像素尺寸={Image.open(phone).size} "
          f"EXIF Orientation={Image.open(phone).getexif().get(274)}")

    out = normalize_image(phone)
    after = Image.open(out)
    print(f"规范化后: {after.size}  长边<=2000: {max(after.size) <= 2000}  "
          f"方向已摆正(高>宽，与试卷一致: {base.size[1] > base.size[0]}): {after.size[1] > after.size[0]}")

    res = recognize_answers([os.path.abspath(out)], qs)
    print("规范化后 OCR 识别结果：")
    for a in res.get("answers", []):
        print(f"  no={a['no']} [{a['confidence']}] {a['answer']}")
    print("未识别(空白/漏读)题号:", res.get("empty"))
    print("页状态:", res.get("pages"))


if __name__ == "__main__":
    main()
