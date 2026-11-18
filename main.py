#!/usr/bin/env python3
"""news-image-20261117: one image summing up the world news of
Tuesday 17 November 2026.

Draws a 1024x1024 front-page poster with Python/PIL only: a masthead naming
the day, one lead story (the Kerch Bridge road arch collapses) with a flat
drawn illustration, and five secondary stories with flat icons and short
factual captions. No network, no randomness, no clock: running it twice
writes byte-identical output to /output/entry.png.

Fonts are vendored in fonts/ (DejaVu, permissive licence — see
fonts/LICENSE.txt) and loaded by path relative to this file, so the program
does not depend on system fonts.
"""
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BASE = Path(__file__).resolve().parent
FONTS = BASE / "fonts"

PAPER = (247, 242, 231)
WHITE = (255, 255, 255)
INK = (22, 19, 14)
NAVY = (28, 43, 69)
RED = (180, 35, 24)
GOLD = (201, 154, 43)
BLUE = (46, 94, 140)
SKY = (220, 233, 242)
SEA = (111, 168, 207)
STEEL = (90, 107, 127)
GREY = (110, 108, 100)


def F(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(d, x, y, lines, font, fill, leading=None):
    if leading is None:
        leading = int(font.size * 1.18)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def icon_drone(d, x, y, s, col):
    d.rectangle([x, y, x + s, y + s], fill=col)
    cx, cy, r = x + s / 2, y + s / 2, s * 0.30
    arm = s * 0.26
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        px, py = cx + dx * arm, cy + dy * arm
        d.line([cx, cy, px, py], fill=WHITE, width=max(3, s // 18))
        d.ellipse([px - r / 2, py - r / 2, px + r / 2, py + r / 2],
                  outline=WHITE, width=max(2, s // 28))
    d.rounded_rectangle([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
                        radius=r * 0.4, fill=WHITE)


def icon_globe(d, x, y, s, col):
    d.rectangle([x, y, x + s, y + s], fill=col)
    cx, cy, r = x + s / 2, y + s / 2, s * 0.32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=max(3, s // 18))
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=WHITE,
              width=max(2, s // 28))
    d.line([cx - r, cy, cx + r, cy], fill=WHITE, width=max(2, s // 28))
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 200, 340, fill=WHITE,
          width=max(2, s // 28))


def icon_rocket(d, x, y, s, col):
    d.rectangle([x, y, x + s, y + s], fill=col)
    cx, cy = x + s / 2, y + s / 2
    w, h = s * 0.22, s * 0.52
    d.polygon([(cx, cy - h / 2), (cx + w / 2, cy - h * 0.1), (cx + w / 2, cy + h * 0.25),
               (cx, cy + h * 0.42), (cx - w / 2, cy + h * 0.25), (cx - w / 2, cy - h * 0.1)],
              fill=WHITE)
    d.polygon([(cx - w / 2, cy + h * 0.1), (cx - w * 0.85, cy + h * 0.42),
               (cx - w / 2, cy + h * 0.32)], fill=WHITE)
    d.polygon([(cx + w / 2, cy + h * 0.1), (cx + w * 0.85, cy + h * 0.42),
               (cx + w / 2, cy + h * 0.32)], fill=WHITE)
    d.polygon([(cx, cy + h * 0.42), (cx - w * 0.3, cy + h * 0.62),
               (cx + w * 0.3, cy + h * 0.62)], fill=GOLD)


def icon_jet(d, x, y, s, col):
    d.rectangle([x, y, x + s, y + s], fill=col)
    cx, cy = x + s / 2, y + s / 2
    d.polygon([(cx - s * 0.42, cy + s * 0.05), (cx + s * 0.28, cy - s * 0.10),
               (cx + s * 0.46, cy), (cx + s * 0.28, cy + s * 0.10)],
              fill=WHITE)
    d.polygon([(cx - s * 0.05, cy - s * 0.02), (cx - s * 0.22, cy - s * 0.30),
               (cx - s * 0.08, cy - s * 0.02)], fill=WHITE)
    d.polygon([(cx - s * 0.05, cy + s * 0.02), (cx - s * 0.22, cy + s * 0.30),
               (cx - s * 0.08, cy + s * 0.02)], fill=WHITE)


def icon_scales(d, x, y, s, col):
    d.rectangle([x, y, x + s, y + s], fill=col)
    cx, cy = x + s / 2, y + s / 2
    d.line([cx, cy - s * 0.30, cx, cy + s * 0.30], fill=WHITE, width=max(3, s // 16))
    d.line([cx - s * 0.30, cy - s * 0.18, cx + s * 0.30, cy - s * 0.18], fill=WHITE,
           width=max(3, s // 16))
    d.line([cx, cy - s * 0.38, cx - s * 0.10, cy - s * 0.30], fill=WHITE,
           width=max(2, s // 28))
    d.line([cx, cy - s * 0.38, cx + s * 0.10, cy - s * 0.30], fill=WHITE,
           width=max(2, s // 28))
    for dx in (-1, 1):
        px = cx + dx * s * 0.30
        d.line([px, cy - s * 0.18, px, cy + s * 0.02], fill=WHITE, width=max(2, s // 28))
        d.polygon([(px - s * 0.13, cy + s * 0.02), (px + s * 0.13, cy + s * 0.02),
                   (px, cy + s * 0.22)], fill=WHITE)
    d.line([cx - s * 0.16, cy + s * 0.30, cx + s * 0.16, cy + s * 0.30], fill=WHITE,
           width=max(3, s // 16))


def draw_bridge(d, x, y, w, h):
    """Flat side view of the Kerch Bridge: left half intact, right arch fallen."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # (no sun: the scene reads cleaner without it)
    sea_y = y + h * 0.62
    d.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    for i in range(3):
        wy = sea_y + h * (0.12 + i * 0.12)
        d.line([x + 8, wy, x + w - 8, wy], fill=WHITE, width=3)
    rail_y = y + h * 0.52
    d.rectangle([x, rail_y, x + w, rail_y + 6], fill=(70, 85, 105))
    deck_y = y + h * 0.44
    d.rectangle([x, deck_y, x + w * 0.52, deck_y + 10], fill=INK)
    # fallen span: a thick slab tilted down into the water
    d.polygon([(x + w * 0.56, deck_y + 10), (x + w * 0.82, deck_y + h * 0.30),
               (x + w * 0.84, deck_y + h * 0.30 + 34), (x + w * 0.58, deck_y + 44)],
              fill=INK)
    for px in (0.10, 0.34):
        d.rectangle([x + w * px, deck_y - h * 0.16, x + w * px + 8, sea_y], fill=STEEL)
    d.arc([x + w * 0.06, deck_y - h * 0.34, x + w * 0.46, deck_y + 6], 180, 360,
          fill=RED, width=9)
    d.arc([x + w * 0.58, deck_y - h * 0.34, x + w * 0.98, deck_y + 6], 180, 265,
          fill=RED, width=9)
    d.arc([x + w * 0.58, deck_y - h * 0.34, x + w * 0.98, deck_y + 6], 295, 360,
          fill=RED, width=9)
    for cx, cy, r in ((0.60, 0.30, 0.055), (0.66, 0.22, 0.07), (0.73, 0.28, 0.05)):
        d.ellipse([x + w * cx - h * r, y + h * cy - h * r,
                   x + w * cx + h * r, y + h * cy + h * r], fill=(200, 200, 196))
    d.arc([x + w * 0.68, sea_y - 6, x + w * 0.86, sea_y + h * 0.16], 180, 360,
          fill=WHITE, width=4)


SECONDARIES = [
    ("MIDDLE EAST", "Iran drones target US radar in Bahrain",
     "US strikes an IRGC launch site on Qeshm in reply.", icon_drone, NAVY),
    ("ASIA", "Trump lands in Manila for ASEAN summit",
     "Xi\u2013Trump\u2013Putin three-way talks set for Thursday.", icon_globe, BLUE),
    ("SPACE", "ULA: Vulcan's first stage faltered",
     "Tuesday update on the launch that lost 40 satellites.", icon_rocket, RED),
    ("ASIA-PACIFIC", "Japan scrambles jets over Russian planes",
     "Tokyo protests after an airspace violation.", icon_jet, (42, 90, 90)),
    ("BRITAIN", "UK sanctions eight settlement firms",
     "Asset freezes over West Bank building; aid-blockers hit too.",
     icon_scales, (96, 74, 28)),
]


def render():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((36, 22), "THE WORLD IN ONE PICTURE", font=F("DejaVuSerif-Bold.ttf", 44),
           fill=WHITE)
    d.text((36, 74), "TUESDAY, 17 NOVEMBER 2026", font=F("DejaVuSans-Bold.ttf", 30),
           fill=GOLD)
    d.text((W - 36, 30), "ONE DAY", font=F("DejaVuSans-Bold.ttf", 26), fill=WHITE,
           anchor="ra")
    d.text((W - 36, 64), "SIX STORIES", font=F("DejaVuSans.ttf", 24),
           fill=(200, 205, 215), anchor="ra")
    d.text((36, 140), "EUROPE \u2022 UKRAINE", font=F("DejaVuSans-Bold.ttf", 24), fill=RED)
    hl = wrap(d, "KERCH BRIDGE ROAD ARCH COLLAPSES", F("DejaVuSans-Bold.ttf", 56), 600)
    y = text_lines(d, 36, 172, hl, F("DejaVuSans-Bold.ttf", 56), INK, leading=62)
    sub = wrap(d, "Ukraine strikes the Crimea link a second day; Kyiv's bridges "
               "hit in return. Traffic halted; the Kremlin vows to rebuild.",
               F("DejaVuSans.ttf", 25), 600)
    text_lines(d, 36, y + 14, sub, F("DejaVuSans.ttf", 25), (52, 48, 40), leading=32)
    draw_bridge(d, 668, 140, 320, 330)
    cap = wrap(d, "The road arch, down in the Kerch Strait.",
               F("DejaVuSans.ttf", 19), 320)
    text_lines(d, 668, 478, cap, F("DejaVuSans.ttf", 19), GREY, leading=24)
    y = 540
    for kicker, head, cap, icon, col in SECONDARIES:
        d.line([36, y, W - 36, y], fill=(210, 203, 188), width=2)
        icon(d, 36, y + 12, 66, col)
        d.text((120, y + 10), kicker, font=F("DejaVuSans-Bold.ttf", 18), fill=RED)
        d.text((120, y + 32), head, font=F("DejaVuSans-Bold.ttf", 26), fill=INK)
        d.text((120, y + 62), cap, font=F("DejaVuSans.ttf", 20), fill=(70, 66, 58))
        y += 82
    f = F("DejaVuSans.ttf", 17)
    d.line([36, 952, W - 36, 952], fill=GREY, width=2)
    d.text((36, 962), "SOURCES: BBC \u2022 AP \u2022 REUTERS \u2022 JUST SECURITY \u2022 GEEK WIRE",
           font=f, fill=GREY)
    d.text((W - 36, 962), "17 NOV 2026", font=f, fill=GREY, anchor="ra")
    return im


def main():
    out_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    render().save(out_dir / "entry.png")
    print("wrote", out_dir / "entry.png")


if __name__ == "__main__":
    main()
