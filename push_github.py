# -*- coding: utf-8 -*-
"""picture-book-creator -> GitHub 上传脚本

用法：把 GitHub PAT 写入 D:\\Workspace\\clean-workspace\\.github_token（纯 token 一行），
      然后运行本脚本。token 不进对话记录。
"""
import json, os, subprocess, sys, tempfile, urllib.request, urllib.error

REPO = r'D:\Workspace\clean-workspace\outputs\huiben-master-v2'
TOKEN_FILE = r'D:\Workspace\clean-workspace\.github_token'
REPO_NAME = 'picture-book-creator'
DESCRIPTION = 'AI 绘本创作大师：四层风格锁定体系，解决 AI 绘本"一本书五个画风"问题。四种画风模板，三本实战验证。'

# 空配置文件：用于屏蔽 ~/.gitconfig 里的 ghproxy insteadOf（该镜像已 502）
_EMPTY_CFG = os.path.join(tempfile.gettempdir(), 'empty_gitconfig')
open(_EMPTY_CFG, 'w').close()

def run(cmd, env=None, cwd=REPO):
    e = os.environ.copy()
    # 清掉本机注入的 http(s)_proxy（github 走它会 502 CONNECT tunnel failed）
    for k in list(e):
        if k.lower() in ('http_proxy', 'https_proxy', 'all_proxy', 'ftp_proxy'):
            del e[k]
    e['GIT_CONFIG_GLOBAL'] = _EMPTY_CFG
    e['GIT_CONFIG_SYSTEM'] = _EMPTY_CFG
    e['GIT_TERMINAL_PROMPT'] = '0'
    if env:
        e.update(env)
    r = subprocess.run(cmd, cwd=cwd, env=e, shell=True,
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.returncode, (r.stdout or '') + (r.stderr or '')

# 1. 读 token
if not os.path.exists(TOKEN_FILE):
    print('NO_TOKEN_FILE: 请把 GitHub PAT 写入', TOKEN_FILE)
    sys.exit(1)
token = open(TOKEN_FILE, encoding='utf-8').read().strip()
if not token:
    print('EMPTY_TOKEN')
    sys.exit(1)
print('token 长度:', len(token))

# 2. 查用户名
req = urllib.request.Request('https://api.github.com/user', headers={
    'Authorization': 'Bearer ' + token,
    'Accept': 'application/vnd.github+json',
    'User-Agent': 'picture-book-creator-uploader'
})
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        user = json.load(resp)
except urllib.error.HTTPError as ex:
    print('AUTH_FAILED:', ex.code, ex.read().decode('utf-8', 'replace')[:200])
    sys.exit(1)
login = user['login']
print('GitHub 用户:', login)

# 3. 建仓（已存在则跳过）
payload = json.dumps({
    'name': REPO_NAME,
    'description': DESCRIPTION,
    'private': False,
    'auto_init': False,
    'has_issues': True,
    'has_wiki': False,
}).encode()
req = urllib.request.Request('https://api.github.com/user/repos', data=payload, method='POST', headers={
    'Authorization': 'Bearer ' + token,
    'Accept': 'application/vnd.github+json',
    'Content-Type': 'application/json',
    'User-Agent': 'picture-book-creator-uploader'
})
created = False
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        repo = json.load(resp)
    created = True
    print('仓库已创建:', repo['html_url'])
except urllib.error.HTTPError as ex:
    body = ex.read().decode('utf-8', 'replace')
    if ex.code == 422 and 'already exists' in body:
        print('仓库已存在，跳过创建')
    else:
        print('CREATE_FAILED:', ex.code, body[:300])
        sys.exit(1)

html_url = f'https://github.com/{login}/{REPO_NAME}'
# 4. 设置 remote（token 内联，绕过 credential）
push_url = f'https://{login}:{token}@github.com/{login}/{REPO_NAME}.git'
code, out = run(f'git remote remove origin 2>nul & git remote add origin "{push_url}"')
print('remote 设置:', out.strip() or 'ok')

# 5. push
code, out = run('git push -u origin main')
print('push exit:', code)
print(out.strip()[:800])
if code != 0:
    sys.exit(1)

# 6. 把 remote 里的 token 去掉，改为干净 URL（避免明文常驻）
run('git remote set-url origin "https://github.com/%s/%s.git"' % (login, REPO_NAME))
print('remote 已回写为干净 URL')

# 7. 验证
code, out = run('git ls-remote --heads origin')
print('验证 ls-remote:', out.strip()[:200])
print('DONE:', html_url)
