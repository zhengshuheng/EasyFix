# -*- coding: utf-8 -*-
"""导入入口配置门禁自测"""
import json
import urllib.request
import urllib.error

CFG = r'backend\textbook_import_config.json'
BASE = 'http://127.0.0.1:8016'


def get(url, method='GET'):
    req = urllib.request.Request(url, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode('utf-8')[:200]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='replace')[:200]


def write_cfg(d):
    with open(CFG, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


# 1. 关掉在线大纲 + PDF 下载两个在线入口（对外推广形态）
write_cfg({'enable_online_ctsf': False, 'enable_online_pdf': False, 'enable_photo': True})
print('ctsf/catalog  ->', get(BASE + '/api/textbook/ctsf/catalog'))
print('ctsf/import   ->', get(BASE + '/api/textbook/ctsf/import'))
print('pdf import    ->', get(BASE + '/api/textbook/import'))
print('import-config ->', get(BASE + '/api/textbook/import-config'))
print('photo-import  ->', get(BASE + '/api/textbook/photo-import', method='POST'))

# 2. 恢复全开
write_cfg({'enable_online_ctsf': True, 'enable_online_pdf': True, 'enable_photo': True})
print('restored      ->', get(BASE + '/api/textbook/import-config'))
