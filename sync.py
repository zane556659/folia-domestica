#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# sync.py - Notion -> 家中花草志 靜態網站同步腳本
# 用法：python sync.py
# 跑完把整個 plant-website 資料夾上傳到 Netlify 即可

import json
import os
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

# ── 路徑設定 ─────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
ENV_PATH = BASE_DIR.parent / '400_Private' / '.env'

# ── 讀取 .env ─────────────────────────────────────────────
def load_env(path):
    env = {}
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return env

env = load_env(ENV_PATH)
NOTION_TOKEN        = env.get('NOTION_TOKEN') or os.environ.get('NOTION_TOKEN', '')
NOTION_DB_ID        = env.get('NOTION_DATABASE_ID') or os.environ.get('NOTION_DATABASE_ID', '')
NOTION_SUBSTRATE_ID = env.get('NOTION_SUBSTRATE_DB_ID') or os.environ.get('NOTION_SUBSTRATE_DB_ID', '')

# ── Notion API ────────────────────────────────────────────
def notion_req(method, path, body=None):
    url = f'https://api.notion.com/v1{path}'
    headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json',
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def get_public_substrates():
    results = []
    body = {
        'filter': {'property': '是否公開', 'checkbox': {'equals': True}},
        'sorts': [{'property': '新增日期', 'direction': 'descending'}],
    }
    while True:
        data = notion_req('POST', f'/databases/{NOTION_SUBSTRATE_ID}/query', body)
        results.extend(data['results'])
        if not data.get('has_more'):
            break
        body['start_cursor'] = data['next_cursor']
    return results

def get_public_plants():
    results = []
    body = {
        'filter': {'property': '發布狀態', 'select': {'equals': '公開'}},
        'sorts': [{'property': '拍攝日期', 'direction': 'descending'}],
    }
    while True:
        data = notion_req('POST', f'/databases/{NOTION_DB_ID}/query', body)
        results.extend(data['results'])
        if not data.get('has_more'):
            break
        body['start_cursor'] = data['next_cursor']
    return results

def get_blocks(page_id):
    blocks = []
    cursor = ''
    while True:
        path = f'/blocks/{page_id}/children?page_size=100'
        if cursor:
            path += f'&start_cursor={cursor}'
        data = notion_req('GET', path)
        blocks.extend(data['results'])
        if not data.get('has_more'):
            break
        cursor = data['next_cursor']
    return blocks

# ── 文字工具 ──────────────────────────────────────────────
def plain(rich):
    return ''.join(r.get('plain_text', '') for r in rich)

def to_html(rich):
    out = []
    for r in rich:
        t = (r.get('plain_text', '')
             .replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
        ann = r.get('annotations', {})
        if ann.get('bold'):   t = f'<strong>{t}</strong>'
        if ann.get('italic'): t = f'<em>{t}</em>'
        if ann.get('code'):   t = f'<code>{t}</code>'
        out.append(t)
    return ''.join(out)

# ── Notion blocks → HTML ──────────────────────────────────
def blocks_to_html(blocks):
    parts = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        bt = b['type']

        if bt == 'heading_2':
            text = plain(b['heading_2']['rich_text'])
            parts.append(f'<h2 class="sec-h2">{text}</h2>')

        elif bt == 'heading_3':
            text = plain(b['heading_3']['rich_text'])
            parts.append(f'<h3 class="sec-h3">{text}</h3>')

        elif bt == 'paragraph':
            text = to_html(b['paragraph']['rich_text'])
            if text.strip():
                parts.append(f'<p class="para">{text}</p>')

        elif bt == 'bulleted_list_item':
            items = []
            while i < len(blocks) and blocks[i]['type'] == 'bulleted_list_item':
                items.append(to_html(blocks[i]['bulleted_list_item']['rich_text']))
                i += 1
            li = ''.join(f'<li>{x}</li>' for x in items)
            parts.append(f'<ul class="blist">{li}</ul>')
            continue

        elif bt == 'numbered_list_item':
            items = []
            while i < len(blocks) and blocks[i]['type'] == 'numbered_list_item':
                items.append(to_html(blocks[i]['numbered_list_item']['rich_text']))
                i += 1
            li = ''.join(f'<li>{x}</li>' for x in items)
            parts.append(f'<ol class="blist">{li}</ol>')
            continue

        elif bt == 'image':
            img = b['image']
            src = (img['external']['url'] if img['type'] == 'external'
                   else img['file']['url'] if img['type'] == 'file' else '')
            if src:
                cap = plain(img.get('caption', []))
                cap_html = f'<figcaption class="img-cap">{cap}</figcaption>' if cap else ''
                parts.append(f'<figure class="obs-fig"><img src="{src}" alt="{cap}" loading="lazy" />{cap_html}</figure>')

        elif bt == 'callout':
            emoji = (b['callout'].get('icon') or {}).get('emoji', '')
            text  = plain(b['callout']['rich_text'])
            if emoji == '📷':
                parts.append('<div class="img-placeholder"><span class="img-placeholder-label">📷 圖片待補</span></div>')
            else:
                parts.append(f'<div class="callout">{emoji} {text}</div>')

        elif bt == 'divider':
            parts.append('<hr class="divider" />')

        elif bt == 'quote':
            text = to_html(b['quote']['rich_text'])
            parts.append(f'<blockquote class="bquote">{text}</blockquote>')

        i += 1
    return '\n'.join(parts)

# ── CSS 共用變數 ──────────────────────────────────────────
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com" /><link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=IM+Fell+English:ital@0;1&family=IM+Fell+English+SC&family=JetBrains+Mono&display=swap" rel="stylesheet" />'

GA_TAG = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-239WJ037YX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-239WJ037YX');
</script>'''

ROOT_VARS = """:root {
  --paper: #f1e9d6; --paper-light: #f7f0dd;
  --ink: #2a2419; --ink-soft: #4a3f2c; --ink-faded: #7a6a4f;
  --rule: #8a7a5c; --moss: #4a5a36; --moss-deep: #2f3a22; --rust: #9a4a2a;
  --serif-body: 'EB Garamond', Georgia, serif;
  --display: 'IM Fell English', 'EB Garamond', Georgia, serif;
  --display-sc: 'IM Fell English SC', 'EB Garamond', Georgia, serif;
  --mono: 'JetBrains Mono', 'Courier New', monospace;
}"""

SHARED_CSS = """
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; background: var(--paper); color: var(--ink); font-family: var(--serif-body); }
.site-header { max-width: 1180px; margin: 0 auto; padding: 20px 40px 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--rule); }
.logo { display: flex; align-items: center; gap: 12px; text-decoration: none; color: inherit; }
.logo-box { width: 30px; height: 30px; border: 1.5px solid var(--moss-deep); display: flex; align-items: center; justify-content: center; font-family: var(--display); font-style: italic; font-size: 17px; color: var(--moss-deep); }
.logo-name { font-family: var(--display); font-size: 20px; color: var(--moss-deep); }
.back-link { font-family: var(--display-sc); font-size: 11px; letter-spacing: 0.15em; color: var(--ink-faded); text-decoration: none; }
.back-link:hover { color: var(--ink); }
.site-footer { border-top: 3px double var(--rule); background: var(--paper-light); margin-top: 60px; }
.footer-inner { max-width: 1180px; margin: 0 auto; padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; font-family: var(--display-sc); font-size: 11px; letter-spacing: 0.2em; color: var(--ink-faded); }
"""

# ── 介質頁 HTML ───────────────────────────────────────────
CATEGORY_ORDER = ['無機的顆粒介質', '有機的基質介質', '功能性添加介質']

def make_substrate_html(substrates):
    # 依分類分組
    groups = {cat: [] for cat in CATEGORY_ORDER}
    for s in substrates:
        cat = ((s['properties'].get('分類') or {}).get('select') or {}).get('name', '')
        if cat in groups:
            groups[cat].append(s)

    # 每種介質取 blocks（含圖片佔位符與三個段落）
    sections_html = []
    for cat in CATEGORY_ORDER:
        items = groups.get(cat, [])
        if not items:
            continue
        entries = []
        for s in items:
            name   = plain(s['properties']['名稱']['title'])
            blocks = get_blocks(s['id'])
            body   = blocks_to_html(blocks)
            entries.append(f'<div class="sb-entry"><h3 class="sb-name">{name}</h3>{body}</div>')

        entries_joined = '\n<hr class="sb-entry-rule" />\n'.join(entries)
        sections_html.append(f'''<section class="sb-section">
  <h2 class="sb-cat">{cat}</h2>
  {entries_joined}
</section>''')

    count        = len(substrates)
    content_html = '\n'.join(sections_html) if sections_html else '<p class="sb-empty">尚無介質資料。</p>'

    return f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
{GA_TAG}
<meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<title>介質介紹 — 家中花草志</title>
{FONTS}
<style>
{ROOT_VARS}
{SHARED_CSS}
.page-header  {{ max-width: 900px; margin: 48px auto 0; padding: 0 40px 28px; border-bottom: 3px double var(--rule); }}
.page-title   {{ font-family: var(--display); font-weight: 400; font-size: 42px; color: var(--moss-deep); margin: 0 0 6px; }}
.page-sub     {{ font-family: var(--display); font-style: italic; font-size: 18px; color: var(--ink-soft); margin: 0 0 8px; }}
.page-meta    {{ font-family: var(--mono); font-size: 11px; color: var(--ink-faded); }}
.sb-body      {{ max-width: 900px; margin: 0 auto; padding: 0 40px 80px; }}
.sb-section   {{ margin-top: 56px; }}
.sb-cat       {{ font-family: var(--display-sc); font-size: 12px; letter-spacing: 0.25em; color: var(--ink-faded); border-bottom: 3px double var(--rule); padding-bottom: 8px; margin: 0 0 36px; font-weight: 400; }}
.sb-entry     {{ padding: 0 0 8px; }}
.sb-entry-rule{{ border: none; border-top: 1px solid var(--rule); margin: 32px 0; }}
.sb-name      {{ font-family: var(--display); font-weight: 400; font-size: 28px; color: var(--moss-deep); margin: 0 0 16px; }}
.img-placeholder {{ border: 1px dashed var(--rule); background: var(--paper-light); height: 200px; display: flex; align-items: center; justify-content: center; margin: 0 0 20px; }}
.img-placeholder-label {{ font-family: var(--display-sc); font-size: 11px; letter-spacing: 0.2em; color: var(--ink-faded); }}
.sec-h2       {{ font-family: var(--display); font-weight: 400; font-size: 17px; color: var(--moss-deep); border-bottom: 1px solid var(--rule); padding-bottom: 4px; margin: 20px 0 8px; }}
.para         {{ font-size: 15px; line-height: 1.85; color: var(--ink-soft); margin: 6px 0; }}
.sb-empty     {{ font-family: var(--display); font-style: italic; color: var(--ink-faded); padding: 48px 0; font-size: 17px; }}
.site-nav-link{{ font-family: var(--display-sc); font-size: 11px; letter-spacing: .18em; color: var(--ink-faded); text-decoration: none; padding: 4px 16px; border-left: 1px solid var(--rule); }}
.site-nav-link:hover {{ color: var(--moss-deep); }}
.site-nav-link.active {{ color: var(--moss-deep); }}
.site-nav-link:first-child {{ border-left: none; padding-left: 0; }}
</style>
</head>
<body>
<header class="site-header">
  <a class="logo" href="index.html"><div class="logo-box">F</div><span class="logo-name">家中花草志</span></a>
  <nav style="display:flex;align-items:center;">
    <a class="site-nav-link" href="home.html">植物目錄</a>
    <a class="site-nav-link active" href="substrate.html">介質介紹</a>
  </nav>
</header>

<div class="page-header">
  <h1 class="page-title">介質介紹 · Substrates</h1>
  <div class="page-sub">Growing media — properties &amp; applications</div>
  <div class="page-meta">共 {count} 種介質</div>
</div>

<div class="sb-body">
{content_html}
</div>

<footer class="site-footer"><div class="footer-inner"><span>—— Folia Domestica ——</span><span>MMXXVI</span></div></footer>
</body>
</html>'''

# ── 文章頁 HTML ───────────────────────────────────────────
def make_post_html(page):
    props = page['properties']
    name     = plain(props['植物名稱']['title'])
    sci      = plain(props['學名']['rich_text'])
    cover    = (props.get('封面照片') or {}).get('url', '')
    date_raw = ((props.get('拍攝日期') or {}).get('date') or {}).get('start', '')
    status   = ((props.get('生長狀況') or {}).get('select') or {}).get('name', '')
    tags     = [t['name'] for t in (props.get('分類標籤') or {}).get('multi_select', [])]

    blocks = get_blocks(page['id'])
    body   = blocks_to_html(blocks)

    date_disp  = date_raw.replace('-', ' / ') if date_raw else ''
    sci_html   = f'<div class="sci-name"><em>{sci}</em></div>' if sci else ''
    cover_html = (f'<div class="cover-wrap"><img class="cover-img" src="{cover}" alt="{name}" /></div>'
                  if cover else '')
    tags_html  = ''.join(f'<span class="tag">{t}</span>' for t in tags)
    title_tag  = f'{name}{" · " + sci if sci else ""} — 家中花草志'

    return f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
{GA_TAG}
<meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title_tag}</title>
{FONTS}
<style>
{ROOT_VARS}
{SHARED_CSS}
article {{ max-width: 760px; margin: 0 auto; padding: 48px 40px 60px; }}
.article-meta {{ font-family: var(--mono); font-size: 11px; color: var(--ink-faded); margin-bottom: 8px; display: flex; gap: 16px; }}
.plant-name {{ font-family: var(--display); font-size: 52px; font-weight: 400; line-height: 1.05; color: var(--moss-deep); margin: 8px 0 4px; }}
.sci-name {{ font-family: var(--display); font-style: italic; font-size: 21px; color: var(--ink-soft); margin-bottom: 16px; }}
.tags {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px; }}
.tag {{ font-family: var(--display-sc); font-size: 10px; letter-spacing: 0.2em; color: var(--ink-faded); border: 1px solid var(--rule); padding: 2px 10px; }}
.cover-wrap {{ margin: 0 0 32px; }}
.cover-img {{ width: 100%; max-height: 480px; object-fit: cover; border: 1px solid rgba(60,45,20,0.55); outline: 4px solid var(--paper); outline-offset: -7px; filter: sepia(0.15) contrast(0.96) saturate(0.9); display: block; }}
.sec-h2 {{ font-family: var(--display); font-weight: 400; font-size: 26px; color: var(--moss-deep); border-bottom: 1px solid var(--rule); padding-bottom: 6px; margin: 36px 0 14px; }}
.sec-h3 {{ font-family: var(--display); font-style: italic; font-weight: 400; font-size: 18px; color: var(--rust); margin: 28px 0 8px; }}
.para {{ font-size: 16px; line-height: 1.85; color: var(--ink); text-align: justify; margin: 12px 0; }}
.blist {{ margin: 10px 0; padding-left: 22px; }}
.blist li {{ font-size: 15px; line-height: 1.8; color: var(--ink-soft); margin-bottom: 4px; }}
.obs-fig {{ margin: 20px 0; }}
.obs-fig img {{ width: 100%; display: block; border: 1px solid rgba(60,45,20,0.45); filter: sepia(0.12) contrast(0.96); }}
.img-cap {{ text-align: center; font-family: var(--display); font-style: italic; font-size: 12px; color: var(--ink-faded); margin-top: 6px; }}
.divider {{ border: none; border-top: 1px solid var(--rule); margin: 24px 0; }}
.bquote {{ border-left: 3px double var(--rule); margin: 18px 0; padding: 12px 18px; background: var(--paper-light); font-style: italic; color: var(--ink-soft); }}
</style>
</head>
<body>
<header class="site-header">
  <a class="logo" href="home.html"><div class="logo-box">F</div><span class="logo-name">家中花草志</span></a>
  <a class="back-link" href="home.html">← 回首頁 · home</a>
</header>

<article>
  <div class="article-meta"><span>{date_disp}</span><span>{status}</span></div>
  <h1 class="plant-name">{name}</h1>
  {sci_html}
  <div class="tags">{tags_html}</div>
  {cover_html}
  {body}
</article>

<footer class="site-footer"><div class="footer-inner"><span>—— Folia Domestica ——</span><span>MMXXVI</span></div></footer>
</body>
</html>'''

# ── 首頁 HTML ─────────────────────────────────────────────
def make_home_html(plants):
    cards = []
    for p in plants:
        props  = p['properties']
        name   = plain(props['植物名稱']['title'])
        sci    = plain(props['學名']['rich_text'])
        cover  = (props.get('封面照片') or {}).get('url', '')
        date_r = ((props.get('拍攝日期') or {}).get('date') or {}).get('start', '')
        status = ((props.get('生長狀況') or {}).get('select') or {}).get('name', '')
        tags   = [t['name'] for t in (props.get('分類標籤') or {}).get('multi_select', [])]
        slug   = p['id'].replace('-', '')

        date_d     = date_r.replace('-', ' / ') if date_r else '—'
        sci_html   = f'<div class="card-sci"><em>{sci}</em></div>' if sci else ''
        cover_html = (f'<div class="card-cover" style="background-image:url(\'{cover}\')"></div>'
                      if cover else '<div class="card-cover card-cover--empty"></div>')
        tags_html     = ''.join(f'<span class="card-tag">{t}</span>' for t in tags[:3])
        data_tags_attr = ' '.join(tags)

        cards.append(f'''<a class="card" href="post-{slug}.html" data-tags="{data_tags_attr}">
  {cover_html}
  <div class="card-body">
    <div class="card-date">{date_d}</div>
    <div class="card-name">{name}</div>
    {sci_html}
    <div class="card-tags">{tags_html}</div>
    <div class="card-status">{status}</div>
  </div>
</a>''')

    count    = len(plants)
    now      = datetime.now().strftime('%Y-%m-%d %H:%M')
    all_tags = sorted({t for p in plants for t in [tt['name'] for tt in (p['properties'].get('分類標籤') or {}).get('multi_select', [])]})
    filter_btns = '<button class="filter-btn active" data-filter="all">全部</button>' + ''.join(
        f'<button class="filter-btn" data-filter="{t}">{t}</button>' for t in all_tags
    )

    return f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
{GA_TAG}
<meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<title>家中花草志 · 所有植物</title>
{FONTS}
<style>
{ROOT_VARS}
{SHARED_CSS}
.page-header {{ max-width: 1180px; margin: 40px auto 0; padding: 0 40px 24px; border-bottom: 3px double var(--rule); }}
.page-title {{ font-family: var(--display); font-weight: 400; font-size: 36px; color: var(--moss-deep); margin: 0 0 6px; }}
.page-meta {{ font-family: var(--mono); font-size: 11px; color: var(--ink-faded); }}
.grid {{ max-width: 1180px; margin: 36px auto 60px; padding: 0 40px; display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 24px; }}
.card {{ text-decoration: none; color: inherit; border: 1px solid var(--rule); background: var(--paper-light); display: flex; flex-direction: column; transition: transform 0.15s; }}
.card:hover {{ transform: translateY(-2px); }}
.card-cover {{ height: 200px; background-size: cover; background-position: center; filter: sepia(0.15) contrast(0.96); border-bottom: 1px solid var(--rule); }}
.card-cover--empty {{ background: var(--paper); }}
.card-body {{ padding: 18px 20px; }}
.card-date {{ font-family: var(--mono); font-size: 10px; color: var(--ink-faded); margin-bottom: 6px; }}
.card-name {{ font-family: var(--display); font-size: 24px; color: var(--moss-deep); line-height: 1.2; }}
.card-sci {{ font-family: var(--display); font-style: italic; font-size: 13px; color: var(--ink-soft); margin-top: 4px; }}
.card-tags {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; }}
.card-tag {{ font-family: var(--display-sc); font-size: 9px; letter-spacing: 0.18em; color: var(--ink-faded); border: 1px solid var(--rule); padding: 2px 8px; }}
.card-status {{ font-size: 12px; color: var(--ink-soft); margin-top: 8px; }}
.filter-bar {{ max-width: 1180px; margin: 28px auto 0; padding: 0 40px; display: flex; gap: 8px; flex-wrap: wrap; }}
.filter-btn {{ font-family: var(--display-sc); font-size: 11px; letter-spacing: 0.18em; color: var(--ink-faded); background: none; border: 1px solid var(--rule); padding: 5px 16px; cursor: pointer; transition: all 0.15s; }}
.filter-btn:hover {{ color: var(--ink); border-color: var(--ink-soft); }}
.filter-btn.active {{ background: var(--moss-deep); color: var(--paper-light); border-color: var(--moss-deep); }}
.card.hidden {{ display: none; }}
</style>
</head>
<body>
<header class="site-header">
  <a class="logo" href="index.html"><div class="logo-box">F</div><span class="logo-name">家中花草志</span></a>
  <nav style="display:flex;gap:0;align-items:center;">
    <a class="back-link" href="home.html" style="border-right:1px solid var(--rule);padding-right:16px;margin-right:0;color:var(--moss-deep);">植物目錄</a>
    <a class="back-link" href="substrate.html" style="padding-left:16px;">介質介紹</a>
  </nav>
</header>

<div class="page-header">
  <h1 class="page-title">所有植物 · Catalogue</h1>
  <div class="page-meta">共 {count} 筆 · 最後同步：{now}</div>
</div>

<div class="filter-bar">
  {filter_btns}
</div>

<div class="grid">
{''.join(cards)}
</div>

<footer class="site-footer"><div class="footer-inner"><span>—— Folia Domestica ——</span><span>MMXXVI</span></div></footer>

<script>
document.querySelectorAll('.filter-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const f = btn.dataset.filter;
    document.querySelectorAll('.card').forEach(card => {{
      if (f === 'all' || card.dataset.tags.split(' ').includes(f)) {{
        card.classList.remove('hidden');
      }} else {{
        card.classList.add('hidden');
      }}
    }});
  }});
}});
</script>
</body>
</html>'''

# ── 主程式 ─────────────────────────────────────────────────
def main():
    if not NOTION_TOKEN or not NOTION_DB_ID:
        print('[error] 找不到 NOTION_TOKEN 或 NOTION_DATABASE_ID')
        print(f'[error] 預期位置：{ENV_PATH}')
        return

    print('[sync] 家中花草志同步開始...')
    print(f'[sync] 資料庫：{NOTION_DB_ID[:8]}...')

    plants = get_public_plants()
    print(f'[sync] 找到 {len(plants)} 筆公開植物')

    if not plants:
        print('[sync] 沒有「發布狀態 = 公開」的植物，結束。')
        return

    for p in plants:
        name = plain(p['properties']['植物名稱']['title'])
        slug = p['id'].replace('-', '')
        print(f'[sync] 生成 post-{slug}.html ({name})')
        html = make_post_html(p)
        (BASE_DIR / f'post-{slug}.html').write_text(html, encoding='utf-8')

    print('[sync] 生成 home.html...')
    (BASE_DIR / 'home.html').write_text(make_home_html(plants), encoding='utf-8')

    if NOTION_SUBSTRATE_ID:
        print('[sync] 找到 NOTION_SUBSTRATE_DB_ID，同步介質資料...')
        substrates = get_public_substrates()
        print(f'[sync] 找到 {len(substrates)} 筆公開介質')
        print('[sync] 生成 substrate.html...')
        (BASE_DIR / 'substrate.html').write_text(make_substrate_html(substrates), encoding='utf-8')
    else:
        print('[sync] 未設定 NOTION_SUBSTRATE_DB_ID，跳過介質頁面')

    print(f'[sync] 完成！{len(plants)} 篇文章 + home.html')
    print(f'[sync] 接下來：把 plant-website 資料夾上傳到 Netlify')

if __name__ == '__main__':
    main()
