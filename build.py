#!/usr/bin/env python3
"""Builds the Kairon Arcade portal (static). Edit SITE_URL when a custom domain is added, then re-run.
All internal links are root-relative (/about/, /play/x/), so the site works on any domain unchanged."""
import os, html, json, datetime, urllib.parse
SITE_URL = os.environ.get('SITE_URL', 'https://songyisong88.github.io')
GAMES_BASE = '/teepuan-games/'   # games stay in the songyisong88/teepuan-games repo (same origin)
OUT = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()
CATS = {'action': ('แอคชัน', 'Action'), 'timing': ('จังหวะไว', 'Timing'), 'strategy': ('วางแผน', 'Strategy'), 'puzzle': ('ไขปริศนา', 'Puzzle')}
# slug, Thai title, English title, cat, Thai line, English line, badge(th,en)
GAMES = [
 ('star-river-market','ตลาดน้ำอวกาศ','Star River Market','strategy','พายเรือขายของให้ลูกค้าต่างดาว ข้ามดาวหลายดวง มีเพื่อนสัตว์เลี้ยงช่วย','Row your boat and sell goods to alien customers across planets',('ใหม่','NEW')),
 ('notebluff','สมุดจอมกวน','Notebluff','puzzle','ปริศนาหลอกสมอง 40 ด่าน ดินสอปากดีคอยแซว','40 trick puzzles with a cheeky talking pencil',('ใหม่','NEW')),
 ('foldwind','ร่อนฟ้า','Foldwind','action','บินเครื่องร่อนกระดาษ 3 มิติ ผ่านเกาะลอยฟ้า','Glide a 3D paper plane past floating islands',('ใหม่','NEW')),
 ('dejavault-97','ปล้นข้ามเวลา','Dejavault \'97','puzzle','ย้อนเวลา 10 วิ ร่วมมือกับตัวเองในอดีต งัดตู้เซฟ','Rewind 10 seconds and team up with your past self',('ใหม่','NEW')),
 ('locktide-93','ประตูน้ำ','Locktide \'93','puzzle','คุมระดับน้ำ พาเรือทุกลำเข้าท่า','Control the water and bring every boat to port',('ใหม่','NEW')),
 ('umbramble-99','เดินบนเงา','Umbramble \'99','puzzle','เลื่อนโคมไฟให้เงากลายเป็นทางเดิน','Move the lamps so shadows become paths',('ใหม่','NEW')),
 ('clawtron-95','ตู้คีบตุ๊กตา','Clawtron \'95','timing','คีบตุ๊กตาสะสมให้ครบอัลบั้ม','Grab plushies and complete your album',('ใหม่','NEW')),
 ('mergetron-96','ร้านตู้เกมรวมร่าง','Mergetron \'96','strategy','รวมตู้เกม 18 ระดับ เก็บเงินแม้ไม่เล่น','Merge arcade cabinets through 18 levels',None),
 ('bulwark','ป้อมปราการสุดท้าย','Last Bulwark','action','ยิงเอาตัวรอด สู้บอส 3 เฟส','Auto-shooter survival with a 3-phase boss',('ฮิต','HOT')),
 ('steel-stack','หอคอยเหล็ก','Steel Stack','timing','แตะให้ถูกจังหวะ ซ้อนให้สูงที่สุด','Tap on time and stack as high as you can',('ฮิต','HOT')),
 ('frog','กบข้ามถนน','Klong Hop \'94','action','หลบรถ ขี่ขอนไม้ข้ามคลอง','Dodge cars and ride logs across the canal',None),
 ('pinball','พินบอลยุค 90','Deep Core Pinball','action','ตีลูกเจาะลงสู่แกนโลก','Smash the ball down to the Earth\'s core',None),
 ('snake','งูมือถือยุค 90','Snake \'98','timing','งูกินจุด 3 โหมด','Classic snake with 3 modes',None),
 ('retro90','เกมกดยุค 90','Pixtron Brick Game','timing','เครื่องเกมกด 9999 in 1','A 9999-in-1 brick handheld',None),
]

HOW = {
 'star-river-market': ('แตะรับออเดอร์จากลูกค้าต่างดาว พายเรือไปส่งของ เลือกทางแยกให้ดี เก็บเหรียญไปอัปเกรดเรือและแผงขายของ','Take orders from alien customers, row to deliver, pick the right river fork, and spend coins on boat and stall upgrades.'),
 'notebluff': ('อ่านโจทย์ให้ดี แตะ ลาก หรือเขย่าเพื่อหาคำตอบ บางด่านคำตอบไม่ได้อยู่ในที่ที่คิด','Read each riddle carefully, then tap, drag or shake to solve. The answer is often not where you expect.'),
 'foldwind': ('ลากนิ้วซ้ายขวาเพื่อเอียงเครื่องร่อน บินผ่านห่วงลมให้ลอยสูงขึ้น หลบเกาะและเก็บดาว','Drag left and right to bank your glider, fly through wind rings to climb, dodge islands and collect stars.'),
 'dejavault-97': ('เดินไปกดสวิตช์ภายใน 10 วินาที แล้วย้อนเวลา ตัวคุณในอดีตจะทำซ้ำท่าเดิมช่วยเปิดประตูให้','Move and press switches within 10 seconds, then rewind. Your past self repeats your moves to hold doors open.'),
 'locktide-93': ('แตะประตูน้ำเพื่อเปิดปิด ปรับระดับน้ำให้เท่ากัน แล้วพาเรือทุกลำเข้าท่า','Tap the lock gates to open or close them, level the water, and guide every boat into port.'),
 'umbramble-99': ('ลากโคมไฟไปมา เงาของสิ่งของจะกลายเป็นสะพาน พาตัวละครเดินบนเงาไปถึงประตู','Drag the lamps around so object shadows become bridges, then walk your hero along the shadows to the door.'),
 'clawtron-95': ('กดค้างเพื่อเลื่อนก้ามคีบ ปล่อยเมื่อตรงตุ๊กตา จับจังหวะให้ดีเพื่อคีบให้ติด','Hold to move the claw, release over a plushie, and time it right to grab it.'),
 'mergetron-96': ('ลากตู้เกมที่เหมือนกันมาชนกันเพื่อรวมเป็นตู้ระดับสูงขึ้น ตู้จะหาเงินให้แม้ปิดเกม','Drag two identical cabinets together to merge them into a higher level. Cabinets earn even while you are away.'),
 'bulwark': ('ลากนิ้วเพื่อเคลื่อนที่ ตัวละครยิงอัตโนมัติ กดปุ่มพุ่งเพื่อหลบ เลือกอัปเกรด 1 ใน 3 หลังทุกคลื่น','Drag to move, you shoot automatically, tap dash to dodge, and choose 1 of 3 upgrades after each wave.'),
 'steel-stack': ('แตะเมื่อบล็อกอยู่ตรงกับชั้นล่าง ส่วนที่เกินจะถูกตัดทิ้ง วางตรงเป๊ะได้คอมโบ','Tap when the block lines up with the one below. Overhangs get cut off; perfect drops build combos.'),
 'frog': ('ปัดจอหรือกดปุ่มลูกศรเพื่อกระโดด หลบรถ ขี่ขอนไม้และแพไม้ไผ่ เข้ารังให้ครบ 5 ช่อง','Swipe or use the arrow buttons to hop, dodge cars, ride logs and rafts, and fill all 5 homes.'),
 'pinball': ('แตะครึ่งซ้ายหรือขวาของจอเพื่อตีไม้ กดค้างแล้วปล่อยเพื่อยิงลูก','Tap the left or right half of the screen to flip, hold and release to launch the ball.'),
 'snake': ('ปัดจอหรือกดปุ่มเพื่อเลี้ยวงู กินจุดให้ยาวขึ้น อย่าชนตัวเอง เลือกได้ 3 โหมด','Swipe or press buttons to turn, eat dots to grow, never hit yourself. Three modes to choose from.'),
 'retro90': ('เลือกเกมในเครื่อง แล้วใช้ปุ่มทิศทางกับปุ่ม A B เล่นเหมือนเครื่องเกมกดจริง','Pick a game on the handheld and play with the D-pad and A/B buttons, just like the real thing.'),
}
e = html.escape
def bi(th, en, tag='span'):
    return f'<{tag} data-th>{e(th)}</{tag}><{tag} data-en lang="en">{e(en)}</{tag}>'

def head(title, desc, path, noindex=False, nozoom=False, image='/assets/og.png'):
    url = SITE_URL + path
    vp = 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover' if nozoom else 'width=device-width, initial-scale=1, viewport-fit=cover'
    return f'''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="{vp}">
{'<script data-kz src="/assets/no-zoom.js"></script>' if nozoom else ''}
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#12141F">{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{url}">'}
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="/assets/icon-32.png"><link rel="apple-touch-icon" href="/assets/icon-180.png"><link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website"><meta property="og:site_name" content="Kairon Arcade · ห้องเกม ไครอน"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE_URL}{image}"><meta property="og:locale" content="th_TH"><meta property="og:locale:alternate" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/site.css"><script src="/assets/config.js"></script><script src="/assets/site.js"></script>
</head><body>'''

def top(active=''):
    items = [('/', 'หน้าแรก', 'Home', 'home'), ('/about/', 'เกี่ยวกับเรา', 'About', 'about'), ('/contact/', 'ติดต่อ', 'Contact', 'contact')]
    nav = ''.join(f'<a href="{h}"{" class=on" if k==active else ""}>{bi(t,en)}</a>' for h,t,en,k in items)
    return f'''<header class="top"><a class="home" href="/"><img src="/assets/logo.png" alt="" width="34" height="34"><span><b>ห้องเกม ไครอน</b><small>KAIRON ARCADE</small></span></a>
<button class="lang" type="button" aria-label="Language / ภาษา">{bi('EN','ไทย')}</button></header><nav class="nav">{nav}</nav>'''

def foot():
    return f'''<footer class="foot"><nav><a href="/">{bi('หน้าแรก','Home')}</a><a href="/about/">{bi('เกี่ยวกับเรา','About')}</a><a href="/privacy/">{bi('นโยบายความเป็นส่วนตัว','Privacy Policy')}</a><a href="/terms/">{bi('ข้อตกลงการใช้งาน','Terms')}</a><a href="/contact/">{bi('ติดต่อเรา','Contact')}</a><button class="lk" type="button" data-consent-open>{bi('ตั้งค่าคุกกี้','Cookie settings')}</button></nav>
{bi('เล่นฟรี · © 2026 Kairon Arcade','Free to play · © 2026 Kairon Arcade','div')}</footer>
<div class="consent" id="consent" role="dialog" aria-live="polite"><p>{bi('เว็บนี้ใช้คุกกี้และพื้นที่เก็บข้อมูลในเครื่อง เพื่อจำเซฟเกม ภาษา และ (ในอนาคต) แสดงโฆษณาจาก Google และพาร์ทเนอร์ ','We use cookies and local storage to keep your game saves and language, and (in future) to show ads from Google and partners. ')}<a href="/privacy/">{bi('อ่านนโยบาย','Read policy')}</a></p>
<div class="row"><button class="yes" type="button">{bi('ยอมรับ','Accept')}</button><button class="no" type="button">{bi('ไม่ยอมรับ','Decline')}</button></div></div>
</body></html>'''

def ad(slot):
    return f'<div class="ad-slot" data-ad-slot="{slot}" aria-hidden="true"><span class="ad-label">โฆษณา</span>{bi("พื้นที่โฆษณา (ตัวอย่าง)","Ad space (preview)")}</div>'

def card(g, feat=False):
    slug, th, en, cat, lth, len_, badge = g
    img = f'/assets/thumbs/{"hero-" if feat else ""}{slug}.webp'
    b = f'<span class="badge">{bi(*badge)}</span>' if badge else ''
    return f'''<a class="cab" href="/play/{slug}/" data-c="{cat}"><div class="mq">{bi(th,en)}</div><div class="bd"><div class="scr"><img src="{img}" alt="{e(th)} · {e(en)}" loading="{"eager" if feat else "lazy"}">{b}</div>
<div class="pan"><span class="joy"></span><span class="go">{bi('แตะเล่น','PLAY')}</span><span class="bt"><i></i><i></i></span></div></div>
<div class="cat">{bi(*CATS[cat])}</div><div class="line1">{bi(lth,len_)}</div></a>'''


def share(slug, th, en):
    u = f'{SITE_URL}/games/{slug}/'
    return f'''<div class="share" data-url="{u}" data-title="{e(th)} · {e(en)} | Kairon Arcade"><button class="cta ghost" type="button" data-share>{bi('แชร์เกมนี้','Share')}</button>
<a class="cta ghost" href="https://social-plugins.line.me/lineit/share?url={urllib.parse.quote(u, safe='')}" target="_blank" rel="noopener">{bi('แชร์ไป LINE','Share to LINE')}</a>
<span class="share-msg" role="status"></span></div>'''

def write(path, s):
    p = os.path.join(OUT, path.lstrip('/'))
    if p.endswith('/'): p += 'index.html'
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)

# ---------- home
feat = GAMES[0]
tabs = '<button class="tab on" data-c="">' + bi('ทุกตู้','All') + '</button>' + ''.join(f'<button class="tab" data-c="{k}">{bi(*v)}</button>' for k,v in CATS.items())
home = head('Kairon Arcade · ห้องเกม ไครอน — เกมฟรีเล่นบนมือถือ', 'ห้องเกม ไครอน (Kairon Arcade) รวมเกม HTML5 ฟรี เล่นได้ทันทีบนมือถือและคอม ไม่ต้องโหลดแอป', '/', nozoom=True) + top('home') + f'''
<div class="sign"><div class="box"><img src="/assets/logo.png" alt="" width="46" height="46"><div><b>ห้องเกม ไครอน</b><small>KAIRON ARCADE</small></div></div>
<div class="sub">{bi('เดินเลือกตู้ แตะแล้วเล่นได้ทันที ไม่ต้องโหลดแอป','Pick a cabinet and play instantly. No app needed.')}</div></div>
<section class="feat">{bi('เกมเด่น','Featured','div class="h2" style="margin-top:6px"').replace('<div class="h2" style="margin-top:6px" data-en','<div class="h2" style="margin-top:6px" data-en')}
{card(feat, True)}
<div class="desc" style="margin-top:10px;text-align:center"><a class="cta" href="/play/{feat[0]}/">{bi('เล่นเลย','Play now')}</a></div></section>
{ad('home-top')}
<div class="h2">{bi('ตู้เกมทั้งหมด','All games')} ({len(GAMES)})</div>
<div class="tabs" id="tabs">{tabs}</div>
<div class="room" id="room">{''.join(card(g) for g in GAMES)}</div>
{ad('home-bottom')}<div class="floor"></div>''' + foot()
# fix: bi() with attributes in tag -> simple header instead
home = home.replace(bi('เกมเด่น','Featured','div class="h2" style="margin-top:6px"'), '<div class="h2" style="margin-top:6px">' + bi('เกมเด่น','Featured') + '</div>')
write('/', home)

# ---------- play wrappers
for g in GAMES:
    slug, th, en, cat, lth, len_, badge = g
    src = f'{GAMES_BASE}{slug}/'
    s = head(f'{th} · {en} — เล่นฟรี | Kairon Arcade', f'{lth} เล่นฟรีบนมือถือที่ ห้องเกม ไครอน (Kairon Arcade)', f'/play/{slug}/', nozoom=True, image=f'/assets/thumbs/{slug}.webp') + top() + f'''
<main class="play"><h1>{bi(th,en)}</h1>
<div class="stage"><iframe src="{src}" title="{e(th)} · {e(en)}" allow="autoplay; fullscreen; gamepad" allowfullscreen loading="eager"></iframe></div>
<div class="acts"><a class="cta" href="{src}">{bi('เล่นเต็มจอ','Full screen')}</a><a class="cta ghost" href="/games/{slug}/">{bi('วิธีเล่น','How to play')}</a><a class="cta ghost" href="/">{bi('เกมอื่น ๆ','More games')}</a></div>
{share(slug, th, en)}
{ad('play-below')}
<div class="about-game card" style="margin-top:6px"><p>{bi(lth,len_)}</p><p class="cat" style="text-align:left;margin-top:4px">{bi('หมวด: '+CATS[cat][0],'Category: '+CATS[cat][1])}</p></div>
</main>''' + foot()
    write(f'/play/{slug}/', s)


# ---------- SEO game pages
for g in GAMES:
    slug, th, en, cat, lth, len_, badge = g
    hth, hen = HOW[slug]
    ld = {'@context':'https://schema.org','@type':'VideoGame','name':f'{th} ({en})','alternateName':en,'description':f'{lth} — {len_}',
          'url':f'{SITE_URL}/games/{slug}/','image':f'{SITE_URL}/assets/thumbs/{slug}.webp','genre':CATS[cat][1],'inLanguage':['th','en'],
          'gamePlatform':['Web browser','Mobile web'],'applicationCategory':'Game','operatingSystem':'Any',
          'offers':{'@type':'Offer','price':'0','priceCurrency':'THB'},'isAccessibleForFree':True,
          'author':{'@type':'Organization','name':'Kairon Arcade'},'publisher':{'@type':'Organization','name':'Kairon Arcade','url':SITE_URL+'/'},
          'potentialAction':{'@type':'PlayAction','target':f'{SITE_URL}/play/{slug}/'}}
    s = head(f'{th} ({en}) — เกมฟรี เล่นบนมือถือ | Kairon Arcade', f'{th} ({en}): {lth} เล่นฟรีทันทีไม่ต้องโหลดแอป ที่ ห้องเกม ไครอน', f'/games/{slug}/', image=f'/assets/thumbs/{slug}.webp')
    s = s.replace('</head>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script></head>')
    s += top() + f'''
<main class="page"><article class="card gamepage"><img class="gthumb" src="/assets/thumbs/{slug}.webp" alt="{e(th)} · {e(en)}" width="640" height="480">
<h1>{e(th)} <span class="en-sub">{e(en)}</span></h1><p class="cat" style="text-align:left">{bi('หมวด: '+CATS[cat][0],'Category: '+CATS[cat][1])} · {bi('เล่นฟรี','Free')}</p>
<p>{bi(lth,len_)}</p>
<p style="margin:14px 0"><a class="cta big" href="/play/{slug}/">{bi('▶ เล่นเลย','▶ Play now')}</a></p>
<h2>{bi('วิธีเล่น','How to play')}</h2><p>{bi(hth,hen)}</p>
<h2>{bi('เล่นได้ที่ไหน','Where to play')}</h2><p>{bi('เล่นบนเบราว์เซอร์มือถือ แท็บเล็ต หรือคอม รวมถึงเปิดในแอป LINE ได้ ไม่ต้องติดตั้ง','Runs in any mobile, tablet or desktop browser, including inside the LINE app. No install needed.')}</p>
{share(slug, th, en)}
</article>{ad('game-page')}</main><div class="floor"></div>''' + foot()
    write(f'/games/{slug}/', s)

# ---------- text pages
def page(path, key, th_title, en_title, desc, th_body, en_body):
    s = head(f'{th_title} · {en_title} | Kairon Arcade', desc, path) + top(key) + f'''
<main class="page"><article class="card"><div data-th><h1>{th_title}</h1>{th_body}</div><div data-en lang="en"><h1>{en_title}</h1>{en_body}</div></article></main><div class="floor"></div>''' + foot()
    write(path, s)

UPD = f'<p class="upd">ปรับปรุงล่าสุด {TODAY}</p>'; UPDE = f'<p class="upd">Last updated {TODAY}</p>'
page('/about/','about','เกี่ยวกับเรา','About us','เกี่ยวกับ Kairon Arcade ห้องเกม ไครอน',
f'''<p>Kairon Arcade (ห้องเกม ไครอน) คือห้องเกมออนไลน์ของคนไทย รวมเกม HTML5 ที่เราออกแบบและเขียนขึ้นเองทั้งหมด เล่นฟรีได้ทันทีบนมือถือ แท็บเล็ต และคอม ไม่ต้องโหลดแอป ไม่ต้องสมัครสมาชิก</p>
<h2>เกมของเรา</h2><ul><li>เกมทุกเกมเป็นผลงานต้นฉบับ ภาพและเสียงสร้างขึ้นใหม่ ไม่ได้ลอกจากเกมของคนอื่น</li><li>เล่นจบได้ในเวลาสั้น ๆ เหมาะกับการเล่นแก้เบื่อระหว่างวัน</li><li>รองรับภาษาไทยเป็นหลัก หลายเกมมีภาษาอังกฤษด้วย</li><li>ความคืบหน้าในเกมเก็บไว้ในเครื่องของคุณเอง</li></ul>
<h2>ทำไมมีโฆษณา</h2><p>เราเปิดให้เล่นฟรี ในอนาคตอาจมีโฆษณาในบางจุด เช่น ใต้เกม หรือปุ่ม "ดูโฆษณาแลกรางวัล" ที่คุณเลือกกดเองได้ รายได้นี้ช่วยให้เราทำเกมใหม่ต่อไปได้</p>
<p>มีเกมให้เล่นแล้ว {len(GAMES)} เกม และจะเพิ่มขึ้นเรื่อย ๆ</p>''',
f'''<p>Kairon Arcade (ห้องเกม ไครอน) is a Thai online arcade of original HTML5 games that we design and build ourselves. Play free, instantly, on phone, tablet or computer. No app, no sign-up.</p>
<h2>Our games</h2><ul><li>Every game is original work; art and sound are made from scratch.</li><li>Short sessions, perfect for a quick break.</li><li>Thai first, many games also in English.</li><li>Your progress is saved on your own device.</li></ul>
<h2>Why ads?</h2><p>The games are free. In future some places may show ads, such as below a game or an optional "watch an ad for a reward" button. This helps us keep making new games.</p>
<p>{len(GAMES)} games available so far, with more on the way.</p>''')

page('/privacy/','privacy','นโยบายความเป็นส่วนตัว','Privacy Policy','นโยบายความเป็นส่วนตัวของ Kairon Arcade ห้องเกม ไครอน: คุกกี้ โฆษณา Google และข้อมูลเซฟในเครื่อง',
f'''{UPD}<p>นโยบายนี้อธิบายว่าเว็บ Kairon Arcade (ห้องเกม ไครอน) ที่ {SITE_URL} และเกมในเว็บ เก็บและใช้ข้อมูลอย่างไร</p>
<h2>1. ข้อมูลที่เราเก็บ</h2><ul><li>เราไม่ขอชื่อ อีเมล หรือเบอร์โทร และไม่มีระบบสมัครสมาชิก</li><li><b>ข้อมูลเซฟเกมในเครื่อง</b>: คะแนนสูงสุด ด่านที่ผ่าน ภาษา ระดับเสียง และการตั้งค่าคุกกี้ เก็บใน localStorage ของเบราว์เซอร์คุณเท่านั้น ไม่ได้ส่งมาที่เรา ลบได้โดยล้างข้อมูลเว็บไซต์ในเบราว์เซอร์</li><li>ผู้ให้บริการเว็บ (GitHub Pages) อาจบันทึกข้อมูลทางเทคนิค เช่น ที่อยู่ IP เพื่อความปลอดภัยของระบบ ตามนโยบายของ GitHub</li></ul>
<h2>2. คุกกี้</h2><p>คุกกี้คือไฟล์เล็ก ๆ ที่เว็บเก็บไว้ในเบราว์เซอร์ เมื่อเข้าเว็บครั้งแรกจะมีแถบให้เลือก "ยอมรับ" หรือ "ไม่ยอมรับ" และเปลี่ยนใจได้ทุกเมื่อที่ปุ่ม "ตั้งค่าคุกกี้" ด้านล่างทุกหน้า</p>
<h2>3. โฆษณาจาก Google และผู้ให้บริการรายอื่น</h2><ul><li>เว็บนี้อาจแสดงโฆษณาจาก Google (เช่น Google AdSense / H5 Games Ads) และผู้ให้บริการโฆษณาภายนอกรายอื่น</li><li>ผู้ให้บริการภายนอก รวมถึง Google ใช้คุกกี้เพื่อแสดงโฆษณาตามการเข้าชมเว็บนี้หรือเว็บอื่นของคุณก่อนหน้า</li><li>คุกกี้โฆษณาของ Google ช่วยให้ Google และพาร์ทเนอร์แสดงโฆษณาตามการเข้าชมเว็บไซต์ของคุณบนอินเทอร์เน็ต</li><li>คุณเลือกไม่รับโฆษณาตามความสนใจได้ที่ <a href="https://adssettings.google.com/" rel="noopener">การตั้งค่าโฆษณาของ Google</a> หรือเลือกไม่รับคุกกี้ของผู้ให้บริการภายนอกบางรายได้ที่ <a href="https://www.aboutads.info/choices/" rel="noopener">aboutads.info</a></li><li>อ่านวิธีที่ Google ใช้ข้อมูลได้ที่ <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">policies.google.com/technologies/partner-sites</a></li><li>ถ้าคุณกด "ไม่ยอมรับ" เราจะขอให้แสดงเฉพาะโฆษณาที่ไม่ปรับตามบุคคล (เท่าที่ผู้ให้บริการรองรับ)</li></ul>
<p>ตอนนี้ (ช่วงทดลอง) เว็บยังไม่ได้โหลดสคริปต์โฆษณาใด ๆ</p>
<h2>4. โฆษณาแลกรางวัลในเกม</h2><p>บางเกมอาจมีปุ่ม "ดูโฆษณาแลกรางวัล" ซึ่งบอกรางวัลก่อนเสมอ ไม่บังคับดู และมีปุ่ม "ไม่เป็นไร" ขนาดเท่ากัน</p>
<h2>5. เด็กและเยาวชน</h2><p>เราไม่ตั้งใจเก็บข้อมูลส่วนบุคคลของเด็ก และไม่มีช่องให้กรอกข้อมูลส่วนตัวในเกม</p>
<h2>6. ลิงก์ไปเว็บอื่น</h2><p>เว็บอื่นที่เราลิงก์ไปมีนโยบายของตัวเอง เราไม่รับผิดชอบต่อเนื้อหาของเว็บเหล่านั้น</p>
<h2>7. การเปลี่ยนแปลงนโยบาย</h2><p>เราอาจปรับนโยบายนี้ เมื่อปรับจะแก้วันที่ด้านบน</p>
<h2>8. ติดต่อ</h2><p>สอบถามเรื่องความเป็นส่วนตัว ดูช่องทางที่หน้า <a href="/contact/">ติดต่อเรา</a></p>''',
f'''{UPDE}<p>This policy explains how Kairon Arcade (ห้องเกม ไครอน) at {SITE_URL} and its games collect and use data.</p>
<h2>1. What we collect</h2><ul><li>We never ask for your name, email or phone number and there are no accounts.</li><li><b>Local save data</b>: high scores, levels, language, volume and your cookie choice are stored in your browser's localStorage only and are not sent to us. Clear them by clearing site data in your browser.</li><li>Our host (GitHub Pages) may log technical data such as IP addresses for security, under GitHub's own policy.</li></ul>
<h2>2. Cookies</h2><p>Cookies are small files a site stores in your browser. On your first visit a banner lets you Accept or Decline, and you can change your choice anytime with "Cookie settings" at the bottom of every page.</p>
<h2>3. Ads from Google and other vendors</h2><ul><li>This site may show ads from Google (e.g. Google AdSense / H5 Games Ads) and other third-party ad vendors.</li><li>Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this website or other websites.</li><li>Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits to this and/or other sites on the Internet.</li><li>You may opt out of personalized advertising by visiting <a href="https://adssettings.google.com/" rel="noopener">Google Ads Settings</a>, or opt out of some third-party vendors' cookies at <a href="https://www.aboutads.info/choices/" rel="noopener">aboutads.info</a>.</li><li>See how Google uses data: <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">policies.google.com/technologies/partner-sites</a></li><li>If you Decline, we request non-personalized ads only (where the vendor supports it).</li></ul>
<p>Right now (preview stage) the site loads no ad scripts at all.</p>
<h2>4. Rewarded ads in games</h2><p>Some games may offer an optional "watch an ad for a reward" button. The reward is shown first, it is never forced, and a same-size "No thanks" button is always there.</p>
<h2>5. Children</h2><p>We do not knowingly collect personal data from children and games have no fields for personal information.</p>
<h2>6. Links to other sites</h2><p>Other sites we link to have their own policies; we are not responsible for their content.</p>
<h2>7. Changes</h2><p>We may update this policy and will change the date above when we do.</p>
<h2>8. Contact</h2><p>For privacy questions see our <a href="/contact/">Contact page</a>.</p>''')

page('/terms/','terms','ข้อตกลงการใช้งาน','Terms of Use','ข้อตกลงการใช้งานเว็บ Kairon Arcade ห้องเกม ไครอน',
f'''{UPD}<h2>1. การใช้งาน</h2><p>เกมทั้งหมดเล่นฟรีเพื่อความบันเทิงส่วนตัว การใช้เว็บนี้ถือว่าคุณยอมรับข้อตกลงนี้</p>
<h2>2. ลิขสิทธิ์</h2><p>เกม ภาพ เสียง ตัวละคร และโค้ดในเว็บนี้เป็นของ Kairon Arcade ห้ามคัดลอก ดัดแปลง หรือนำไปเผยแพร่ซ้ำเพื่อการค้าโดยไม่ได้รับอนุญาต ฟอนต์ Kanit ใช้ภายใต้สัญญาอนุญาต SIL Open Font License</p>
<h2>3. ข้อห้าม</h2><ul><li>ห้ามโจมตี รบกวน หรือพยายามเจาะระบบของเว็บ</li><li>ห้ามกดโฆษณาซ้ำ ๆ หรือใช้โปรแกรมกดโฆษณาแทนคน</li></ul>
<h2>4. ข้อจำกัดความรับผิด</h2><p>เราให้บริการ "ตามสภาพ" ข้อมูลเซฟอยู่ในเครื่องของคุณ อาจหายได้ถ้าล้างข้อมูลเบราว์เซอร์ เราไม่รับผิดชอบความเสียหายจากการใช้งาน</p>
<h2>5. การเปลี่ยนแปลง</h2><p>เราอาจเพิ่ม ลบ หรือแก้ไขเกมและข้อตกลงนี้ได้ตลอดเวลา</p>''',
f'''{UPDE}<h2>1. Use</h2><p>All games are free for personal entertainment. Using this site means you accept these terms.</p>
<h2>2. Copyright</h2><p>Games, art, sound, characters and code on this site belong to Kairon Arcade. Do not copy, modify or republish them commercially without permission. The Kanit font is used under the SIL Open Font License.</p>
<h2>3. Not allowed</h2><ul><li>Attacking, disrupting or trying to break into the site.</li><li>Repeatedly clicking ads or using bots to click ads.</li></ul>
<h2>4. Disclaimer</h2><p>The service is provided "as is". Saves live on your device and may be lost if you clear browser data. We are not liable for damages from use.</p>
<h2>5. Changes</h2><p>We may add, remove or change games and these terms at any time.</p>''')

page('/contact/','contact','ติดต่อเรา','Contact us','ติดต่อ Kairon Arcade ห้องเกม ไครอน',
'''<p>ติดต่อผ่าน LINE OA ห้องเกม ไครอน</p><p>แจ้งปัญหาการเล่น เสนอไอเดียเกมใหม่ หรือติดต่อเรื่องลิขสิทธิ์และความเป็นส่วนตัวได้ที่ช่องทางนี้</p>''',
'''<p>Contact us via the ห้องเกม ไครอน LINE Official Account.</p><p>Report a bug, suggest a game idea, or reach us about copyright or privacy through this channel.</p>''')

# ---------- 404
write('/404.html', head('ไม่พบหน้านี้ · Page not found | Kairon Arcade','ไม่พบหน้าที่ค้นหา','/404.html',noindex=True) + top() + f'''
<main class="page" style="text-align:center"><div class="card"><h1 style="font-size:44px;color:var(--amb)">404</h1><p>{bi('ตู้นี้ยังไม่เปิด หรือย้ายไปที่อื่นแล้ว','This cabinet is closed or has moved.')}</p>
<p style="margin-top:14px"><a class="cta" href="/">{bi('กลับหน้าแรก','Back to home')}</a></p></div></main><div class="floor"></div>''' + foot())

# ---------- robots, sitemap, ads.txt, manifest
write('/robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n')
urls = ['/', '/about/', '/privacy/', '/terms/', '/contact/'] + [f'/games/{g[0]}/' for g in GAMES] + [f'/play/{g[0]}/' for g in GAMES]
write('/sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE_URL}{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n')
write('/ads.txt', '''# ads.txt for Kairon Arcade (ห้องเกม ไครอน)
# PLACEHOLDER - no ad network is connected yet.
# After Google AdSense is approved, replace pub-XXXXXXXXXXXXXXXX with the real publisher ID and remove the leading "# " on the line below.
# google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0
''')
write('/site.webmanifest', json.dumps({'name':'Kairon Arcade · ห้องเกม ไครอน','short_name':'ห้องเกม ไครอน','start_url':'/','display':'standalone','background_color':'#181B2A','theme_color':'#12141F','icons':[{'src':'/assets/icon-192.png','sizes':'192x192','type':'image/png'},{'src':'/assets/icon-512.png','sizes':'512x512','type':'image/png'}]}, ensure_ascii=False, indent=1))
write('/.nojekyll', '')
print('built', len(GAMES), 'games,', len(urls), 'urls')
