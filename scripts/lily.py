"""Paint a red spider lily (higanbana) in code, as the source for the ASCII card.

Two blooms on bare stems, the way higanbana flower before their leaves: petals that curl
back on themselves and long stamens arching out past them, with a few fallen petals.

Returns (image, tint): an LA image whose alpha marks what is drawn and whose luminance
becomes glyph density, and an L mask marking the parts drawn in red.
"""

import math
import random
from collections.abc import Callable

from PIL import Image, ImageDraw, ImageFilter

SIZE = (600, 776)
SUPERSAMPLE = 3
SEED = 19

MAIN = ((290, 270), 1.3)      # bloom centre, scale
SECOND = ((150, 505), 0.8)
BUD = ((468, 455), 0.9)       # a closed bud on its own stem, balancing the right side
STEMS = (
    ((292, 300), (282, 450), (334, 620), (318, 776), 8),
    ((152, 522), (142, 630), (214, 700), (236, 776), 6),
    ((468, 478), (478, 600), (430, 700), (402, 776), 5),
)
FALLEN = (((520, 640), 0.35), ((96, 690), 1.9), ((530, 740), 2.8))


class _Canvas:
    """Luminance, coverage and red-tint layers, drawn together at supersampled size."""

    def __init__(self) -> None:
        big = (SIZE[0] * SUPERSAMPLE, SIZE[1] * SUPERSAMPLE)
        self.images = [Image.new("L", big, 0) for _ in range(3)]
        self.lum, self.alpha, self.tint = (ImageDraw.Draw(image) for image in self.images)

    def dot(self, x: float, y: float, r: float, lum: int, red: bool) -> None:
        box = [v * SUPERSAMPLE for v in (x - r, y - r, x + r, y + r)]
        self.lum.ellipse(box, fill=lum)
        self.alpha.ellipse(box, fill=255)
        self.tint.ellipse(box, fill=255 if red else 0)


def _stroke(canvas: _Canvas, start: tuple[float, float], angle: float, length: float, bend: float,
            width: Callable[[float], float], lum: int, red: bool = True,
            bend_power: float = 1.0, steps: int = 70) -> tuple[float, float]:
    """A curved stroke whose heading turns by `bend` radians along its length; returns its tip."""
    x, y = start
    step = length / steps
    for i in range(steps + 1):
        t = i / steps
        heading = angle + bend * t ** bend_power
        canvas.dot(x, y, width(t), lum, red)
        x += step * math.cos(heading)
        y += step * math.sin(heading)
    return x, y


def _petal_width(scale: float) -> Callable[[float], float]:
    return lambda t: scale * (3 + 9 * math.sin(math.pi * min(1.0, t * 1.15)) ** 0.7) * (1 - 0.3 * t)


def _bloom(canvas: _Canvas, centre: tuple[float, float], scale: float, rng: random.Random) -> None:
    cx, cy = centre
    petals = 13
    for i in range(petals):
        angle = i * math.tau / petals + rng.uniform(-0.18, 0.18)
        # Recurved: each petal curls back away from the centre, right-hand ones clockwise.
        curl = rng.uniform(2.6, 3.4) * (1 if math.cos(angle) >= 0 else -1)
        length = rng.uniform(118, 148) * scale
        _stroke(canvas, centre, angle, length, curl, _petal_width(scale), rng.randint(215, 240), bend_power=2.2)

    # Mostly upward, a few to each side: the stamens are what make it a spider lily.
    stamens = [rng.uniform(-math.pi + 0.3, -0.3) for _ in range(12)]
    stamens += [rng.uniform(-0.2, 0.45) for _ in range(3)]
    stamens += [rng.uniform(math.pi - 0.45, math.pi + 0.2) for _ in range(3)]
    for angle in stamens:
        bend = -0.55 if math.cos(angle) > 0 else 0.55  # arch up and outward
        length = rng.uniform(150, 200) * scale
        tip = _stroke(canvas, centre, angle, length, bend, lambda t: 3.2 * scale + 1.2, 255)
        canvas.dot(*tip, 6 * scale + 2, 255, True)

    canvas.dot(cx, cy, 12 * scale, 200, True)


def _bud(canvas: _Canvas, centre: tuple[float, float], scale: float) -> None:
    """A closed bud: three petals folded upward into a teardrop, with stamens just showing."""
    cx, cy = centre
    for bend in (-0.35, 0.0, 0.35):
        _stroke(canvas, (cx, cy + 18 * scale), -math.pi / 2 + bend * 0.4, 62 * scale, -bend,
                lambda t: scale * (4 + 8 * math.sin(math.pi * t) ** 0.8), 228, bend_power=1.4)
    for bend in (-0.3, 0.3):
        tip = _stroke(canvas, (cx, cy - 30 * scale), -math.pi / 2 + bend, 40 * scale, bend * 0.8,
                      lambda t: 2.4 * scale, 255)
        canvas.dot(*tip, 4 * scale, 255, True)


def _stem(canvas: _Canvas, p0, p1, p2, p3, width: float) -> None:
    """A cubic Bézier stem, a little thinner toward the flower."""
    for i in range(241):
        t = i / 240
        u = 1 - t
        x = u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]
        canvas.dot(x, y, width * (0.75 + 0.25 * t) / 2, 140, False)


def render() -> tuple[Image.Image, Image.Image]:
    rng = random.Random(SEED)
    canvas = _Canvas()
    for *points, width in STEMS:
        _stem(canvas, *points, width)
    for centre, scale in (SECOND, MAIN):
        _bloom(canvas, centre, scale, rng)
    _bud(canvas, *BUD)
    for start, angle in FALLEN:
        _stroke(canvas, start, angle, 42, 1.6, lambda t: 2 + 5 * math.sin(math.pi * t), 225, bend_power=1.6)

    lum, alpha, tint = (image.resize(SIZE, Image.LANCZOS) for image in canvas.images)
    return Image.merge("LA", (lum, alpha)).filter(ImageFilter.SMOOTH), tint
