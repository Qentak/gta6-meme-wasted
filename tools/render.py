from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1024, 1024
SCENE = "art/scene.jpg"
FONT_PATH = "fonts/Anton-Regular.ttf"
OUTPUT = "meme.png"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GTA_RED = (205, 32, 44)
MAGENTA = (197, 29, 133)
ENGRAVE = (34, 34, 40)
ENGRAVE_LIGHT = (200, 200, 205)

img = Image.open(SCENE).convert("RGB")
assert img.size == (WIDTH, HEIGHT), img.size
draw = ImageDraw.Draw(img)
measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def fit(text, max_size, max_width):
    size = max_size
    while size > 0:
        f = font(size)
        left, _, right, _ = measure.textbbox((0, 0), text, font=f)
        if right - left <= max_width:
            return size
        size -= 1
    raise ValueError(f"cannot fit {text!r} within {max_width}px")


def draw_outlined(draw, xy, text, font, fill, stroke):
    if isinstance(xy, (int, float)):
        xy = (WIDTH // 2, xy)
    draw.text(
        xy,
        text,
        font=font,
        fill=fill,
        anchor="mt",
        stroke_width=stroke,
        stroke_fill=BLACK,
    )


def draw_runs(draw, runs, y, fnt, stroke):
    widths = [draw.textlength(text, font=fnt) for text, _ in runs]
    x = (WIDTH - sum(widths)) / 2
    for (text, colour), width in zip(runs, widths):
        draw.text(
            (x, y),
            text,
            font=fnt,
            fill=colour,
            anchor="lt",
            stroke_width=stroke,
            stroke_fill=BLACK,
        )
        x += width


# 1. Top band.
line_a = "WAITED 13 YEARS FOR GTA 6"
size_a = fit(line_a, 62, 940)
draw_outlined(draw, 14, line_a, font(size_a), WHITE, 4)

line_b = "WASTED"
size_b = fit(line_b, 118, 700)
draw_outlined(draw, 78, line_b, font(size_b), GTA_RED, 7)

# 2. Gravestone engraving.
engraving = [
    ("R.I.P.", 46, 566),
    ("GTA FAN", 36, 620),
    ("2013\u20132026", 30, 664),
]
engraving_sizes = []
for text, max_size, y in engraving:
    size = fit(text, max_size, 140)
    engraving_sizes.append(size)
    f = font(size)
    draw.text((675 + 1, y + 1), text, font=f, fill=ENGRAVE_LIGHT, anchor="mt")
    draw.text((675, y), text, font=f, fill=ENGRAVE, anchor="mt")

# 3. Bottom band.
line_c = "CAME BACK FOR LAUNCH DAY ANYWAY."
size_c = fit(line_c, 54, 950)
draw_outlined(draw, 828, line_c, font(size_c), WHITE, 4)

runs_d = [
    ("MY AI AGENT PAID FOR IT WITH ", WHITE),
    ("make.fun", MAGENTA),
    (" BOUNTIES", WHITE),
]
size_d = 46
while size_d > 0:
    f_d = font(size_d)
    if sum(draw.textlength(text, font=f_d) for text, _ in runs_d) <= 950:
        break
    size_d -= 1
if size_d == 0:
    raise ValueError("bottom run line cannot fit within 950px")
draw_runs(draw, runs_d, 896, f_d, 4)

size_pitch = fit("YOU AND YOUR AI AGENT CAN EARN REAL MONEY TOO.", 36, 900)
draw_outlined(
    draw,
    962,
    "YOU AND YOUR AI AGENT CAN EARN REAL MONEY TOO.",
    font(size_pitch),
    (225, 196, 240),
    3,
)

# 4. Save and report.
img.save(OUTPUT, optimize=True)
print(f"{OUTPUT} {img.width}x{img.height} {img.mode}")
print(
    "font sizes: "
    f"A={size_a}, WASTED={size_b}, "
    f"R.I.P.={engraving_sizes[0]}, GTA FAN={engraving_sizes[1]}, "
    f"years={engraving_sizes[2]}, C={size_c}, D={size_d}, pitch={size_pitch}"
)
