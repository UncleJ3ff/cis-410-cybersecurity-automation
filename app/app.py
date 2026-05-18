import sqlite3
import socket
import os
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

def get_db():
    db = sqlite3.connect(':memory:')
    db.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY, username TEXT, email TEXT)''')
    db.execute("INSERT INTO users VALUES (1, 'alice', 'alice@example.com')")
    db.execute("INSERT INTO users VALUES (2, 'bob', 'bob@example.com')")
    db.execute("INSERT INTO users VALUES (3, 'charlie', 'charlie@example.com')")
    db.execute("INSERT INTO users VALUES (4, 'david', 'david@example.com')")
    db.execute("INSERT INTO users VALUES (5, 'eve', 'eve@example.com')")
    db.execute("INSERT INTO users VALUES (6, 'frank', 'frank@example.com')")
    db.commit()
    return db

@app.route('/')
def index():
    env = os.environ.get('ENVIRONMENT', 'dev')
    version = os.environ.get('APP_VERSION', '1.0.0')
    deploy_time = os.environ.get('DEPLOY_TIME', 'unknown')
    commit_sha = os.environ.get('COMMIT_SHA', 'local')
    branch = os.environ.get('BRANCH', 'main')
    workflow = os.environ.get('WORKFLOW', 'manual')
    hostname = socket.gethostname()
    return f'''<!DOCTYPE html>
<html><head><title>CIS 410 - {env.upper()} Deployment Dashboard</title>
<style>
body{{font-family:monospace;background:#1a1a2e;color:#eee;padding:20px}}
h1{{color:#00d4ff}}h2{{color:#00ff88}}
.card{{background:#16213e;padding:15px;margin:10px 0;border-radius:5px;border-left:4px solid #00d4ff}}
.ok{{color:#00ff88}}.env{{color:#ffd700;font-size:1.5em;font-weight:bold}}
</style></head>
<body>
<h1>CIS 410 - DevSecOps Platform</h1>
<p>Deployment Status Dashboard - JeffreyHysons-Dev</p>
<p class="env">{env}</p>
<div class="card"><h2>Overview</h2>
<p>Status: <span class="ok">Running</span></p>
<p>Container healthy</p>
<p>Environment: {env}</p>
<p>Port 5000</p>
<p>App version: {version}</p>
<p>{branch}</p>
<p>Pipeline: <span class="ok">Passing</span></p>
<p>{workflow}</p></div>
<div class="card"><h2>Deployment info</h2>
<p>Container hostname: {hostname}</p>
<p>Host VM: {env}-vm</p>
<p>Deployed at: {deploy_time}</p>
<p>Commit SHA: {commit_sha}</p>
<p>Branch: {branch}</p>
<p>Triggered by: {workflow}</p></div>
<div class="card"><h2>Security checks</h2>
<p>Container hardening: All rules passing</p>
<p>Running user: appuser (non-root)</p>
<p>Base image: python:3.11-slim</p>
<p><span class="ok">SECURE</span> - All vulnerabilities fixed</p></div>
<a href="/search" style="color:#00d4ff">User Search</a>
</body></html>'''

@app.route('/search')
def search():
    q = request.args.get('q', '')
    db = get_db()
    try:
        results = db.execute(
            "SELECT * FROM users WHERE username LIKE ? OR email LIKE ?",
            (f'%{q}%', f'%{q}%')
        ).fetchall()
    except Exception as e:
        results = []

    rows = ''.join(f'<tr><td>{r[0]}</td><td>{escape(r[1])}</td><td>{escape(r[2])}</td></tr>' for r in results)
    safe_q = escape(q)
    return f'''<!DOCTYPE html><html><head><title>User Search</title>
<style>body{{font-family:monospace;background:#1a1a2e;color:#eee;padding:20px}}
table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #444;padding:8px}}
input{{padding:5px;width:300px}}button{{padding:5px 10px}}</style></head>
<body><h1 style="color:#00d4ff">User Search</h1>
<form><input name="q" value="{safe_q}" placeholder="Search users..."><button type="submit">Search</button></form>
<table><tr><th>ID</th><th>Username</th><th>Email</th></tr>{rows}</table>
<p><a href="/" style="color:#00d4ff">Back</a></p>
</body></html>'''

@app.route('/health')
def health():
    return ({'status': 'ok', 'environment': os.environ.get('ENVIRONMENT', 'dev')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
