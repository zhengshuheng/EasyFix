"""幂等迁移：为所有 word 表补 source/edition_key/revision 三列（模型有字段库表缺失）。
覆盖：正式库、模板库、全部租户库。可重复执行（缺列才 ALTER）。"""
import os
import sqlite3

BACKEND = 'E:/qianwenpaw/EasyFix-main/backend'
DB_PATHS = [
    os.path.join(BACKEND, 'easyfix_main.db'),
    os.path.join(BACKEND, 'trial_data', 'template.db'),
]
TENANTS_DIR = os.path.join(BACKEND, 'trial_data', 'tenants')
DB_PATHS += [os.path.join(TENANTS_DIR, f) for f in os.listdir(TENANTS_DIR) if f.endswith('.db')]

ADD_COLUMNS = [
    ('source', "VARCHAR(20) DEFAULT 'custom'"),
    ('edition_key', 'VARCHAR(50)'),
    ('revision', 'VARCHAR(20)'),
]

def migrate(path):
    if not os.path.isfile(path):
        return 'MISSING'
    c = sqlite3.connect(path)
    try:
        tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='word'")]
        if not tables:
            return 'no-word-table'
        cols = [r[1] for r in c.execute('PRAGMA table_info(word)').fetchall()]
        added = []
        for col, ddl in ADD_COLUMNS:
            if col not in cols:
                c.execute(f'ALTER TABLE word ADD COLUMN {col} {ddl}')
                added.append(col)
        c.commit()
        return 'added=' + ','.join(added) if added else 'ok(no-op)'
    except Exception as e:
        return f'ERR {e}'
    finally:
        c.close()

for p in DB_PATHS:
    print(os.path.basename(p), '=>', migrate(p))
