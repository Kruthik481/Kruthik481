"""Paint utility poles and power lines at dusk, the recurring image of Serial Experiments Lain.

Three poles recede toward the right, their wires sagging between cross-arms. A low sun sits
behind them, and the poles cast long shadows across the road. In Lain, shadows are pale and
full of red spots, so these are too. That detail and the sun form the red tint mask.

Returns (image, tint): an LA image whose alpha marks what is drawn and whose luminance
becomes glyph density, and an L mask marking the parts drawn in red.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFilter

SIZE = (600, 776)
SUPERSAMPLE = 3
SEED = 7
HORIZON = 600
SUN = ((452, 290), 92)

# (x, top, bottom, width, arm half-length); nearest pole first.
POLES = (
    (150, 30, 776, 34, 104),
    (420, 240, 668, 20, 60),
    (550, 345, 628, 12, 34),
)
ARM_OFFSETS = (0.05, 0.13)  # cross-arms, as a fraction of pole height below the top
SAG = (52, 26)              # how far wires dip between near-mid and mid-far poles


class _Canvas:
    """Luminance, coverage and red-tint layers, drawn together at supersampled size."""

    def __init__(self) -> None:
        big = (SIZE[0] * SUPERSAMPLE, SIZE[1] * SUPERSAMPLE)
        self.images = [Image.new("L", big, 0) for _ in range(3)]
        self.lum, self.alpha, self.tint = (ImageDraw.Draw(image) for image in self.images)

    def _scale(self, points):
        return [(x * SUPERSAMPLE, y * SUPERSAMPLE) for x, y in points]

    def line(self, points, width: float, lum: int, red: bool = False) -> None:
        pts = self._scale(points)
        w = max(1, round(width * SUPERSAMPLE))
        self.lum.line(pts, fill=lum, width=w, joint="curve")
        self.alpha.line(pts, fill=255, width=w, joint="curve")
        self.tint.line(pts, fill=255 if red else 0, width=w, joint="curve")

    def polygon(self, points, lum: int, red: bool = False) -> None:
        pts = self._scale(points)
        self.lum.polygon(pts, fill=lum)
        self.alpha.polygon(pts, fill=255)
        self.tint.polygon(pts, fill=255 if red else 0)

    def dot(self, x: float, y: float, r: float, lum: int, red: bool = False) -> None:
        box = [v * SUPERSAMPLE for v in (x - r, y - r, x + r, y + r)]
        self.lum.ellipse(box, fill=lum)
        self.alpha.ellipse(box, fill=255)
        self.tint.ellipse(box, fill=255 if red else 0)


def _arms(pole) -> list[tuple[float, float, float]]:
    """(y, left end, right end) for each cross-arm of a pole."""
    x, top, bottom, _, half = pole
    height = bottom - top
    return [(top + f * height, x - half, x + half) for f in ARM_OFFSETS]


def _catenary(a: tuple[float, float], b: tuple[float, float], sag: float, steps: int = 60):
    """A wire hanging between two points: a straight chord plus a parabolic dip."""
    return [
        (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t + sag * 4 * t * (1 - t))
        for t in (i / steps for i in range(steps + 1))
    ]


def _sun(canvas: _Canvas) -> None:
    (cx, cy), r = SUN
    canvas.dot(cx, cy, r, 170, red=True)
    canvas.dot(cx, cy, r * 0.7, 225, red=True)


def _ground(canvas: _Canvas, rng: random.Random) -> None:
    """A faint road surface, then each pole's long shadow with Lain's red spots inside it."""
    for y in range(HORIZON + 10, SIZE[1], 22):
        canvas.line([(0, y), (SIZE[0], y)], 3.2, 95)
    for x, _, bottom, width, _ in POLES:
        length = (bottom - HORIZON + 60) * 3.2
        foot = (x, bottom)
        tip = (x - length * 0.92, bottom + length * 0.18)
        spread = width * 1.6
        canvas.polygon([(foot[0] - spread, foot[1] - spread * 0.4), (foot[0] + spread, foot[1] + spread * 0.4),
                        (tip[0] + spread * 2, tip[1] + spread), (tip[0] - spread * 2, tip[1] - spread)], 150)
        for _ in range(int(length / 18)):
            t = rng.uniform(0.08, 0.95)
            px = foot[0] + (tip[0] - foot[0]) * t + rng.uniform(-spread, spread)
            py = foot[1] + (tip[1] - foot[1]) * t + rng.uniform(-spread * 0.5, spread * 0.5)
            canvas.dot(px, py, rng.uniform(4.5, 7.5), 255, red=True)


def _poles(canvas: _Canvas) -> None:
    for pole in POLES:
        x, top, bottom, width, _ = pole
        canvas.polygon([(x - width / 2, top), (x + width / 2, top),
                        (x + width * 0.62, bottom), (x - width * 0.62, bottom)], 235)
        for y, left, right in _arms(pole):
            canvas.line([(left, y), (right, y)], max(5, width * 0.4), 225)
            for ix in (left + 6, x - (x - left) * 0.45, x + (right - x) * 0.45, right - 6):
                canvas.dot(ix, y - width * 0.45, width * 0.28 + 1, 255)
    near = POLES[0]
    x, top, bottom, width, _ = near
    # A transformer drum on the nearest pole, under its arms.
    drum_top = top + 0.2 * (bottom - top)
    canvas.polygon([(x + width * 0.6, drum_top), (x + width * 2.6, drum_top),
                    (x + width * 2.6, drum_top + 70), (x + width * 0.6, drum_top + 70)], 200)
    # A step bolt ladder up the near pole.
    for y in range(int(drum_top + 110), int(bottom - 60), 26):
        side = 1 if (y // 26) % 2 else -1
        canvas.line([(x, y), (x + side * width * 0.95, y)], 2.4, 210)


def _wires(canvas: _Canvas) -> None:
    arms = [_arms(pole) for pole in POLES]
    ends = lambda arm: (arm[1] + 6, arm[2] - 6)  # noqa: E731 - outer insulators
    for level in range(len(ARM_OFFSETS)):
        for side in (0, 1):
            points = [(ends(a[level])[side], a[level][0] - 4) for a in arms]
            for (a, b), sag in zip(zip(points, points[1:]), SAG):
                canvas.line(_catenary(a, b, sag), 6.5, 250)
            # Wires run on out of frame to the left and right, as they do in every establishing shot.
            first, last = points[0], points[-1]
            canvas.line(_catenary((-20, first[1] - 30), first, 30), 7, 250)
            canvas.line(_catenary(last, (SIZE[0] + 20, last[1] + 18), 8), 5, 250)


def render() -> tuple[Image.Image, Image.Image]:
    rng = random.Random(SEED)
    canvas = _Canvas()
    _sun(canvas)
    _ground(canvas, rng)
    _poles(canvas)
    _wires(canvas)
    lum, alpha, tint = (image.resize(SIZE, Image.LANCZOS) for image in canvas.images)
    return Image.merge("LA", (lum, alpha)).filter(ImageFilter.SMOOTH), tint


if __name__ == "__main__":
    image, tint = render()
    preview = Image.new("RGB", SIZE, "white")
    preview.paste(Image.merge("RGB", [image.getchannel("L")] * 3), mask=image.getchannel("A"))
    red = Image.new("RGB", SIZE, (210, 40, 40))
    preview.paste(red, mask=Image.eval(tint, lambda v: v if v > 128 else 0))
    import sys
    preview.save(sys.argv[1] if len(sys.argv) > 1 else "wired-preview.png")
