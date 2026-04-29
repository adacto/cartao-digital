from PIL import Image, ImageDraw, ImageFont
import math

FONTS = "C:/Users/artur/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/6ba18fdc-fd6f-4526-860d-f869f7aac49e/e1dad583-8209-42ec-979d-c51513833980/skills/canvas-design/canvas-fonts/"
def F(name, size): return ImageFont.truetype(FONTS + name, size)

# ── Palette ──────────────────────────────────────
BG      = (10,  15,  30)
NAVY    = (13,  20,  42)
AMBER   = (217, 119,  6)
AMBER_L = (251, 191, 36)
WHITE   = (245, 248, 252)
MUTED   = (120, 140, 170)
SOFT    = ( 40,  65, 110)

W, H = 700, 390   # frame size
TOTAL = 52        # total frames
frames = []

def ease(t):        return t * t * (3 - 2*t)          # smooth step
def ease_out(t):    return 1 - (1-t)**3
def clamp(v,a,b):   return max(a, min(b, v))
def lerp(a,b,t):    return a + (b-a)*clamp(t,0,1)

def blend_color(c1, c2, t):
    return tuple(int(lerp(a,b,t)) for a,b in zip(c1,c2))

def circle_photo_frame(draw, base, cx, cy, size, alpha_pct):
    """Paste circular photo with opacity simulation via blend."""
    try:
        img = Image.open("C:/Users/artur/cartao-digital-repo/foto.png").convert('RGBA')
        w, h = img.size
        side = min(w, h)
        l = (w-side)//2; t = max(0, int((h-side)*0.1))
        img = img.crop((l,t,l+side,t+side)).resize((size,size), Image.LANCZOS)
        mask = Image.new('L',(size,size),0)
        ImageDraw.Draw(mask).ellipse([(0,0),(size-1,size-1)], fill=int(255*alpha_pct))
        bg = Image.new('RGB',(size,size), BG)
        bg.paste(img.convert('RGB'), mask=mask)
        base.paste(bg,(cx-size//2, cy-size//2))
        # amber ring
        if alpha_pct > 0.1:
            ring = size+8
            draw.ellipse([(cx-ring//2,cy-ring//2),(cx+ring//2,cy+ring//2)],
                         outline=blend_color(BG, AMBER, alpha_pct), width=3)
    except: pass

# ── Font preload ──────────────────────────────────
fn_hero  = F("Outfit-Bold.ttf", 32)
fn_hero2 = F("Outfit-Bold.ttf", 26)
fn_badge = F("InstrumentSans-Bold.ttf", 10)
fn_lbl   = F("InstrumentSans-Regular.ttf", 9)
fn_val   = F("InstrumentSans-Regular.ttf", 11)
fn_tag   = F("InstrumentSans-Bold.ttf", 12)
fn_name  = F("Outfit-Bold.ttf", 9)

contacts = [
    ("TEL",      "(61) 9 9968-2929"),
    ("E-MAIL",   "adactoartur.gestor@gmail.com"),
    ("LINKEDIN", "adacto-artur-dornas-de-oliveira"),
    ("DIGITAL",  "adacto.github.io/cartao-digital"),
]

# ── QR preload ────────────────────────────────────
qr_size = 180
qr_img  = Image.open("C:/Users/artur/cartao-digital-repo/qrcode-impressao.png").convert('RGB')
qr_img  = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

print("Gerando frames...")

for f in range(TOTAL):
    t = f / (TOTAL - 1)   # 0.0 → 1.0

    img = Image.new('RGB', (W, H), BG)
    d   = ImageDraw.Draw(img)

    # ── PHASE 0 (0–0.12): amber bar sweeps left→right ──
    bar_t = clamp((t - 0.0) / 0.12, 0, 1)
    bar_x = int(ease_out(bar_t) * W)
    if bar_x > 0:
        d.rectangle([(0,0),(bar_x,4)], fill=AMBER_L)
        d.rectangle([(0,4),(bar_x,6)], fill=AMBER)

    # ── PHASE 1 (0.08–0.25): left navy panel slides in ──
    panel_t = clamp((t - 0.08) / 0.17, 0, 1)
    panel_w = int(ease_out(panel_t) * 200)
    if panel_w > 0:
        img.paste(Image.new('RGB',(panel_w,H),NAVY),(0,0))
        d.rectangle([(0,0),(panel_w,4)], fill=AMBER_L)
        d.rectangle([(0,4),(panel_w,6)], fill=AMBER)
        d.rectangle([(panel_w-2,0),(panel_w,H)], fill=AMBER)

    # ── PHASE 2 (0.2–0.4): photo fades in ──
    photo_t = clamp((t - 0.2) / 0.2, 0, 1)
    photo_a = ease_out(photo_t)
    if photo_a > 0.05:
        # glow rings
        for r in range(70, 50, -5):
            a = int(20 * photo_a * (1 - (r-50)/20))
            d.ellipse([(100-r,H//2-r),(100+r,H//2+r)],
                      outline=blend_color(NAVY, AMBER, photo_a*0.3), width=1)
        circle_photo_frame(d, img, 100, H//2-10, 120, photo_a)

    # ── PHASE 3 (0.35–0.52): name slides up ──
    name_t = clamp((t - 0.35) / 0.17, 0, 1)
    name_a = ease_out(name_t)
    name_offset = int(lerp(30, 0, name_a))
    if name_a > 0.05:
        col = blend_color(BG, WHITE, name_a)
        d.text((225, 38 + name_offset), "Adacto Artur",       font=fn_hero,  fill=col)
        d.text((225, 75 + name_offset), "Dornas de Oliveira", font=fn_hero2, fill=col)

    # ── PHASE 4 (0.48–0.58): badge appears ──
    badge_t = clamp((t - 0.48) / 0.10, 0, 1)
    badge_a = ease_out(badge_t)
    if badge_a > 0.1:
        bx, by = 225, 110
        bb = d.textbbox((0,0),"GESTOR  PÚBLICO",font=fn_badge)
        bw,bh = bb[2]-bb[0]+20, 20
        bg_c  = blend_color(BG,(50,28,2),badge_a)
        brd_c = blend_color(BG, AMBER, badge_a)
        d.rounded_rectangle([(bx,by),(bx+bw,by+bh)], radius=3, fill=bg_c)
        d.rounded_rectangle([(bx,by),(bx+bw,by+bh)], radius=3, outline=brd_c, width=1)
        txt_c = blend_color(BG, AMBER_L, badge_a)
        d.text((bx+10,by+5),"GESTOR  PÚBLICO",font=fn_badge,fill=txt_c)

    # ── PHASE 5 (0.55–0.65): divider line draws ──
    div_t = clamp((t - 0.55) / 0.10, 0, 1)
    div_x = int(lerp(225, W-40, ease_out(div_t)))
    if div_t > 0:
        d.line([(225,140),(div_x,140)], fill=blend_color(BG,AMBER,ease_out(div_t)), width=1)
        d.ellipse([(222,137),(228,143)], fill=blend_color(BG,AMBER_L,ease_out(div_t)))

    # ── PHASE 6 (0.60–0.82): contacts appear one by one ──
    for i, (lbl, val) in enumerate(contacts):
        c_start = 0.60 + i * 0.055
        ct = clamp((t - c_start) / 0.08, 0, 1)
        ca = ease_out(ct)
        if ca > 0.05:
            cy_row = 155 + i * 26
            off    = int(lerp(12, 0, ca))
            dot_c  = blend_color(BG, AMBER, ca)
            lbl_c  = blend_color(BG, MUTED, ca)
            val_c  = blend_color(BG, WHITE, ca)
            d.ellipse([(225,cy_row+off+3),(230,cy_row+off+8)], fill=dot_c)
            d.text((240, cy_row+off),    lbl, font=fn_lbl, fill=lbl_c)
            d.text((290, cy_row+off-2),  val, font=fn_val, fill=val_c)

    # ── PHASE 7 (0.84–1.0): FLIP TO VERSO ──────────
    flip_t  = clamp((t - 0.84) / 0.16, 0, 1)
    flip_ea = ease(flip_t)

    if flip_ea > 0.01:
        # simulate flip: compress width then expand with back content
        scale   = abs(math.cos(flip_ea * math.pi / 2)) if flip_ea < 1 else 0
        back_w  = int(W * (1 - scale))

        if back_w > 10:
            back_img = Image.new('RGB', (back_w, H), BG)
            bd2 = ImageDraw.Draw(back_img)

            # background
            back_img.paste(Image.new('RGB',(back_w,H),BG))

            # amber frame
            bd2.rectangle([(0,0),(back_w-1,4)], fill=AMBER_L)
            bd2.rectangle([(0,H-6),(back_w-1,H)], fill=AMBER_L)
            bd2.rectangle([(0,0),(3,H)], fill=AMBER)
            bd2.rectangle([(back_w-3,0),(back_w,H)], fill=AMBER)

            # dot grid
            for row in range(12):
                for col in range(20):
                    dx = 20 + col * int(back_w/20)
                    dy = 20 + row * 30
                    if dx < back_w-10:
                        bd2.ellipse([(dx,dy),(dx+2,dy+2)],fill=(22,34,58))

            # QR code scaled
            if flip_ea > 0.5:
                qa = clamp((flip_ea - 0.5)/0.5, 0, 1)
                q_sc = int(qr_size * min(back_w/W, 1.0))
                if q_sc > 40:
                    q_resized = qr_img.resize((q_sc, q_sc), Image.LANCZOS)
                    fp = 8
                    qx = (back_w-q_sc)//2
                    qy = (H-q_sc)//2 - 20
                    bd2.rounded_rectangle([(qx-fp,qy-fp),(qx+q_sc+fp,qy+q_sc+fp)],
                                          radius=5, fill=(248,250,252))
                    back_img.paste(q_resized,(qx,qy))
                    # tagline
                    if qa > 0.6:
                        tg_c = blend_color(BG,WHITE,(qa-0.6)/0.4)
                        tag  = "Escaneie para meu cartão digital"
                        tb   = bd2.textbbox((0,0),tag,font=fn_tag)
                        tw   = tb[2]-tb[0]
                        bd2.text(((back_w-tw)//2, qy+q_sc+fp+10), tag,
                                 font=fn_tag, fill=tg_c)

            # paste verso over front
            img.paste(back_img, (W-back_w, 0))

    # Amber bar always on top
    if bar_x > 0 and flip_ea < 0.5:
        d.rectangle([(0,0),(min(bar_x,W),4)], fill=AMBER_L)
        d.rectangle([(0,4),(min(bar_x,W),6)], fill=AMBER)

    frames.append(img)
    if f % 10 == 0:
        print(f"  frame {f+1}/{TOTAL}")

# Hold last frame 2x
frames += [frames[-1]] * 8

# ── Export GIF ────────────────────────────────────
out = "C:/Users/artur/cartao-digital-repo/cartao-animado.gif"
durations = [80] * TOTAL + [120] * 8
frames[0].save(
    out,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    optimize=True
)
print(f"\nSalvo: {out}")
import os
size_kb = os.path.getsize(out) // 1024
print(f"Tamanho: {size_kb} KB")
