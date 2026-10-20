# -*- coding: utf-8 -*-
"""把三本实战样书转成 GitHub 友好版本（图片外链 + JPEG 压缩）

为什么：原 HTML 是单文件内嵌 base64，单本 25-34MB，三本 88MB 直接传会把仓库撑爆。
做法：图片抽出来压成 JPEG（尺寸不变 1024x1536），HTML 里的 data URI 换成相对路径，
      这样仓库 ~10MB，且开 GitHub Pages 后可在线翻页。

用法：python build_samples.py   （输出到 huiben-master-v2/samples/）
"""
import os, re, json

from PIL import Image

ROOT = r'D:\Workspace\clean-workspace\outputs'
DEST = r'D:\Workspace\clean-workspace\outputs\huiben-master-v2\samples'
QUALITY = 85

BOOKS = [
    ('moonlight',       'mianhua-moonlight', '小棉花和月亮灯.html',   '小棉花和月亮灯',   '低幼水彩', 8),
    ('red-riding-hood', 'xiaohongmao',       '小红帽智斗大灰狼.html', '小红帽智斗大灰狼', '低幼水彩', 10),
    ('ink-drop',        'xiaomodi',          '小墨滴和文房四宝.html', '小墨滴和文房四宝', '水墨国风', 8),
]

PAT = re.compile(r'data:image/png;base64,[A-Za-z0-9+/=]+')

total = 0
summary = []

for slug, dirname, htmlname, title, style, npages in BOOKS:
    src_html = os.path.join(ROOT, dirname, htmlname)
    src_img = os.path.join(ROOT, dirname, 'images')
    out_dir = os.path.join(DEST, slug)
    out_img = os.path.join(out_dir, 'images')
    os.makedirs(out_img, exist_ok=True)

    html = open(src_html, encoding='utf-8').read()
    uris = PAT.findall(html)

    # 图片顺序：封面在前，其后 p01..pNN（与原 build_html.py 的注入顺序一致）
    pages = sorted(f for f in os.listdir(src_img) if re.match(r'^p\d{2}\.png$', f))
    files = ['cover.png'] + pages
    assert len(uris) == len(files), f'{title}: data URI {len(uris)} != 图片 {len(files)}'

    # 1) 压缩图片
    for f in files:
        im = Image.open(os.path.join(src_img, f)).convert('RGB')
        dst = os.path.join(out_img, f.replace('.png', '.jpg'))
        im.save(dst, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
        total += os.path.getsize(dst)

    # 2) HTML 里的 data URI 换成相对路径
    counter = {'i': 0}

    def repl(_m):
        f = files[counter['i']]
        counter['i'] += 1
        return 'images/' + f.replace('.png', '.jpg')

    html = PAT.sub(repl, html)
    assert counter['i'] == len(files)
    assert 'data:image/png;base64,' not in html

    with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8', newline='\n') as fp:
        fp.write(html)

    size = sum(os.path.getsize(os.path.join(out_img, f.replace('.png', '.jpg'))) for f in files)
    hs = os.path.getsize(os.path.join(out_dir, 'index.html'))
    total += hs
    summary.append((slug, title, style, npages, len(files), size / 1048576, hs / 1024))
    print(f'[ok] {title}: {len(files)} 图 {size/1048576:.1f}MB + html {hs/1024:.0f}KB')

print(f'\n合计 {total/1048576:.1f} MB')

# 3) samples/README.md
meta = {
    'moonlight': ('睡前情绪 · 3-5 岁', '小棉花怕黑，月亮灯陪它入睡。8 页全 bottom 布局终版，三轮版式迭代的定型样本。'),
    'red-riding-hood': ('经典改编 · 5-7 岁', '温和智慧版：无惊吓，小红帽用热茶计和晾衣绳识破大灰狼。10 页，多角色锚点链样本。'),
    'ink-drop': ('国学启蒙 · 4-7 岁', '水墨国风模板首跑，小墨滴认识笔、墨、纸、砚。8 页，繁体「學」字正确渲染。'),
}
lines = ['# 实战样书', '',
         '三本全部由 `picture-book-creator` 技能实跑产出，未做任何人工修图。',
         '图片为 1024×1536 JPEG（原图 PNG 体积过大，已压缩以便在线浏览），文字版式与原版一致。',
         '']
for slug, title, style, npages, nimg, mbs, _hs in summary:
    tag, desc = meta[slug]
    lines += [f'## {title}', '',
              f'- 画风模板：{style}　页数：{npages}　定位：{tag}',
              f'- {desc}',
              f'- 在线翻页：[samples/{slug}/](samples/{slug}/)（需先开启 GitHub Pages）',
              f'- 离线单文件（内嵌原图，25-34MB）：见本地 `outputs/{slug}/`，不入库',
              '']
with open(os.path.join(DEST, 'README.md'), 'w', encoding='utf-8', newline='\n') as fp:
    fp.write('\n'.join(lines))
print('samples/README.md 已生成')
