"""
Camp '26 Flyer Generator — Pure Pillow, no browser needed.
Draws all 4 flyer versions as PNG images.
"""

from PIL import Image, ImageDraw, ImageFont
import io
import math

# ── Flyer size ────────────────────────────────────────────────────────────────
W, H = 540, 780

# ── Theme definitions ─────────────────────────────────────────────────────────
THEMES = {
    "Version 1 – Blue & Orange": {
        "banner_top":    "#1A73E8",
        "banner_bot":    "#0D47A1",
        "bg":            "#FFF8F0",
        "badge_bg":      "#FF6B35",
        "badge_shadow":  "#c44e1f",
        "badge_fg":      "#FFFFFF",
        "name_border":   "#4CC9F0",
        "name_shadow":   "#4CC9F0",
        "name_fg":       "#1A73E8",
        "sticker_col":   "#FFD93D",
        "footer_fg":     "#FFFFFF",
        "footer_sub":    "#FFD93D",
        "chip_colors":   ["#FF6B35", "#C77DFF", "#06D6A0"],
        "ring_colors":   ["#FFD93D", "#FF6B9D", "#4CC9F0", "#06D6A0"],
        "dot_col":       (255, 255, 255, 30),
        "theme_star":    "⭐",
    },
    "Version 2 – Purple & Pink": {
        "banner_top":    "#7B2FBE",
        "banner_bot":    "#4a1680",
        "bg":            "#FDF5FF",
        "badge_bg":      "#FF6B9D",
        "badge_shadow":  "#c44472",
        "badge_fg":      "#FFFFFF",
        "name_border":   "#C77DFF",
        "name_shadow":   "#C77DFF",
        "name_fg":       "#7B2FBE",
        "sticker_col":   "#FF6B9D",
        "footer_fg":     "#FFFFFF",
        "footer_sub":    "#FFD93D",
        "chip_colors":   ["#FF6B9D", "#7B2FBE", "#C77DFF"],
        "ring_colors":   ["#C77DFF", "#FF6B9D", "#FFD93D", "#C77DFF"],
        "dot_col":       (255, 255, 255, 30),
        "theme_star":    "💜",
    },
    "Version 3 – Green & Teal": {
        "banner_top":    "#0A7C59",
        "banner_bot":    "#065c41",
        "bg":            "#F0FFF8",
        "badge_bg":      "#FF6B35",
        "badge_shadow":  "#c44e1f",
        "badge_fg":      "#FFFFFF",
        "name_border":   "#06D6A0",
        "name_shadow":   "#06D6A0",
        "name_fg":       "#0A7C59",
        "sticker_col":   "#06D6A0",
        "footer_fg":     "#FFFFFF",
        "footer_sub":    "#FFD93D",
        "chip_colors":   ["#FF6B35", "#06D6A0", "#4CC9F0"],
        "ring_colors":   ["#06D6A0", "#4CC9F0", "#FFD93D", "#06D6A0"],
        "dot_col":       (255, 255, 255, 30),
        "theme_star":    "💚",
    },
    "Version 4 – Gold & Navy": {
        "banner_top":    "#0D47A1",
        "banner_bot":    "#0D47A1",
        "bg":            "#FFFBEE",
        "badge_bg":      "#FFD93D",
        "badge_shadow":  "#b89a10",
        "badge_fg":      "#0D47A1",
        "name_border":   "#FFD93D",
        "name_shadow":   "#FFD93D",
        "name_fg":       "#0D47A1",
        "sticker_col":   "#FFD93D",
        "footer_fg":     "#FFD93D",
        "footer_sub":    "#FFFFFF",
        "chip_colors":   ["#b89a10", "#1A73E8", "#FF6B35"],
        "ring_colors":   ["#FFD93D", "#FF6B35", "#1A73E8", "#FFD93D"],
        "dot_col":       (255, 255, 255, 30),
        "theme_star":    "⭐",
    },
}


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def draw_rounded_rect(draw, xy, radius, fill, outline=None, outline_width=3, shadow_color=None, shadow_offset=4):
    x0, y0, x1, y1 = xy
    if shadow_color:
        sx0, sy0, sx1, sy1 = x0 + shadow_offset, y0 + shadow_offset, x1 + shadow_offset, y1 + shadow_offset
        draw.rounded_rectangle([sx0, sy0, sx1, sy1], radius=radius, fill=shadow_color)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill,
                            outline=outline, width=outline_width if outline else 0)


def draw_circle(draw, center, radius, fill, outline=None, width=3):
    cx, cy = center
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                 fill=fill, outline=outline, width=width)


def draw_dot_pattern(img, area, color_rgba, spacing=22, dot_r=2):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    x0, y0, x1, y1 = area
    for x in range(x0, x1, spacing):
        for y in range(y0, y1, spacing):
            d.ellipse([x - dot_r, y - dot_r, x + dot_r, y + dot_r], fill=color_rgba)
    img.paste(Image.alpha_composite(img.crop((0, 0, img.width, img.height)), overlay) if False else overlay,
              mask=overlay)


def load_font(size, bold=False):
    """Try to load a system font, fall back gracefully."""
    candidates_bold = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf",
        "fonts/DejaVuSans-Bold.ttf",
        "fonts/DejaVuSans.ttf",
    ]
    candidates_reg = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "fonts/DejaVuSans.ttf",
    ]
    candidates = candidates_bold if bold else candidates_reg
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    # Last resort: use default and hope for the best
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()


def centered_text(draw, text, y, font, color, width=W):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, y), text, font=font, fill=color)


def draw_photo_ring(img, center, outer_r, ring_colors, photo_img=None):
    """Draw colourful ring then paste photo (or placeholder) inside."""
    draw = ImageDraw.Draw(img)
    cx, cy = center
    ring_w = 5
    num = len(ring_colors)
    for i, col in enumerate(ring_colors):
        start = int(360 * i / num) - 90
        end = int(360 * (i + 1) / num) - 90
        draw.arc([cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r],
                 start=start, end=end, fill=col, width=ring_w)

    # white border circle
    inner_r = outer_r - ring_w - 3
    draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
                 fill="white", outline="white", width=2)

    if photo_img:
        # paste user photo clipped to circle
        photo_size = inner_r * 2 - 4
        photo_resized = photo_img.resize((photo_size, photo_size), Image.LANCZOS)
        mask = Image.new("L", (photo_size, photo_size), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, photo_size, photo_size], fill=255)
        img.paste(photo_resized, (cx - inner_r + 2, cy - inner_r + 2), mask)
    else:
        # placeholder face
        face_r = inner_r - 10
        draw.ellipse([cx - face_r, cy - face_r, cx + face_r, cy + face_r],
                     fill="#e8e8e8")
        # Draw a simple smiley face with shapes instead of emoji
        eye_r = int(face_r * 0.1)
        eye_y = cy - int(face_r * 0.2)
        eye_lx = cx - int(face_r * 0.25)
        eye_rx = cx + int(face_r * 0.25)
        draw.ellipse([eye_lx-eye_r, eye_y-eye_r, eye_lx+eye_r, eye_y+eye_r], fill="#aaaaaa")
        draw.ellipse([eye_rx-eye_r, eye_y-eye_r, eye_rx+eye_r, eye_y+eye_r], fill="#aaaaaa")
        smile_y = cy + int(face_r * 0.1)
        smile_r = int(face_r * 0.4)
        draw.arc([cx-smile_r, smile_y-smile_r//2, cx+smile_r, smile_y+smile_r//2],
                 start=10, end=170, fill="#aaaaaa", width=3)
        font_small = load_font(11)
        ph_text = "YOUR PHOTO"
        bbox2 = draw.textbbox((0, 0), ph_text, font=font_small)
        tw2 = bbox2[2] - bbox2[0]
        draw.text((cx - tw2 // 2, cy + face_r - 18), ph_text, font=font_small, fill="#bbbbbb")


def generate_flyer(theme_name, attendee_name="", photo_img=None, badge_text="I WILL BE ATTENDING!"):
    t = THEMES[theme_name]

    img = Image.new("RGBA", (W, H), hex2rgb(t["bg"]) + (255,))
    draw = ImageDraw.Draw(img)

    # ── BANNER (top portion) ───────────────────────────────────────────────
    BANNER_H = 200
    banner = Image.new("RGBA", (W, BANNER_H + 40), (0, 0, 0, 0))
    bd = ImageDraw.Draw(banner)
    bd.rectangle([0, 0, W, BANNER_H], fill=t["banner_top"])

    # dot pattern overlay
    dot_overlay = Image.new("RGBA", (W, BANNER_H + 40), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dot_overlay)
    for x in range(0, W, 22):
        for y in range(0, BANNER_H, 22):
            dd.ellipse([x-2, y-2, x+2, y+2], fill=t["dot_col"])
    banner = Image.alpha_composite(banner, dot_overlay)

    # curved bottom of banner
    bd2 = ImageDraw.Draw(banner)
    bd2.ellipse([-60, BANNER_H - 30, W + 60, BANNER_H + 50],
                fill=hex2rgb(t["bg"]) + (255,))

    img.paste(banner, (0, 0), banner)
    draw = ImageDraw.Draw(img)

    # ── BANNER TEXT ───────────────────────────────────────────────────────
    f_stars  = load_font(15)
    f_title  = load_font(28, bold=True)
    f_theme  = load_font(11, bold=True)

    # Draw small decorative circles across top of banner
    dot_col_banner = (255, 255, 255, 80)
    banner_draw = ImageDraw.Draw(img)
    for di, dx in enumerate([W//2 - 80, W//2 - 40, W//2, W//2 + 40, W//2 + 80]):
        r = 5 if di == 2 else 4
        banner_draw.ellipse([dx-r, 28-r, dx+r, 28+r], fill=(255,255,255,120))

    centered_text(draw, "SUNDAY SCHOOL CAMP '26", 46, f_title, "white")
    theme_str = "~ GOD ANSWERS PRAYERS ~"
    centered_text(draw, theme_str, 90, f_theme,
                  t["footer_sub"] if t["banner_top"] != "#0D47A1" else "white")

    # ── BADGE TEXT ────────────────────────────────────────────────────────
    badge_text = badge_text.upper()
    # Auto-shrink font so badge always fits within flyer width
    for badge_size in [20, 17, 14, 12]:
        f_badge = load_font(badge_size, bold=True)
        bbox = draw.textbbox((0, 0), badge_text, font=f_badge)
        bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if bw <= W - 80:
            break
    pad_x, pad_y = 28, 12
    bx0 = (W - bw - pad_x * 2) // 2
    bx1 = bx0 + bw + pad_x * 2
    by0 = 145
    by1 = by0 + bh + pad_y * 2
    draw_rounded_rect(draw, [bx0, by0, bx1, by1], radius=30,
                      fill=t["badge_bg"],
                      shadow_color=t["badge_shadow"], shadow_offset=5)
    draw.text((bx0 + pad_x, by0 + pad_y), badge_text, font=f_badge, fill=t["badge_fg"])

    # ── PHOTO RING ────────────────────────────────────────────────────────
    photo_center = (W // 2, 310)
    draw_photo_ring(img, photo_center, outer_r=85,
                    ring_colors=t["ring_colors"], photo_img=photo_img)
    draw = ImageDraw.Draw(img)

    # ── NAME BOX ─────────────────────────────────────────────────────────
    name_display = attendee_name.upper() if attendee_name else "YOUR NAME HERE"
    f_name  = load_font(26, bold=True)
    f_label = load_font(10)
    label_text = "✏️  NAME"
    bbox_n = draw.textbbox((0, 0), name_display, font=f_name)
    nw = bbox_n[2] - bbox_n[0]
    pad_nx, pad_ny = 28, 10
    box_w = max(nw + pad_nx * 2, 220)
    nx0 = (W - box_w) // 2
    nx1 = nx0 + box_w
    ny0 = 410
    ny1 = ny0 + 58
    # shadow
    draw.rounded_rectangle([nx0 + 3, ny0 + 3, nx1 + 3, ny1 + 3],
                            radius=14, fill=t["name_shadow"])
    draw.rounded_rectangle([nx0, ny0, nx1, ny1], radius=14,
                            fill="white",
                            outline=t["name_border"], width=3)
    bbox_l = draw.textbbox((0, 0), label_text, font=f_label)
    lw = bbox_l[2] - bbox_l[0]
    draw.text(((W - lw) // 2, ny0 + 7), label_text, font=f_label, fill="#bbbbbb")
    centered_text(draw, name_display, ny0 + 22, f_name, t["name_fg"])

    # ── STICKER ROW ───────────────────────────────────────────────────────
    # Draw decorative star shapes instead of emoji
    def draw_star(d, cx, cy, r, color):
        import math
        points = []
        for i in range(10):
            angle = math.pi * i / 5 - math.pi / 2
            radius = r if i % 2 == 0 else r * 0.45
            points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
        d.polygon(points, fill=color)

    star_y = 492
    star_positions = [W//2 - 80, W//2 - 40, W//2, W//2 + 40, W//2 + 80]
    for sx in star_positions:
        draw_star(draw, sx, star_y, 10, t["sticker_col"])

    # ── DETAIL CHIPS ─────────────────────────────────────────────────────
    chip_data = [
        ("📅  Aug 13–16, 2026",      t["chip_colors"][0]),
        ("📍  All Souls' Chapel, OAU", t["chip_colors"][1]),
        ("⏰  9:00 AM Daily",          t["chip_colors"][2]),
    ]
    f_chip = load_font(11, bold=True)
    chip_y = 515
    chip_h = 28
    pad_cx = 14
    total_w = 0
    chip_widths = []
    for txt, _ in chip_data:
        b = draw.textbbox((0, 0), txt, font=f_chip)
        cw = b[2] - b[0] + pad_cx * 2
        chip_widths.append(cw)
        total_w += cw
    gap = 10
    total_w += gap * (len(chip_data) - 1)
    cx_start = (W - total_w) // 2
    for i, ((txt, col), cw) in enumerate(zip(chip_data, chip_widths)):
        cx0 = cx_start + sum(chip_widths[:i]) + gap * i
        cx1 = cx0 + cw
        draw.rounded_rectangle([cx0, chip_y, cx1, chip_y + chip_h],
                                radius=14, fill="white",
                                outline=col, width=2)
        b = draw.textbbox((0, 0), txt, font=f_chip)
        tw = b[2] - b[0]
        draw.text((cx0 + (cw - tw) // 2, chip_y + 7), txt, font=f_chip, fill=col)

    # ── SECOND CHIP ROW (venue on own line if needed) is already included ─

    # ── BOTTOM FOOTER BANNER ──────────────────────────────────────────────
    footer_top = H - 110
    draw.rectangle([0, footer_top, W, H], fill=t["banner_bot"])
    f_footer   = load_font(15, bold=True)
    f_footer_s = load_font(10, bold=True)
    centered_text(draw, "God Answers Prayers!",
                  footer_top + 18, f_footer, t["footer_fg"])
    centered_text(draw, "All Souls' Chapel  •  OAU Ile-Ife  •  #SundaySchoolCamp26",
                  footer_top + 46, f_footer_s, t["footer_sub"])
    centered_text(draw, "August 13 – 16, 2026",
                  footer_top + 66, f_footer_s, t["footer_sub"])

    # ── CONVERT TO RGB PNG ────────────────────────────────────────────────
    final = img.convert("RGB")
    buf = io.BytesIO()
    final.save(buf, format="PNG", dpi=(150, 150))
    buf.seek(0)
    return buf


# ── Quick test when run directly ─────────────────────────────────────────────
if __name__ == "__main__":
    for name, theme in THEMES.items():
        buf = generate_flyer(name, attendee_name="Favour Adeyemi")
        safe = name.replace(" ", "_").replace("–", "").replace("/", "")
        with open(f"flyer_{safe}.png", "wb") as f:
            f.write(buf.read())
        print(f"Saved: flyer_{safe}.png")
