# -*- coding: utf-8 -*-
"""临时探针：验证 OCR（多模态）链路是否可用。

用法（在 backend 目录下，用 .venv 解释器）：
    ..\.venv\Scripts\python.exe ..\tools\ocr_probe.py [pdf路径或图片路径]
"""
import os
import sys
import glob

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))
sys.path.insert(0, os.getcwd())

def render_pdf_page(pdf_path, out_png, page=0, zoom=2.0):
    import fitz  # PyMuPDF
    doc = fitz.open(pdf_path)
    pg = doc[page]
    mat = fitz.Matrix(zoom, zoom)
    pix = pg.get_pixmap(matrix=mat)
    pix.save(out_png)
    doc.close()
    return out_png


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    if target is None:
        pdfs = sorted(glob.glob("uploads/images/practice_sets/*.pdf"), key=os.path.getmtime)
        target = pdfs[-1]
    print("目标文件:", target)

    if target.lower().endswith(".pdf"):
        img = render_pdf_page(target, os.path.join("uploads", "images", "_probe_paper.png"))
        print("已渲染图片:", img, os.path.getsize(img), "bytes")
    else:
        img = target

    from app.services.ocr import ocr_service
    print("provider:", ocr_service.provider, "| available:", ocr_service.is_available)
    # 探测服务是否会真的加载 multimodal
    try:
        from app.services.multimodal_ocr import multimodal_ocr_service
        print("multimodal.provider:", multimodal_ocr_service.provider,
              "| available:", multimodal_ocr_service.is_available)
    except Exception as e:
        print("multimodal 探测失败:", e)

    if not ocr_service.is_available:
        print("!! OCR 不可用")
        return

    res = ocr_service.recognize(img)
    print("返回 keys:", list(res.keys()))
    text = res.get("full_text") or ""
    print("full_text 前 800 字:\n" + text[:800])
    blocks = res.get("blocks") or []
    print("blocks:", len(blocks))
    if res.get("error"):
        print("error:", res["error"])


if __name__ == "__main__":
    main()
