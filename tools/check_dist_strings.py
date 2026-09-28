# -*- coding: utf-8 -*-
import glob

hits = {}
for p in glob.glob(r'frontend\dist\assets\*.js'):
    try:
        s = open(p, encoding='utf-8').read()
    except Exception:
        continue
    keys = [k for k in ['自备教材 PDF', '教材同步使用协议', '拍照教材同步',
                        'user-pdf-import', 'import-config', 'enable_user_pdf'] if k in s]
    if keys:
        hits[p.split('\\')[-1]] = keys
for k, v in hits.items():
    print(k, '->', v)
