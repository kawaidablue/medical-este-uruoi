# -*- coding: utf-8 -*-
import os, pathlib, math

SRC = pathlib.Path("/home/claude/uruoi")          # ソースCSS/JSの置き場
MAIN_CSS = (SRC / "css" / "main.css").read_text(encoding="utf-8")   # 全ページ共通ベース
SUB_CSS  = (SRC / "css" / "sub.css").read_text(encoding="utf-8")    # 下層ページ共通
# 下層ページ固有CSS（HTML名に対応。固有が無ければ空でも可）
SUB_PAGE_CSS = ["treatment-shimi.css","treatment-nikibi.css","treatment-shiwa.css",
                "treatment-hari.css","price.css","voice.css","cosmetics.css","news.css"]
OUT = "/mnt/user-data/outputs/uruoi"
os.makedirs(OUT, exist_ok=True)

# ============ 仮画像（クリーン版・可読性優先） ============
THEMES = {
 'shimi':     dict(bg=('#F5EFE1','#ECDFC6'), e='#EAD9B6', acc='#C49A55'),
 'nikibi':    dict(bg=('#EDF2F0','#DBE7E2'), e='#CFE3DD', acc='#7FB3A4'),
 'shiwa':     dict(bg=('#EEF1E6','#DEE4CE'), e='#D6DEC0', acc='#97A86C'),
 'hari':      dict(bg=('#F5EFE2','#ECDFC2'), e='#EAD7A8', acc='#C8A24B'),
 'voice':     dict(bg=('#F5EEE8','#ECDBCF'), e='#EAD6C9', acc='#C2917A'),
 'price':     dict(bg=('#F4EFE4','#E8DEC8'), e='#E3D7BD', acc='#B19A6C'),
 'cosmetics': dict(bg=('#F3EFE4','#E7DFCB'), e='#E2D8BF', acc='#97A86C'),
}

def bottle(x,y,s,c):
    return (f'<rect x="{x-s*0.3:.0f}" y="{y-s*0.45:.0f}" width="{s*0.6:.0f}" height="{s*1.25:.0f}" '
            f'rx="{s*0.12:.0f}" fill="{c}" opacity=".09" stroke="{c}" stroke-width="1.6" stroke-opacity=".3"/>'
            f'<rect x="{x-s*0.12:.0f}" y="{y-s*0.78:.0f}" width="{s*0.24:.0f}" height="{s*0.36:.0f}" '
            f'fill="{c}" opacity=".12" stroke="{c}" stroke-width="1.3" stroke-opacity=".3"/>')
def jar(x,y,s,c):
    return (f'<rect x="{x-s*0.45:.0f}" y="{y-s*0.5:.0f}" width="{s*0.9:.0f}" height="{s*1.0:.0f}" '
            f'rx="{s*0.14:.0f}" fill="{c}" opacity=".09" stroke="{c}" stroke-width="1.6" stroke-opacity=".3"/>'
            f'<rect x="{x-s*0.3:.0f}" y="{y-s*0.74:.0f}" width="{s*0.6:.0f}" height="{s*0.26:.0f}" '
            f'rx="{s*0.06:.0f}" fill="{c}" opacity=".12" stroke="{c}" stroke-width="1.5" stroke-opacity=".3"/>')

def m_radiance(cx,cy,s,acc):
    out=[f'<g stroke="{acc}" stroke-linecap="round" stroke-opacity=".3">']
    for a in range(0,360,30):
        r=math.radians(a)
        out.append(f'<line x1="{cx+math.cos(r)*s*0.6:.0f}" y1="{cy+math.sin(r)*s*0.6:.0f}" '
                   f'x2="{cx+math.cos(r)*s*0.95:.0f}" y2="{cy+math.sin(r)*s*0.95:.0f}" stroke-width="1.6"/>')
    out.append('</g>')
    out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{s*0.45:.0f}" fill="{acc}" opacity=".08"/>'
               f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{s*0.45:.0f}" fill="none" stroke="{acc}" stroke-width="1.6" stroke-opacity=".3"/>')
    return ''.join(out)
def m_drops(cx,cy,s,acc):
    def d(x,y,r):
        return (f'<path d="M{x:.0f} {y-r*1.4:.0f} C{x+r:.0f} {y-r*0.2:.0f} {x+r*0.9:.0f} {y+r:.0f} {x:.0f} {y+r:.0f} '
                f'C{x-r*0.9:.0f} {y+r:.0f} {x-r:.0f} {y-r*0.2:.0f} {x:.0f} {y-r*1.4:.0f} Z" '
                f'fill="{acc}" opacity=".08" stroke="{acc}" stroke-width="1.6" stroke-opacity=".3"/>')
    return d(cx,cy,s*0.42)+d(cx-s*0.62,cy+s*0.2,s*0.26)+d(cx+s*0.6,cy+s*0.05,s*0.3)
def m_lift(cx,cy,s,acc):
    out=[]
    for i in range(3):
        y=cy+(i-1)*s*0.32
        out.append(f'<path d="M{cx-s:.0f} {y+s*0.15:.0f} C{cx-s*0.3:.0f} {y-s*0.5:.0f} {cx+s*0.3:.0f} {y-s*0.5:.0f} '
                   f'{cx+s:.0f} {y-s*0.15:.0f}" fill="none" stroke="{acc}" stroke-width="2" '
                   f'stroke-linecap="round" stroke-opacity="{0.34-i*0.07:.2f}"/>')
    return ''.join(out)
def m_serum(cx,cy,s,acc):
    return (f'<ellipse cx="{cx-s*0.42:.0f}" cy="{cy:.0f}" rx="{s*0.4:.0f}" ry="{s*0.38:.0f}" '
            f'fill="{acc}" opacity=".09" stroke="{acc}" stroke-width="1.6" stroke-opacity=".3"/>'
            f'<ellipse cx="{cx+s*0.48:.0f}" cy="{cy+s*0.04:.0f}" rx="{s*0.42:.0f}" ry="{s*0.4:.0f}" '
            f'fill="{acc}" opacity=".07" stroke="{acc}" stroke-width="1.6" stroke-opacity=".3"/>')
def m_quote(cx,cy,s,acc):
    return (f'<text x="{cx:.0f}" y="{cy+s*0.4:.0f}" font-family="Cormorant Garamond, Georgia, serif" '
            f'font-style="italic" font-size="{s*2.2:.0f}" fill="{acc}" opacity=".2" text-anchor="middle">\u201d</text>')
def m_botanical(cx,cy,s,acc):
    return (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{s*0.5:.0f}" fill="none" stroke="{acc}" stroke-width="1.4" stroke-opacity=".25"/>')
def m_cosmetics(cx,cy,s,acc):
    return bottle(cx-s*0.45,cy+s*0.1,s*0.9,acc)+jar(cx+s*0.55,cy+s*0.18,s*0.78,acc)
def m_bottle(cx,cy,s,acc):
    return bottle(cx,cy+s*0.1,s*1.05,acc)
def m_jar(cx,cy,s,acc):
    return jar(cx,cy+s*0.1,s*0.95,acc)

MOTIF = dict(radiance=m_radiance, drops=m_drops, lift=m_lift, serum=m_serum,
             quote=m_quote, botanical=m_botanical, cosmetics=m_cosmetics,
             bottle=m_bottle, jar=m_jar)

_uid=[0]
def hero_art(theme):
    """ヒーロー用：文字が読みやすいクリーンなグラデーションのみ"""
    _uid[0]+=1; u=_uid[0]; t=THEMES[theme]; c1,c2=t['bg']
    return (f'<svg class="artsvg" viewBox="0 0 1280 480" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><linearGradient id="hg{u}" x1="0" y1="0" x2="0.5" y2="1">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
            f'<radialGradient id="hh{u}" cx="68%" cy="26%" r="62%">'
            f'<stop offset="0" stop-color="#ffffff" stop-opacity=".5"/>'
            f'<stop offset="100%" stop-color="#ffffff" stop-opacity="0"/></radialGradient></defs>'
            f'<rect width="1280" height="480" fill="url(#hg{u})"/>'
            f'<rect width="1280" height="480" fill="url(#hh{u})"/></svg>')

def media_art(theme, vw, vh, motif):
    """画像枠用：やわらかいグラデ＋控えめなモチーフ（装飾は最小限）"""
    _uid[0]+=1; u=_uid[0]; t=THEMES[theme]; c1,c2=t['bg']; e=t['e']; acc=t['acc']
    cx,cy=vw*0.5,vh*0.47; s=min(vw,vh)*0.32
    return (f'<svg class="artsvg" viewBox="0 0 {vw} {vh}" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><linearGradient id="mg{u}" x1="0" y1="0" x2="0.7" y2="1">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
            f'<filter id="mb{u}" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="{max(vw,vh)*0.06:.0f}"/></filter></defs>'
            f'<rect width="{vw}" height="{vh}" fill="url(#mg{u})"/>'
            f'<ellipse cx="{vw*0.72:.0f}" cy="{vh*0.26:.0f}" rx="{vw*0.4:.0f}" ry="{vh*0.34:.0f}" fill="{e}" opacity=".55" filter="url(#mb{u})"/>'
            f'{MOTIF[motif](cx,cy,s,acc)}</svg>')
# ===============================================================

# ---- 写真（無料・Unsplash由来をローカル取り込み → data URIで確実に表示） ----
import base64
_IMGDIR = "/home/claude/uruoi/img"
IMGDATA = {}
for _f in os.listdir(_IMGDIR):
    if _f.lower().endswith((".jpg",".jpeg")):
        with open(os.path.join(_IMGDIR,_f),"rb") as _fh:
            IMGDATA[os.path.splitext(_f)[0]] = "data:image/jpeg;base64," + base64.b64encode(_fh.read()).decode()
with open(os.path.join(_IMGDIR,"logo.png"),"rb") as _lf:
    LOGO = "data:image/png;base64," + base64.b64encode(_lf.read()).decode()

def photo(key, w=900):
    if not key or key not in IMGDATA: return ""
    return f'<img class="ph" src="{IMGDATA[key]}" alt="" decoding="async">'
def mfill(theme, vw, vh, motif, imgkey=None, w=800):
    return f'{photo(imgkey,w)}{media_art(theme,vw,vh,motif)}'

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&family=Shippori+Mincho:wght@400;500;600;700&family=Noto+Serif+JP:wght@300;400;500;600&family=Noto+Sans+JP:wght@300;400;500&family=Zen+Kaku+Gothic+New:wght@300;400;500;700&family=Parisienne&display=swap" rel="stylesheet">"""

LOGO_SVG = """<svg class="logo-ico" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<ellipse cx="40" cy="60" rx="30" ry="8" fill="none" stroke="#028DC6" stroke-width="2.4"/>
<ellipse cx="40" cy="60" rx="20" ry="5" fill="none" stroke="#48B399" stroke-width="2"/>
<path d="M40 16 C40 16 54 36 54 47 a14 14 0 0 1 -28 0 C26 36 40 16 40 16 Z" fill="#028DC6"/>
<circle cx="46" cy="40" r="4.5" fill="#bfe9f7" opacity=".9"/>
</svg>"""

def header():
    return f"""<header class="site-header">
  <a class="brand" href="index.html"><img class="logo-img" src="{LOGO}" alt="メディカルエステ うるおい"></a>
  <div class="hd-right">
    <a class="hd-cta" href="https://airrsv.net/medical-uruoi/calendar" target="_blank" rel="noopener"><span class="hd-cta-tx">ご予約はこちらから</span><span class="hd-cta-ar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/></svg></span></a>
    <button class="burger" id="menuBtn" aria-label="メニュー">
      <span class="circle"><i></i><i></i><i></i></span><span class="lbl">MENU</span>
    </button>
  </div>
</header>
<nav class="nav-overlay" id="navOverlay">
  <button class="close" id="navClose" aria-label="閉じる"><svg class="x-ico" width="34" height="34" viewBox="0 0 34 34" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 3 31 31M31 3 3 31"/></svg></button>
  <div class="nav-grid">
    <div class="nav-side">
      <a href="index.html"><img class="nav-logo" src="{LOGO}" alt="メディカルエステ うるおい"></a>
      <p class="nav-concept">皮膚科専門医監修の<br>メディカルエステサロン</p>
      <p class="nav-tel-l">ご予約・お問い合わせ</p>
      <a class="nav-tel" href="tel:0477122552">047-712-2552</a>
      <p class="nav-hours">平日 10:00–18:00 ／ 土 9:00–17:00 ・ 完全予約制</p>
      <p class="nav-addr">千葉県松戸市日暮3-10-2<br>グレースビア参番館103号</p>
      <div class="nav-sns">
        <a href="#" aria-label="Facebook"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.78-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.44 2.89h-2.34v6.99A10 10 0 0 0 22 12Z"/></svg></a>
        <a href="#" aria-label="Instagram"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="3.6"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor"/></svg></a>
      </div>
      {BRANCH}
    </div>
    <ul class="nav-list"><li><a href="index.html"><span class="jp">ホーム</span><span class="en">Home</span></a></li><li class="nav-cat">お悩み・施術</li><li><a href="treatment-shimi.html"><span class="jp">シミ・くすみ・肝斑</span><span class="en">Mesoactis</span></a></li><li><a href="treatment-nikibi.html"><span class="jp">ニキビ</span><span class="en">Hydrogen Peeling</span></a></li><li><a href="treatment-shiwa.html"><span class="jp">しわ・たるみ</span><span class="en">SMAS-up NEO</span></a></li><li><a href="treatment-hari.html"><span class="jp">ハリ・ツヤ</span><span class="en">Environ</span></a></li><li class="nav-cat">料金・製品</li><li><a href="price.html"><span class="jp">料金表</span><span class="en">Price</span></a></li><li><a href="cosmetics.html"><span class="jp">お取り扱い製品</span><span class="en">Products</span></a></li><li class="nav-cat">サロン案内</li><li><a href="voice.html"><span class="jp">お客様の声</span><span class="en">Voice</span></a></li><li><a href="news.html"><span class="jp">お知らせ</span><span class="en">News</span></a></li><li><a href="index.html#greet"><span class="jp">代表ごあいさつ</span><span class="en">Greeting</span></a></li><li><a href="index.html#access"><span class="jp">アクセス</span><span class="en">Access</span></a></li></ul>
  </div>
</nav>"""

BRANCH = """"""

def page_hero(mark, script, h1, lead, crumb_label, theme, motif, hero_img=None):
    return f"""<section class="page-hero">
  <div class="hero-art">{photo(hero_img,1600)}{hero_art(theme)}</div>
  <div class="hero-veil"></div>
  <div class="wrap hero-content reveal">
    <span class="script">{script}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>"""

RESERVE = """<section class="reserve" id="cta">
  <div class="wrap reveal">
    <span class="rs-script">Reservation</span>
    <h2>ご予約・お問い合わせ</h2>
    <p class="rs-lead">カウンセリングは無料です。気になることはお気軽にご相談ください。</p>
    <div class="rs-card">
      <div class="rs-tel">
        <span class="rs-lbl">お電話でのご予約・ご相談</span>
        <a class="rs-num" href="tel:0477122552"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>047-712-2552</a>
        <span class="rs-hours">受付 平日 10:00–18:00 ／ 土 9:00–17:00 ・ 完全予約制</span>
      </div>
      <div class="rs-sep"></div>
      <div class="rs-act">
        <a class="btn btn-cta" href="#">WEBで予約する（24時間受付）</a>
        <a class="btn btn-line-app" href="#"><img class="line-ico" src="img/LINE_Brand_icon.png" alt="">LINEで相談する</a>
        <div class="rs-sns">
          <a href="#" aria-label="Facebook"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.78-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.44 2.89h-2.34v6.99A10 10 0 0 0 22 12Z"/></svg></a>
          <a href="#" aria-label="Instagram"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="3.6"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor"/></svg></a>
        </div>
      </div>
    </div>
  </div>
</section>"""

FOOTER = f"""<footer class="site-footer">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <a href="index.html"><img class="logo-img foot-logo" src="{LOGO}" alt="メディカルエステ うるおい"></a>
      <address>千葉県松戸市日暮3-10-2<br>グレースビア参番館103号<br>完全予約制 ／ <span style="white-space:nowrap">カウンセリング無料</span></address>
    </div>
    <div class="foot-col">
      <h5><a href="index.html">HOME</a></h5>
      <p class="foot-sub">お悩み・症状別</p>
      <a href="treatment-shimi.html">シミ</a>
      <a href="treatment-nikibi.html">ニキビ</a>
      <a href="treatment-shiwa.html">しわ・たるみ</a>
      <a href="treatment-hari.html">ハリ・ツヤ</a>
    </div>
    <div class="foot-col"><h5>施術メニュー</h5>
      <a href="treatment-shimi.html">メソアクティス</a>
      <a href="treatment-nikibi.html">水素水ピーリング</a>
      <a href="treatment-shiwa.html">スマスアップNEO</a>
      <a href="treatment-hari.html">エンビロン</a>
    </div>
    <div class="foot-col">
      <h5><a href="voice.html">お客様の声</a></h5>
      <a href="price.html">料金表</a>
      <a href="cosmetics.html">お取り扱い製品</a>
      <a href="news.html">お知らせ</a>
    </div>
    <div class="foot-col"><h5>サロン案内</h5>
      <a href="index.html#concept">コンセプト</a>
      <a href="index.html#staff">スタッフ紹介</a>
      <a href="index.html#access">アクセス</a>
      <a href="index.html#greet">代表ごあいさつ</a>
    </div>
  </div>
  <p class="foot-bottom">Copyright (C) メディカルエステうるおい All Rights Reserved.</p>
</footer>"""

JS = """<script>
const mb=document.getElementById('menuBtn'),nv=document.getElementById('navOverlay'),nc=document.getElementById('navClose');
const openNav=()=>{nv.classList.add('open');document.body.style.overflow='hidden';};
const closeNav=()=>{nv.classList.remove('open');document.body.style.overflow='';};
mb.addEventListener('click',openNav);
if(nc)nc.addEventListener('click',closeNav);
nv.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeNav));
const els=[...document.querySelectorAll('.reveal')];
if('IntersectionObserver'in window){
  const io=new IntersectionObserver((es)=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}}),{threshold:0,rootMargin:'0px 0px -10% 0px'});
  els.forEach(el=>io.observe(el));
}else{els.forEach(e=>e.classList.add('in'));}
</script>"""

def page(title, body, css=None):
    # css = このページ固有のCSSファイル名（例 "voice.css"）。未指定なら共通のみ。
    page_css = f'\n<link rel="stylesheet" href="css/{css}?v=110">' if css else ""
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}｜メディカルエステ うるおい</title>
<link rel="icon" type="image/png" href="img/cropped-favicon.png?v=110">
{FONTS}
<script>document.documentElement.className+=" js";</script>
<link rel="stylesheet" href="css/main.css?v=110">
<link rel="stylesheet" href="css/sub.css?v=110">{page_css}
</head>
<body>
{header()}
{body}
{RESERVE}
{FOOTER}
<script src="js/app.js?v=110"></script>
</body>
</html>"""

def sec_head(mark, script, ttl, left=False):
    cls = "sec-head left" if left else "sec-head"
    return f'<div class="{cls} reveal"><span class="mark">{mark}</span><span class="script">{script}</span><h2 class="ttl">{ttl}</h2></div>'

# ---------------- 施術ページ共通テンプレート（雛形・編集的レイアウト） ----------------
ICONS = {
 'drop': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 3s6 6.6 6 10.4A6 6 0 1 1 6 13.4C6 9.6 12 3 12 3Z"/></svg>',
 'sparkle': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4z"/></svg>',
 'clock': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3.2 2"/></svg>',
}

def khead(jp, en, desc=None, center=True, mark=None):
    d = f'<p class="kdesc">{desc}</p>' if desc else ""
    return f'<div class="sec-head reveal"><span class="mark">{mark or en.upper()}</span><span class="script">{en}</span><h2 class="ttl">{jp}</h2>{d}</div>'

def khead2(jp, en):
    # 補足セクション用：小さな左寄せ見出し（罫線＋筆記体＋和文）
    return f'<div class="sub-head reveal"><span class="scr">{en}</span><h3 class="ttl">{jp}</h3></div>'

_CAUSE_ICONS = {
 "uv":'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19"/>',
 "age":'<path d="M6 3h12M6 21h12"/><path d="M7 3c0 4 5 6 5 9s-5 5-5 9M17 3c0 4-5 6-5 9s5 5 5 9"/>',
 "cycle":'<path d="M4 11a8 8 0 0 1 13.5-5.3L20 8"/><path d="M20 4v4h-4"/><path d="M20 13a8 8 0 0 1-13.5 5.3L4 16"/><path d="M4 20v-4h4"/>',
 "stress":'<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 "life":'<path d="M21 12.8A8 8 0 1 1 11.2 3 6.5 6.5 0 0 0 21 12.8z"/>',
 "dry":'<path d="M12 3s5 5.5 5 9a5 5 0 0 1-10 0c0-3.5 5-9 5-9z"/><line x1="5" y1="5" x2="19" y2="19"/>',
 "smoke":'<rect x="3" y="14" width="13" height="4" rx="1"/><path d="M19 6c1 1 1 2 0 3M16 5c1 1 1 2 0 3"/>',
 "friction":'<path d="M3 11c2-2 4-2 6 0s4 2 6 0 4-2 6 0"/><path d="M3 16c2-2 4-2 6 0s4 2 6 0 4-2 6 0"/>',
}
def cause_icon(k):
    p = _CAUSE_ICONS.get(k, '<circle cx="12" cy="12" r="6"/>')
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{p}</svg>'

def hero_split(meta, th):
    return f"""<section class="page-hero hero-split">
  <div class="hero-img art">{photo(meta.get("hero_img"),1400)}{hero_art(th)}</div>
  <div class="wrap">
    <div class="hero-text">
      <nav class="crumb"><a href="index.html">HOME</a><span>›</span>{meta["crumb"]}</nav>
      <span class="kick">{meta["script"]}</span>
      <h1>{meta["h1"]}</h1>
      <p class="lead">{meta["lead"]}</p>
      <div class="hero-offer">{meta["intro_price"]}</div>
    </div>
  </div>
</section>"""

def hero_full(meta, th):
    return f"""<section class="page-hero">
  <div class="hero-art">{photo(meta.get("hero_img"),1600)}{hero_art(th)}</div>
  <div class="hero-veil"></div>
  <div class="wrap hero-content">
    <span class="script">{meta.get("method_en","")}</span>
    <h1>{meta["h1"]}</h1>
    <p class="lead">{meta.get("lead","")}</p>
  </div>
</section>"""

def skin_diagram():
    def panel(x,label,kind):
        s=f'<rect x="{x}" y="18" width="200" height="32" rx="6" fill="#f3e7d4"/>'
        s+=f'<rect x="{x}" y="50" width="200" height="58" rx="6" fill="#e6d2b3"/>'
        s+=f'<text x="{x+8}" y="38" font-family="Noto Sans JP,sans-serif" font-size="9" fill="#8a7c5e">表皮</text>'
        s+=f'<text x="{x+8}" y="76" font-family="Noto Sans JP,sans-serif" font-size="9" fill="#8a7c5e">真皮</text>'
        s+=f'<circle cx="{x+100}" cy="98" r="7" fill="#7a5a36"/>'
        if kind=='healthy':
            for dx,dy in [(74,78),(100,62),(128,80),(112,44)]:
                s+=f'<circle cx="{x+dx}" cy="{dy}" r="3" fill="#a9763f"/>'
            s+=f'<path d="M{x+100} 26 l-4 8 M{x+100} 26 l4 8 M{x+100} 26 l0 13" stroke="#7c8a4e" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
        else:
            for dx,dy in [(78,40),(94,36),(110,40),(86,48),(102,48),(96,30),(120,46)]:
                s+=f'<circle cx="{x+dx}" cy="{dy}" r="3.2" fill="#8a5a30"/>'
        s+=f'<text x="{x+100}" y="130" text-anchor="middle" font-family="Shippori Mincho,serif" font-size="13" fill="#5E574A">{label}</text>'
        return s
    return ('<svg viewBox="0 0 440 145" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto">'
            + panel(10,"健康な肌","healthy") + panel(230,"シミのある肌","spot") + '</svg>')

def face_svg(pattern):
    if pattern=="solar":
        spots=('<g fill="#9c6a37" stroke="none">'
               '<circle cx="93" cy="95" r="3.4" opacity=".85"/><circle cx="101" cy="103" r="2.5" opacity=".8"/>'
               '<circle cx="86" cy="105" r="2.1" opacity=".7"/><circle cx="104" cy="90" r="1.9" opacity=".7"/></g>')
    elif pattern=="freckle":
        pts=[(66,86),(72,84),(78,85),(60,92),(67,93),(75,93),(83,92),(90,90),(58,99),(66,101),(74,101),(83,100),(91,99),(70,107),(80,107)]
        spots='<g fill="#a9763f" stroke="none" opacity=".72">'+"".join(f'<circle cx="{x}" cy="{y}" r="1.5"/>' for x,y in pts)+'</g>'
    else:  # melasma
        spots=('<g fill="#a9763f" stroke="none">'
               '<ellipse cx="58" cy="95" rx="13" ry="10" opacity=".22"/>'
               '<ellipse cx="92" cy="95" rx="13" ry="10" opacity=".22"/>'
               '<ellipse cx="75" cy="63" rx="15" ry="6" opacity=".14"/></g>')
    face=('<g fill="none" stroke="#9b8a64" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
          '<path d="M40 72 C35 40 54 22 75 22 C96 22 115 40 110 72"/>'
          '<path d="M41 74 C41 56 45 42 55 35"/><path d="M109 74 C109 56 105 42 95 35"/>'
          '<path d="M45 67 C45 60 48 54 54 50 C59 37 68 31 75 31 C82 31 91 37 96 50 C102 54 105 60 105 67 C105 87 97 108 86 121 C81 127 78 129 75 129 C72 129 69 127 64 121 C53 108 45 87 45 67 Z"/>'
          '<path d="M45 80 q-6 2 -4 9"/><path d="M105 80 q6 2 4 9"/>'
          '<path d="M55 73 q8 -4 16 -1"/><path d="M79 72 q9 -3 16 1"/>'
          '<path d="M56 81 q7 -4 14 0"/><path d="M80 81 q8 -4 14 0"/>'
          '<path d="M75 83 l-3 15 q3 2 6 0"/>'
          '<path d="M67 110 q8 5 16 0"/>'
          '</g>')
    return ('<svg viewBox="0 0 150 152" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto">'
            '<circle cx="75" cy="76" r="71" fill="#FBF8F0"/>'
            '<circle cx="75" cy="76" r="71" fill="none" stroke="#E4DCC8" stroke-width="1.4"/>'
            + face + spots + '</svg>')

def video_block(v):
    # v = (title, youtube_id) なら実埋め込み、文字列だけなら準備中プレースホルダ
    title, vid = (v[0], v[1]) if isinstance(v, (list, tuple)) else (v, None)
    if vid:
        frame = (f'<div class="frame"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" '
                 f'title="{title}" loading="lazy" '
                 f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
                 f'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>')
    else:
        frame = '<div class="frame"><span class="play"></span></div>'
    return f'<div class="video reveal"><h4>{title}</h4>{frame}</div>'

def treatment_page(meta):
    th, mo = meta["theme"], meta["motif"]
    P = [hero_full(meta, th)]

    # イントロ（メソアクティス紹介）
    if meta.get("intro_paras"):
        paras = "".join(f"<p>{x}</p>" for x in meta["intro_paras"])
        link = f'<p class="linkrow"><a href="{meta["clinic_link"][1]}">{meta["clinic_link"][0]}</a></p>' if meta.get("clinic_link") else ""
        P.append(f'<section class="section cream"><div class="wrap">{khead(meta["method_label"],meta.get("method_en","Mesoactis"),center=True)}<div class="proseblock reveal">{paras}{link}</div></div></section>')

    # こんなお悩み（CHECK）＋ 〜とは（ABOUT）は同一セクションにまとめる
    # こんなお悩み（CHECK）カード — ABOUT セクションの中（見出しの下）に入れる
    check_card = ""
    if meta.get("concern_list"):
        items = "".join(f"<li>{x}</li>" for x in meta["concern_list"])
        check_card = f'<div class="concern-card reveal" style="margin-bottom:48px"><h3 class="concern-card-ttl">{meta.get("concern_title","こんなお悩みありませんか？")}</h3><ul class="concern-check">{items}</ul></div>'

    # 〜とは（図解）※ 図版キー whatis_img があるときだけ図を出す
    if meta.get("whatis"):
        t, txt = meta["whatis"]
        wimg = meta.get("whatis_img")
        fig = (f'<figure class="skin-fig reveal">{photo(wimg,1100)}<figcaption>※ イメージ図</figcaption></figure>'
               if wimg and wimg in IMGDATA else "")
        prose_style = "text-align:left;margin:0 auto 40px" if fig else "text-align:left;margin:0 auto"
        cause_html = ""
        if meta.get("cause_grid"):
            cells = "".join(f'<div class="cause-cell reveal"><span class="cause-ic">{cause_icon(k)}</span><span class="cause-lb">{lb}</span></div>' for k, lb in meta["cause_grid"])
            note = f'<p class="cause-note">{meta.get("cause_note","")}</p>' if meta.get("cause_note") else ""
            cause_html = (f'<div class="cause-sub">{meta.get("cause_grid_title","主な原因")}</div>'
                          f'<div class="cause-grid">{cells}</div>{note}')
        about_inner = (f'<div class="wrap">{khead(t,"About")}{check_card}'
                       f'<div class="proseblock reveal" style="{prose_style}"><p>{txt}</p></div>'
                       f'{cause_html}{fig}</div>')
        P.append(f'<section class="section cream">{about_inner}</section>')
    elif check_card:
        P.append(f'<section class="section cream"><div class="wrap">{check_card}</div></section>')

    # 種類 ※ ty_<pattern> 画像があれば添える。無ければテキストのみ行
    if meta.get("types"):
        def _trow(n, d, p):
            key = "ty_" + p if p else None
            if key and key in IMGDATA:
                return f'<div class="type-row reveal"><div class="type-photo">{photo(key,360)}</div><div><h4>{n}</h4><p>{d}</p></div></div>'
            return f'<div class="type-row text-only reveal"><div><h4>{n}</h4><p>{d}</p></div></div>'
        rows = "".join(_trow(n, d, p) for n, d, p in meta["types"])
        _tfig = (f'<div class="type-figure reveal"><img src="img/{meta["type_img"]}" alt="{meta.get("types_title","")}" loading="lazy" decoding="async"></div>'
                 if meta.get("type_img") else "")
        P.append(f'<section class="section cream"><div class="wrap narrow">{khead(meta.get("types_title","シミの種類"),"Type")}{_tfig}<div>{rows}</div></div></section>')

    # 特定のお悩み（マスクニキビ・しこりニキビ等）※ topics があれば1セクションに集約
    if meta.get("topics"):
        blocks = ""
        for title, parts in meta["topics"]:
            sub = "".join(f'<div class="topic-part"><h4>{sh}</h4><p>{tx}</p></div>' for sh, tx in parts)
            blocks += f'<div class="topic reveal"><h3 class="topic-h">{title}</h3>{sub}</div>'
        P.append(f'<section class="section cream"><div class="wrap narrow">{khead(meta.get("topics_title","気になるニキビ"),"Concern")}{blocks}</div></section>')

    # 施術について（施術内容・流れ・動画・症例・注意を1セクションに集約）
    tsub = []
    if meta.get("treatment"):
        tl_, td = meta["treatment"]
        feat = ""
        if meta.get("feature_cols"):
            fc = meta["feature_cols"]
            if len(fc) == 2:
                a, b = fc
                feat = (f'<div class="feat-cols"><div class="feat-col"><div class="feat-h">{a[0]}</div><p>{a[1]}</p></div>'
                        f'<div class="feat-plus">＋</div>'
                        f'<div class="feat-col"><div class="feat-h">{b[0]}</div><p>{b[1]}</p></div></div>')
            else:
                cols = "".join(f'<div class="feat-col"><div class="feat-h">{t}</div><p>{x}</p></div>' for t, x in fc)
                feat = f'<div class="feat-cols feat-cols-{len(fc)}">{cols}</div>'
        _tm = meta.get("treatment_media","tall")
        _tvw,_tvh = (820,560) if _tm=="wide" else (620,820)
        tsub.append(f'<div class="tsub">{khead2(meta.get("treatment_title","施術内容"),"Method")}<div class="split reveal"><div class="media {_tm} art">{mfill(th,_tvw,_tvh,mo,meta.get("img1_key"),max(_tvw,_tvh))}</div><div class="txt"><p class="eyebrow">{meta.get("method_en","")}</p><h3>{tl_}</h3><p>{td}</p></div></div>{feat}</div>')
    if meta.get("flow"):
        tl = "".join(f'<div class="fstep reveal"><div class="fstep-head"><div class="lbl"><span class="s">Step</span><span class="n">0{i+1}</span></div><div class="ln"></div></div><div class="fstep-body"><h4>{s[0]}</h4><p>{s[1]}</p></div></div>' for i,s in enumerate(meta["flow"]))
        tsub.append(f'<div class="tsub">{khead2("施術の流れ","Step")}<div class="flow-min">{tl}</div></div>')
    if meta.get("videos"):
        vids = "".join(video_block(v) for v in meta["videos"])
        tsub.append(f'<div class="tsub">{khead2("解説動画","Movie")}<div class="videos">{vids}</div></div>')
    if meta.get("case_img") or meta.get("cases"):
        if meta.get("case_img"):
            if meta.get("case_steps"):
                _steps = "".join(f'<span class="step"><b>{l}</b>{d}</span>' for l, d in meta["case_steps"])
                _cap_html = f'<div class="case-steps">{_steps}</div>'
            else:
                _cap_html = f'<p class="case-cap">{meta.get("case_cap","左：術前　／　右：術後")}</p>'
            case_html = (f'<div class="case-frame has-img reveal">'
                         f'<img src="img/{meta["case_img"]}" alt="{meta.get("title","")} 施術の症例" loading="lazy" decoding="async">'
                         f'{_cap_html}</div>')
        else:
            case_html = f'<div class="case-frame reveal">{meta["cases"]}</div>'
        tsub.append(f'<div class="tsub">{khead2("施術の症例写真","Case")}{case_html}</div>')
    if meta.get("risks") or meta.get("contra"):
        left = f'<div class="notice-col"><h4>副作用・リスク</h4><p>{meta["risks"]}</p></div>' if meta.get("risks") else ""
        right = ""
        if meta.get("contra"):
            items = "".join(f"<li>{x}</li>" for x in meta["contra"])
            right = f'<div class="notice-col"><h4>禁忌事項</h4><ul class="bullets">{items}</ul></div>'
        tsub.append(f'<div class="tsub">{khead2("注意事項","Notice")}<div class="notice-card reveal">{left}{right}</div></div>')
    if tsub:
        P.append(f'<section class="section beige"><div class="wrap">{khead("施術について","Treatment",center=True)}{"".join(tsub)}</div></section>')

    # お客様の声
    if meta.get("voice_more"):
        P.append(f'<section class="section cream"><div class="wrap">{khead("施術のお客様の声","Voice",center=True)}<p class="vlead reveal">実際に施術を受けられたお客様から、うれしいお声をいただいています。</p><div style="text-align:center"><a class="btn btn-solid" href="voice.html">さらにお客様のお声を見る</a></div></div></section>')

    # 料金
    if meta.get("pricing"):
        pr = meta["pricing"]; fr = pr.get("first")
        first_html = ""
        if fr:
            first_html = (f'<div class="price-first reveal"><div class="lbl">◆ 初回限定価格</div><div class="nm">{fr["name"]}</div>'
                          f'<div><span class="was2">{fr["was"]}</span><span class="amt">{fr["now"]}</span></div>'
                          f'<div style="margin-top:6px;font-size:12px;color:var(--ink-soft)">{fr["tax"]}</div></div>')
        menu = "".join(f'<div class="mrow"><span class="mn">{n}</span><span class="mp">{p}<small>{tax}</small></span></div>' for n,p,tax in pr["menu"])
        opt_html = ""
        if pr.get("options"):
            orows = "".join(f'<div class="mrow"><span class="mn">{n}</span><span class="mp">{p}<small>{tax}</small></span></div>' for n,p,tax in pr["options"])
            opt_html = f'<p class="menu-h" style="margin-top:26px">◆ オプション（組み合わせ自由）</p><div class="menu-table reveal">{orows}</div>'
        P.append(f'''<section class="section beige" id="price"><div class="wrap">{khead("施術の料金","Price",center=True)}
        {first_html}
        <p class="menu-h">◆ 通常メニュー</p>
        <div class="menu-table reveal">{menu}</div>
        {opt_html}
        <p class="price-note" style="text-align:center;margin-top:16px">{meta.get("price_note","※ 表示は税込価格です。※ 完全予約制・初回カウンセリング無料。")}</p>
        </div></section>''')

    # よくある質問
    if meta.get("faq"):
        items = "".join(f'<div class="qaitem reveal"><div class="q"><span class="qn">Q{i+1}</span><span>{q}</span></div><div class="a">{a}</div></div>' for i,(q,a) in enumerate(meta["faq"]))
        P.append(f'<section class="section cream"><div class="wrap">{khead("施術のよくある質問","Question",center=True)}<div class="qa">{items}</div></div></section>')

    # ほかのお悩み・施術（他症状への遷移）
    if meta.get("related"):
        rc = "".join(
            f'<a class="rel-card reveal" href="{href}"><div class="media art">{mfill(t2,560,360,m2,ik,700)}</div>'
            f'<div class="rc-body"><div><span class="en">{en}</span><h4>{jp}</h4></div><span class="arr">›</span></div></a>'
            for en,jp,href,t2,m2,ik in meta["related"])
        P.append(f'<section class="section cream"><div class="wrap">{khead("ほかのお悩み・施術","Menu",center=True)}<div class="related-grid">{rc}</div></div></section>')

    import re as _re
    _bg = [0]
    def _alt(m):
        c = "cream" if _bg[0] % 2 == 0 else "beige"
        _bg[0] += 1
        return f'<section class="section {c}">'
    _body = _re.sub(r'<section class="section (?:cream|beige)">', _alt, "\n".join(P))
    return page(meta["title"], _body, css=f'treatment-{meta["theme"]}.css')

# === シミ・肝斑（メソアクティス） ===
shimi = dict(
    title="シミ・肝斑でお悩みの方", crumb="シミ・肝斑", theme="shimi", motif="radiance",
    hero_img="texture", img1_key="mesoactis", treatment_media="wide",
    script="Menu", h1="シミ・肝斑でお悩みの方",
    lead="皮膚科専門医監修のメソアクティス（エレクトロポレーション）で、シミ・肝斑・くすみにアプローチします。",
    intro_price='<span class="was">通常 ¥20,000</span><span class="now">初回 ¥11,000</span><span class="tag">初回限定</span><span class="note">税込</span>',
    method_label="メソアクティス（エレクトロポレーション）", method_en="Mesoactis",
    intro_paras=[
      "当サロンのシミ・肝斑の施術は、皮膚科専門医監修のもと行っています。皮膚科や形成外科、美容外科などで行われている光・レーザーのシミ・肝斑治療はちょっと怖い、痛そうだから躊躇してしまう。でも、効果はしっかり実感したいという方に向いています。",
      "確かに当サロンのシミ・肝斑の施術は光・レーザー治療のように即効性はありませんが、美白効果が期待できますので、お客様からは徐々にシミ・肝斑が薄くなったり、お肌がワントーン明るくなって自信がもてたという嬉しいご報告をたくさんいただいています。",
      "肝斑ケアではメソアクティス（エレクトロポレーション）、シミ・肝斑の予防ではエンビロンのトリートメントが人気のメニューです。即効性のある光・レーザー治療にご興味をお持ちの方は、当サロン提携の皮膚科クリニックをご紹介いたしますのでお気軽にお問い合わせください。",
    ],
    clinic_link=("提携皮膚科クリニックのホームページはこちらから", "#"),
    whatis=("シミとは",
      "シミとは、紫外線や活性酸素のダメージで傷ついたメラノサイトがメラニンを過剰生成することで起こります。本来メラニンは新陳代謝によって排出されますが、皮膚の機能が衰え新陳代謝が悪くなると、メラニンが皮膚にとどまりシミができてしまいます。メラノサイト自体のはたらきが鈍り、メラニンが過剰に出続けている状態で表面からはたらきかけても根本的なケアにはなりません。あわせてメラノサイトのはたらきをコントロールする必要があります。"),
    whatis_img="skin_diagram",
    treatment_title="シミ・肝斑の施術",
    types=[
      ("日光黒子（老人性色素斑）","40代以降にできはじめることが多い最も一般的なシミで、紫外線が主な原因と言われています。紫外線を浴びやすい顔によくできますが、手の甲にできることも少なくありません。一度できると自然に消えることはなく、徐々に濃くなったり盛り上がったりすることもあります。","solar"),
      ("雀卵斑（ソバカス）","遺伝的要素の強いシミで、幼少期から出現することも珍しくありません。細かく散らばるようにできるのが特徴で、鼻を中心とした頬によくでき、紫外線の強い夏に濃くなり、冬には薄くなります。","freckle"),
      ("肝斑","紫外線、摩擦（特にお化粧・クレンジングの際）、女性ホルモンなど様々な原因が考えられていますが、人によっても異なります。徹底した紫外線対策と摩擦の回避、ビタミン剤内服が基本ですが、改善に長期間かかる方や十分に改善しきらない方もいらっしゃいます。","melasma"),
    ],
    treatment=("メソアクティス（エレクトロポレーション）",
      "エレクトロポレーションと呼ばれる特殊な電気の力で皮膚細胞間に隙間をあけ、有用成分を大量に浸透させることができます。今まで注射でしか浸透させることが不可能と言われていた様々な有用成分を、お肌にダメージを与えることなく導入できます。シミ・肝斑やキメなどの効果が見込めます。"),
    videos=[("【うるおい皮ふ科クリニック 豊田院長による肝斑の説明】","COeOKtGLAfs"),("【メソアクティス 施術紹介】","xg5if9s4vXY")],
    flow=[
      ("カウンセリング","肌のお悩みや生活習慣などをお聞きしてカウンセリングいたします。施術の詳しいご説明と、その方にあった適切なトリートメントをご提案します。"),
      ("洗顔","スタッフがベッドにて洗顔させていただきます。"),
      ("施術（メソアクティス）","エレクトロポレーションで有用成分をお肌の奥へ届けます。"),
      ("施術後","保湿とUVケアを行います。ダウンタイムがなくお化粧してお帰りいただけます。"),
    ],
    cases="只今準備中です。",
    risks="まれに使用する溶剤が肌に合わない場合があり、かゆみや腫れ・かさつきが起こる場合がございます。",
    contra=["妊娠中の方","ペースメーカーを装着している方","心臓病の方","電子機器・金属などの人工器官を内蔵している方","静脈瘤・動脈瘤の方","てんかんの既往歴がある方"],
    voice_more=True,
    pricing=dict(
      first=dict(name="ホワイトニングトリートメント＋肝斑ケア", was="通常1回 ¥18,000", now="初回 ¥9,000", tax="（税込 ¥9,900）"),
      menu=[
        ("肝斑ケア","¥13,000","（税込 ¥14,300）"),
        ("ホワイトニングトリートメント","¥15,000","（税込 ¥16,500）"),
        ("ホワイトニングトリートメント＋肝斑ケア","¥18,000","（税込 ¥19,800）"),
        ("トータルアンチエイジングコース","¥20,000","（税込 ¥22,000）"),
      ],
    ),
    price_note="※ 完全予約制・初回カウンセリング無料。",
    faq=[
      ("しみが気になっているが、どれくらいのペースで通えば良いですか？","個人差がございますが、2〜3週間に1度のペースで5〜6回通うことをおすすめしています。その後はお肌の状態に合わせて通うことをおすすめしています。"),
      ("施術後のお肌の状態は？","皆さん、化粧水が浸透するのを実感されています。"),
      ("メソアクティスは痛いですか？","個人差はございますが、多少電気の刺激がございます。レベルは調節できますので、リラックスして受けていただけます。"),
    ],
    related=[
      ("Acne","ニキビ","treatment-nikibi.html","nikibi","drops","cleanse"),
      ("Wrinkles","しわ・たるみ","treatment-shiwa.html","shiwa","lift","smear"),
      ("Firmness","ハリ・ツヤ","treatment-hari.html","hari","serum","serum"),
    ],
)

# === ニキビ / 水素水ピーリング ===
nikibi = dict(
    title="ニキビでお悩みの方", crumb="ニキビ", theme="nikibi", motif="drops",
    hero_img="cleanse", img1_key="suiso_peeling", treatment_media="wide",
    script="Menu", h1="ニキビでお悩みの方",
    lead="水素水ピーリングで毛穴の汚れや古い角質を洗浄・吸引。原因からケアして、ニキビのできにくい肌へ整えます。",
    method_label="水素水ピーリング", method_en="Hydrogen Peeling",
    treatment_title="施術内容",
    whatis=("ニキビとは",
      "ニキビとは、皮脂の過剰分泌やニキビの原因菌であるアクネ菌の増悪、化粧品・紫外線・髪の毛や衣類・不適切な洗顔などの外的刺激や、ストレス・胃腸障害・喫煙などによるホルモンバランスの乱れといった内的要因によって毛穴がつまり、炎症が起こることでできます。ニキビは原因からケアして、できにくい肌に整えていくことが大切です。"),
    types_title="ニキビの種類", type_img="nikibi01.png",
    types=[
      ("炎症のないニキビ","毛穴がつまって、微小面皰より大きくなってきた状態のことを言います。白ニキビと黒ニキビがあります。",None),
      ("炎症を生じたニキビ","毛穴の中でアクネ菌が増殖し、炎症を起こした状態です。赤ニキビや黄ニキビがあります。",None),
    ],
    topics_title="気になるニキビ",
    topics=[
      ("マスクニキビ", [
        ("マスクニキビの原因","マスクの蒸れなどでアクネ菌が増殖し、ニキビが増えます。毎日マスクを使用するため、洗顔や予防をしてもニキビができてしまいます。"),
        ("当サロンのマスクニキビの施術方法","水素水ピーリングで、毎日の洗顔でも落としきれない毛穴の汚れをごっそり落とし、水素の力でニキビができづらくなります。"),
      ]),
      ("しこりニキビ", [
        ("しこりニキビとは","ニキビが悪化・炎症を起こし、「紫ニキビ」のような状態になると、毛穴周りにも炎症が広がります。皮膚の下に膿や血液が溜まって腫れたような状態のニキビとなり、痛みを生じたり、硬いしこりができたりします。このようにしこりができた状態を「しこりニキビ」と言います。"),
        ("当サロンのしこりニキビの施術法","当サロンの水素水ピーリング施術を受けていただいた後、提携している医療機関のうるおい皮ふ科クリニックの治療を受けていただきます。クリニックでは、ニキビに直接ステロイド剤を注射し、炎症を沈静化してニキビ跡のしこりを除去します。しこりになってしまったニキビは注射を行いますが、水素水ピーリングを継続することで、ニキビ・しこりの発生を予防することができます。"),
      ]),
    ],
    treatment=("水素水ピーリング ＋ インパクトポレーション or イオン導入",
      "高濃度の水素水でお肌をトリートメント。水素水が噴射と同時に吸引し、毛穴の汚れや古い角質を洗浄します。白ニキビや黒ニキビ等の段階で毛穴の入口を洗浄・吸引することで、ニキビに効果的です。インパクトポレーションは高濃度の美容成分をイオン化せずにお肌へ届け、イオン導入は電気の力でビタミンCをお肌の奥まで届けます。"),
    videos=[("【水素水ピーリングの有効性について】","MmbkxRqP3cA"),("【水素水ピーリング 施術紹介】","tuqjFeSY1to")],
    flow=[
      ("カウンセリング","肌のお悩みや生活習慣などをお聞きしてカウンセリングいたします。施術の詳しいご説明と、その方にあった適切なトリートメントをご提案いたします。"),
      ("洗顔","スタッフがベッドにて洗顔させていただきます。"),
      ("施術","水素水ピーリング（＋インパクトポレーション／イオン導入）を行います。"),
      ("施術後","保湿とUVケアまで行います。ダウンタイムがなく、お化粧してお帰りいただけます。"),
    ],
    cases="只今準備中です。", case_img="nikibi_case.png", case_steps=[("1回目","2020.12.26"),("6回目","2021.3.5"),("9回目","2021.5.29")],
    risks="施術後、一時的に赤みが出る場合があります。",
    contra=["過剰な皮膚疾患がある方","金属アレルギーの方","ペースメーカーを装着されている方","妊娠中、または妊娠の可能性のある方","施術部位に金属が入っている方"],
    voice_more=True,
    pricing=dict(
      first=dict(name="水素水ピーリング ＋ インパクトポレーション or イオン導入（全顔）", was="通常1回 ¥16,000", now="初回 ¥8,000", tax="（税込 ¥8,800）"),
      menu=[
        ("水素水ピーリング（全顔）","¥11,000","（税込 ¥12,100）"),
        ("水素水ピーリング（背中上部／デコルテ／お尻）","¥13,000","（税込 ¥14,300）"),
        ("水素水ピーリング（背中全体）","¥19,000","（税込 ¥20,900）"),
        ("水素水ピーリング ＋ ポレーション／イオン導入（全顔）","¥16,000","（税込 ¥17,600）"),
        ("水素水ピーリング ＋ ポレーション／イオン導入（背中上部／デコルテ／お尻）","¥20,000","（税込 ¥22,000）"),
        ("水素水ピーリング ＋ ポレーション／イオン導入（背中全体）","¥26,000","（税込 ¥28,600）"),
      ],
    ),
    price_note="※ 完全予約制・初回カウンセリング無料。",
    faq=[
      ("水素水ピーリングはどのような効果が期待できますか？","ニキビ、吹き出物などの肌トラブルの改善に期待ができます。"),
      ("水素水ピーリングは痛いですか？","ジェットの刺激はとても気持ち良く、痛みはほとんど伴いません。"),
      ("ニキビの施術は何回受ける必要がありますか？","状態にもよりますが、5〜6回の施術が必要な事が多いです。"),
      ("マスクニキビの予防や治療法はありますか？","予防としては予防効果が期待できるピーリング石鹸と「うるおいリッチミルク」でのケアを、治療としては白・赤ニキビに効果が期待できる水素水ピーリングをおすすめしています。"),
      ("マスクニキビがひどいのですが、水素水ピーリングでよくなりますか？","水素水ピーリングは毛穴の汚れ・詰まりをごっそり取り除き、水素の力で赤ニキビも沈静化させる効果が期待できます。"),
      ("ニキビの硬くなったしこりは治療できますか？","当サロンの水素水ピーリングと、提携するうるおい皮ふ科クリニックのステロイド注射を併用することで治療を行うことができます。"),
    ],
    related=[
      ("Spots","シミ・肝斑","treatment-shimi.html","shimi","radiance","serum"),
      ("Wrinkles","しわ・たるみ","treatment-shiwa.html","shiwa","lift","smear"),
      ("Firmness","ハリ・ツヤ","treatment-hari.html","hari","serum","serum"),
    ],
)

# === しわ・たるみ / スマスアップNEO ===
shiwa = dict(
    title="しわ・たるみでお悩みの方", crumb="しわ・たるみ", theme="shiwa", motif="lift",
    hero_img="smear", img1_key="smear", treatment_media="wide",
    script="Menu", h1="しわ・たるみでお悩みの方",
    lead="スマスアップNEOで、痛みやダウンタイムなく深部の筋肉とコラーゲンにアプローチ。引き締まった印象へ導くトータルエイジングケアです。",
    method_label="スマスアップNEO", method_en="SMAS-up NEO",
    treatment_title="施術内容",
    concern_title="こんなお悩みありませんか",
    concern_list=[
      "顔が老けた印象になった",
      "目の下のたるみが目立つ",
      "表情が暗く見える",
      "疲れてみえる",
    ],
    whatis=("しわとは",
      "しわは、さまざまな要因によって皮膚が下垂することにより生じます。主な原因として、下記が挙げられます。<br><br>"
      "・加齢による肌の弾力の低下<br>"
      "・加齢による乾燥（肌の水分保持力の低下）<br>"
      "・気温や湿度の低下による乾燥<br>"
      "・紫外線による真皮や表皮へのダメージから起こる弾力低下<br>"
      "・加齢による女性ホルモンの低下<br><br>"
      "以上のような要因により、しわは引き起こされます。"),
    treatment=("スマスアップNEO",
      "スマスアップNEOは、独自のRF技術を用いた、痛みやダウンタイムのないトータルエイジングケアです。顔の筋肉の老化は、反復的な筋収縮と緊張により引き起こされます。表情筋とその上部の皮膚は、軟組織の構造を保持する重要な役目を果たすリガメントで結合しているため、土台である筋肉の衰えは顔のボリュームや輪郭にも大きな影響を与えます。つまり顔のアンチエイジングにおいては、上部の皮膚だけではなく深部の筋肉の双方へのケアが重要です。<br><br>"
      "新感覚の電気パルスでダイナミックに筋肉を刺激することで、顔全体を引き締めます。同時にコラーゲン繊維へ熱を与えることで繊維芽細胞の代謝を促し、コラーゲンの再構築や長期にわたる効果の持続性を生み出します。スマスアップNEOは、即時の効果と長い持続性を兼ね備えた最新の施術法です。"),
    feature_cols=[
      ("熱効果","高周波の熱エネルギーにより皮膚深層部周辺の温度を上昇させ、コラーゲンの生成を促して肌のハリ・ツヤが向上します。むくみの改善にも効果があります。"),
      ("電気刺激","EMSや電磁パルスとは異なる高周波数帯の電気パルスにより、普段の生活では動かしにくい部分の筋肉までダイナミックに刺激し、顔全体を引き締めます。"),
    ],
    flow=[
      ("カウンセリング","肌のお悩みや生活習慣などをお聞きしてカウンセリングいたします。施術の詳しいご説明と、その方にあった適切なトリートメントをご提案いたします。"),
      ("洗顔","スタッフがベッドにて洗顔させていただきます。"),
      ("施術（スマスアップNEO）","スマスアップNEOで深部の筋肉とコラーゲンにアプローチします。"),
      ("施術後","保湿とUVケアまで行います。ダウンタイムがなく、お化粧してお帰りいただけます。"),
    ],
    cases="只今準備中です。", case_img="smas_before_after.png", case_cap="左：術前　／　右：術後　（Courtesy of Dr.Daniel Taher, Romania）",
    risks="ダウンタイムはありません。少々のほてり感や赤みが出る場合がございますが、徐々に落ち着きます。（個人差がございます。）",
    contra=["心臓ペースメーカーを装着中の方","活動的な血管疾患のある方","血栓症または血栓性静脈炎を有する方","妊娠中または授乳中の方","腫瘍がある箇所","プロテーゼが挿入されている箇所","組織内凝固がある箇所","メラノーマ・上皮腫などの悪性腫瘍がある箇所"],
    voice_more=True,
    pricing=dict(
      first=dict(name="スマスアップNEO（全顔）", was="通常1回 ¥44,000", now="初回トライアル ¥22,000", tax="（税込）"),
      menu=[
        ("全顔","¥40,000","（税込 ¥44,000）"),
      ],
    ),
    price_note="※ 各種コースもございます。詳しくはお問い合わせください。完全予約制・初回カウンセリング無料。",
    faq=[
      ("どんな効果がありますか？","輪郭形成やフェイスリフティング、筋肉の引き締め、デトックス作用、スキンタイトニングが見込めます。"),
      ("痛みはありますか？","RFによる熱と電気刺激を感じます。RFは施術部位全体がぽかぽかと温かくなり、電気刺激は多少の違和感を感じることがあります。基本的には痛みを感じにくいマイルドな施術です。"),
      ("1回で効果はでますか？","1回でも効果は出ますが、より高い効果と持続力を生み出すために、定期的に施術を受けていただくことを推奨します。"),
      ("施術間隔はどのくらいあけるとよいですか？","最初の1クール（5回）までは2〜3週間に1度のペースで、その後は1〜3ヶ月おきに1度の施術を推奨いたします。"),
    ],
    related=[
      ("Spots","シミ・肝斑","treatment-shimi.html","shimi","radiance","serum"),
      ("Acne","ニキビ","treatment-nikibi.html","nikibi","drops","cleanse"),
      ("Firmness","ハリ・ツヤ","treatment-hari.html","hari","serum","serum"),
    ],
)

# === ハリ・ツヤ / エンビロン ===
hari = dict(
    title="ハリ・ツヤでお悩みの方", crumb="ハリ・ツヤ", theme="hari", motif="serum",
    hero_img="serum", img1_key="vitamin_treatment", treatment_media="wide",
    script="Menu", h1="ハリ・ツヤでお悩みの方",
    lead="エンビロンでお肌に不足したビタミンAを補給。皮膚細胞を正常化し、皮膚本来のはたらきを取り戻します。",
    method_label="エンビロン", method_en="Environ",
    treatment_title="施術内容",
    whatis=("ハリ・ツヤとは",
      "ハリ・ツヤは、紫外線や活性酸素、加齢などにより肌のハリや弾力が失われることで低下します。肌の角質が厚くなってごわついたりくすんだりし、スキンケアをしても保湿成分などが肌に浸透しにくくなってしまいます。<br><br>"
      "ハリ・ツヤがなくなる主な原因<br>"
      "・紫外線<br>・加齢<br>・ターンオーバーの乱れ<br>・ストレス<br>・不規則な生活習慣<br>・乾燥<br>・喫煙<br>・摩擦　など"),
    treatment=("エンビロン クールビタミントリートメント",
      "エンビロンは、お肌に不足したビタミンAを補給し、皮膚細胞を正常化することで、皮膚本来のはたらきを取り戻す施術です。"),
    flow=[
      ("カウンセリング","肌のお悩みや生活習慣などをお聞きしてカウンセリングいたします。施術の詳しいご説明と、その方にあった適切なトリートメントをご提案いたします。"),
      ("洗顔","スタッフがベッドにて洗顔させていただきます。"),
      ("施術（エンビロン クールビタミントリートメント）","エンビロン クールビタミントリートメントを行います。"),
      ("施術後","保湿とUVケアまで行います。ダウンタイムがなく、お化粧してお帰りいただけます。"),
    ],
    cases="只今準備中です。",
    risks="「レチノイド反応」をおこす場合がございます。赤み、ほてり、腫れ、かゆみ（むずむずする）、ニキビ・吹き出物の一時的な活発化、乾燥（角質の落屑）などがあらわれることがあります。",
    contra=["妊娠中の方","ペースメーカーを使用している方","施術部位に皮膚疾患がある方"],
    voice_more=True,
    pricing=dict(
      menu=[
        ("クールビタミントリートメント","¥8,000","（税込 ¥8,800）"),
      ],
      options=[
        ("エッセンシャルトリートメント／ソノイオントリートメント（全顔）<small>導入剤をお悩み別に選択：ハリ・弾力＝ソノDFP312／乾燥＝ハイドレーティングセラム／シミ・くすみ＝ルーセントブライトセラム I&amp;II</small>","+¥6,000","（税込 ¥6,600）"),
        ("フォーカスオントリートメント アイゾーン（目元・ソノイオン部分）<small>ソノDFP312 ＋ ハイドレーティングセラム</small>","+¥4,000","（税込 ¥4,400）"),
        ("フォーカスオントリートメント エヴァネッセント（頬などのシミ・色むら・ソノイオン部分）<small>ルーセントブライトセラム I&amp;II</small>","+¥4,000","（税込 ¥4,400）"),
        ("ラックトリートメント（AHA・全顔）","+¥5,000","（税込 ¥5,500）"),
        ("ポリッシングトリートメント（オイル＋クレイ）","+¥3,000","（税込 ¥3,300）"),
      ],
    ),
    price_note="※ オプションは組み合わせ自由です。※ 完全予約制・初回カウンセリング無料。",
    faq=[
      ("ビタミンAは肌に良いのですか？","ビタミンAは皮膚の健康維持に欠かせない成分です。紫外線やフリーラジカルなどの影響でダメージを受けた皮膚は補修されにくく、受けてしまったダメージを補修するには、できる限り高濃度のビタミンAを蓄えることが重要です。"),
      ("ビタミンAはお肌に刺激などありますか？","ビタミンAを使用した際に「レチノイド反応」と呼ばれる反応をおこす可能性があります。主な症状は赤み・ほてり・腫れ・かゆみ（むずむずする）・乾燥（角質の落屑）・ニキビや吹き出物の一時的な活発化などです。アレルギー反応でも毒性反応でもないため、使い続けることで肌のビタミンAを受け入れるシステムが補修され、反応は落ち着きます。"),
      ("エンビロンのホームケア製品について","ホームケアの基本は、洗顔→トーニング→保湿（ビタミン補給）→日焼け止めのシンプルな4ステップです。まずは基本のケアからお使いいただくのがファーストステップ。ビタミンAレベルは低いものからスタートし、慣れたら次の製品をおすすめします。詳しくはお問い合わせください。"),
    ],
    related=[
      ("Spots","シミ・肝斑","treatment-shimi.html","shimi","radiance","serum"),
      ("Acne","ニキビ","treatment-nikibi.html","nikibi","drops","cleanse"),
      ("Wrinkles","しわ・たるみ","treatment-shiwa.html","shiwa","lift","smear"),
    ],
)

for m in (shimi, nikibi, shiwa, hari):
    pass

pathlib.Path(f"{OUT}/treatment-shimi.html").write_text(treatment_page(shimi), encoding="utf-8")
pathlib.Path(f"{OUT}/treatment-nikibi.html").write_text(treatment_page(nikibi), encoding="utf-8")
pathlib.Path(f"{OUT}/treatment-shiwa.html").write_text(treatment_page(shiwa), encoding="utf-8")
pathlib.Path(f"{OUT}/treatment-hari.html").write_text(treatment_page(hari), encoding="utf-8")

# ---------------- お客様の声 ----------------
voices = [
 ("メソアクティス","2回目くらいで肌のトーンが上がり、肝斑が劇的に薄くなるのを実感しました。会う人みんなに「大きなシミがなくなってる！」「肌がすごく綺麗になった」と言われて嬉しくて、自分でもケアを気をつけるようになりました。肌に無頓着だった自分が、大きな肝斑をきっかけに通うようになってから、こんなに意識が変わるとは思いませんでした。それほど効果を実感しています！","40代 女性"),
 ("メソアクティス","数年前の同窓会で、数十年ぶりに会った男性に「お前が一番老けた！」と言われ、心の中はズタボロ…。職場でお肌のきれいな人に声をかけ、メディカルエステうるおいさんを紹介していただきました。メソアクティスは施術後から顔色が明るくなるのを実感でき、翌日も友人に肌を褒めてもらえることばかり。スタッフの方々もいつも優しくて、通うのが楽しみです。今では「お肌のために何かしているの？」と聞かれることも多く、改善を実感しています。正直、同級生に心から感謝しています。","40代 女性"),
]
vcards = "".join(
 f'<div class="voice-card reveal"><span class="quote">”</span><p>{c}</p><div class="meta"><span>{n}</span><span class="tx">{tx}</span></div></div>'
 for tx,c,n in voices)
voice_body = f"""
{page_hero("VOICE","Voice","お客様の声","施術を受けられたお客様からいただいた、うれしいお声をご紹介します。","お客様の声","voice","quote","te_concept1")}
<section class="section cream">
  <div class="wrap">
    {sec_head("CUSTOMER","Voice","みなさまの声")}
    <div class="voice-grid">{vcards}</div>
  </div>
</section>
<section class="cta-banner"><div class="wrap reveal">
  <p>あなたのお悩みも、<br>一緒に整えていきましょう。</p>
  <a class="btn btn-solid" href="#">無料カウンセリングを予約する</a>
</div></section>
"""
pathlib.Path(f"{OUT}/voice.html").write_text(page("お客様の声", voice_body, css="voice.css"), encoding="utf-8")

# ---------------- お知らせ（News） ----------------
news_items = [
    ("2026.05.31", "お知らせ",   "新着情報を更新しました"),
    ("2026.05.27", "キャンペーン", "初回限定・お得なキャンペーンのお知らせ"),
    ("2026.05.10", "メニュー",   "新メニュー導入のお知らせ"),
    ("2026.04.20", "休業",      "ゴールデンウィーク休業のお知らせ"),
    ("2026.03.15", "お知らせ",   "公式LINEアカウントを開設しました"),
    ("2026.02.01", "メニュー",   "化粧品（エンビロン）取り扱い開始のお知らせ"),
]
news_rows = "".join(
    f'<li class="nrow reveal"><div class="nmeta"><time class="ndate">{d}</time>'
    f'<span class="ncat">{c}</span></div><a class="ntitle" href="news-single.html">{t}</a></li>'
    for d, c, t in news_items)
NEWS_HERO_IMG = '<div class="hero-art"><img class="ph" src="img/texture.jpg" alt=""></div>\n  <div class="hero-veil"></div>'
news_body = f"""<section class="page-hero">
  {NEWS_HERO_IMG}
  <div class="wrap hero-content">
    <span class="script">News</span>
    <h1>お知らせ</h1>
    <p class="lead">うるおいからのお知らせ・キャンペーン情報をご案内します。</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal"><span class="mark">INFORMATION</span><span class="script">News</span><h2 class="ttl">新着情報</h2></div>
    <ul class="nlist">{news_rows}</ul>
  </div>
</section>"""
pathlib.Path(f"{OUT}/news.html").write_text(page("お知らせ", news_body, css="news.css"), encoding="utf-8")

# お知らせ 記事詳細（news single）
_ns_date, _ns_cat, _ns_title = news_items[1]
_ns_paras = [
    "平素よりメディカルエステ うるおいをご利用いただき、誠にありがとうございます。",
    "このたび、初めてご来院いただくお客様を対象に、対象施術がお得にお試しいただける初回限定キャンペーンを実施いたします。日頃のお肌のお悩みに寄り添い、本来の美しさを引き出すケアをぜひこの機会にご体感ください。",
    "期間中は人気の施術メニューを特別価格でご用意しております。カウンセリングは無料です。お肌の状態やご希望に合わせて、最適なプランをご提案いたしますので、お気軽にご相談ください。",
    "ご予約・お問い合わせは、お電話または公式LINEより承っております。皆さまのご来院を心よりお待ちしております。",
]
_ns_body = "".join(f"<p>{p}</p>" for p in _ns_paras)
news_single_body = f"""<section class="page-hero">
  {NEWS_HERO_IMG}
  <div class="wrap hero-content">
    <span class="script">News</span>
    <h1>{_ns_title}</h1>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <div class="nsingle reveal">
      <div class="nmeta-s"><time class="ndate">{_ns_date}</time><span class="ncat">{_ns_cat}</span></div>
      <div class="nbody">{_ns_body}</div>
      <a class="nback" href="news.html">‹ お知らせ一覧へ戻る</a>
    </div>
  </div>
</section>"""
pathlib.Path(f"{OUT}/news-single.html").write_text(page(_ns_title, news_single_body, css="news.css"), encoding="utf-8")

# ---------------- 料金表 ----------------
def pl_rows(rows):
    return "".join(f'<div class="mrow"><span class="mn">{n}</span><span class="mp">{p}<small>{tax}</small></span></div>' for n,p,tax in rows)

def pl_cat(anchor, jp, en, tag, thumb, first, rows, options=None):
    fh = ""
    if first:
        nm, was, now, tax = first
        fh = (f'<div class="pl-first"><span class="pl-tag">初回限定</span>'
              f'<span class="pl-first-nm">{nm}<small>通常 {was}</small></span>'
              f'<span class="pl-first-amt">{now}<small>{tax}</small></span></div>')
    head = (f'<div class="pcat-head"><div class="pcat-thumb">{photo(thumb,300)}</div>'
            f'<div class="pcat-meta"><span class="pcat-en">{en}</span><h3 class="pcat-jp">{jp}</h3><p class="pcat-tag">{tag}</p></div></div>')
    opt = ""
    if options:
        opt = f'<p class="pl-sub" style="margin-top:24px">オプション（組み合わせ自由）</p><div class="menu-table">{pl_rows(options)}</div>'
    return f'<div class="pcat reveal" id="{anchor}">{head}{fh}<div class="menu-table">{pl_rows(rows)}</div>{opt}</div>'

_PNAV = "".join(f'<a href="#{a}">{j}</a>' for a,j in [
  ("price-shimi","シミ・肝斑"),("price-nikibi","ニキビ"),("price-shiwa","しわ・たるみ"),("price-hari","ハリ・ツヤ")])

price_body = f"""
{page_hero("PRICE","Price","料金表","施術メニューと料金のご案内です。完全予約制となっております。","料金表","price","botanical","te_pickup")}
<section class="section cream">
  <div class="wrap narrow">
    <div class="price-nav reveal">{_PNAV}</div>
    {pl_cat("price-shimi","シミ・肝斑","Mesoactis","メソアクティス（エレクトロポレーション）","mesoactis",
      ("ホワイトニングトリートメント＋肝斑ケア","¥18,000","初回 ¥9,000","（税込 ¥9,900）"),
      [("肝斑ケア","¥13,000","（税込 ¥14,300）"),
       ("ホワイトニングトリートメント","¥15,000","（税込 ¥16,500）"),
       ("ホワイトニングトリートメント＋肝斑ケア","¥18,000","（税込 ¥19,800）"),
       ("トータルアンチエイジングコース","¥20,000","（税込 ¥22,000）")])}
    {pl_cat("price-nikibi","ニキビ","Hydrogen Peeling","水素水ピーリング","suiso_peeling",
      ("水素水ピーリング＋ポレーション／イオン導入（全顔）","¥16,000","初回 ¥8,000","（税込 ¥8,800）"),
      [("水素水ピーリング（全顔）","¥11,000","（税込 ¥12,100）"),
       ("水素水ピーリング（背中上部／デコルテ／お尻）","¥13,000","（税込 ¥14,300）"),
       ("水素水ピーリング（背中全体）","¥19,000","（税込 ¥20,900）"),
       ("＋ポレーション／イオン導入（全顔）","¥16,000","（税込 ¥17,600）"),
       ("＋ポレーション／イオン導入（背中上部／デコルテ／お尻）","¥20,000","（税込 ¥22,000）"),
       ("＋ポレーション／イオン導入（背中全体）","¥26,000","（税込 ¥28,600）")])}
    {pl_cat("price-shiwa","しわ・たるみ","SMAS-up NEO","スマスアップNEO","スマスアップ",
      ("スマスアップNEO（全顔）","¥44,000","初回トライアル ¥22,000","（税込）"),
      [("全顔","¥40,000","（税込 ¥44,000）")])}
    {pl_cat("price-hari","ハリ・ツヤ","Environ","エンビロン クールビタミントリートメント","vitamin_treatment",
      None,
      [("クールビタミントリートメント","¥8,000","（税込 ¥8,800）")],
      options=[
       ("エッセンシャル／ソノイオントリートメント（全顔）","+¥6,000","（税込 ¥6,600）"),
       ("フォーカスオン アイゾーン（目元・部分）","+¥4,000","（税込 ¥4,400）"),
       ("フォーカスオン エヴァネッセント（部分）","+¥4,000","（税込 ¥4,400）"),
       ("ラックトリートメント（AHA・全顔）","+¥5,000","（税込 ¥5,500）"),
       ("ポリッシングトリートメント（オイル＋クレイ）","+¥3,000","（税込 ¥3,300）")])}
    <p class="price-note">※ 完全予約制となります。初回はカウンセリング無料です。<br>※ 各種コース・お得なキャンペーンの詳細はカウンセリング時にご案内いたします。<br>※ 肌トラブルのご相談は、提携「うるおい皮ふ科クリニック」院長へ直接おつなぎいたします。</p>
  </div>
</section>
<section class="cta-banner"><div class="wrap reveal">
  <p>料金やコースのご相談も、<br>お気軽にお問い合わせください。</p>
  <a class="btn btn-solid" href="#">無料カウンセリングを予約する</a>
</div></section>
"""
pathlib.Path(f"{OUT}/price.html").write_text(page("料金表", price_body, css="price.css"), encoding="utf-8")

# ---------------- 化粧品 ----------------
SHOP_URL = "https://verilab.jp/shop"
def prod_card(name, sub, price, tax, desc, img="cream", tag=""):
    sub_h = f'<span class="pc-sub">{sub}</span>' if sub else ""
    price_h = f'<div class="pc-price">{price}<small>{tax}</small></div>' if price else ""
    tag_h = f'<span class="pc-tag">{tag}</span>' if tag else ""
    return (f'<div class="product-card reveal"><div class="media wide art">{mfill("cosmetics",600,420,"cosmetics",img,600)}{tag_h}</div>'
            f'<div class="pc-body"><h4>{name}{sub_h}</h4>{price_h}<p>{desc}</p></div></div>')

env_pc = "".join([
  prod_card("モイスチャー1セット","", "¥8,200","（税込 ¥9,020）","エンビロンを初めて使われる方におすすめ。洗顔から保湿までラインでお試しできるセットです。ビタミンA配合の保湿ジェルと美容クリームで、うるおいに満ちた明るく健康的な肌に。","cream","初めての方に"),
  prod_card("クレンジングジェル","ノーマル肌・オイリー肌","¥4,400","（税込 ¥4,840）","肌のうるおいを保ちながら、メイクも汚れもすっきり落とします。弱酸性の泡立つジェル状洗顔料。","serum"),
  prod_card("クレンジングクリーム","すべての肌","¥4,400","（税込 ¥4,840）","メイクも汚れも落としながら肌のうるおいも保つ、クリーム状洗顔料。やさしくしっとり洗い上げます。","texture"),
])
acseine_pc = prod_card("アクセーヌ スーパーサンシールド ブライトヴェール ＜ナチュラルカバー＞","","¥4,000","（税込 ¥4,400）","紫外線や刺激から守り抜く日やけ止め。潤いの保護膜で、くすみ・色ムラを明るくカバーします。","serum")
uruoi_pc = "".join([
  prod_card("うるおいプラチナCEシリーズ","高濃度天然セラミド配合","","","皮膚の保湿の“カギ”であるセラミドを角質に浸透させ、不足しがちなセラミドを補います。","cream"),
  prod_card("うるおいリッチHミルク","高濃度水素含有乳液","¥2,900","（税込 ¥3,190）","安定した高濃度水素が強力に作用。抗酸化（悪玉活性酸素の除去）・抗炎症・抗アレルギー・肌バリア機能の回復・かゆみの軽減が期待できます。","texture"),
])
def shop_card(name, rating, count, sub_price, single_price, img="img/cream.jpg"):
    return (f'<div class="product-card reveal"><div class="media wide art"><img class="ph" src="{img}" alt="{name}" decoding="async"></div>'
            f'<div class="pc-body"><h4>{name}</h4>'
            f'<div class="pc-2price"><div class="pc-pr"><span class="lbl">定期初回価格</span><span class="amt">{sub_price}</span></div>'
            f'<div class="pc-pr single"><span class="lbl">単品価格</span><span class="amt2">{single_price}</span></div></div></div></div>')
verilab_pc = "".join([
  shop_card("SIGNATURE 重曹水素クエン酸","4.4","16","¥3,240","¥10,800","img/VELILAB_zyusou.png"),
  shop_card("オーガニックオイルインミスト","4.5","16","¥3,300","¥8,250","img/VERILAB_mist.png"),
  shop_card("オーガニックミルク","4.6","18","¥3,300","¥9,625","img/VERILAB_milk.png"),
])
denba_pc = ('<div class="product-card reveal"><div class="media wide art">'
            '<img class="ph" src="img/denba.png" alt="DENBA Health" decoding="async"></div>'
            '<div class="pc-body"><h4>DENBA Health</h4>'
            '<p>特殊な電界技術で、体の内側からめぐりとコンディションをサポートする健康機器。ご自宅でのリラックスタイムにお使いいただけます。サロンでもご体感いただけますので、お気軽にお問い合わせください。</p></div></div>')
cos_body = f"""
{page_hero("PRODUCTS","Products","お取り扱い製品","化粧品・健康機器など、お取り扱い製品のご案内です。","化粧品","cosmetics","cosmetics","serum")}
<section class="section cream">
  <div class="wrap">
    <h3 class="brand-head">エンビロン<span class="en">ENVIRON</span></h3>
    <p class="brand-intro">お肌の状態に合わせてビタミンAの濃度を段階的に高めていく、エンビロン独自の「ステップアップシステム」を採用。ビタミンAの量を徐々に増やしながら、トラブルのないみずみずしい美肌へと導きます。ご自宅での「ホームケア」とサロンでの「フェイシャルトリートメント」のダブルケアをおすすめしています。カウンセリングで、お客様とともに理想の肌を目指します。</p>
    <p class="pl-sub" style="text-align:left;margin-bottom:18px">おすすめ製品</p>
    <div class="product-grid">{env_pc}</div>
    <div class="shop-link"><a class="btn btn-green" href="{SHOP_URL}" target="_blank" rel="noopener">オンラインショップで購入する</a></div>
  </div>
</section>
<section class="section beige">
  <div class="wrap">
    <h3 class="brand-head">アクセーヌ<span class="en">ACSEINE</span></h3>
    <p class="brand-intro">化粧品によるトラブルを繰り返さないための理論を研究した、お肌にやさしい化粧品です。</p>
    <p class="pl-sub" style="text-align:left;margin-bottom:18px">おすすめ製品</p>
    <div class="product-grid">{acseine_pc}</div>
    <div class="shop-link"><a class="btn btn-green" href="{SHOP_URL}" target="_blank" rel="noopener">オンラインショップで購入する</a></div>
  </div>
</section>
<section class="section cream">
  <div class="wrap">
    <h3 class="brand-head">VERILAB<span class="en">VERILAB</span></h3>
    <p class="brand-intro">水素・オーガニック処方にこだわったスキンケアシリーズ。日々のお手入れに取り入れやすい製品を取り揃えています。</p>
    <p class="pl-sub" style="text-align:left;margin-bottom:18px">お取り扱い製品</p>
    <div class="product-grid">{verilab_pc}</div>
    <div class="shop-link"><a class="btn btn-green" href="{SHOP_URL}" target="_blank" rel="noopener">オンラインショップで購入する</a></div>
  </div>
</section>
<section class="section beige">
  <div class="wrap">
    <h3 class="brand-head">DENBA Health<span class="en">DENBA</span></h3>
    <p class="brand-intro">独自の電界技術で健康をサポートする「DENBA Health」のお取り扱いをはじめました。</p>
    <div class="product-grid">{denba_pc}</div>
  </div>
</section>
<section class="section cream">
  <div class="wrap">
    <div class="produce-head reveal">
      <span class="ph-script">Produced by Dr. Toyoda</span>
      <h3 class="ph-title">うるおい皮ふ科クリニック 豊田院長プロデュース</h3>
      <span class="ph-rule"></span>
    </div>
    <div class="product-grid">{uruoi_pc}</div>
    <p class="price-note" style="margin-top:26px">※ 取り扱い製品・在庫の詳細はお問い合わせください。</p>
  </div>
</section>
<section class="cta-banner"><div class="wrap reveal">
  <p>あなたの肌に合うケアを、<br>カウンセリングでご提案します。</p>
  <a class="btn btn-solid" href="#">製品について相談する</a>
</div></section>
"""
pathlib.Path(f"{OUT}/cosmetics.html").write_text(page("お取り扱い製品", cos_body, css="cosmetics.css"), encoding="utf-8")

# ==================== トップページ ====================
PERSON_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" style="width:34px;height:34px;color:#9c8c66"><circle cx="12" cy="8" r="4"/><path d="M5 21c0-4 3.5-6 7-6s7 2 7 6"/></svg>'

def home_page():
    # ヒーロー
    hero = f"""<section class="home-hero">
  <div class="wrap hh-grid">
    <div class="hh-text">
      <span class="hh-script">uruoi</span>
      <h1>素肌に、<br><span class="g">自信</span>と潤いを。</h1>
      <p class="hh-sub">一人ひとりのお悩みに寄り添い、<br>本来の美しさを引き出す<br>メディカルエステサロン</p>
    </div>
    <div class="hh-img">{photo("te_hero",760)}</div>
  </div>
</section>"""

    # お悩みから探す（メニュー）
    menus = [
      ("ニキビでお悩みの方","初回限定 水素ピーリング",'<span class="mprice">¥8,800</span>',"50%OFF","cleanse","treatment-nikibi.html"),
      ("ハリ・ツヤでお悩みの方","エンビロン",'<span class="mprice">¥8,800</span>',"","serum","treatment-hari.html"),
      ("しわ・たるみでお悩みの方","スマスアップNEO",'<span class="mprice" style="font-size:13px;color:var(--ink-soft)">メスを使わずリフトアップ</span>',"NEW","home_pickup","treatment-shiwa.html"),
      ("シミでお悩みの方","初回限定 メソアクティス",'<span class="mprice">¥11,000</span>',"50%OFF","te_pickup","treatment-shimi.html"),
    ]
    cards = "".join(
      f'<a class="mcard reveal" href="{href}"><div class="mcard-img">{photo(img,420)}<span class="mcard-cap">{cap}</span></div>'
      f'<div class="mcard-foot">{f"<span class=mbadge>{badge}</span>" if badge else ""}{price}<span class="mname">{name}</span></div></a>'
      for cap,name,price,badge,img,href in menus)
    menu = f'<section class="section beige"><div class="wrap">{khead("お悩みから探す","Menu",mark="MEDICAL TREATMENT")}<div class="menu-grid">{cards}</div></div></section>'

    # 注目の施術
    pickup = f"""<section class="section cream"><div class="wrap">{khead("注目の施術","Pick up",mark="PICK UP")}
    <div class="pickup-card reveal">
      <div class="pk-img">{photo("home_pickup",820)}</div>
      <div class="pk-body">
        <p class="pk-script">Pick up</p><p class="pk-en">SMAS-UP NEO</p>
        <h3>メスを使わず、<br>引き締まった印象へ。</h3>
        <p>スマスアップNEOは肌の奥のSMAS層にもアプローチ。トータルエイジングケアで、ハリ・弾力のあるリフトアップした印象を目指します。</p>
        <div class="pk-price"><span class="was">¥45,000</span><span class="now">¥22,000</span><span style="font-size:11px;color:var(--ink-soft)">初回トライアル（税込）</span></div>
        <a class="btn btn-solid" href="treatment-shiwa.html">この施術を予約する</a>
      </div>
    </div></div></section>"""

    # お知らせ
    news_items = [
      ("2026.05.31","新着情報を更新しました"),
      ("2026.05.27","お得なキャンペーンのお知らせ"),
      ("2026.05.10","新メニュー導入のお知らせ"),
      ("2026.04.20","ゴールデンウィーク休業のお知らせ"),
    ]
    ni = "".join(f'<a class="ni" href="#"><span class="nd">{d}</span><span class="nt">{t}</span></a>' for d,t in news_items)
    news = f'<section class="section beige"><div class="wrap">{khead("お知らせ","News")}<div class="news reveal">{ni}<div class="news-more"><a href="#">お知らせ一覧 ›</a></div></div></div></section>'

    # コンセプト
    concept = f"""<section class="section green"><div class="wrap">
    <div class="concept reveal">
      <div>
        <p class="c-script">Concept</p>
        <h3>癒しのひとときと、<br>結果を見据えたケアを。</h3>
        <p>難しいことは一切なく、しみ・たるみのお悩みからお肌に親和性のある施術を中心にしています。肌トラブルのご相談は、提携する皮膚科クリニックの院長へ直接。ご納得のうえで進められるので、安心して通っていただけます。</p>
      </div>
      <div class="c-imgs">
        <div class="ci ci1">{photo("home_concept1",640)}</div>
        <div class="ci ci2">{photo("home_concept2",560)}</div>
      </div>
    </div></div></section>"""

    # 施術内容・特徴
    trs = [
      ("ニキビ（にきび）","水素水ピーリングで毛穴の汚れや古い角質を洗浄・吸引。炎症前のニキビから、しこりになってしまったニキビまで幅広く対応します。","home_tr1",False),
      ("シミ（しみ）","メソアクティスで美容成分をお肌の奥まで浸透。シミ・そばかす・肝斑にアプローチします。光・レーザー治療をご希望の方は提携クリニックをご紹介します。","te_shimi",True),
      ("しわ・たるみ","スマスアップNEOで肌の奥のSMAS層にアプローチ。ゆるんだ筋肉を引き締め、ハリのある印象へ導きます。","te_shiwa",False),
      ("ハリ・ツヤ（化粧品）","エンビロンのステップアップシステムで、ビタミンAの濃度を段階的に。ご自宅でのホームケアとサロンのダブルケアをおすすめしています。","serum",True),
    ]
    tritems = "".join(
      f'<div class="tr-item{" rev" if rev else ""} reveal"><div class="tr-img">{photo(img,720)}</div><div class="tr-txt"><h4>{t}</h4><p>{d}</p></div></div>'
      for t,d,img,rev in trs)
    treat = f'<section class="section cream"><div class="wrap">{khead("施術内容・特徴","Treatment")}<div class="tr-list">{tritems}</div></div></section>'

    # 院長挨拶
    greet = f"""<section class="section beige"><div class="wrap">{khead("ご挨拶","Greeting")}
    <div class="greet reveal">
      <div class="g-img">{photo("home_doctor",560)}</div>
      <div>
        <p class="g-script">Greeting</p>
        <h3>みなさまに寄り添った<br>最適な治療を共に。</h3>
        <p class="g-name">豊田 雅彦</p>
        <p class="g-role">メディカルエステうるおい 代表 ／ 皮膚科専門医</p>
        <p class="g-msg">日々の忙しさやストレスにさらされた心身を癒し、「心の鏡」と言われるお肌を整えて、お客様本来の輝き・美肌を引き出すお手伝いをいたします。女性セラピストが、お一人おひとりのご要望に合わせた施術を、常に心がけております。気兼ねなくリラックスしていただける空間とおもてなしの心をコンセプトに、皆さまが美しく健やかな毎日を送れるよう精一杯ご対応いたします。</p>
      </div>
    </div></div></section>"""

    # スタッフ
    staff = [
      ("石川","親しみやすさと笑顔を大切に、お客様と接することを心がけています。"),
      ("須賀","お客様の理想の素肌が手に入れられるように、全力でサポートいたします。"),
      ("大城","お客様に寄り添い、心身ともに癒されるように、心を込めて施術いたします。"),
    ]
    sc = "".join(f'<div class="staff-card reveal"><div class="av">{PERSON_ICON}</div><h4>{n}</h4><p>{d}</p></div>' for n,d in staff)
    staff_sec = f'<section class="section cream"><div class="wrap">{khead("スタッフ紹介","Staff")}<div class="staff-grid">{sc}</div></div></section>'

    # 衛生・感染対策
    safety = ["手指アルコール消毒の徹底（お客様・スタッフ）","店内・施術ベッドなどの定期的な消毒","来店時の検温・記録、発熱時はご案内をお断り","マスク着用・手洗い・うがいの徹底","施術室・パウダールームの定期的な換気","スタッフの体調管理・健康観察"]
    sl = "".join(f"<li>{s}</li>" for s in safety)
    safety_sec = f'<section class="section beige"><div class="wrap">{khead("衛生・感染対策について","Safety")}<div class="safety-card reveal"><ul>{sl}</ul></div></div></section>'

    # アクセス・診療時間
    access = f"""<section class="section cream"><div class="wrap">{khead("アクセス・診療時間","Access",mark="INFORMATION")}
    <div class="access reveal">
      <div class="map"><span class="pin"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8 2 5 5 5 9c0 5 7 13 7 13s7-8 7-13c0-4-3-7-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg></span><span class="maplabel">メディカルエステ うるおい</span></div>
      <div class="info">
        <table class="htable"><tr><th></th><th>月</th><th>火</th><th>水</th><th>木</th><th>金</th><th>土</th><th>日/祝</th></tr>
        <tr><td style="text-align:left">平日 10:00–18:00</td><td>●</td><td>●</td><td>△</td><td>△</td><td>●</td><td>—</td><td>—</td></tr>
        <tr><td style="text-align:left">土曜 9:00–17:00</td><td></td><td></td><td></td><td></td><td></td><td>●</td><td>—</td></tr></table>
        <p class="ad">● 診療　△ 水曜・木曜は隔週で休診　— 休診（日・祝）<br><b>住所</b> 千葉県松戸市日暮3-10-2 グレースビア参番館103号<br><b>アクセス</b> 八柱駅・新八柱駅から徒歩1分<br><b>TEL</b> 047-712-2552</p>
        <a class="btn btn-line" href="#" style="margin-top:8px">WEBで予約する</a>
      </div>
    </div></div></section>"""

    body = hero + menu + pickup + news + concept + treat + greet + staff_sec + safety_sec + access
    return page("ホーム", body)

# --- トップ(index.html)は build.py では生成しない。クライアント提供の本物HTMLを採用する ---
# （旧 home_page() / index_page() はテンプレ参照用に関数定義のみ残し、書き出しはしない）
# pathlib.Path(f"{OUT}/index.html").write_text(home_page(), encoding="utf-8")

# --- 外部アセットを書き出し（css/ と js/ フォルダにまとめる）---
os.makedirs(f"{OUT}/css", exist_ok=True)
os.makedirs(f"{OUT}/js", exist_ok=True)
# 共通CSS（全ページ）＋ 下層共通CSS
pathlib.Path(f"{OUT}/css/main.css").write_text(MAIN_CSS, encoding="utf-8")
pathlib.Path(f"{OUT}/css/sub.css").write_text(SUB_CSS, encoding="utf-8")
# 下層ページ固有CSS（ソースをそのままコピー。固有が無ければ空でも可）
for _css in SUB_PAGE_CSS:
    _p = SRC / "css" / _css
    if _p.exists():
        pathlib.Path(f"{OUT}/css/{_css}").write_text(_p.read_text(encoding="utf-8"), encoding="utf-8")
# 共通JS
pathlib.Path(f"{OUT}/js/app.js").write_text(
    JS.replace("<script>", "").replace("</script>", "").strip() + "\n",
    encoding="utf-8")

print("built sub-pages:", sorted([f for f in os.listdir(OUT) if f.endswith('.html')]))

# ================= トップページ =================
def staff_av():
    return '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="8" r="4"/><path d="M4.5 20c0-4 3.6-6.2 7.5-6.2S19.5 16 19.5 20"/></svg>'

def index_page():
    H=[]
    # Hero
    H.append(f'''<section class="home-hero">
      <div class="hero-img">{photo("te_hero",1000)}</div>
      <div class="wrap"><div class="htext">
        <span class="uruoi">uruoi</span>
        <h1>素肌に、<br><span class="g">自信</span>と潤いを。</h1>
        <p class="hsub">一人ひとりのお悩みに寄り添い、<br>本来の美しさを引き出す<br>メディカルエステサロン</p>
      </div></div>
    </section>''')

    # Menu (お悩みから探す)
    def mcard(concern,img,name,price,badge,href):
        b=f'<span class="mbadge">{badge}</span>' if badge else ''
        return (f'<a class="mcard reveal" href="{href}"><div class="mimg">{photo(img,640)}<span class="mconcern">{concern}</span></div>'
                f'<div class="mbody">{b}<div class="mtxt"><span class="mname">{name}</span>{price}</div></div></a>')
    cards=(mcard("ニキビでお悩みの方","cleanse","初回限定 水素水ピーリング",'<span class="mwas">¥17,600</span><span class="mnow">¥8,800</span>','50%<br>OFF','treatment-nikibi.html')
          +mcard("ハリ・ツヤでお悩みの方","serum","エンビロン",'<span class="mnow">¥8,800</span>','','treatment-hari.html')
          +mcard("しわ・たるみでお悩みの方","te_shiwa","スマスアップNEO",'<span class="msub">メスを使わずにリフトアップ</span>','NEW','treatment-shiwa.html')
          +mcard("シミでお悩みの方","te_shimi","初回限定 メソアクティス",'<span class="mwas">¥22,000</span><span class="mnow">¥11,000</span>','50%<br>OFF','treatment-shimi.html'))
    H.append(f'<section class="section beige"><div class="wrap">{khead("お悩みから探す","Menu")}<div class="menu-grid">{cards}</div></div></section>')

    # Pickup
    H.append(f'''<section class="section cream"><div class="wrap">{khead("注目の施術","Pick up")}
      <div class="pickup reveal"><div class="pic">{photo("te_pickup",820)}</div>
      <div class="pbody"><span class="pscript">Pick up</span><div class="plabel">SMAS-UP NEO</div>
        <h3>メスを使わず、<br>引き締まった印象へ。</h3>
        <p>スマスアップNEOは肌の奥のSMAS層にもアプローチ。トータルエイジングケアで、ハリ・弾力のあるリフトアップを目指します。</p>
        <div class="pprice"><span class="was">¥45,000</span><span class="now">¥22,000</span><span class="nt">初回トライアル（税込）</span></div>
        <a class="btn btn-solid" href="treatment-shiwa.html">この施術を予約する</a>
      </div></div></div></section>''')

    # News
    news=[("2026.05.31","新着情報を更新しました"),("2026.05.27","お得なキャンペーンのお知らせ"),
          ("2026.05.10","新メニュー導入のお知らせ"),("2026.04.20","ゴールデンウィーク休業のお知らせ")]
    rows="".join(f'<a class="row" href="#"><span class="date">{d}</span><span class="nt">{t}</span></a>' for d,t in news)
    H.append(f'<section class="section beige"><div class="wrap">{khead("お知らせ","News")}<div class="news-list reveal">{rows}</div><div class="news-more"><a href="#">お知らせ一覧 ›</a></div></div></section>')

    # Concept
    H.append(f'''<section class="section green"><div class="wrap">
      <div class="concept reveal"><div class="ctext"><span class="cs">Concept</span>
        <h2>癒しのひとときと、<br>結果を見据えたケアを。</h2>
        <p>難しいことは一切なく、しみ・たるみのお悩みからお肌に親和性のある施術を中心にしています。肌トラブルのご相談は、提携する皮膚科クリニックの院長へ直接。ご納得のうえで進められるので、安心して通っていただけます。</p>
      </div>
      <div class="cimgs"><div class="c1">{photo("te_concept1",520)}</div><div class="c2">{photo("te_concept2",560)}</div></div>
      </div></div></section>''')

    # Treatment（施術内容・特徴）
    def trow(no,title,img,desc,rev):
        tx=f'<div class="tx"><span class="tno">{no}</span><h3>{title}</h3><p>{desc}</p></div>'
        pic=f'<div class="tpic">{photo(img,640)}</div>'
        inner=(tx+pic) if rev else (pic+tx)
        return f'<div class="treat-row reveal {"rev" if rev else ""}">{inner}</div>'
    tr=(trow("01","ニキビ（にきび）","cleanse","水素水ピーリングで毛穴の汚れや古い角質を洗浄・吸引。炎症前のニキビから、しこりになってしまったニキビまで幅広く対応します。",False)
       +trow("02","シミ（しみ）","te_shimi","メソアクティスで美容成分をお肌の奥まで浸透。シミ・そばかす・肝斑にアプローチします。光・レーザー治療をご希望の方は提携クリニックをご紹介します。",True)
       +trow("03","しわ・たるみ","te_shiwa","スマスアップNEOで肌の奥のSMAS層にアプローチ。ゆるんだ筋肉を引き締め、ハリのある印象へ導きます。",False)
       +trow("04","ハリ・ツヤ（化粧品）","serum","エンビロンのステップアップシステムで、ビタミンAの濃度を段階的に。ご自宅でのホームケアとサロンのダブルケアをおすすめしています。",True))
    H.append(f'<section class="section beige"><div class="wrap">{khead("施術内容・特徴","Treatment")}{tr}</div></section>')

    # Greeting
    H.append(f'''<section class="section cream"><div class="wrap">{khead("院長挨拶","Greeting")}
      <div class="greeting reveal"><div class="gpic">{photo("te_doctor",560)}</div>
      <div><span class="gs">Greeting</span><h2>みなさまに寄り添った<br>最適な治療を共に。</h2>
        <p class="gname">豊田 雅彦</p><p class="grole">メディカルエステうるおい 代表 ／ 皮膚科専門医</p>
        <p>当院は「メディカルエステうるおい」をご愛顧いただき誠にありがとうございます。提携医療機関である「うるおい皮ふ科クリニック」と密接に連携を取りながら、美のトータルケアと医療の補助的役割の架け橋を担っています。難治性ニキビ・シミ・くすみ・しわ・たるみでお悩みの方々に、結果の期待できる施術を中心に行ってまいります。お一人おひとりのご要望に合わせた施術を、常に心がけております。</p>
      </div></div></div></section>''')

    # Staff
    staff=[("石川","親しみやすさと笑顔を大切に、お客様と接することを心がけています。"),
           ("須賀","お客様の理想の素肌が手に入れられるように、全力でサポートいたします。"),
           ("大城","お客様に寄り添い、心身ともに癒されるように、心を込めて施術いたします。")]
    sc="".join(f'<div class="staff reveal"><div class="av">{staff_av()}</div><h4>{n}</h4><p>{d}</p></div>' for n,d in staff)
    H.append(f'<section class="section cream"><div class="wrap">{khead("スタッフ紹介","Staff")}<div class="staff-grid">{sc}</div></div></section>')

    # Safety
    safety=["手指アルコール消毒の徹底（お客様・スタッフ）","店内・施術ベッドなどの定期的な消毒","来店時の検温・記録、発熱時はご案内をお断り","マスク着用・手洗い・うがいの徹底","施術室・パウダールームの定期的な換気","スタッフの体調管理・健康観察"]
    si="".join(f"<li>{x}</li>" for x in safety)
    H.append(f'<section class="section beige"><div class="wrap">{khead("衛生・感染対策について","Safety")}<ul class="safety reveal">{si}</ul></div></section>')

    # Access
    H.append(f'''<section class="section cream"><div class="wrap">{khead("アクセス・診療時間","Access")}
      <div class="access reveal">
        <div class="map"><span class="pin"></span><span class="mlabel">千葉県松戸市日暮3-10-2 グレースビア参番館103号 ／ 八柱駅・新八柱駅から徒歩1分</span></div>
        <div class="info">
          <p class="tel">047-712-2552</p>
          <table>
            <tr><th>診療時間</th><td>平日 10:00–18:00 ／ 土 9:00–17:00</td></tr>
            <tr><th>休診</th><td>日曜・祝日／水曜・木曜（隔週）</td></tr>
            <tr><th>住所</th><td>千葉県松戸市日暮3-10-2 グレースビア参番館103号</td></tr>
            <tr><th>アクセス</th><td>八柱駅・新八柱駅から徒歩1分</td></tr>
          </table>
          <a class="btn btn-line" href="#" style="width:100%">WEBで予約する</a>
        </div>
      </div></div></section>''')

    return page("ホーム", "\n".join(H))

# --- 旧・自前トップ（緑基調・自動生成）は破棄。index.html は上の home_page() を採用するため上書きしない ---
# pathlib.Path(f"{OUT}/index.html").write_text(index_page(), encoding="utf-8")
# print("index.html written")
print("index.html = home_page() (top-9準拠)")
