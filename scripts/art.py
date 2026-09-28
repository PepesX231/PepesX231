"""Draws the profile's artwork (black · white · blue, like pepesx231.github.io):
   assets/banner.svg  — name + the roles typing themselves out, and the little white square climbing its stairs
   assets/roles.svg   — what I do: game dev · web dev · machine learning · AI training
   assets/stack.svg   — the tools I use (icons: github.com/tandpfun/skill-icons, MIT)
Run it by hand after changing something:  python3 scripts/art.py   (it downloads the icons it needs)."""
import os, re, io, base64, urllib.request, html
from fontTools import subset
from fontTools.ttLib import TTFont

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
INK, PAPER, BLUE, DIM = '#0b0b0c', '#f6f6f3', '#4da3ff', '#8a8a90'
# the website's own fonts, embedded (only the letters used) — so it looks the same on every screen
MONO = "PMono,'SFMono-Regular',Consolas,Menlo,monospace"
SANS = "PPlex,'Segoe UI','Helvetica Neue',Arial,sans-serif"
THAI = "PPlex,'Sukhumvit Set','Leelawadee UI',Tahoma,sans-serif"
BIG = "PAnton,Impact,'Arial Black',sans-serif"
esc = html.escape
GF = 'https://raw.githubusercontent.com/google/fonts/main/ofl/'
FONTS = {'PAnton': ('anton/Anton-Regular.ttf', 400), 'PPlex': ('ibmplexsansthai/IBMPlexSansThai-SemiBold.ttf', 600),
         'PPlexR': ('ibmplexsansthai/IBMPlexSansThai-Medium.ttf', 500), 'PMono': ('jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf', 600)}
_cache = {}
def ttf(fam):
    if fam not in _cache: _cache[fam] = urllib.request.urlopen(GF + FONTS[fam][0]).read()
    return _cache[fam]
def face(fam, text, as_fam=None):
    """@font-face with the font cut down to just these letters (woff, base64)"""
    f = TTFont(io.BytesIO(ttf(fam)))
    o = subset.Options(); o.layout_features = ['*']; o.flavor = 'woff'; o.name_IDs = []; o.notdef_outline = True
    sb = subset.Subsetter(o); sb.populate(text=text + ' .'); sb.subset(f)
    b = io.BytesIO(); f.flavor = 'woff'; f.save(b)
    return f"@font-face{{font-family:{as_fam or fam};font-weight:{FONTS[fam][1]};src:url(data:font/woff;base64,{base64.b64encode(b.getvalue()).decode()}) format('woff')}}"
def width(fam, text, size):
    f = TTFont(io.BytesIO(ttf(fam))); cm = f.getBestCmap(); hm = f['hmtx']; up = f['head'].unitsPerEm
    return sum(hm[cm[ord(c)]][0] for c in text if ord(c) in cm) * size / up

# ---------------------------------------------------------------- banner
ROLES = ['Game Developer', 'Web Developer', 'Machine Learning', 'AI Training']
def banner():
    W, H = 1200, 400
    CYC = 12.0                                   # seconds for all four roles
    fs, cw = 34, 34 * .6                         # role line: monospace, every letter .6em wide (forced with textLength)
    rx, ry = 88, 272
    name = 'PEEPEE'; nx = 58; dotx = nx + width('PAnton', name, 150) + 10
    txt_mono = "HELLO, I'M · FAIL FAST. LEARN FAST.■>" + ''.join(ROLES)
    css = [face('PAnton', name), face('PMono', txt_mono), face('PPlex', 'สวัสดีครับ ผม ชมน์ปภพ ดีจริง ·'),
           f""".bg{{fill:{INK}}}.mono{{font:600 16px {MONO};letter-spacing:4px;fill:{DIM}}}.big{{font:400 150px {BIG};fill:{PAPER};letter-spacing:1px}}.thm{{font:600 17px {THAI};letter-spacing:0;fill:{DIM}}}
.th{{font:600 27px {THAI};fill:{PAPER}}}.role{{font:600 {fs}px {MONO};fill:{PAPER}}}.gt{{font:600 {fs}px {MONO};fill:{BLUE}}}
.dot{{animation:bob 2.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-9px) rotate(90deg)}}}}
.blk{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}"""]
    roles_svg = []
    n = len(ROLES); slot = 100 / n
    for i, r in enumerate(ROLES):
        L = len(r); w = L * cw
        # type in · hold · delete — then the next one
        t_in, t_hold, t_out = slot * .34, slot * .8, slot * .96
        css.append(f"@keyframes r{i}{{0%{{clip-path:inset(0 100% 0 0)}}{t_in:.2f}%{{clip-path:inset(0 0 0 0)}}{t_hold:.2f}%{{clip-path:inset(0 0 0 0)}}{t_out:.2f}%,100%{{clip-path:inset(0 100% 0 0)}}}}"
                   f"@keyframes c{i}{{0%{{transform:translateX(0);opacity:1}}{t_in:.2f}%{{transform:translateX({w:.1f}px)}}{t_hold:.2f}%{{transform:translateX({w:.1f}px)}}{t_out:.2f}%{{transform:translateX(0);opacity:1}}{t_out+.01:.2f}%,100%{{opacity:0}}}}"
                   f".r{i}{{animation:r{i} {CYC}s steps({L},end) {-(n - i) * CYC / n:.2f}s infinite}}.c{i}{{animation:c{i} {CYC}s steps({L},end) {-(n - i) * CYC / n:.2f}s infinite;opacity:0}}")
        roles_svg.append(f'<text class="role r{i}" x="{rx}" y="{ry}" textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs">{esc(r)}</text>'
                         f'<rect class="c{i}" x="{rx + 4}" y="{ry - fs * .78:.1f}" width="{cw * .9:.1f}" height="{fs * .92:.1f}" fill="{BLUE}"/>')
    # the stairs on the right, and the square climbing them (it's the same square that travels through the website)
    sx, sy = 740, 340
    steps = [(sx + 150 + k * 76, 34 + k * 34) for k in range(4)]
    stairs = ''.join(f'<rect x="{x}" y="{sy - h}" width="70" height="{h}" fill="url(#st)" stroke="rgba(246,246,243,.12)"/>'
                     f'<rect x="{x}" y="{sy - h}" width="70" height="2" fill="{BLUE}" class="lit" style="animation-delay:{1.1 + k * .9:.1f}s"/>' for k, (x, h) in enumerate(steps))
    spots = [(sx + 70, sy)] + [(x + 35, sy - h) for x, h in steps]
    S = 44
    # keyframes: crouch, jump (arc + quarter turn), land — four times, a pause at the top, then fade and start again
    kf, T = [], 7.2
    def at(t, x, y, r=0, sx_=1, sy_=1, o=1):
        kf.append((t, x - S / 2, y - S * sy_, r, sx_, sy_, o))
    t = 0
    at(0, *spots[0], o=0); at(.04, *spots[0])
    t = .08
    for k in range(4):
        (x0, y0), (x1, y1) = spots[k], spots[k + 1]
        at(t, x0, y0, 90 * k); at(t + .03, x0, y0, 90 * k, 1.16, .78)
        at(t + .075, (x0 + x1) / 2, min(y0, y1) - 34, 90 * k + 45, .92, 1.1)
        at(t + .12, x1, y1, 90 * k + 90, 1.18, .76); at(t + .15, x1, y1, 90 * k + 90)
        t += .17
    at(.86, *spots[-1], 360); at(.95, *spots[-1], 360, o=0); at(1, *spots[-1], 360, o=0)
    frames = ''.join(f"{t * 100:.1f}%{{transform:translate({x:.1f}px,{y:.1f}px) rotate({r}deg) scale({a},{b});opacity:{o}}}" for t, x, y, r, a, b, o in kf)
    css.append(f"@keyframes climb{{{frames}}}.me{{animation:climb {T}s linear infinite;transform-box:view-box;transform-origin:0 0}}"
               f".me rect{{transform-box:fill-box;transform-origin:50% 100%}}"
               f".lit{{animation:lit {T}s linear infinite;opacity:0}}@keyframes lit{{0%,100%{{opacity:0}}12%,88%{{opacity:1}}}}"
               f".op{{animation:op {T}s cubic-bezier(.5,0,.5,1) infinite;transform-box:fill-box;transform-origin:center}}"
               f"@keyframes op{{0%,6%{{opacity:0;transform:translateY(-30px)}}14%,74%{{opacity:1;transform:translateY(0)}}82%{{opacity:1;transform:translateY(78px) scale(.45)}}84%,100%{{opacity:0;transform:translateY(78px) scale(.45)}}}}"
               f".core{{animation:core {T}s linear infinite;opacity:0}}@keyframes core{{0%,81%{{opacity:0}}83%,93%{{opacity:1}}95%,100%{{opacity:0}}}}")
    # it reaches the top, the blue one (the chance) drops into it — the same story as on the website
    me = f'<g class="me"><rect width="{S}" height="{S}" fill="{PAPER}"/><rect class="core" x="{S*.29:.1f}" y="{S*.29:.1f}" width="{S*.42:.1f}" height="{S*.42:.1f}" fill="{BLUE}"/></g>'
    ox, oy = spots[-1][0], spots[-1][1] - S / 2 - 78
    opp = (f'<g class="op" style="transform-box:fill-box"><rect x="{ox - 11}" y="{oy - 11}" width="22" height="22" fill="{BLUE}"/>'
           f'<rect x="{ox - 4}" y="{oy - 4}" width="8" height="8" fill="#bfe0ff"/></g>')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<radialGradient id="glow" cx="78%" cy="58%" r="45%"><stop offset="0" stop-color="{BLUE}" stop-opacity=".22"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<linearGradient id="st" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2c33"/><stop offset="1" stop-color="#121215"/></linearGradient>
<linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="{PAPER}" stop-opacity="0"/><stop offset=".2" stop-color="{PAPER}" stop-opacity=".3"/><stop offset=".85" stop-color="{PAPER}" stop-opacity=".3"/><stop offset="1" stop-color="{PAPER}" stop-opacity="0"/></linearGradient>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><rect x="11" y="11" width="2" height="2" fill="{PAPER}" fill-opacity=".07"/></pattern>
</defs>
<style>{''.join(css)}</style>
<rect class="bg" width="{W}" height="{H}" rx="18"/><rect width="{W}" height="{H}" rx="18" fill="url(#dots)"/><rect width="{W}" height="{H}" rx="18" fill="url(#glow)"/>
<text class="mono" x="64" y="62">HELLO, I'M ·<tspan class="thm" dx="10">สวัสดีครับ ผม</tspan></text>
<text class="big" x="{nx}" y="222">{name}</text><rect class="dot" x="{dotx:.0f}" y="196" width="27" height="27" fill="{BLUE}"/>
<text class="gt" x="60" y="{ry}">&gt;</text>{''.join(roles_svg)}
<text class="th" x="64" y="322">ชมน์ปภพ ดีจริง</text>
<text class="mono" x="64" y="362"><tspan>FAIL FAST.</tspan><tspan fill="{BLUE}" dx="14">LEARN FAST.</tspan><tspan class="blk" fill="{BLUE}" dx="8">■</tspan></text>
<rect x="{sx}" y="{sy}" width="{W - sx - 40}" height="1.5" fill="url(#fl)"/>{stairs}{opp}{me}
</svg>"""
    open(os.path.join(OUT, 'banner.svg'), 'w').write(svg)

# ---------------------------------------------------------------- roles
def roles():
    W, H = 1200, 560
    cw, ch, g = 576, 256, 24
    cards = [
        ('GAME DEV', 'ทำเกมด้วย Unity — เกมแจม 72 ชม., แฮกกาธอน, ห้องแล็บวิทย์เสมือนจริง', ['Unity', 'C#', 'Game Systems', 'Level Design'], 'game'),
        ('WEB DEV', 'เว็บพอร์ตของผมเขียนเองทั้งหมด — HTML · CSS · JavaScript ล้วน ๆ', ['JavaScript', 'HTML', 'CSS', 'PHP'], 'web'),
        ('MACHINE LEARNING', 'เขียน Python ทำงานกับข้อมูล และสร้างโมเดลให้เรียนรู้จากมัน', ['Python', 'Data', 'Models'], 'ml'),
        ('AI TRAINING', 'เทรนโมเดล AI — และสอนคนให้ใช้ AI เป็น (1,500+ คนในงาน Science Day × AI)', ['Python', 'Training', 'Prompting'], 'train')]
    alltext = ''.join(t + d + ''.join(c) for t, d, c, _ in cards)
    css = face('PAnton', alltext.upper() + '.') + face('PPlexR', alltext, 'PPlexR') + face('PMono', alltext + '0123456789</>')
    css += f""".ttl{{font:400 40px {BIG};fill:{PAPER};letter-spacing:1px}}.no{{font:600 14px {MONO};fill:{BLUE};letter-spacing:3px}}
.tx{{font:500 17px PPlexR,{THAI};fill:#c9c9cd}}.chip{{font:600 13px {MONO};fill:{PAPER};letter-spacing:1px}}
.in{{animation:in .9s cubic-bezier(.2,.8,.2,1) both}}@keyframes in{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.pl{{animation:pl 2.4s ease-in-out infinite}}@keyframes pl{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
.bar{{transform-box:fill-box;transform-origin:50% 100%;animation:bar 3.2s cubic-bezier(.5,0,.3,1) infinite}}@keyframes bar{{0%{{transform:scaleY(.15)}}45%,80%{{transform:scaleY(1)}}100%{{transform:scaleY(.15)}}}}
.pk{{animation:pk 1.8s linear infinite}}@keyframes pk{{from{{stroke-dashoffset:40}}to{{stroke-dashoffset:0}}}}
.cur{{animation:cur 1s steps(1) infinite}}@keyframes cur{{50%{{opacity:0}}}}
.hop{{transform-box:fill-box;transform-origin:50% 100%;animation:hop 1.6s cubic-bezier(.3,0,.3,1) infinite}}@keyframes hop{{0%,100%{{transform:none}}15%{{transform:scale(1.15,.8)}}45%{{transform:translateY(-20px) rotate(90deg)}}75%{{transform:rotate(90deg) scale(1.1,.85)}}}}"""
    def glyph(kind, x, y):          # a little picture made of squares, top-right of each card
        if kind == 'game':          # a pad: d-pad + two buttons, and the white square hopping on it
            s = f'<rect x="{x}" y="{y+22}" width="120" height="60" rx="14" fill="#18191d" stroke="rgba(246,246,243,.14)"/>'
            s += ''.join(f'<rect x="{x+18+dx}" y="{y+43+dy}" width="10" height="10" fill="{PAPER}" fill-opacity=".8"/>' for dx, dy in ((10, 0), (0, 10), (10, 10), (20, 10), (10, 20)))
            s += f'<rect x="{x+82}" y="{y+42}" width="11" height="11" fill="{BLUE}" class="pl"/><rect x="{x+96}" y="{y+54}" width="11" height="11" fill="{BLUE}" class="pl" style="animation-delay:.6s"/>'
            s += f'<rect class="hop" x="{x+49}" y="{y}" width="22" height="22" fill="{PAPER}"/>'
            return s
        if kind == 'web':           # a browser window with </> typed in it
            s = f'<rect x="{x}" y="{y}" width="124" height="84" rx="8" fill="#18191d" stroke="rgba(246,246,243,.14)"/><rect x="{x}" y="{y}" width="124" height="18" rx="8" fill="#23252b"/>'
            s += ''.join(f'<rect x="{x+10+k*12}" y="{y+6}" width="6" height="6" fill="{c}"/>' for k, c in enumerate((PAPER, BLUE, '#5a5a60')))
            s += f'<text x="{x+20}" y="{y+62}" style="font:600 28px {MONO};fill:{BLUE}">&lt;/&gt;</text><rect class="cur" x="{x+96}" y="{y+40}" width="12" height="26" fill="{PAPER}"/>'
            return s
        if kind == 'ml':            # a tiny network: squares for neurons, signals running along the links
            L = [[(x, y + 14), (x, y + 44), (x, y + 74)], [(x + 52, y), (x + 52, y + 30), (x + 52, y + 60), (x + 52, y + 90)], [(x + 104, y + 30), (x + 104, y + 60)]]
            s = ''
            for a, b in ((0, 1), (1, 2)):
                for p in L[a]:
                    for q in L[b]:
                        s += f'<line x1="{p[0]+6}" y1="{p[1]+6}" x2="{q[0]+6}" y2="{q[1]+6}" stroke="{BLUE}" stroke-opacity=".28"/>'
                        s += f'<line class="pk" x1="{p[0]+6}" y1="{p[1]+6}" x2="{q[0]+6}" y2="{q[1]+6}" stroke="#bfe0ff" stroke-width="1.6" stroke-dasharray="4 36" style="animation-delay:{(p[1]*7+q[1]*3)%17/10:.1f}s"/>'
            for k, lay in enumerate(L):
                for j, (px, py) in enumerate(lay):
                    s += f'<rect x="{px}" y="{py}" width="12" height="12" fill="{PAPER if k != 1 else BLUE}" class="pl" style="animation-delay:{(k*3+j)*.25:.2f}s"/>'
            return s
        # train: bars (the model getting better) under a falling loss line
        s = ''.join(f'<rect class="bar" x="{x+k*22}" y="{y+90-h}" width="14" height="{h}" fill="{BLUE if k==4 else "#2f3440"}" style="animation-delay:{k*.12:.2f}s"/>' for k, h in enumerate((30, 44, 58, 70, 86)))
        s += f'<polyline points="{x},{y+8} {x+24},{y+30} {x+50},{y+44} {x+76},{y+60} {x+102},{y+66}" fill="none" stroke="{PAPER}" stroke-width="2"/>'
        s += f'<rect x="{x+98}" y="{y+62}" width="8" height="8" fill="{PAPER}"/>'
        return s
    body = ''
    for i, (t, d, chips, kind) in enumerate(cards):
        x, y = (i % 2) * (cw + g), (i // 2) * (ch + g)
        c = f'<g class="in" style="animation-delay:{i*.12:.2f}s">'
        c += f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="#111113" stroke="rgba(246,246,243,.08)"/>'
        c += f'<rect x="{x+30}" y="{y+32}" width="10" height="10" fill="{BLUE}"/><text class="no" x="{x+50}" y="{y+42}">0{i+1}</text>'
        c += f'<text class="ttl" x="{x+30}" y="{y+92}">{t}<tspan fill="{BLUE}">.</tspan></text>'
        # the line of text (wrapped by hand into two lines)
        words, lines, cur = d.split(' '), [], ''
        for wd in words:
            if len(cur) + len(wd) > 36 and cur: lines.append(cur); cur = wd
            else: cur = (cur + ' ' + wd).strip()
        lines.append(cur)
        for k, ln in enumerate(lines[:3]): c += f'<text class="tx" x="{x+30}" y="{y+124+k*26}">{esc(ln)}</text>'
        cx = x + 30
        for ch_ in chips:
            w = len(ch_) * 8.4 + 22
            c += f'<rect x="{cx}" y="{y+ch-58}" width="{w:.0f}" height="28" rx="14" fill="none" stroke="{BLUE}" stroke-opacity=".6"/><text class="chip" x="{cx+11}" y="{y+ch-39}">{esc(ch_)}</text>'
            cx += w + 8
        c += glyph(kind, x + cw - 164, y + 40) + '</g>'
        body += c
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>{css}</style>{body}</svg>"""
    open(os.path.join(OUT, 'roles.svg'), 'w').write(svg)

# ---------------------------------------------------------------- stack
STACK = [('Unity-Dark', 'Unity'), ('CS', 'C#'), ('Python-Dark', 'Python'), ('JavaScript', 'JavaScript'), ('HTML', 'HTML'), ('CSS', 'CSS'),
         ('PHP-Dark', 'PHP'), ('Java-Dark', 'Java'), (None, 'AI / ML'), ('Figma-Dark', 'Figma'), ('Git', 'Git'), ('Github-Dark', 'GitHub')]
def icon(name, uid):
    src = urllib.request.urlopen(f'https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/{name}.svg').read().decode()
    inner = re.sub(r'^<svg[^>]*>|</svg>\s*$', '', src.strip())
    return re.sub(r'(id="|url\(#)([^")]+)', lambda m: m.group(1) + uid + m.group(2), inner)
def ai_icon():                    # no logo for "AI / ML" — a little network of squares instead
    s = f'<rect width="256" height="256" rx="60" fill="#242938"/>'
    P = [(64, 80), (64, 176), (128, 56), (128, 128), (128, 200), (192, 96), (192, 160)]
    for a, b in ((0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 5), (3, 5), (3, 6), (4, 6), (2, 6), (4, 5)):
        s += f'<line x1="{P[a][0]}" y1="{P[a][1]}" x2="{P[b][0]}" y2="{P[b][1]}" stroke="{BLUE}" stroke-width="6" stroke-opacity=".55"/>'
    for k, (x, y) in enumerate(P): s += f'<rect x="{x-16}" y="{y-16}" width="32" height="32" fill="{BLUE if 2 <= k <= 4 else PAPER}"/>'
    return s
def stack():
    cols, tw, th, gap = 6, 184, 168, 19
    W = cols * tw + (cols - 1) * gap; rows = (len(STACK) + cols - 1) // cols; H = rows * th + (rows - 1) * gap
    css = face('PMono', ''.join(l for _, l in STACK)) + f""".lb{{font:600 15px {MONO};fill:#c9c9cd;letter-spacing:1px}}.t{{animation:t .7s cubic-bezier(.2,.8,.2,1) both}}@keyframes t{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
.f{{animation:f 5s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}@keyframes f{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}"""
    body = ''
    for i, (name, label) in enumerate(STACK):
        x, y = (i % cols) * (tw + gap), (i // cols) * (th + gap)
        ic = icon(name, f'i{i}_') if name else ai_icon()
        body += (f'<g class="t" style="animation-delay:{i*.06:.2f}s"><rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="16" fill="#111113" stroke="rgba(246,246,243,.08)"/>'
                 f'<g class="f" style="animation-delay:{-i*.4:.1f}s"><svg x="{x+tw/2-36:.0f}" y="{y+26}" width="72" height="72" viewBox="0 0 256 256">{ic}</svg></g>'
                 f'<text class="lb" x="{x+tw/2:.0f}" y="{y+th-30}" text-anchor="middle">{esc(label)}</text></g>')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>{css}</style>{body}</svg>"""
    open(os.path.join(OUT, 'stack.svg'), 'w').write(svg)

if __name__ == '__main__':
    banner(); roles(); stack(); print('ok')
