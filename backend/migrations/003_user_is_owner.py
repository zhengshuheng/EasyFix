"""003 幂等迁移：users 表加 is_owner 列，并按 registry 把各空间注册者标为主账号。
覆盖：正式库、模板库、全部租户库。可重复执行。"""
import os
import sqlite3

BACKEND = 'E:/qianwenpaw/EasyFix-main/backend'
REGISTRY = os.path.join(BACKEND, 'trial_data', 'registry.db')

def db_paths():
    paths = [os.path.join(BACKEND, 'easyfix_main.db'), os.path.join(BACKEND, 'trial_data', 'template.db')]
    td = os.path.join(BACKEND, 'trial_data', 'tenants')
    if os.path.isdir(td):
        paths += [os.path.join(td, f) for f in os.listdir(td) if f.endswith('.db')]
    return paths

def add_column(path):
    c = sqlite3.connect(path)
    try:
        cols = [r[1] for r in c.execute('PRAGMA table_info(users)').fetchall()]
        if 'is_owner' not in cols:
            c.execute('ALTER TABLE users ADD COLUMN is_owner INTEGER NOT NULL DEFAULT 0')
            c.commit()
            return 'added'
        return 'no-op'
    finally:
        c.close()

def mark_owner(path, username):
    c = sqlite3.connect(path)
    try:
        cur = c.execute("UPDATE users SET is_owner = 1 WHERE username = ? AND role = 'admin'", (username,))
        c.commit()
        return cur.rowcount
    finally:
        c.close()

# 1) 全库加列
for p in db_paths():
    if os.path.isfile(p):
        print('col', os.path.basename(p), '=>', add_column(p))

# 2) 按 registry 标主账号
r = sqlite3.connect(REGISTRY)
rows = r.execute("SELECT key, db_path, username FROM spaces WHERE username IS NOT NULL AND username != ''").fetchall()
r.close()
for key, db_path, username in rows:
    path = os.path.join(BACKEND, db_path) if not os.path.isabs(db_path) else db_path
    if not os.path.isfile(path):
        print('owner', key, 'DB MISSING', db_path)
        continue
    n = mark_owner(path, username)
    print('owner', key, 'user=', username, 'marked=', n)
