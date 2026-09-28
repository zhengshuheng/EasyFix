# -*- coding: utf-8 -*-
"""POST 门禁复测"""
import json
import urllib.request
import urllib.error

CFG = r'backend\textbook_import_config.json'
BASE = 'http://127.0.0.1:8016'


def post(url, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST',
                                 headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode('utf-8')[:200]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='replace')[:200]


with open(CFG, 'w', encoding='utf-8') as f:
    json.dump({'enable_online_ctsf': False, 'enable_online_pdf': False, 'enable_photo': True}, f, ensure_ascii=False)

print('ctsf/import POST ->', post(BASE + '/api/textbook/ctsf/import', {'subject': '数学', 'version': '人教版', 'grade': '三年级', 'semester': '上册'}))
print('pdf import POST  ->', post(BASE + '/api/textbook/import', {'subject': '数学', 'version': '人教版', 'grade': '三年级', 'semester': '上册'}))

with open(CFG, 'w', encoding='utf-8') as f:
    json.dump({'enable_online_ctsf': True, 'enable_online_pdf': True, 'enable_photo': True}, f, ensure_ascii=False)
print('restored')
