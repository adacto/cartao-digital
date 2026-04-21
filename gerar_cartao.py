from PIL import Image, ImageDraw, ImageFont
import math, os

FONTS = "C:/Users/artur/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/6ba18fdc-fd6f-4526-860d-f869f7aac49e/e1dad583-8209-42ec-979d-c51513833980/skills/canvas-design/canvas-fonts/"

def F(name, size):
    return ImageFont.truetype(FONTS + name, size)

# ── Palette ──────────────────────────────────────
BG_OUT  = (6,  10,  20)
BG_CARD = (11, 17,  32)
BG_SURF = (15, 23,  42)
AMBER   = (217,119,  6)
AMBER_L = (251,191, 36)
WHITE   = (241,245,249)
MUTED   = (100,116,139)
DARK_HI = (20, 32,  60)
BLEED_C = (30, 48,  80)

# ── Dimensions ───────────────────────────────────
CW, CH = 1063, 591          # one card face at 300 DPI (9x5cm)
PAD    = 50                 # outer canvas padding
GAP    = 70                 # gap between front and back
TW     = PAD*2 + CW*2 + GAP
TH     = PAD*2 + CH + 30   # +30 for labels at bottom

canvas = Image.new('RGB', (TW, TH), BG_OUT)
draw   = ImageDraw.Draw(canvas)

# ─────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────

def paste_circle(base, img_path, cx, cy, size, border=4, border_color=AMBER):
    img = Image.open(img_path).convert('RGBA')
    w, h = img.size
    side = min(w, h)
    l = (w - side)//2
    t = max(0, (h - side)//5)      # crop favor face
    img = img.crop((l, t, l+side, t+side)).resize((size, size), Image.LANCZOS)

    # amber border disc
    total = size + border*2
    disc  = Image.new('RGBA', (total, total), (0,0,0,0))
    dd    = ImageDraw.Draw(disc)
    dd.ellipse([(0,0),(total-1,total-1)], fill=(*border_color,255))
    disc_rgb = Image.new('RGB', (total, total), BG_CARD)
    disc_rgb.paste(disc.convert('RGB'), (0,0))
    bx, by = cx - total//2, cy - total//2
    base.paste(disc_rgb, (bx, by))

    # circular photo
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse([(0,0),(size-1,size-1)], fill=255)
    bg   = Image.new('RGB', (size, size), BG_CARD)
    bg.paste(img.convert('RGB'), mask=mask)
    px, py = cx - size//2, cy - size//2
    base.paste(bg, (px, py))

def bleed_marks(d, w, h, b=25):
    c = BLEED_C
    step, seg = 14, 7
    for x in range(b, w-b, step):
        d.line([(x, b),(x+seg, b)], fill=c)
        d.line([(x, h-b),(x+seg, h-b)], fill=c)
    for y in range(b, h-b, step):
        d.line([(b, y),(b, y+seg)], fill=c)
        d.line([(w-b, y),(w-b, y+seg)], fill=c)

def amber_line(d, x1, y, x2, width=2):
    d.line([(x1, y),(x2, y)], fill=AMBER, width=width)

def amber_line_v(d, x, y1, y2, width=1):
    d.line([(x,y1),(x,y2)], fill=(30,48,75), width=width)

# ─────────────────────────────────────────────────
# FRONT CARD
# ─────────────────────────────────────────────────
front = Image.new('RGB', (CW, CH), BG_CARD)
fd    = ImageDraw.Draw(front)

# Bleed marks
bleed_marks(fd, CW, CH)

# Subtle geometric fill — top-right corner triangle
pts = [(CW,0),(CW,180),(CW-180,0)]
fd.polygon(pts, fill=BG_SURF)

# Top amber bar
amber_line(fd, 60, 0, CW-60, width=3)

# Left column background (slightly lighter)
fd.rectangle([(0,0),(295,CH)], fill=(13,21,38))

# Photo
photo_cx, photo_cy = 148, CH//2 - 10
paste_circle(front, "C:/Users/artur/cartao-digital-repo/foto.png",
             photo_cx, photo_cy, size=120, border=4)

# Vertical separator
amber_line_v(fd, 300, 50, CH-50, width=1)

# ── RIGHT SIDE ────────────────────────────────────
tx = 340
ty = 72

# Name
fn_bold = F("Outfit-Bold.ttf", 30)
fn_reg  = F("InstrumentSans-Regular.ttf", 13)
fn_sm   = F("InstrumentSans-Regular.ttf", 11)
fn_lbl  = F("InstrumentSans-Regular.ttf", 10)
fn_mono = F("Outfit-Bold.ttf", 60)

fd.text((tx, ty), "Adacto Artur", font=fn_bold, fill=WHITE)
ty += 38
fd.text((tx, ty), "Dornas de Oliveira", font=fn_bold, fill=WHITE)
ty += 52

# Badge
badge_txt = "GESTOR  PÚBLICO"
bb = fd.textbbox((0,0), badge_txt, font=fn_lbl)
bw, bh = bb[2]-bb[0]+24, 24
fd.rounded_rectangle([(tx, ty),(tx+bw, ty+bh)], radius=4, fill=(35,22,4))
fd.rounded_rectangle([(tx, ty),(tx+bw, ty+bh)], radius=4, outline=(*AMBER,200), width=1)
fd.text((tx+12, ty+6), badge_txt, font=fn_lbl, fill=AMBER_L)
ty += bh + 28

# Amber divider
amber_line(fd, tx, ty, tx+290, width=1)
ty += 18

# Contacts
rows = [
    ("TEL",      "(61) 9 9968-2929"),
    ("E-MAIL",   "adactoartur.gestor@gmail.com"),
    ("LINKEDIN", "adacto-artur-dornas-de-oliveira"),
    ("DIGITAL",  "adacto.github.io/cartao-digital"),
]
for lbl, val in rows:
    fd.text((tx,     ty+2), lbl, font=fn_lbl, fill=MUTED)
    fd.text((tx+90,  ty),   val, font=fn_reg,  fill=WHITE)
    ty += 30

# Subtle background monogram
fd.text((CW-105, CH-82), "AA", font=fn_mono, fill=(18,29,54))

canvas.paste(front, (PAD, PAD))

# ─────────────────────────────────────────────────
# BACK CARD
# ─────────────────────────────────────────────────
back  = Image.new('RGB', (CW, CH), BG_CARD)
bd    = ImageDraw.Draw(back)

bleed_marks(bd, CW, CH)

# Corner amber accents
cm = 45
for px_, py_, dx, dy in [(0,0,cm,cm),(CW-cm,0,CW,cm),(0,CH-cm,cm,CH),(CW-cm,CH-cm,CW,CH)]:
    cx1,cy1 = (px_,py_) if dx>px_ else (px_,py_)
    # L-shaped corner lines
    pass
for x0,y0,x1,y1,x2,y2 in [
    (cm,0, 0,0, 0,cm),
    (CW-cm,0, CW,0, CW,cm),
    (0,CH-cm, 0,CH, cm,CH),
    (CW-cm,CH, CW,CH, CW,CH-cm),
]:
    bd.line([(x0,y0),(x1,y1),(x2,y2)], fill=AMBER, width=2)

# QR code
qr_size = 230
qr = Image.open("C:/Users/artur/cartao-digital-repo/qrcode-impressao.png").convert('RGB')
qr = qr.resize((qr_size, qr_size), Image.LANCZOS)

qr_x = (CW - qr_size)//2
qr_y = (CH - qr_size)//2 - 22

# White frame around QR
fp = 12
bd.rounded_rectangle(
    [(qr_x-fp, qr_y-fp),(qr_x+qr_size+fp, qr_y+qr_size+fp)],
    radius=6, fill=(245,248,252)
)
back.paste(qr, (qr_x, qr_y))

# Tagline
tag_f = F("InstrumentSans-Regular.ttf", 14)
tag   = "Escaneie para meu cartão digital"
tb    = bd.textbbox((0,0), tag, font=tag_f)
tw    = tb[2]-tb[0]
bd.text(((CW-tw)//2, qr_y+qr_size+fp+16), tag, font=tag_f, fill=MUTED)

# Amber dot accent
ay = qr_y+qr_size+fp+16 + 8
bd.ellipse([((CW-tw)//2 - 14, ay),((CW-tw)//2 - 6, ay+8)], fill=AMBER)

# Name subtle
nm_f  = F("Outfit-Bold.ttf", 10)
nm    = "ADACTO ARTUR DORNAS DE OLIVEIRA"
nb    = bd.textbbox((0,0), nm, font=nm_f)
nw    = nb[2]-nb[0]
nx    = (CW-nw)//2
bd.line([(nx, CH-52),(nx+nw, CH-52)], fill=(30,48,78), width=1)
bd.text((nx, CH-46), nm, font=nm_f, fill=(50,72,110))

# Top amber bar (back)
amber_line(bd, 60, 0, CW-60, width=3)

canvas.paste(back, (PAD + CW + GAP, PAD))

# ─────────────────────────────────────────────────
# LABELS
# ─────────────────────────────────────────────────
lf = F("InstrumentSans-Regular.ttf", 11)
draw.text((PAD + CW//2 - 28, TH-22), "FRENTE", font=lf, fill=(40,62,95))
draw.text((PAD + CW + GAP + CW//2 - 22, TH-22), "VERSO", font=lf, fill=(40,62,95))

# ─────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────
out = "C:/Users/artur/cartao-digital-repo/cartao-visita.png"
canvas.save(out, dpi=(300,300))
print(f"Salvo: {out} ({TW}x{TH}px)")
