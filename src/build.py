import re, json, subprocess, base64, io, os, sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

B = '/tmp/claude-0/-home-claude/9c937368-bad6-5eb9-9add-513d473957f5/scratchpad/build'
ctx = open('/tmp/claude-0/-home-claude/9c937368-bad6-5eb9-9add-513d473957f5/scratchpad/ctx/ctx.txt').read()
fin = open(B + '/final.txt').read()

AS = 'https://www.figma.com/api/mcp/asset/'
def tok(uid_ext):
    return 'ASSET::' + uid_ext
def consts(t):
    return {n: tok(u[len(AS):]) for n, u in re.findall(r'const (\w+) = "(https://www\.figma\.com/api/mcp/asset/[^"]+)"', t)}

def convert(jsx, cs):
    s = jsx
    s = re.sub(r'\s+data-node-id="[^"]*"', '', s)
    s = re.sub(r'\s+data-name="[^"]*"', '', s)
    s = re.sub(r'\s+data-snippet-language="[^"]*"', '', s)
    s = re.sub(r"\s+style=\{\{ fontVariationSettings: '\"wdth\" \d+' \}\}", '', s)
    s = re.sub(r'\s+style=\{\{ containerType: "size" \}\}', ' style="container-type:size"', s)
    def mask(m):
        return ' style="mask-image:url(%s);-webkit-mask-image:url(%s)"' % (cs[m.group(1)], cs[m.group(1)])
    s = re.sub(r'\s+style=\{\{ maskImage: `url\("\$\{(\w+)\}"\)` \}\}', mask, s)
    s = re.sub(r'src=\{(\w+)\}', lambda m: 'src="%s"' % cs[m.group(1)], s)
    s = re.sub(r'\{`([^`]*)`\}', lambda m: m.group(1), s)
    s = s.replace('className=', 'class=')
    s = s.replace('<br aria-hidden />', '<br>')
    s = re.sub(r'<div([^>]*?)\s*/>', r'<div\1></div>', s)
    return s

def lines_of(t, a, b):
    L = t.split('\n')
    return '\n'.join(L[a - 1:b])

cs_top = consts(ctx)
top_block = convert(lines_of(ctx, 67, 95), cs_top)
top_part = convert(lines_of(ctx, 96, 157), cs_top)
tabs_grid = convert(lines_of(ctx, 159, 296), cs_top)
bg_url = re.search(r'const imgBg = "([^"]+)"', ctx).group(1)

# Watchlist/Final root (strip the code-connect Button snippet, replaced by hand-built button)
cs_fin = consts(fin)
body = fin[fin.index('return (') + len('return ('):]
body = body[:body.rindex(');')]
body = re.sub(r'<CodeConnectSnippet[\s\S]*?</CodeConnectSnippet>', '@@ADDBTN@@', body)
wl_final = convert(body, cs_fin)
plus_tok = cs_fin['img24Plus']
add_btn = ('<div class="addsym"><img alt="" src="%s" width="20" height="20"><span>Add symbols</span></div>' % plus_tok)
wl_final = wl_final.replace('@@ADDBTN@@', add_btn)
# the original root uses size-full; give it a normal width
wl_final = wl_final.replace('rounded-[28px] shrink-0 w-full', 'rounded-[28px] shrink-0 w-full', 1)

# ---------- hand-built sections ----------
def A(uid):
    return tok(uid)

def pair(sz, inner, left, right, sym):
    return ('<span class="pr" style="--sz:%dpx;--in:%dpx"><span class="r" style="mask-image:url(%s);-webkit-mask-image:url(%s)"><img alt="" src="%s"></span>'
            '<span class="l"><img alt="" src="%s"></span></span>') % (sz, inner, sym, sym, right, left)

def caret(img):
    return '<span class="caret"><img alt="" src="%s"></span>' % img

# Quick trade
qt_sym = A('05eb7de7-c409-4313-af2e-f339f26ac99a.svg')
qt_usd = A('49b43d71-9282-4a72-a86b-7543da38291a.svg')
qt_xau = A('5779847a-f539-4d0f-918d-bb9838d53f22.svg')
qt_minus = A('fd5d8dd1-46f5-475d-bbf1-7d5fca3ef365.svg')
qt_plus = A('39314a13-d5b5-4cac-8054-3fc9c4568a43.svg')

def vol(h, minus, plus, bg):
    return ('<div class="vol" style="height:%dpx;background:%s"><div class="vi"><b>0.15</b><span>lots</span></div>'
            '<div class="va"><i><img alt="" src="%s"></i><i><img alt="" src="%s"></i></div></div>') % (h, bg, minus, plus)

def px(label, bg):
    return ('<div class="px" style="background:%s"><p><span class="d8">1.094</span><span>17</span><span class="d8">3</span><br><span class="d5">%s</span></p></div>' % (bg, label))

quick = '''<section class="card qt">
<div class="qt-h">%s<div class="qt-t"><p class="t16">XAUUSD</p><p class="t14 sec">Gold / US Dollar</p></div><p class="t16 neg">-0.03%%</p></div>
%s
<div class="btns">%s%s</div></section>''' % (
    pair(40, 28, qt_xau, qt_usd, qt_sym),
    vol(64, qt_minus, qt_plus, 'var(--сontrol)'),
    px('Sell', 'var(--accent\\/negative\\/normal)'), px('Buy', 'var(--accent\\/positive\\/normal)'))

# Signal / Autochartist
s_avatar = A('612c05b7-da23-4bca-aa60-a8838284ae92.png')
s_chart = A('04391832-a4eb-4b38-a9c2-38041cbaa79c.png')
s_group = A('2e763903-faa6-4083-9373-ff6213337244.svg')
s_down = A('b9405330-dcb3-42f7-a104-c00630704759.svg')
s_bell = A('9d5cfba3-54fc-4108-8803-5eb565d3b613.svg')
s_dot = A('c3c9a520-c6f5-4801-a335-4031f68a48e3.svg')
s_v1 = A('51908c35-e000-4c51-bd2d-fc79e8b89d70.svg')
s_v2 = A('0e060e70-dd9d-48ea-a8f7-786fe1ad2cfd.svg')
s_minus = A('4acf5085-9048-4d24-a6d3-82b93817d55d.svg')
s_plus = A('ec02ea8c-738f-455d-b68b-8ef7d33f9004.svg')

signal = '''<section class="card sig">
<div class="sg-h"><div class="sg-top"><div class="badge"><img class="av" alt="" src="%(av)s"><span>AUTOCHARTIST</span></div><span class="cbtn32 str">%(car)s</span></div>
<div class="sg-t"><div><p class="t20">XAUUSD&nbsp;&nbsp;&nbsp;Down&nbsp;<img class="ad" alt="" src="%(down)s"></p><p class="t14 sec2">Triangle&nbsp;·&nbsp;m1&nbsp;·&nbsp;51 candles</p></div><span class="ibtn"><img alt="" src="%(bell)s"></span></div></div>
<div class="sg-b"><div class="live"><div class="lv-l"><img alt="" src="%(dot)s" class="dot"><span>32 min left</span></div><div class="lv-r"><span>Quality&nbsp;</span><span>25%%</span><span class="qi"><img class="q1" alt="" src="%(v1)s"><img class="q2" alt="" src="%(v2)s"></span></div></div>
<div class="chartbox"><img alt="" src="%(chart)s"></div></div>
<div class="sg-f">%(vol)s<div class="bigbtn" style="background:var(--accent\\/negative\\/normal)">Sell 1.1024</div></div></section>''' % dict(
    av=s_avatar, car=caret(s_group), down=s_down, bell=s_bell, dot=s_dot, v1=s_v1, v2=s_v2, chart=s_chart,
    vol=vol(56, s_minus, s_plus, 'var(--сontrol)'))

# Calendar
c_germany = A('c3cff49f-d46d-4b4b-b6fe-54645f298725.svg')
c_group = A('d212d41a-7c0a-47c3-8387-264a88f2a698.svg')
c_sym = A('9c719cbe-bfeb-40fb-9aea-c8beb0340eae.svg')
c_usd = A('39eaf16c-c24a-4003-bf31-bee227ee111c.svg')
c_xau = A('b4c5453f-ba52-4815-898d-b0b8454f5e9d.svg')
c_flag = A('cd6bdb6f-b2ef-4112-a44a-c7af2ca82dd9.svg')

def ev(time, title, impact, chips_extra, country, flagimg):
    bar = ('<span class="imp"><i class="trk"></i><i class="fl" style="height:50%;background:var(--accent\\/warning\\/normal)"></i></span>'
           if impact == 'mid' else '<span class="imp"><i class="fl" style="height:100%;background:var(--error\\/accent\\/normal)"></i></span>')
    extra = '<span class="chip"><span>+3</span></span>' if chips_extra else ''
    return ('<div class="ev">%s<div class="ev-m"><div class="ev-t"><p class="t16 dis">%s</p><p class="t16m">%s</p></div>'
            '<div class="chips"><span class="chip"><span class="pi">%s</span><span>XAUUSD</span></span>%s</div></div>'
            '<div class="flag"><span class="fi"><span class="fb"><img alt="" src="%s"></span></span><span class="fc">%s</span></div></div>') % (
        bar, time, title, pair(20, 14, c_xau, c_usd, c_sym), extra, flagimg, country)

calendar = '''<section class="card cal"><div class="hd"><p class="t20">Today’s Events</p><span class="cbtn32 str">%s</span></div>
<div class="evs">%s%s%s</div></section>''' % (
    caret(c_group),
    ev('12:30', 'S&amp;P Global Services PMI', 'mid', True, 'EUR', c_germany),
    ev('16:00', '4-Week Bill Auction', 'high', True, 'USA', c_flag),
    ev('17:30', 'Core PCE Price Index MoM', 'mid', False, 'USA', c_flag))

# News
n_img = A('3c92c6c9-2b6c-4ff1-a282-cf034343d731.png')
n_group = A('feb3f76f-aca7-4caa-b84d-fe8188495921.svg')
n_sym = A('1e7ab8d8-e83c-4f96-8188-3c0f10d03fec.svg')
n_usd = A('a551f001-3471-4b7f-9ba2-c26d7614812b.svg')
n_xau = A('3087e6d9-3f60-49b6-a627-b4ef53da96d6.svg')
n_eur = A('52bbe86c-ddcc-486a-b715-6c3e0dbdaa34.svg')

def news(title, tick, chg, prov, ago, right):
    return ('<div class="nc"><div class="ar"><p class="t16m ttl">%s</p><span class="th"><img alt="" src="%s"></span></div>'
            '<div class="ci"><span class="info">%s<span class="tk">%s</span><span class="ch">%s</span></span>'
            '<span class="pv">%s<span>·</span><span>%s</span></span></div></div>') % (
        title, n_img, pair(20, 14, n_xau, right, n_sym), tick, chg, prov, ago)

newsh = '''<section class="card nw"><div class="hd"><p class="t20">News</p><span class="cbtn32 ctl">%s</span></div>
<div class="nl">%s%s%s</div></section>''' % (
    caret(n_group),
    news('Bitwise Appoints Author Jonathan Bier as Advisor o...', 'XAUUSD', '+0.32%', '<span>FXS</span>', '32 min ago', n_usd),
    news('Indonesia stocks higher at close of trade; IDX Composite Index up 0.62%', 'GoldV3', '+0.04%', '<span class="bb">Bloomberg M..</span>', '48 min ago', n_usd),
    news('ECB’s Nagel: high inflation not yet setting off second-round effects', 'XAUEUR', '+0.08%', '<span>Reuters</span>', '52 min ago', n_eur))

# App bar
menu = [A('c9ca0d55-8fb5-499d-a55d-a2d4370afc4b.svg'), A('7e274667-1e25-4a1d-93b0-e214dbe543df.svg'),
        A('170bb899-6ba6-4566-bac1-cfadde15a4a2.svg'), A('4de871d3-9c1b-4e01-91cb-269a739b9d9d.svg'),
        A('17c3c5ac-695b-4ce9-a070-4935b46c0921.svg')]
names = ['Markets', 'Charts', 'Positions', 'Signals', 'My cTrader']
appbar = '<nav class="appbar" aria-label="Sections">' + ''.join(
    '<div class="mi%s"><img alt="" src="%s"><p>%s</p></div>' % (' on' if i == 0 else '', menu[i], names[i]) for i in range(5)) + '</nav>'

css = open(B + '/theme.css').read()
js = open(B + '/theme.js').read()
page = open(B + '/page.tpl.html').read()
page = (page.replace('@@TOPBLOCK@@', top_block).replace('@@TOPPART@@', top_part)
        .replace('@@TABS@@', tabs_grid).replace('@@WLFINAL@@', wl_final)
        .replace('@@QUICK@@', quick).replace('@@SIGNAL@@', signal)
        .replace('@@CAL@@', calendar).replace('@@NEWS@@', newsh).replace('@@APPBAR@@', appbar)
        .replace('@@BGIMG@@', tok(bg_url[len(AS):])))
page = page.replace('bg-[var(--background\\/primary,white)] content-stretch flex flex-col gap-[var(--spacing\\/4,16px)]','bg-[var(--card-light,rgba(209,209,209,0.1))] backdrop-blur-[18px] content-stretch flex flex-col gap-[var(--spacing\\/4,16px)]',1)
page = page.replace('text-right tracking-[var(--letterspacing\\/dense,-0.1px)] w-px">€ </p>','text-right tracking-[var(--letterspacing\\/dense,-0.1px)] whitespace-nowrap">€</p>',1)
page = page.replace('<img alt="" class="absolute block inset-0 max-w-none size-full" src="ASSET::7cc8c203','<img id="logo" alt="" class="absolute block inset-0 max-w-none size-full" src="ASSET::7cc8c203',1)
page = page.replace('class="block max-w-none size-full" src="ASSET::f147ece8','class="block max-w-none size-full sb" src="ASSET::f147ece8')
page = page.replace('bg-[var(--buttonbackground\\/secondary\\/normal,#f7f7f7)] content-stretch flex gap-[var(--spacing\\/2,8px)] h-[40px]','bg-[var(--сontrol,rgba(209,209,209,0.1))] content-stretch flex gap-[var(--spacing\\/2,8px)] h-[40px]').replace('bg-[var(--buttonbackground\\/secondary\\/normal,#f7f7f7)] content-stretch flex gap-[var(--spacing/1,4px)] h-[40px]','bg-[var(--сontrol,rgba(209,209,209,0.1))] content-stretch flex gap-[var(--spacing/1,4px)] h-[40px]')
open(B + '/page.src.html', 'w').write(page)

# ---- download assets ----
ids = sorted(set(re.findall(r'ASSET::([0-9a-f-]+\.(?:svg|png))', page)))
print('assets', len(ids))
os.makedirs(B + '/assets', exist_ok=True)
def dl(i):
    p = B + '/assets/' + i
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        subprocess.run(['curl', '-f', '-L', '-s', '-o', p, AS + i], check=True)
    return i
with ThreadPoolExecutor(8) as ex:
    list(ex.map(dl, ids))
uris = {}
inv = set()
for i in ids:
    raw = open(B + '/assets/' + i, 'rb').read()
    if i.endswith('.svg'):
        _t = raw.decode()
        if '#' not in re.sub(r'url\(#[^)]*\)|href="#[^"]*"|id="[^"]*"','',_t) and 'ctrader-logo' not in _t and ('black' in _t):
            raw = _t.replace('"black"','"white"').encode(); inv.add(i)
        _cols = set(x.lower() for x in re.findall(r'(?:fill|stroke)="([^"]*)"', raw.decode())) - {'none'}
        if _cols and _cols <= {'#d9d9d9','white','#2b2b2c'} and 'url(' not in raw.decode(): inv.add(i)
        uris[i] = 'data:image/svg+xml;base64,' + base64.b64encode(raw).decode()
    else:
        im = Image.open(io.BytesIO(raw)).convert('RGBA')
        if max(im.size) > 1400:
            r = 1400 / max(im.size); im = im.resize((int(im.width * r), int(im.height * r)))
        buf = io.BytesIO(); im.save(buf, 'WEBP', quality=82)
        uris[i] = 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()
        print(i, im.size, len(buf.getvalue()))
# write a tailwind-source version (tokens kept) and a final version
open(B + '/page.tw.html', 'w').write(page)
final = re.sub(r'ASSET::([0-9a-f-]+\.(?:svg|png))', lambda m: uris[m.group(1)] + ('#inv' if (m.group(1) in inv and 'src="ASSET::'+m.group(1) in m.string[max(0,m.start()-5):m.end()]) else ''), page)
open(B + '/page.final.html', 'w').write(final)
print('final bytes', len(final))
