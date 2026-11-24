#!/usr/bin/env python3
"""Draw entry.png: a newspaper front page summing up the world news of
Tuesday 24 November 2026. Shapes and text only, no photos, no network.
Deterministic: the same input always produces the same bytes.

Run: python3 draw.py   (writes entry.png next to this file)
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (24, 24, 24)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GREY = (110, 110, 105)
LIGHT = (232, 226, 212)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}.ttf", size)


SERIF_B = "LiberationSerif-Bold"
SERIF = "LiberationSerif-Regular"
SERIF_I = "LiberationSerif-Italic"
SANS_B = "LiberationSans-Bold"
SANS = "LiberationSans-Regular"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, y, x0=28, x1=996, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def icon_jet(draw, x, y, s, color):
    """Simple delta jet silhouette, pointing up-right."""
    draw.polygon(
        [
            (x + s * 0.95, y + s * 0.05),
            (x + s * 0.45, y + s * 0.45),
            (x + s * 0.10, y + s * 0.30),
            (x + s * 0.30, y + s * 0.60),
            (x + s * 0.05, y + s * 0.95),
            (x + s * 0.55, y + s * 0.70),
            (x + s * 0.70, y + s * 0.95),
            (x + s * 0.62, y + s * 0.52),
        ],
        fill=color,
    )


def icon_blast(draw, x, y, s, color):
    """Starburst for an explosion / strike."""
    cx, cy = x + s / 2, y + s / 2
    pts = []
    import math

    for i in range(16):
        r = s * 0.48 if i % 2 == 0 else s * 0.20
        a = math.pi * i / 8 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=color)
    draw.ellipse([cx - s * 0.12, cy - s * 0.12, cx + s * 0.12, cy + s * 0.12], fill=PAPER)


def icon_cuffs(draw, x, y, s, color):
    """Two linked rings, suggesting an arrest."""
    r = s * 0.26
    draw.ellipse([x + s * 0.06, y + s * 0.30, x + s * 0.06 + 2 * r, y + s * 0.30 + 2 * r],
                 outline=color, width=max(3, int(s * 0.07)))
    draw.ellipse([x + s * 0.94 - 2 * r, y + s * 0.30, x + s * 0.94, y + s * 0.30 + 2 * r],
                 outline=color, width=max(3, int(s * 0.07)))
    draw.line([(x + s * 0.32, y + s * 0.56), (x + s * 0.68, y + s * 0.56)],
              fill=color, width=max(3, int(s * 0.07)))


def icon_tanker(draw, x, y, s, color):
    """Oil tanker silhouette on waves."""
    draw.polygon(
        [
            (x + s * 0.05, y + s * 0.55),
            (x + s * 0.95, y + s * 0.55),
            (x + s * 0.85, y + s * 0.78),
            (x + s * 0.15, y + s * 0.78),
        ],
        fill=color,
    )
    draw.rectangle([x + s * 0.62, y + s * 0.30, x + s * 0.82, y + s * 0.55], fill=color)
    draw.rectangle([x + s * 0.68, y + s * 0.18, x + s * 0.76, y + s * 0.30], fill=color)
    draw.arc([x + s * 0.05, y + s * 0.78, x + s * 0.35, y + s * 0.98], 0, 180,
             fill=color, width=max(2, int(s * 0.05)))
    draw.arc([x + s * 0.40, y + s * 0.78, x + s * 0.70, y + s * 0.98], 0, 180,
             fill=color, width=max(2, int(s * 0.05)))
    draw.arc([x + s * 0.72, y + s * 0.78, x + s * 0.98, y + s * 0.98], 0, 180,
             fill=color, width=max(2, int(s * 0.05)))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- frame ---
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=1)

    # --- masthead ---
    d.rectangle([28, 28, 996, 132], fill=NAVY)
    name = "THE WORLD TODAY"
    f_name = font(SERIF_B, 64)
    nw = d.textlength(name, font=f_name)
    d.text(((W - nw) / 2, 40), name, font=f_name, fill=(255, 255, 255))

    # --- date strip ---
    f_date = font(SERIF_B, 30)
    date = "TUESDAY, 24 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 146), date, font=f_date, fill=NAVY)
    f_tag = font(SERIF_I, 19)
    tag = "One day's world news, in one image"
    tw = d.textlength(tag, font=f_tag)
    d.text(((W - tw) / 2, 182), tag, font=f_tag, fill=GREY)
    hrule(d, 212, width=3)
    hrule(d, 217, width=1)

    # --- lead story ---
    lx, lw = 28, 640
    y = 232
    f_kick = font(SANS_B, 19)
    d.text((lx, y), "LEAD STORY  ·  TECHNOLOGY & MARKETS", font=f_kick, fill=RED)
    y += 30
    f_head = font(SERIF_B, 48)
    y = draw_lines(d, ["HUANG IS BACK,", "AND MARKETS ROAR"], lx, y, f_head, INK, 55)
    y += 6
    f_body = font(SANS, 20)
    lead = (
        "Asia shares jumped on Tuesday as Jensen Huang returned as chief "
        "executive of Nvidia, 11 days after resigning over a scandal. "
        "Nvidia stock had surged 31% on Monday, lifting world markets. "
        "Washington blacklisted two firms at the heart of the affair."
    )
    y = draw_lines(d, wrap(d, lead, f_body, lw), lx, y, f_body, INK, 25)

    # --- lead chart (right of lead) ---
    cx0, cy0, cx1, cy1 = 700, 232, 996, 470
    d.rectangle([cx0, cy0, cx1, cy1], outline=NAVY, width=2)
    d.rectangle([cx0, cy0, cx1, cy0 + 34], fill=NAVY)
    f_ct = font(SANS_B, 17)
    ct = "MONDAY'S RALLY"
    d.text((cx0 + (cx1 - cx0 - d.textlength(ct, font=f_ct)) / 2, cy0 + 7),
           ct, font=f_ct, fill=(255, 255, 255))
    bars = [("NVIDIA", 31.0, "+31%"), ("NASDAQ", 6.5, "+6.5%"), ("S&P 500", 4.7, "+4.7%")]
    base = cy1 - 56
    max_h = 100
    bw, gap = 62, 22
    x = cx0 + 22
    f_bl = font(SANS_B, 15)
    f_bv = font(SANS_B, 17)
    for label, val, txt in bars:
        bh = max_h * val / 31.0
        d.rectangle([x, base - bh, x + bw, base], fill=RED if label == "NVIDIA" else NAVY)
        vw = d.textlength(txt, font=f_bv)
        d.text((x + (bw - vw) / 2, base - bh - 24), txt, font=f_bv, fill=INK)
        lw2 = d.textlength(label, font=f_bl)
        d.text((x + (bw - lw2) / 2, base + 8), label, font=f_bl, fill=INK)
        x += bw + gap
    f_cn = font(SERIF_I, 14)
    note = "Shares, Monday 23 Nov"
    d.text((cx0 + (cx1 - cx0 - d.textlength(note, font=f_cn)) / 2, cy1 - 26),
           note, font=f_cn, fill=GREY)

    # --- divider ---
    hrule(d, 488, width=3)
    hrule(d, 493, width=1)

    # --- four supporting stories, 2 x 2 ---
    stories = [
        ("KOREA · SECURITY", "SEOUL SOUNDS AIR-RAID ALERT AS RUSSIAN JETS NEAR ISLAND",
         "Russian warplanes entered South Korea's air defence zone near "
         "Ulleung Island and residents were told to shelter. The alert was "
         "lifted within minutes; Seoul said no airspace was violated.",
         icon_jet),
        ("UKRAINE · WAR", "DEADLY OVERNIGHT STRIKE ON ZAPORIZHZHIA",
         "A Russian attack killed two people and wounded 22, including two "
         "children, Ukrainian officials said on Tuesday.",
         icon_blast),
        ("MEXICO · CRIME", "MEXICO TO TRY CAPTURED CARTEL BOSS AT HOME",
         "'El Chapo Isidro', an FBI most-wanted fugitive captured on Friday, "
         "will face Mexican courts despite a US extradition order.",
         icon_cuffs),
        ("GULF · ENERGY", "IRAN STEPS UP STRIKES ON GULF SHIPPING",
         "Attacks on tankers in the Strait of Hormuz climb as a US blockade "
         "and sanctions squeeze Tehran; Middle East oil exports slide.",
         icon_tanker),
    ]
    f_sk = font(SANS_B, 16)
    f_sh = font(SERIF_B, 25)
    f_sb = font(SANS, 18)
    cell_w, cell_h = 470, 182
    for i, (kicker, head, body, icon) in enumerate(stories):
        col, row = i % 2, i // 2
        x0 = 28 + col * (cell_w + 28)
        y0 = 506 + row * (cell_h + 12)
        d.rectangle([x0, y0, x0 + cell_w, y0 + 4], fill=NAVY)
        icon(d, x0 + cell_w - 52, y0 + 14, 44, NAVY)
        d.text((x0, y0 + 14), kicker, font=f_sk, fill=RED)
        head_lines = wrap(d, head, f_sh, cell_w - 60)
        yy = draw_lines(d, head_lines, x0, y0 + 38, f_sh, INK, 29)
        draw_lines(d, wrap(d, body, f_sb, cell_w), x0, yy + 6, f_sb, INK, 23)

    # --- ticker ---
    ty0, ty1 = 900, 976
    d.rectangle([28, ty0, 996, ty1], fill=NAVY)
    f_tk = font(SANS_B, 16)
    f_ti = font(SANS, 16)
    d.text((44, ty0 + 8), "ALSO IN THE NEWS", font=f_tk, fill=(255, 214, 64))
    ticker = (
        "Trump to meet NATO chief Rutte on Wednesday  •  "
        "Sheikh Hasina seeks return to Bangladesh on 16 Dec  •  "
        "UN chief urges global AI rules within a year  •  "
        "COP31 ends with no deal"
    )
    draw_lines(d, wrap(d, ticker, f_ti, 996 - 44 - 16), 44, ty0 + 30, f_ti,
               (255, 255, 255), 20)

    # --- footer ---
    f_ft = font(SERIF_I, 13)
    foot = "Sources: Reuters, BBC, Al Jazeera, Korea JoongAng Daily, The Wall Street Journal — 24 November 2026"
    fw = d.textlength(foot, font=f_ft)
    d.text(((W - fw) / 2, 984), foot, font=f_ft, fill=GREY)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
