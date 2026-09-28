# -*- coding: utf-8 -*-
"""拍照导入自测：生成模拟教材页图片 + 上传识别"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

from PIL import Image, ImageDraw, ImageFont

BASE = 'http://127.0.0.1:8016'


def http_json(method, url, data=None, headers=None, timeout=60):
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


def gen_images():
    out = r'backend\data\photo_upload\selftest'
    os.makedirs(out, exist_ok=True)
    font = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 40)
    bold = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 56)
    pages = [
        ('第一单元 万以内的加法和减法', [
            '1. 口算两位数加两位数', '例：35 + 48 = 83',
            '先把相同数位对齐再相加', '2. 三位数加三位数',
            '笔算加法：从个位加起，哪一位满十向前一位进一',
            '3. 加法的验算方法', '用交换加数位置再加一遍来验算']),
        ('第二单元 除数是一位数的除法', [
            '1. 口算整十数除以一位数', '例：60 ÷ 3 = 20',
            '2. 笔算除法', '从被除数的高位除起，除到哪一位商就写在哪一位上面',
            '3. 有余数的除法', '余数一定要比除数小']),
    ]
    paths = []
    for i, (title, lines) in enumerate(pages):
        img = Image.new('RGB', (1600, 2200), 'white')
        d = ImageDraw.Draw(img)
        d.text((120, 120), title, font=bold, fill=(0, 0, 0))
        y = 320
        for ln in lines:
            d.text((120, y), ln, font=font, fill=(30, 30, 30))
            y += 110
        p = os.path.join(out, f'page_{i + 1}.jpg')
        img.save(p, quality=92)
        paths.append(p)
        print('saved', p, title)
    return paths


def photo_import(paths):
    import uuid
    boundary = '----selftest' + uuid.uuid4().hex
    body = b''
    for k, v in [('subject', '\u6570\u5b66'), ('grade', '\u4e09\u5e74\u7ea7'), ('semester', '\u4e0a\u518c')]:
        body += ('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (boundary, k, v)).encode('utf-8')
    for p in paths:
        fn = os.path.basename(p)
        with open(p, 'rb') as f:
            data = f.read()
        body += ('--%s\r\nContent-Disposition: form-data; name="files"; filename="%s"\r\nContent-Type: image/jpeg\r\n\r\n' % (boundary, fn)).encode('utf-8') + data + b'\r\n'
    body += ('--%s--\r\n' % boundary).encode('utf-8')
    headers = {'Content-Type': f'multipart/form-data; boundary={boundary}'}
    st, d = http_json('POST', BASE + '/api/textbook/photo-import', data=body, headers=headers, timeout=120)
    print('POST /photo-import ->', st, json.dumps(d, ensure_ascii=False))
    return d.get('task_id') if isinstance(d, dict) else None


def poll(task_id, timeout=300):
    t0 = time.time()
    last = None
    while time.time() - t0 < timeout:
        st, d = http_json('GET', BASE + f'/api/textbook/task/{task_id}', timeout=30)
        if st == 404:
            print('task 404'); return None
        last = d
        print(f"[{d.get('progress')}%] {d.get('stage')} {d.get('message')} status={d.get('status')}")
        if d.get('status') in ('done', 'failed'):
            return d
        time.sleep(4)
    print('timeout; last:', json.dumps(last, ensure_ascii=False))
    return last


if __name__ == '__main__':
    paths = gen_images()
    task_id = photo_import(paths)
    if task_id:
        res = poll(task_id)
        print('FINAL:', json.dumps(res, ensure_ascii=False))
        sys.exit(0 if res and res.get('status') == 'done' else 1)
    sys.exit(1)
