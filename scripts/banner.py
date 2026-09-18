"""The header: a quiet Bleach-inspired night. Zangetsu planted on a rooftop under the moon.

Original vector art, not frames from the show. Every motion is slow on purpose: the
banner should feel still at a glance and alive if you keep looking.
"""

import random
from dataclasses import dataclass

from fontpaths import FontRef, Shaped, text_path, vertical_path

W, H = 1280, 440
SEED = 7

MOON = (905, 178, 118)  # cx, cy, r
ROOF_Y = 344            # ridge of the roof the sword stands in
SWORD_X = 874
SKY = ("#04060d", "#0a0f22", "#141b39")
SILHOUETTE = "#05070d"
RIM = "#b7c3ff"         # moonlight catching an edge
WINDOW = "#f2c47c"
PAPER = "#eceaf3"
SEAL = "#d9543f"


@dataclass(frozen=True)
class Fonts:
    serif: FontRef
    italic: FontRef
    sans: FontRef
    sans_medium: FontRef
    mono: FontRef
    brush: FontRef


def _stars(rng: random.Random) -> str:
    cx, cy, r = MOON
    out = []
    for i in range(90):
        x, y = rng.uniform(20, W - 20), rng.uniform(14, 300)
        if (x - cx) ** 2 + (y - cy) ** 2 < (r + 70) ** 2:
            continue  # the moon's glare washes these out
        size = rng.choice((0.6, 0.8, 0.8, 1.0, 1.3))
        base = rng.uniform(0.25, 0.75)
        twinkle = ""
        if i % 7 == 0:
            dur = rng.uniform(4, 9)
            twinkle = (
                f'<animate attributeName="opacity" values="{base:.2f};{base * 0.25:.2f};{base:.2f}" '
                f'dur="{dur:.1f}s" begin="-{rng.uniform(0, dur):.1f}s" repeatCount="indefinite"/>'
            )
        out.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size}" fill="#dfe4ff" opacity="{base:.2f}">{twinkle}</circle>'
        )
    return "".join(out)


def _moon() -> str:
    cx, cy, r = MOON
    craters = [(-38, -30, 26, 0.07), (30, 18, 34, 0.06), (-12, 52, 18, 0.05), (48, -44, 14, 0.05), (-58, 28, 12, 0.04)]
    marks = "".join(
        f'<circle cx="{cx + dx}" cy="{cy + dy}" r="{cr}" fill="#8d93a8" opacity="{o}"/>'
        for dx, dy, cr, o in craters
    )
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r * 2.6:.0f}" fill="url(#halo)"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#moonFace)"/>{marks}'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#moonShade)"/>'
    )


def _clouds(rng: random.Random) -> str:
    """Soft layered masses, each built from overlapping blurred ellipses."""
    out = []
    for cy, width, dur in ((142, 420, 110), (226, 320, 135), (84, 260, 160)):
        cx = rng.uniform(700, 980)
        puffs = "".join(
            f'<ellipse cx="{cx + rng.uniform(-width / 2, width / 2):.0f}" cy="{cy + rng.uniform(-6, 6):.0f}" '
            f'rx="{rng.uniform(60, 130):.0f}" ry="{rng.uniform(9, 17):.0f}"/>'
            for _ in range(6)
        )
        out.append(
            f'<g fill="#c3cbee" opacity="0.13" filter="url(#cloud)">{puffs}'
            f'<animateTransform attributeName="transform" type="translate" values="-300 0;300 0" '
            f'dur="{dur}s" begin="-{rng.uniform(0, dur):.0f}s" repeatCount="indefinite"/></g>'
        )
    return "".join(out)


def _building(x: float, w: float, top: float, style: str) -> str:
    """One rooftop silhouette: flat, gabled, or flat with a water tank or antenna."""
    if style == "gable":
        pitch = min(22.0, w * 0.22)
        return f'<path d="M{x:.0f} {H} L{x:.0f} {top + pitch:.0f} L{x + w / 2:.0f} {top:.0f} L{x + w:.0f} {top + pitch:.0f} L{x + w:.0f} {H} Z"/>'
    body = f'<rect x="{x:.0f}" y="{top:.0f}" width="{w + 1:.0f}" height="{H - top:.0f}"/>'
    if style == "tank":
        tx = x + w * 0.62
        return body + (
            f'<rect x="{tx:.0f}" y="{top - 16:.0f}" width="16" height="11" rx="2"/>'
            f'<rect x="{tx + 2:.0f}" y="{top - 6:.0f}" width="2" height="6"/><rect x="{tx + 12:.0f}" y="{top - 6:.0f}" width="2" height="6"/>'
        )
    if style == "antenna":
        ax = x + w * 0.3
        return body + f'<rect x="{ax:.0f}" y="{top - 26:.0f}" width="1.6" height="26"/><rect x="{ax - 5:.0f}" y="{top - 20:.0f}" width="12" height="1.4"/>'
    return body


def _skyline(rng: random.Random) -> str:
    """Two layers of rooftops. The left stays low so it never crowds the name."""
    far, near, windows = [], [], []
    styles = ("flat", "flat", "gable", "tank", "antenna")
    x = 0.0
    while x < W:
        w = rng.uniform(44, 110)
        top = rng.uniform(378, 404) if x < 560 else rng.uniform(306, 362)
        far.append(_building(x, w, top, rng.choice(styles)))
        for _ in range(rng.randint(0, 3) if x > 520 else rng.randint(0, 1)):
            wx, wy = x + rng.uniform(6, w - 10), top + rng.uniform(14, 60)
            if wy < H - 12:
                windows.append(
                    f'<rect x="{wx:.0f}" y="{wy:.0f}" width="4" height="6" fill="{WINDOW}" '
                    f'opacity="{rng.uniform(0.35, 0.8):.2f}"/>'
                )
        x += w
    x = 0.0
    while x < W:
        w = rng.uniform(70, 160)
        if x <= SWORD_X <= x + w:
            # The sword's roof: a gable whose ridge sits exactly where the blade goes in.
            near.append(
                f'<path d="M{SWORD_X - 70} {H} L{SWORD_X - 70} {ROOF_Y + 24} L{SWORD_X} {ROOF_Y} '
                f'L{SWORD_X + 70} {ROOF_Y + 24} L{SWORD_X + 70} {H} Z"/>'
            )
        else:
            near.append(_building(x, w, rng.uniform(400, 420), rng.choice(("flat", "flat", "tank"))))
        x += w
    # One warm window breathes, slowly, so the town feels inhabited.
    windows.append(
        f'<rect x="1046" y="352" width="4" height="6" fill="{WINDOW}" opacity="0.7">'
        '<animate attributeName="opacity" values="0.7;0.15;0.7" dur="11s" repeatCount="indefinite"/></rect>'
    )
    return (
        f'<g fill="#0a0f1f">{"".join(far)}</g>{"".join(windows)}'
        f'<g fill="{SILHOUETTE}">{"".join(near)}</g>'
    )


def _zangetsu() -> str:
    """Shikai Zangetsu, hilt up: a guardless cleaver lit from the right by the moon,
    a cloth-wrapped hilt and the white bandage streaming off it."""
    blade_len, hilt_len = 206, 78
    top = -blade_len
    # Flat spine, a hard chamfer on the edge side where the blade meets the hilt.
    blade = f"M-20 0 L-20 {top} L6 {top} L22 {top + 16} L22 0 Z"
    edge = f"M12 0 L12 {top + 6} L22 {top + 16} L22 0 Z"
    hilt_top = top - hilt_len
    hilt = f"M-5 {top} L7 {top} L7 {hilt_top} L-5 {hilt_top} Z"
    wraps = "".join(
        f'<path d="M-5 {y} L7 {y - 6} M-5 {y - 6} L7 {y}" stroke="#d8dbea" stroke-opacity="0.32" stroke-width="1.2"/>'
        for y in range(top - 4, hilt_top + 4, -9)
    )
    py = hilt_top
    ribbon_a = (
        f"M1 {py} C-34 {py - 12} -70 {py + 14} -110 {py} C-146 {py - 14} -180 {py + 6} -226 {py - 6} "
        f"L-222 {py - 3} C-176 {py + 17} -144 {py} -106 {py + 13} C-68 {py + 27} -34 {py + 2} 1 {py + 10} Z"
    )
    ribbon_b = (
        f"M1 {py} C-36 {py + 2} -70 {py - 16} -112 {py - 6} C-148 {py + 4} -182 {py - 18} -228 {py - 12} "
        f"L-224 {py - 9} C-178 {py - 7} -146 {py + 17} -108 {py + 7} C-68 {py - 3} -36 {py + 15} 1 {py + 10} Z"
    )
    return f"""
<g transform="translate({SWORD_X} {ROOF_Y}) rotate(-10)">
  <path d="{ribbon_a}" fill="#d9dcea" opacity="0.82">
    <animate attributeName="d" values="{ribbon_a};{ribbon_b};{ribbon_a}" dur="6.5s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>
  </path>
  <path d="{blade}" fill="url(#steel)"/>
  <path d="{edge}" fill="url(#edge)"/>
  <path d="M12 0 L12 {top + 10}" stroke="#8d9ad6" stroke-opacity="0.35" stroke-width="1"/>
  <path d="M22 {top + 18} L22 0" stroke="{RIM}" stroke-opacity="0.8" stroke-width="1.4"/>
  <path d="M-20 {top + 12} L-20 0" stroke="{RIM}" stroke-opacity="0.12" stroke-width="1"/>
  <path d="{hilt}" fill="#0c1020"/>
  {wraps}
</g>"""


def _reishi(rng: random.Random) -> str:
    out = []
    for _ in range(28):
        x, y = rng.uniform(560, W - 30), rng.uniform(330, 425)
        rise, drift = rng.uniform(110, 230), rng.uniform(-24, 24)
        dur = rng.uniform(9, 17)
        begin = -rng.uniform(0, dur)
        r = rng.choice((1.0, 1.3, 1.6, 2.1))
        out.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#cfd9ff" opacity="0">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{drift:.0f} {-rise:.0f}" '
            f'dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.85;0" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            "</circle>"
        )
    return f'<g filter="url(#glow)">{"".join(out)}</g>'


def _getsuga() -> str:
    """The crescent: rare and brief, so it reads as a moment rather than a loop."""
    crescent = "M0 -150 A150 150 0 0 0 0 150 A120 150 0 0 1 0 -150 Z"
    return f'''
<g opacity="0" filter="url(#glow)">
  <g transform="translate(820 190) rotate(18) scale(0.85)">
    <path d="{crescent}" fill="url(#crescent)"/>
    <animateTransform attributeName="transform" type="translate" additive="sum" values="0 0;0 0;-170 0;-170 0" keyTimes="0;0.62;0.74;1" dur="11s" begin="3s" repeatCount="indefinite"/>
  </g>
  <animate attributeName="opacity" values="0;0;0.9;0;0" keyTimes="0;0.62;0.66;0.76;1" dur="11s" begin="3s" repeatCount="indefinite"/>
</g>'''


def _placed(shape: Shaped, x: float, y: float, fill: str, opacity: float = 1.0) -> str:
    return f'<path transform="translate({x:.1f} {y:.1f})" d="{shape.d}" fill="{fill}" opacity="{opacity}"/>'


def _on_baseline(shape: Shaped, x: float, baseline: float, fill: str) -> str:
    return _placed(shape, x, baseline - shape.ascent, fill)


def _type(fonts: Fonts) -> str:
    x = 84
    label = text_path(fonts.mono, "BENGALURU  ·  INDIA", 12.5, tracking=0.28)
    name = text_path(fonts.serif, "Kruthik N", 76, tracking=-0.01)
    role = text_path(fonts.sans_medium, "AI/ML Engineer", 23)
    focus = text_path(fonts.sans, "Applied LLMs & Agentic Systems", 23)
    motto = text_path(fonts.italic, "I give language models tools, limits, and someone to answer to.", 17.5)
    return "".join((
        _on_baseline(label, x, 104, "#8a93ab"),
        _on_baseline(name, x, 190, PAPER),
        f'<rect x="{x}" y="222" width="34" height="2" fill="{SEAL}"/>',
        _on_baseline(role, x, 264, PAPER),
        _on_baseline(focus, x, 296, RIM),
        _on_baseline(motto, x, 344, "#9aa2b8"),
    ))


def _calligraphy(fonts: Fonts) -> str:
    column = vertical_path(fonts.brush, "月牙天衝", 44, gap=0.14)
    seal_char = text_path(fonts.brush, "月", 22)
    x, y = 1168, 58
    seal_y = y + column.height + 18
    return (
        f'<g transform="translate({x} {y})" fill="{PAPER}" opacity="0.9">{column.d}</g>'
        f'<rect x="{x + 7}" y="{seal_y:.0f}" width="30" height="30" rx="3" fill="{SEAL}"/>'
        + _placed(seal_char, x + 7 + (30 - seal_char.width) / 2, seal_y + 3, PAPER)
    )


def render(fonts: Fonts) -> str:
    rng = random.Random(SEED)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Kruthik N, AI/ML Engineer, Applied LLMs and Agentic Systems. A sword planted on a rooftop under a full moon.">
<defs>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{SKY[0]}"/><stop offset="0.62" stop-color="{SKY[1]}"/><stop offset="1" stop-color="{SKY[2]}"/>
  </linearGradient>
  <radialGradient id="halo"><stop offset="0" stop-color="#c9d3ff" stop-opacity="0.22"/><stop offset="0.45" stop-color="#9aa9e6" stop-opacity="0.07"/><stop offset="1" stop-color="#9aa9e6" stop-opacity="0"/></radialGradient>
  <radialGradient id="moonFace" cx="0.42" cy="0.4" r="0.7"><stop offset="0" stop-color="#fbf8ef"/><stop offset="0.7" stop-color="#e6e2d6"/><stop offset="1" stop-color="#cfcbc0"/></radialGradient>
  <radialGradient id="moonShade" cx="0.35" cy="0.3" r="0.9"><stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#1b2140" stop-opacity="0.35"/></radialGradient>
  <linearGradient id="crescent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#9fb2ff" stop-opacity="0"/></linearGradient>
  <radialGradient id="vignette" cx="0.5" cy="0.45" r="0.75"><stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.45"/></radialGradient>
  <filter id="cloud" x="-30%" y="-300%" width="160%" height="700%"><feGaussianBlur stdDeviation="9"/></filter>
  <linearGradient id="steel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#070a13"/><stop offset="0.7" stop-color="#101628"/><stop offset="1" stop-color="#1a2240"/></linearGradient>
  <linearGradient id="edge" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#1a2140"/><stop offset="1" stop-color="#3b4880"/></linearGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  {_stars(rng)}
  {_moon()}
  {_clouds(rng)}
  {_getsuga()}
  {_skyline(rng)}
  {_zangetsu()}
  {_reishi(rng)}
  <rect width="{W}" height="{H}" fill="url(#vignette)"/>
  {_type(fonts)}
  {_calligraphy(fonts)}
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="#1e2430"/>
</svg>'''
