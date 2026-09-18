"""The terminal cards: whoami, the four projects, principles, section headers and links."""

from html import escape

from banner import Fonts
from content import PRINCIPLES, STATUS, WHOAMI, Project
from fontpaths import Shaped, text_path
from theme import MONO, SANS, Theme

CARD_W = 860
PAD = 40
MONO_ADVANCE = 0.6  # JetBrains Mono / Menlo advance width, in ems
# Cards are drawn at 860 wide and shown at about half that, so text is sized for 2x.
ROW_SIZE = 19


def _path(shape: Shaped, x: float, baseline: float, fill: str) -> str:
    return f'<path transform="translate({x:.1f} {baseline - shape.ascent:.1f})" d="{shape.d}" fill="{fill}"/>'


def _text(x: float, y: float, body: str, fill: str, size: float = 15, family: str = MONO,
          anchor: str = "start", extra: str = "") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" xml:space="preserve"{extra}>{body}</text>'
    )


def _svg(width: float, height: float, label: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-label="{escape(label)}">{body}</svg>'
    )


def _chrome(theme: Theme, width: int, height: int, title: str, right: str) -> str:
    return (
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="14" fill="{theme.surface}" stroke="{theme.border}"/>'
        f'<line x1="1" y1="44" x2="{width - 1}" y2="44" stroke="{theme.border}"/>'
        f'<rect x="22" y="17" width="10" height="10" rx="2" fill="{theme.seal}"/>'
        + _text(42, 27, f'kruthik@github <tspan fill="{theme.faint}">·</tspan> {escape(title)}', theme.muted, 12.5)
        + _text(width - 22, 27, escape(right), theme.muted, 12.5, anchor="end")
    )


def _fade_in(delay: float) -> str:
    return (
        f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay:.2f}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="-6 0" to="0 0" dur="0.5s" '
        f'begin="{delay:.2f}s" fill="freeze"/>'
    )


# ---- whoami ----------------------------------------------------------------------------

def _rows(theme: Theme, top: float) -> tuple[list[str], float, float]:
    """The key/value groups, each row fading in after the last. Returns (svg, next y, next delay)."""
    body, y, delay = [], top, 0.35
    for group_index, group in enumerate(WHOAMI):
        body.append(f'<line x1="{PAD}" y1="{y - 22:.0f}" x2="{CARD_W - PAD}" y2="{y - 22:.0f}" stroke="{theme.border}"/>')
        y += 14
        for key, value in group:
            row = _text(PAD, y, escape(key), theme.muted, ROW_SIZE) + _text(PAD + 150, y, escape(value), theme.ink, ROW_SIZE)
            body.append(f'<g opacity="0">{row}{_fade_in(delay)}</g>')
            y += 37
            delay += 0.07
        if group_index < len(WHOAMI) - 1:
            y += 20
    return body, y, delay


def whoami(theme: Theme, fonts: Fonts, footer_left: str, footer_right: str) -> str:
    height = 1000
    name = text_path(fonts.serif, "Kruthik N", 56)
    body = [
        _chrome(theme, CARD_W, height, "~/whoami", "zsh"),
        _text(PAD, 94, f'<tspan fill="{theme.accent}">$</tspan> whoami', theme.ink, ROW_SIZE),
        _path(name, PAD, 162, theme.ink),
    ]
    rows, y, delay = _rows(theme, 222)
    body.extend(rows)

    y += 16
    status = (
        f'<circle cx="{PAD + 6}" cy="{y - 5:.0f}" r="5" fill="{theme.live}">'
        '<animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite"/></circle>'
        + _text(PAD + 22, y, escape(STATUS), theme.live, ROW_SIZE)
    )
    body.append(f'<g opacity="0">{status}{_fade_in(delay)}</g>')
    prompt_y = y + 44
    dollar = _text(PAD, prompt_y, "$", theme.accent, ROW_SIZE)
    cursor = (
        f'<rect x="{PAD + 22}" y="{prompt_y - 17:.0f}" width="11" height="22" fill="{theme.ink}">'
        '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>'
    )
    body.append(f'<g opacity="0">{dollar}{cursor}{_fade_in(delay + 0.1)}</g>')

    body.append(f'<line x1="22" y1="{height - 44}" x2="{CARD_W - 22}" y2="{height - 44}" stroke="{theme.border}"/>')
    body.append(_text(22, height - 18, escape(footer_left), theme.muted, 12))
    body.append(_text(CARD_W - 22, height - 18, escape(footer_right), theme.muted, 12, anchor="end"))
    return _svg(CARD_W, height, "Kruthik N: AI/ML Engineer, Applied LLMs and Agentic Systems", "".join(body))


# ---- project cards ---------------------------------------------------------------------

def _draw_in(path: str, stroke: str, delay: float, width: float = 1.6) -> str:
    """A stroke that draws itself once, then stays."""
    return (
        f'<path d="{path}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" '
        f'stroke-dasharray="400" stroke-dashoffset="400">'
        f'<animate attributeName="stroke-dashoffset" from="400" to="0" dur="1.4s" begin="{delay:.2f}s" fill="freeze"/></path>'
    )


def _node(x: float, y: float, fill: str, r: float = 5) -> str:
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'


def _diagram(slug: str, theme: Theme) -> str:
    """A small signature drawing per project, about 170 x 90."""
    accent, human, quiet = theme.accent, theme.seal, theme.muted
    if slug == "zentinel":  # a plan graph with one human checkpoint
        edges = ("M8 45 L70 12", "M8 45 L70 45", "M8 45 L70 78", "M70 12 L140 30", "M70 45 L140 30", "M70 78 L140 66")
        body = "".join(_draw_in(e, quiet, 0.5 + i * 0.08, 1.3) for i, e in enumerate(edges))
        nodes = ((8, 45, accent, 6), (70, 12, accent, 5), (70, 45, accent, 5), (70, 78, accent, 5), (140, 30, accent, 5), (140, 66, human, 6))
        return body + "".join(_node(x, y, c, r) for x, y, c, r in nodes)
    if slug == "recon":  # three sources, rules, a gate, two outcomes
        body = "".join(_draw_in(f"M4 {y} C40 {y} 50 45 78 45", quiet, 0.5 + i * 0.1, 1.3) for i, y in enumerate((12, 45, 78)))
        body += _draw_in("M92 45 L150 22", accent, 0.9) + _draw_in("M92 45 L150 70", human, 1.0)
        return body + f'<rect x="80" y="26" width="10" height="38" rx="2" fill="{accent}"/>' + _node(156, 20, accent) + _node(156, 72, human)
    if slug == "stacksense":  # two rankings fused into one
        bars = []
        for i, (left, middle, fused) in enumerate(((44, 36, 60), (30, 46, 52), (38, 22, 44), (18, 30, 34))):
            y = 10 + i * 20
            bars.append(f'<rect x="0" y="{y}" width="{left}" height="8" rx="2" fill="{quiet}" opacity="0.5"/>')
            bars.append(f'<rect x="54" y="{y}" width="{middle}" height="8" rx="2" fill="{quiet}" opacity="0.5"/>')
            bars.append(
                f'<rect x="116" y="{y}" width="{fused}" height="8" rx="2" fill="{accent}">'
                f'<animate attributeName="width" from="0" to="{fused}" dur="0.9s" begin="{0.6 + i * 0.1:.1f}s" fill="freeze"/></rect>'
            )
        return "".join(bars) + f'<line x1="104" y1="4" x2="104" y2="86" stroke="{theme.border}"/>'
    # alphaforge: an equity curve against the buy-and-hold line it didn't beat
    curve = "M0 70 C18 64 26 72 40 58 S62 50 74 54 S96 30 110 36 S140 18 168 22"
    baseline = f'<path d="M0 72 L168 14" fill="none" stroke="{quiet}" stroke-width="1.2" stroke-dasharray="4 5"/>'
    return baseline + _draw_in(curve, accent, 0.5, 2) + _node(168, 22, accent, 4)


def _chip(x: float, y: float, label: str, theme: Theme) -> tuple[str, float]:
    width = len(label) * 15 * MONO_ADVANCE + 28
    svg = (
        f'<rect x="{x:.1f}" y="{y}" width="{width:.1f}" height="34" rx="17" fill="none" stroke="{theme.border}"/>'
        + _text(x + width / 2, y + 22.5, escape(label), theme.muted, 15, anchor="middle")
    )
    return svg, width


def project(theme: Theme, fonts: Fonts, index: int, p: Project) -> str:
    height = 480
    name = text_path(fonts.serif, p.name, 46)
    metric = text_path(fonts.serif, p.metric, 62)
    if p.live:
        badge = (
            f'<circle cx="{CARD_W - PAD - 56}" cy="43" r="5" fill="{theme.live}"/>'
            + _text(CARD_W - PAD, 48, "LIVE", theme.live, 14.5, anchor="end", extra=' letter-spacing="2"')
        )
    else:
        badge = _text(CARD_W - PAD, 48, "SOURCE", theme.muted, 14.5, anchor="end", extra=' letter-spacing="2"')
    body = [
        f'<rect x="0.5" y="0.5" width="{CARD_W - 1}" height="{height - 1}" rx="14" fill="{theme.surface}" stroke="{theme.border}"/>',
        _text(PAD, 48, f"{index:02d}  ·  {escape(p.kind.upper())}", theme.muted, 14.5, extra=' letter-spacing="1.5"'),
        badge,
        _path(name, PAD, 114, theme.ink),
        _text(PAD, 146, escape(p.context), theme.muted, 16),
        f'<g transform="translate({CARD_W - PAD - 172} 72)">{_diagram(p.slug, theme)}</g>',
    ]
    body += [_text(PAD, 194 + i * 31, escape(line), theme.ink, 22, SANS, extra=' opacity="0.86"') for i, line in enumerate(p.lines)]
    body.append(f'<line x1="{PAD}" y1="296" x2="{CARD_W - PAD}" y2="296" stroke="{theme.border}"/>')
    body.append(_path(metric, PAD, 372, theme.accent))
    label_x = PAD + metric.width + 22
    body += [_text(label_x, 342 + i * 27, escape(line), theme.muted, 19, SANS) for i, line in enumerate(p.metric_label)]
    x = PAD
    for label in p.stack:
        chip, width = _chip(x, 408, label, theme)
        body.append(chip)
        x += width + 10
    return _svg(CARD_W, height, f"{p.name}: {p.kind}", "".join(body))


# ---- principles, headers, links -------------------------------------------------------

WIDE = 1740


def principles(theme: Theme, fonts: Fonts) -> str:
    height = 230
    column = (WIDE - 2 * PAD) / 3
    body = [f'<rect x="0.5" y="0.5" width="{WIDE - 1}" height="{height - 1}" rx="14" fill="{theme.surface}" stroke="{theme.border}"/>']
    for i, (title, evidence) in enumerate(PRINCIPLES):
        x = PAD + i * column + (28 if i else 0)
        if i:
            body.append(f'<line x1="{x - 28:.0f}" y1="40" x2="{x - 28:.0f}" y2="{height - 40}" stroke="{theme.border}"/>')
        numeral = text_path(fonts.brush, "一二三"[i], 44)
        heading = text_path(fonts.serif, title, 40)
        group = (
            _path(numeral, x, 104, theme.seal) + _path(heading, x + 64, 100, theme.ink)
            + _text(x, 164, escape(evidence), theme.muted, 23, SANS)
        )
        body.append(f'<g opacity="0">{group}{_fade_in(0.3 + i * 0.25)}</g>')
    return _svg(WIDE, height, "How I build: " + "; ".join(t for t, _ in PRINCIPLES), "".join(body))


def header(theme: Theme, command: str) -> str:
    height, size = 70, 26
    prompt = "kruthik@github ~ $ "
    text_end = (len(prompt) + len(command)) * size * MONO_ADVANCE
    body = (
        _text(0, 44, f'<tspan fill="{theme.muted}">kruthik@github</tspan> <tspan fill="{theme.accent}">~ $</tspan> '
              f'{escape(command)}', theme.ink, size)
        + f'<line x1="{text_end + 28:.0f}" y1="36" x2="{WIDE}" y2="36" stroke="{theme.border}"/>'
    )
    return _svg(WIDE, height, f"$ {command}", body)


def link_button(theme: Theme, label: str) -> str:
    width, height = 300, 72
    body = (
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="36" fill="{theme.surface}" stroke="{theme.border}"/>'
        + _text(34, 45, escape(label), theme.ink, 21, SANS)
        + _text(width - 32, 45, "↗", theme.accent, 22, SANS, anchor="end")
    )
    return _svg(width, height, label, body)
