from PIL import Image, ImageDraw, ImageFont
import math

FONTS = "C:/Users/artur/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/6ba18fdc-fd6f-4526-860d-f869f7aac49e/e1dad583-8209-42ec-979d-c51513833980/skills/canvas-design/canvas-fonts/"
def F(name, size): return ImageFont.truetype(FONTS + name, size)

# ── Palette ──────────────────────────────────────
BG      = (10,  15,  30)
NAVY    = (13,  20,  42)
NAVY2   = (16,  26,  52)
AMBER   = (217, 119,  6)
AMBER_L = (251, 191, 36)
WHITE   = (245, 248, 252)
MUTED   = (120, 140, 170)
SOFT    = ( 30,  48,  85)

# ── Dimensions (1080x1920 — universal phone wallpaper) ──
W, H = 1080, 1920
img  = Image.new('RGB', (W, H), BG)
d    = ImageDraw.Draw(img)

# ── Background: radial glow center ───────────────
cx, cy = W//2, H//2
for r in range(700, 0, -20):
    t = 1 - r/700
    alpha = int(t * t * 18)
    col = tuple(min(255, BG[i] + int((AMBER[i]-BG[i]) * t * 0.18)) for i in range(3))
    d.ellipse([(cx-r, cy-r),(cx+r, cy+r)], outline=col)

# ── Dot grid (subtle) ────────────────────────────
for row in range(35):
    for col in range(20):
        dx = 30 + col * 52
        dy = 30 + row * 52
        dist = math.sqrt((dx-cx)**2 + (dy-cy)**2)
        if dist > 320:
            d.ellipse([(dx,dy),(dx+3,dy+3)], fill=SOFT)

# ── Amber top bar ─────────────────────────────────
d.rectangle([(0,0),(W,6)],  fill=AMBER_L)
d.rectangle([(0,6),(W,10)], fill=AMBER)

# ── Amber bottom bar ──────────────────────────────
d.rectangle([(0,H-10),(W,H-6)], fill=AMBER)
d.rectangle([(0,H-6),(W,H)],    fill=AMBER_L)

# ── Amber vertical side accents ───────────────────
d.rectangle([(0,0),(4,H)],   fill=AMBER)
d.rectangle([(W-4,0),(W,H)], fill=AMBER)

# ── Photo (circular, top) ─────────────────────────
photo_size = 200
photo_y    = 180

photo = Image.open("C:/Users/artur/cartao-digital-repo/foto.png").convert('RGBA')
pw, ph = photo.size
side = min(pw, ph)
l = (pw-side)//2; t = max(0, int((ph-side)*0.1))
photo = photo.crop((l,t,l+side,t+side)).resize((photo_size, photo_size), Image.LANCZOS)

# Glow rings
for r in range(130, 100, -6):
    alpha_ratio = (r-100)/30
    glow_col = tuple(int(BG[i] + (AMBER[i]-BG[i]) * 0.15 * alpha_ratio) for i in range(3))
    d.ellipse([(cx-r, photo_y-r),(cx+r, photo_y+r)], outline=glow_col)

# Amber ring
ring = photo_size//2 + 6
d.ellipse([(cx-ring, photo_y-ring),(cx+ring, photo_y+ring)], fill=AMBER)

# Inner dark gap
gap = photo_size//2 + 2
d.ellipse([(cx-gap, photo_y-gap),(cx+gap, photo_y+gap)], fill=BG)

# Photo
mask = Image.new('L',(photo_size,photo_size),0)
ImageDraw.Draw(mask).ellipse([(0,0),(photo_size-1,photo_size-1)], fill=255)
bg_p = Image.new('RGB',(photo_size,photo_size), BG)
bg_p.paste(photo.convert('RGB'), mask=mask)
img.paste(bg_p, (cx-photo_size//2, photo_y-photo_size//2))

# ── Name ──────────────────────────────────────────
fn_name  = F("Outfit-Bold.ttf", 52)
fn_name2 = F("Outfit-Bold.ttf", 44)
fn_cargo = F("InstrumentSans-Bold.ttf", 22)
fn_tag   = F("InstrumentSans-Bold.ttf", 24)
fn_sub   = F("InstrumentSans-Regular.ttf", 18)
fn_url   = F("InstrumentSans-Regular.ttf", 20)

ty = photo_y + photo_size//2 + 36

for text, font in [("Adacto Artur", fn_name), ("Dornas de Oliveira", fn_name2)]:
    bb = d.textbbox((0,0), text, font=font)
    d.text(((W-(bb[2]-bb[0]))//2, ty), text, font=font, fill=WHITE)
    ty += (bb[3]-bb[1]) + 10

ty += 8

# Cargo badge
badge_txt = "GESTOR PÚBLICO"
bb = d.textbbox((0,0), badge_txt, font=fn_cargo)
bw, bh = bb[2]-bb[0]+40, 40
bx = (W-bw)//2
d.rounded_rectangle([(bx,ty),(bx+bw,ty+bh)], radius=8, fill=(45,25,2))
d.rounded_rectangle([(bx,ty),(bx+bw,ty+bh)], radius=8, outline=AMBER, width=2)
d.text(((W - (bb[2]-bb[0]))//2, ty+10), badge_txt, font=fn_cargo, fill=AMBER_L)
ty += bh + 48

# ── Amber divider ─────────────────────────────────
d.line([(cx-180, ty),(cx+180, ty)], fill=AMBER, width=2)
d.ellipse([(cx-184,ty-4),(cx-176,ty+4)], fill=AMBER_L)
d.ellipse([(cx+176,ty-4),(cx+184,ty+4)], fill=AMBER_L)
ty += 52

# ── QR Code (hero element) ────────────────────────
qr_size = 520
qr = Image.open("C:/Users/artur/cartao-digital-repo/qrcode-impressao.png").convert('RGB')
qr = qr.resize((qr_size, qr_size), Image.LANCZOS)

qr_x = (W - qr_size)//2
qr_y = ty

# White frame
fp = 20
d.rounded_rectangle(
    [(qr_x-fp, qr_y-fp),(qr_x+qr_size+fp, qr_y+qr_size+fp)],
    radius=16, fill=(250, 252, 255))

# Amber corner marks
mk = 36
for (ax,ay) in [(qr_x-fp, qr_y-fp),
                (qr_x+qr_size+fp-mk, qr_y-fp),
                (qr_x-fp, qr_y+qr_size+fp-mk),
                (qr_x+qr_size+fp-mk, qr_y+qr_size+fp-mk)]:
    d.rectangle([(ax,ay),(ax+mk,ay+mk)], outline=AMBER, width=4)

img.paste(qr, (qr_x, qr_y))
ty = qr_y + qr_size + fp + 40

# ── Tagline ───────────────────────────────────────
tag = "Escaneie para meu cartão digital"
bb  = d.textbbox((0,0), tag, font=fn_tag)
d.text(((W-(bb[2]-bb[0]))//2, ty), tag, font=fn_tag, fill=WHITE)
ty += (bb[3]-bb[1]) + 14

# Amber underline
d.line([(cx-80,ty),(cx+80,ty)], fill=AMBER, width=3)
ty += 28

# URL
url = "adacto.github.io/cartao-digital"
bb  = d.textbbox((0,0), url, font=fn_url)
d.text(((W-(bb[2]-bb[0]))//2, ty), url, font=fn_url, fill=MUTED)

# ── Save ──────────────────────────────────────────
out = "C:/Users/artur/cartao-digital-repo/wallpaper-celular.png"
img.save(out, dpi=(300,300))
print(f"Salvo: {out}  ({W}x{H}px)")
