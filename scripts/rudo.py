"""The ASCII card's source: Rudo falling into the Abyss, from Gachiakuta (Kei Urana).

art/rudo.jpg is a grayscale crop of the panel. The sun flare behind him is the red tint.

Returns (image, tint) in the shape ascii_card expects: an LA image whose luminance becomes
glyph density, and an L mask marking the parts drawn in red.
"""

from pathlib import Path

import math

from PIL import Image, ImageDraw, ImageFilter, ImageOps

SOURCE = Path(__file__).parent / "art" / "rudo.jpg"
SUN = (98, 367)       # flare centre in the crop
SUN_RADIUS = 60
# Rudo stays crisp and dense; the sky and clouds around him thin out to texture.
FIGURE = (
    (300, 290), (330, 242), (362, 238), (382, 280), (420, 330), (458, 345), (470, 298),
    (490, 258), (532, 258), (548, 300), (562, 362), (546, 422), (502, 470), (472, 540),
    (462, 578), (418, 578), (388, 530), (328, 482), (338, 450), (368, 440), (330, 362),
)
ROPE = ((420, 128), (430, 190), (412, 270))
BACKGROUND_GAMMA = 2.0
BACKGROUND_LEVEL = 0.5
FIGURE_GAMMA = 0.75  # lifts Rudo's mid-tones so the figure is the densest thing in the card
SUN_RAYS = 9   # only the bright flare inside that radius turns red


def render() -> tuple[Image.Image, Image.Image]:
    raw = Image.open(SOURCE).convert("L")
    figure = Image.new("L", raw.size, 0)
    draw = ImageDraw.Draw(figure)
    draw.polygon(FIGURE, fill=255)
    draw.line(ROPE, fill=255, width=14, joint="curve")
    figure = figure.filter(ImageFilter.GaussianBlur(6))
    background = raw.filter(ImageFilter.GaussianBlur(1.6)).point(
        lambda v: round(255 * BACKGROUND_LEVEL * (v / 255) ** BACKGROUND_GAMMA))
    rudo = ImageOps.autocontrast(raw, cutoff=2).point(lambda v: round(255 * (v / 255) ** FIGURE_GAMMA))
    lum = Image.composite(rudo, background, figure)
    alpha = Image.new("L", lum.size, 255)

    # The sun flare, drawn as a clean burst so the red reads as one shape.
    tint = Image.new("L", raw.size, 0)
    draw_lum, draw_tint = ImageDraw.Draw(lum), ImageDraw.Draw(tint)
    x, y = SUN
    for i in range(SUN_RAYS):
        a = i * math.tau / SUN_RAYS + 0.2
        length = SUN_RADIUS * (1.6 if i % 2 else 1.0)
        ray = [(x, y), (x + math.cos(a) * length, y + math.sin(a) * length)]
        draw_lum.line(ray, fill=230, width=5)
        draw_tint.line(ray, fill=255, width=5)
    for draw in (draw_lum, draw_tint):
        draw.ellipse((x - 26, y - 26, x + 26, y + 26), fill=255)
    return Image.merge("LA", (lum, alpha)), tint
