from PIL import Image, ImageDraw, ImageFont
import math

FONTS = "C:/Users/artur/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/6ba18fdc-fd6f-4526-860d-f869f7aac49e/e1dad583-8209-42ec-979d-c51513833980/skills/canvas-design/canvas-fonts/"

def F(name, size):
    return ImageFont.truetype(FONTS + name, size)

# ── Palette ──────────────────────────────────────
BG      = (10,  15,  30)
NAVY    = (13,  20,  42)
NAVY2   = (18,  28,  58)
AMBER   = (217, 119,  6)
AMBER_L = (251, 191, 36)
AMBER_D = (160,  85,  2)
WHITE   = (245, 248, 252)
MUTED   = (120, 140, 170)
SOFT    = ( 60,  85, 130)

# ── Dimensions ───────────────────────────────────
CW, CH = 1063, 591
PAD    = 50
GAP    = 80
TW     = PAD*2 + CW*2 + GAP
TH     = PAD*2 + CH + 32

canvas = Image.new('RGB', (TW, TH), (4, 6, 14))
cdraw  = ImageDraw.Draw(canvas)

# ─────────────────────────────────────────────────
def circle_photo(base, path, cx, cy, size, ring=5):
    img = Image.open(path).convert('RGBA')
    w, h = img.size
    side = min(w, h)
    l = (w - side)//2
    t = max(0, int((h - side) * 0.1))
    img = img.crop((l, t, l+side, t+side)).resize((size, size), Image.LANCZOS)

    # glow ring (amber, soft)
    glow_sz = size + ring*2 + 8
    glow = Image.new('RGBA', (glow_sz, glow_sz), (0,0,0,0))
    gd   = ImageDraw.Draw(glow)
    for i in range(8, 0, -1):
        alpha = int(40 * (i/8))
        gd.ellipse([(i,i),(glow_sz-i-1,glow_sz-i-1)], outline=(*AMBER, alpha), width=1)
    base.paste(glow.convert('RGB'), (cx - glow_sz//2, cy - glow_sz//2),
               mask=glow.split()[3])

    # amber solid ring
    ring_sz = size + ring*2
    ring_img = Image.new('RGBA', (ring_sz, ring_sz), (0,0,0,0))
    rd = ImageDraw.Draw(ring_img)
    rd.ellipse([(0,0),(ring_sz-1,ring_sz-1)], fill=(*AMBER,255))
    bg_ring = Image.new('RGB', (ring_sz, ring_sz), BG)
    bg_ring.paste(ring_img.convert('RGB'))
    base.paste(bg_ring, (cx-ring_sz//2, cy-ring_sz//2))

    # thin inner gap ring (dark)
    gap_sz = size + 2
    gap_img = Image.new('RGBA', (gap_sz, gap_sz), (0,0,0,0))
    gapd = ImageDraw.Draw(gap_img)
    gapd.ellipse([(0,0),(gap_sz-1,gap_sz-1)], fill=(*BG,255))
    bg_gap = Image.new('RGB', (gap_sz, gap_sz), BG)
    bg_gap.paste(gap_img.convert('RGB'))
    base.paste(bg_gap, (cx-gap_sz//2, cy-gap_sz//2))

    # photo circle
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse([(0,0),(size-1,size-1)], fill=255)
    bg = Image.new('RGB', (size, size), BG)
    bg.paste(img.convert('RGB'), mask=mask)
    base.paste(bg, (cx-size//2, cy-size//2))

def bleed(d, w, h, b=22):
    c = (28, 44, 72)
    st, sg = 12, 6
    for x in range(b, w-b, st):
        d.line([(x,b),(x+sg,b)], fill=c)
        d.line([(x,h-b),(x+sg,h-b)], fill=c)
    for y in range(b, h-b, st):
        d.line([(b,y),(b,y+sg)], fill=c)
        d.line([(w-b,y),(w-b,y+sg)], fill=c)

# ─────────────────────────────────────────────────
# FRONT
# ─────────────────────────────────────────────────
front = Image.new('RGB', (CW, CH), BG)
fd    = ImageDraw.Draw(front)

# LEFT PANEL — dark navy block
front.paste(Image.new('RGB', (310, CH), NAVY), (0, 0))

# Amber diagonal slash accent (left panel right edge)
for i in range(6):
    x = 310 + i
    shade = AMBER if i < 3 else AMBER_D
    fd.line([(x, 0),(x, CH)], fill=shade if i==1 else (
        (*AMBER_D, ) if i > 3 else AMBER), width=1)

# Dot pattern — bottom left decorative
for row in range(8):
    for col in range(6):
        dx = 28 + col * 22
        dy = CH - 130 + row * 16
        alpha = max(0, 60 - row*6 - col*3)
        if 0 < dx < 290 and 0 < dy < CH:
            fd.ellipse([(dx,dy),(dx+3,dy+3)], fill=(*SOFT, alpha) if alpha > 10 else SOFT)

# Photo — hero element, large and centered in left panel
circle_photo(front,
             "C:/Users/artur/cartao-digital-repo/foto.png",
             cx=155, cy=220, size=168, ring=5)

# Name below photo in left panel
fn_name = F("Outfit-Bold.ttf", 15)
fn_tiny = F("InstrumentSans-Regular.ttf", 10)
name_parts = ["Adacto Artur", "Dornas de Oliveira"]
for i, part in enumerate(name_parts):
    bb = fd.textbbox((0,0), part, font=fn_name)
    nx = 155 - (bb[2]-bb[0])//2
    fd.text((nx, 312 + i*20), part, font=fn_name, fill=WHITE)

# Cargo below name (left)
cargo_f = F("InstrumentSans-Regular.ttf", 11)
cargo_bb = fd.textbbox((0,0), "GESTOR PÚBLICO", font=cargo_f)
cx_text = 155 - (cargo_bb[2]-cargo_bb[0])//2
fd.text((cx_text, 356), "GESTOR PÚBLICO", font=cargo_f, fill=AMBER_L)

# Thin amber line under cargo
fd.line([(cx_text, 374),(cx_text + cargo_bb[2]-cargo_bb[0], 374)],
        fill=AMBER, width=1)

# ── RIGHT PANEL ───────────────────────────────────
# Top amber bar — thick, full right panel width
fd.rectangle([(320, 0),(CW, 5)], fill=AMBER_L)
fd.rectangle([(320, 5),(CW, 7)], fill=AMBER)

# BIG name — hero on right
fn_hero  = F("Outfit-Bold.ttf", 44)
fn_hero2 = F("Outfit-Bold.ttf", 38)
fn_badge = F("InstrumentSans-Bold.ttf", 12)
fn_lbl   = F("InstrumentSans-Regular.ttf", 10)
fn_val   = F("InstrumentSans-Regular.ttf", 14)

tx, ty = 356, 38
fd.text((tx, ty), "Adacto Artur", font=fn_hero, fill=WHITE)
ty += 52
fd.text((tx, ty), "Dornas de Oliveira", font=fn_hero2, fill=WHITE)
ty += 52

# Badge
badge_txt = "GESTOR  PÚBLICO"
bb = fd.textbbox((0,0), badge_txt, font=fn_badge)
bw, bh = bb[2]-bb[0]+28, 26
fd.rounded_rectangle([(tx, ty),(tx+bw, ty+bh)],
                     radius=4, fill=(50, 28, 2))
fd.rounded_rectangle([(tx, ty),(tx+bw, ty+bh)],
                     radius=4, outline=AMBER, width=1)
fd.text((tx+14, ty+7), badge_txt, font=fn_badge, fill=AMBER_L)
ty += bh + 24

# Amber divider
fd.line([(tx, ty),(CW-50, ty)], fill=AMBER, width=1)
fd.ellipse([(tx-3, ty-3),(tx+3, ty+3)], fill=AMBER_L)
fd.ellipse([(CW-53, ty-3),(CW-47, ty+3)], fill=AMBER_L)
ty += 20

# Contacts — icon dots + label + value
rows = [
    ("TEL",      "(61) 9 9968-2929"),
    ("E-MAIL",   "adactoartur.gestor@gmail.com"),
    ("LINKEDIN", "adacto-artur-dornas-de-oliveira"),
    ("DIGITAL",  "adacto.github.io/cartao-digital"),
]
for lbl, val in rows:
    # amber dot accent
    fd.ellipse([(tx, ty+5),(tx+5, ty+10)], fill=AMBER)
    fd.text((tx+14,  ty+1), lbl, font=fn_lbl, fill=MUTED)
    fd.text((tx+75,  ty-1), val, font=fn_val,  fill=WHITE)
    ty += 32

# Subtle large watermark text bottom-right
wm_f = F("Outfit-Bold.ttf", 80)
fd.text((CW-220, CH-95), "AA", font=wm_f, fill=(20, 32, 60))

bleed(fd, CW, CH)
canvas.paste(front, (PAD, PAD))

# ─────────────────────────────────────────────────
# BACK
# ─────────────────────────────────────────────────
back = Image.new('RGB', (CW, CH), BG)
bd   = ImageDraw.Draw(back)

# Left accent strip
back.paste(Image.new('RGB', (8, CH), NAVY2), (0, 0))
bd.rectangle([(0,0),(3,CH)], fill=AMBER)
bd.rectangle([(3,0),(8,CH)], fill=NAVY2)

# Right accent strip
bd.rectangle([(CW-3,0),(CW,CH)], fill=AMBER)
bd.rectangle([(CW-8,0),(CW-3,CH)], fill=NAVY2)

# Top amber bar
bd.rectangle([(0,0),(CW,5)], fill=AMBER_L)
bd.rectangle([(0,5),(CW,7)], fill=AMBER)

# Bottom bar
bd.rectangle([(0,CH-7),(CW,CH-5)], fill=AMBER)
bd.rectangle([(0,CH-5),(CW,CH)], fill=AMBER_L)

# Dot grid background (subtle)
for row in range(18):
    for col in range(30):
        dx = 40 + col * 34
        dy = 30 + row * 30
        if 40 < dx < CW-40 and 30 < dy < CH-30:
            bd.ellipse([(dx,dy),(dx+2,dy+2)], fill=(22,34,58))

# QR code — large and prominent
qr_size = 290
qr = Image.open("C:/Users/artur/cartao-digital-repo/qrcode-impressao.png").convert('RGB')
qr = qr.resize((qr_size, qr_size), Image.LANCZOS)

qr_x = (CW - qr_size)//2
qr_y = (CH - qr_size)//2 - 18

# White frame
fp = 14
bd.rounded_rectangle(
    [(qr_x-fp, qr_y-fp),(qr_x+qr_size+fp, qr_y+qr_size+fp)],
    radius=8, fill=(248, 250, 252))

# Amber corner markers on frame
mk = 18
for (ax, ay) in [(qr_x-fp, qr_y-fp),(qr_x+qr_size+fp-mk, qr_y-fp),
                  (qr_x-fp, qr_y+qr_size+fp-mk),(qr_x+qr_size+fp-mk, qr_y+qr_size+fp-mk)]:
    bd.rectangle([(ax, ay),(ax+mk, ay+mk)], outline=AMBER, width=2)

back.paste(qr, (qr_x, qr_y))

# Tagline
tag_f  = F("InstrumentSans-Bold.ttf", 15)
tag    = "Escaneie para meu cartão digital"
tb     = bd.textbbox((0,0), tag, font=tag_f)
tw     = tb[2]-tb[0]
tag_x  = (CW-tw)//2
tag_y  = qr_y + qr_size + fp + 14
bd.text((tag_x, tag_y), tag, font=tag_f, fill=WHITE)

# Small amber line under tagline
bd.line([(tag_x+tw//2-30, tag_y+22),(tag_x+tw//2+30, tag_y+22)],
        fill=AMBER, width=2)

# Name
nm_f = F("Outfit-Bold.ttf", 11)
nm   = "ADACTO ARTUR DORNAS DE OLIVEIRA"
nb   = bd.textbbox((0,0), nm, font=nm_f)
nw   = nb[2]-nb[0]
bd.text(((CW-nw)//2, qr_y - 36), nm, font=nm_f, fill=MUTED)

bleed(bd, CW, CH)
canvas.paste(back, (PAD + CW + GAP, PAD))

# Labels
lf = F("InstrumentSans-Regular.ttf", 11)
cdraw.text((PAD + CW//2 - 28, TH-20), "FRENTE", font=lf, fill=(40,62,95))
cdraw.text((PAD + CW + GAP + CW//2 - 22, TH-20), "VERSO",  font=lf, fill=(40,62,95))

out = "C:/Users/artur/cartao-digital-repo/cartao-visita.png"
canvas.save(out, dpi=(300,300))
print(f"Salvo: {out}  ({TW}x{TH}px)")
