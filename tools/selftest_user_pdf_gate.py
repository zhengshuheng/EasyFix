# -*- coding: utf-8 -*-
"""enable_user_pdf 门禁复测（带合法 multipart 文件）"""
import json
import os
import urllib.request
import urllib.error
import uuid

CFG = r'backend\textbook_import_config.json'
BASE = 'http://127.0.0.1:8016'


def post_pdf():
    boundary = '----gate' + uuid.uuid4().hex
    body = b''
    for k, v in [('subject', '\u6570\u5b66'), ('grade', '\u4e09\u5e74\u7ea7'), ('semester', '\u4e0a\u518c')]:
        body += ('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (boundary, k, v)).encode('utf-8')
    body += ('--%s\r\nContent-Disposition: form-data; name="file"; filename="x.pdf"\r\nContent-Type: application/pdf\r\n\r\n%%PDF-1.4-fake\r\n' % boundary).encode('utf-8')
    body += ('--%s--\r\n' % boundary).encode('utf-8')
    req = urllib.request.Request(BASE + '/api/textbook/user-pdf-import', data=body, method='POST',
                                 headers={'Content-Type': f'multipart/form-data; boundary={boundary}'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode('utf-8')[:200]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='replace')[:200]


with open(CFG, 'w', encoding='utf-8') as f:
    json.dump({'enable_online_ctsf': False, 'enable_online_pdf': False,
               'enable_photo': True, 'enable_user_pdf': False}, f, ensure_ascii=False)
print('user-pdf-import (disabled) ->', post_pdf())

with open(CFG, 'w', encoding='utf-8') as f:
    json.dump({'enable_online_ctsf': True, 'enable_online_pdf': True,
               'enable_photo': True, 'enable_user_pdf': True}, f, ensure_ascii=False)
print('restored all true')
