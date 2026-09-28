# -*- coding: utf-8 -*-
"""自备教材 PDF 导入自测：生成 2 页教材 PDF → 上传 → 轮询任务 → 验证清理"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
import uuid

from PIL import Image, ImageDraw, ImageFont

BASE = 'http://127.0.0.1:8016'


def http(method, url, data=None, headers=None, timeout=60):
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode('utf-8')
            return r.status, json.loads(body) if body else None
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, body


def make_pdf(path):
    import fitz
    font = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 34)
    bold = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 50)
    pages = [
        ('第一单元 万以内的加法和减法', ['1. 口算两位数加两位数', '例：35 + 48 = 83', '先把相同数位对齐再相加', '2. 三位数加三位数', '笔算加法：从个位加起，哪一位满十向前一位进一']),
        ('第二单元 除数是一位数的除法', ['1. 口算整十数除以一位数', '例：60 ÷ 3 = 20', '2. 笔算除法', '从被除数的高位除起，除到哪一位商就写在哪一位上面', '3. 有余数的除法', '余数一定要比除数小']),
    ]
    doc = fitz.open()
    for title, lines in pages:
        img = Image.new('RGB', (1600, 2200), 'white')
        d = ImageDraw.Draw(img)
        d.text((120, 120), title, font=bold, fill=(0, 0, 0))
        y = 320
        for ln in lines:
            d.text((120, y), ln, font=font, fill=(30, 30, 30))
            y += 110
        p = 'page_tmp.png'
        img.save(p)
        page = doc.new_page(width=595, height=842)
        page.insert_image(page.rect, filename=p)
        os.remove(p)
    doc.save(path)
    doc.close()
    print('pdf saved:', path, os.path.getsize(path), 'bytes')


def upload(pdf_path):
    boundary = '----selftest' + uuid.uuid4().hex
    body = b''
    for k, v in [('subject', '\u6570\u5b66'), ('grade', '\u4e09\u5e74\u7ea7'), ('semester', '\u4e0a\u518c')]:
        body += ('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (boundary, k, v)).encode('utf-8')
    body += ('--%s\r\nContent-Disposition: form-data; name="file"; filename="textbook.pdf"\r\nContent-Type: application/pdf\r\n\r\n' % boundary).encode('utf-8')
    with open(pdf_path, 'rb') as f:
        body += f.read()
    body += ('\r\n--%s--\r\n' % boundary).encode('utf-8')
    st, d = http('POST', BASE + '/api/textbook/user-pdf-import',
                 data=body, headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}, timeout=120)
    print('POST /user-pdf-import ->', st, json.dumps(d, ensure_ascii=False))
    return d.get('task_id') if isinstance(d, dict) else None


def poll(task_id, timeout=240):
    t0 = time.time()
    last = None
    while time.time() - t0 < timeout:
        st, d = http('GET', BASE + f'/api/textbook/task/{task_id}', timeout=30)
        if st != 200:
            print('task err', st, d); return None
        last = d
        print(f"[{d.get('progress')}%] {d.get('stage')} {d.get('message')} status={d.get('status')}")
        if d.get('status') in ('done', 'failed'):
            return d
        time.sleep(4)
    print('timeout'); return last


if __name__ == '__main__':
    pdf = os.path.join(r'backend\data\pdf_upload', 'selftest_book.pdf')
    os.makedirs(os.path.dirname(pdf), exist_ok=True)
    make_pdf(pdf)
    task_id = upload(pdf)
    res = poll(task_id) if task_id else None
    print('FINAL:', json.dumps(res, ensure_ascii=False))
    # 检查临时目录清理
    remain = [f for f in os.listdir(r'backend\data\pdf_upload') if f.startswith('upload_')]
    print('upload_ dirs remain:', remain)
    sys.exit(0 if res and res.get('status') in ('done', 'failed') else 1)
