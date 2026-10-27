"""Paint a camellia branch over a fallen bloom and a bokken, after Vagabond.

A branch arches across the top with glossy leaves, one open bloom and a bud. One head is
falling, tilted mid-air. Below, a
wooden sword lies on the ground and a whole camellia head has dropped beside it: camellias
fall in one piece, which is why they sit so often next to swordsmen.

Returns (image, tint): an LA image whose alpha marks what is drawn and whose luminance
becomes glyph density, and an L mask marking the parts drawn in red.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFilter

SIZE = (600, 776)
SUPERSAMPLE = 3
SEED = 11

BRANCH = ((-20, 150), (170, 40), (360, 210), (620, 120))
TWIGS = (((240, 120), (300, 40), 7), ((420, 180), (470, 260), 6))
LEAVES = (  # (centre, length, angle in degrees)
    ((70, 112), 96, -150), ((128, 70), 104, -70), ((205, 92), 92, 40), ((292, 52), 88, -100),
    ((262, 168), 84, 120), ((440, 172), 98, -40), ((500, 128), 86, -120), ((470, 250), 80, 70),
    ((575, 132), 82, 10),
)
BLOOM = ((338, 240), 1.3)
FALLING = ((214, 452), 0.78)  # a head mid-fall, tilted
BUD = ((302, 40), 0.55)
FALLEN = ((430, 610), 0.95)
BOKKEN = ((24, 700), (300, 700), (590, 640), 32)


class _Canvas:
    """Luminance, coverage and red-tint layers, drawn together at supersampled size."""

    def __init__(self) -> None:
        big = (SIZE[0] * SUPERSAMPLE, SIZE[1] * SUPERSAMPLE)
        self.images = [Image.new("L", big, 0) for _ in range(3)]
        self.lum, self.alpha, self.tint = (ImageDraw.Draw(image) for image in self.images)

    def polygon(self, points, lum: int, red: bool) -> None:
        pts = [(x * SUPERSAMPLE, y * SUPERSAMPLE) for x, y in points]
        self.lum.polygon(pts, fill=lum)
        self.alpha.polygon(pts, fill=255)
        self.tint.polygon(pts, fill=255 if red else 0)

    def line(self, points, width: float, lum: int, red: bool = False) -> None:
        pts = [(x * SUPERSAMPLE, y * SUPERSAMPLE) for x, y in points]
        w = max(1, round(width * SUPERSAMPLE))
        self.lum.line(pts, fill=lum, width=w, joint="curve")
        self.alpha.line(pts, fill=255, width=w, joint="curve")
        self.tint.line(pts, fill=255 if red else 0, width=w, joint="curve")

    def dot(self, x: float, y: float, r: float, lum: int, red: bool = False) -> None:
        box = [v * SUPERSAMPLE for v in (x - r, y - r, x + r, y + r)]
        self.lum.ellipse(box, fill=lum)
        self.alpha.ellipse(box, fill=255)
        self.tint.ellipse(box, fill=255 if red else 0)


def _bezier(p0, p1, p2, p3, steps: int = 120):
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        yield (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
               u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


def _oval(centre, rx: float, ry: float, angle: float, wobble: float = 0.0, rng=None, n: int = 48):
    """A rotated ellipse as a polygon, optionally with a soft irregular edge like a petal."""
    cx, cy = centre
    ca, sa = math.cos(angle), math.sin(angle)
    points = []
    for i in range(n):
        t = i / n * math.tau
        k = 1 + (wobble * math.sin(3 * t + rng.uniform(0, 0.4)) if rng else 0)
        x, y = rx * k * math.cos(t), ry * k * math.sin(t)
        points.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return points


def _leaf(canvas: _Canvas, centre, length: float, degrees: float) -> None:
    """A glossy pointed leaf: a lens shape with a bright midrib."""
    a = math.radians(degrees)
    cx, cy = centre
    half = length / 2
    tip = (cx + half * math.cos(a), cy + half * math.sin(a))
    base = (cx - half * math.cos(a), cy - half * math.sin(a))
    nx, ny = -math.sin(a), math.cos(a)
    width = length * 0.24
    edge = []
    for side in (1, -1):
        for i in range(25):
            t = i / 24 if side == 1 else 1 - i / 24
            bulge = math.sin(math.pi * t) ** 0.8 * width * side
            edge.append((base[0] + (tip[0] - base[0]) * t + nx * bulge,
                         base[1] + (tip[1] - base[1]) * t + ny * bulge))
    canvas.polygon(edge, 150, False)
    canvas.line([base, tip], 2.6, 235)


def _bloom(canvas: _Canvas, centre, scale: float, rng: random.Random) -> None:
    """Two rings of broad rounded petals around a bright cluster of stamens."""
    for ring, (count, dist, rx, ry, lum) in enumerate(((6, 46, 50, 40, 205), (5, 24, 36, 30, 235))):
        offset = rng.uniform(0, math.tau)
        for i in range(count):
            a = offset + i * math.tau / count + rng.uniform(-0.12, 0.12)
            c = (centre[0] + math.cos(a) * dist * scale, centre[1] + math.sin(a) * dist * scale)
            petal = _oval(c, rx * scale, ry * scale, a, 0.06, rng)
            canvas.polygon(petal, lum, True)
            canvas.line(petal + petal[:1], 3.6, 105 + ring * 25, True)
        # Creases between petals, so the bloom reads as petals and not a disc.
        for i in range(count):
            a = offset + (i + 0.5) * math.tau / count
            inner, outer = (18 + ring * 2) * scale, (dist + rx * 0.9) * scale
            canvas.line([(centre[0] + math.cos(a) * inner, centre[1] + math.sin(a) * inner),
                         (centre[0] + math.cos(a) * outer, centre[1] + math.sin(a) * outer)], 3.2, 95, True)
    for _ in range(26):
        a, r = rng.uniform(0, math.tau), rng.uniform(0, 17) * scale
        canvas.dot(centre[0] + math.cos(a) * r, centre[1] + math.sin(a) * r, 3.2 * scale, 255)


def _bud(canvas: _Canvas, centre, scale: float, rng: random.Random) -> None:
    canvas.polygon(_oval(centre, 34 * scale, 46 * scale, -0.3, 0.05, rng), 215, True)
    for side in (-1, 1):  # the green sepals cupping it
        canvas.polygon(_oval((centre[0] + side * 14 * scale, centre[1] + 30 * scale), 16 * scale, 24 * scale, side * 0.6), 160, False)


def _bokken(canvas: _Canvas) -> None:
    """A wooden sword lying on the ground: a long gentle curve, a rounded tip, a darker grip."""
    p0, mid, p3, width = BOKKEN
    spine = list(_bezier(p0, mid, mid, p3, 160))
    top, bottom = [], []
    for i, (x, y) in enumerate(spine):
        j = min(i + 1, len(spine) - 1)
        dx, dy = spine[j][0] - spine[max(j - 1, 0)][0], spine[j][1] - spine[max(j - 1, 0)][1]
        n = math.hypot(dx, dy) or 1
        w = width / 2 * (1 - 0.35 * (i / len(spine)) ** 3)
        top.append((x - dy / n * w, y + dx / n * w))
        bottom.append((x + dy / n * w, y - dx / n * w))
    canvas.polygon(top + bottom[::-1], 190, False)
    canvas.line(top, 2.4, 245)
    grip = spine[:45]
    canvas.line(grip, width * 0.9, 120)
    for x, y in grip[4::7]:  # the wrap on the grip
        canvas.line([(x - 7, y - 10), (x + 7, y + 10)], 2.4, 230)


def render() -> tuple[Image.Image, Image.Image]:
    rng = random.Random(SEED)
    canvas = _Canvas()
    _bokken(canvas)
    canvas.line(list(_bezier(*BRANCH)), 10, 175)
    for start, end, width in TWIGS:
        canvas.line([start, ((start[0] + end[0]) / 2 + 12, (start[1] + end[1]) / 2), end], width, 175)
    for centre, length, angle in LEAVES:
        _leaf(canvas, centre, length, angle)
    _bud(canvas, *BUD, rng)
    _bloom(canvas, *BLOOM, rng)
    _bloom(canvas, *FALLING, rng)
    _bloom(canvas, *FALLEN, rng)
    lum, alpha, tint = (image.resize(SIZE, Image.LANCZOS) for image in canvas.images)
    return Image.merge("LA", (lum, alpha)).filter(ImageFilter.SMOOTH), tint


if __name__ == "__main__":
    import sys

    image, tint = render()
    preview = Image.new("RGB", SIZE, "white")
    preview.paste(Image.merge("RGB", [image.getchannel("L")] * 3), mask=image.getchannel("A"))
    preview.paste(Image.new("RGB", SIZE, (210, 40, 40)), mask=Image.eval(tint, lambda v: v if v > 128 else 0))
    preview.save(sys.argv[1] if len(sys.argv) > 1 else "camellia-preview.png")
