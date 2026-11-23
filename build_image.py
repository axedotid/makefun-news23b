#!/usr/bin/env python3
"""Generate a 1024x1024 news-summary image for 23 November 2026.

Pure PIL. Writes /output/entry.png (or ./entry.png fallback).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (11, 17, 28)
PANEL = (18, 26, 42)
PANEL2 = (22, 32, 50)
ACCENT = (255, 59, 73)
ACCENT2 = (255, 176, 32)
CYAN = (34, 211, 238)
GREEN = (74, 222, 128)
WHITE = (240, 244, 250)
GREY = (156, 170, 190)
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

def f(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# subtle top accent bar
d.rectangle([0, 0, W, 8], fill=ACCENT)

# ---- Header band ----
d.rectangle([0, 8, W, 196], fill=PANEL)
d.text((40, 34), "23 NOVEMBER 2026", font=f(58), fill=WHITE)
d.text((42, 108), "MONDAY  ·  WORLD NEWS IN ONE IMAGE", font=f(24, False), fill=GREY)
# date block on right
d.rectangle([W-250, 30, W-40, 168], outline=ACCENT, width=4)
d.text((W-232, 44), "DAY", font=f(22, False), fill=ACCENT2)
d.text((W-232, 72), "324", font=f(64), fill=WHITE)
d.text((W-150, 92), "/ 365", font=f(30, False), fill=GREY)

# ---- Lead story banner ----
ly0 = 212
d.rectangle([30, ly0, W-30, ly0+150], fill=(40, 14, 20))
d.rectangle([30, ly0, 42, ly0+150], fill=ACCENT)
d.text((64, ly0+16), "LEAD", font=f(26), fill=ACCENT)
# wrap lead headline
lead = "Ukraine sinks Russian warship in Libya as war spills beyond Europe"
words = lead.split()
lines, cur = [], ""
for w in words:
    t = (cur+" "+w).strip()
    if d.textlength(t, font=f(38)) <= W-130:
        cur = t
    else:
        lines.append(cur); cur = w
if cur: lines.append(cur)
yy = ly0+54
for ln in lines[:2]:
    d.text((64, yy), ln, font=f(38), fill=WHITE)
    yy += 46

# ---- Story cards grid (2 columns) ----
stories = [
    ("CLIMATE", CYAN, "COP31 climate summit in Antalya collapses with no deal over fossil fuels"),
    ("MIDDLE EAST", ACCENT2, "Trump threatens to sink Iranian ships breaking the Hormuz naval blockade"),
    ("EUROPE", GREEN, "Student-led protests sweep Europe over wages, rents and public services"),
    ("DISASTER", (255, 120, 60), "Indonesia candy-factory fire kills 24, dozens missing in Banten"),
    ("UNITED STATES", (180, 140, 255), "Democrats clinch 258 House seats, biggest majority since 1992"),
    ("ASIA", (120, 200, 255), "Nvidia reinstates Jensen Huang as CEO after China-chip scandal"),
]

def wrap(text, font, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur+" "+w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: out.append(cur)
            cur = w
    if cur: out.append(cur)
    return out

col_x = [30, W//2 + 10]
card_w = W//2 - 40
top = 388
card_h = 172
gap = 18
positions = []
for i in range(6):
    r, c = divmod(i, 2)
    x = col_x[c]
    y = top + r*(card_h+gap)
    positions.append((x, y))

for (x, y), (tag, col, head) in zip(positions, stories):
    d.rounded_rectangle([x, y, x+card_w, y+card_h], radius=14, fill=PANEL2)
    d.rounded_rectangle([x, y, x+10, y+card_h], radius=6, fill=col)
    d.text((x+28, y+18), tag, font=f(24), fill=col)
    hl = wrap(head, f(29), card_w-50)
    ty = y+56
    for ln in hl[:4]:
        d.text((x+28, ty), ln, font=f(29), fill=WHITE)
        ty += 36

# ---- Footer ticker ----
fy = top + 3*(card_h+gap) + 4
d.rectangle([0, fy, W, H], fill=(6, 10, 18))
d.rectangle([0, fy, W, fy+4], fill=ACCENT)
ticker = ("ALSO TODAY  •  Democrats clinch 258 House seats, biggest majority since 1992   •   "
          "Manchester arena evacuated   •   Student protests sweep Europe   •   Global markets slide on AI selloff")
size = 22
while d.textlength(ticker, font=f(size, False)) > W-60 and size > 14:
    size -= 1
tfont = f(size, False)
tb = d.textbbox((0,0), ticker, font=tfont)
th = tb[3]-tb[1]
d.text((30, fy + (H-fy-th)//2 - tb[1]), ticker, font=tfont, fill=GREY)

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
try:
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
except Exception:
    out_path = "entry.png"
img.save(out_path, "PNG", optimize=True)
print("saved", out_path, img.size, os.path.getsize(out_path), "bytes")