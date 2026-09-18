"""One palette per GitHub theme. Everything drawn for the profile reads from here."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    name: str
    page: str      # GitHub's own background, so cards sit flush
    surface: str   # card fill
    border: str
    ink: str       # primary text
    muted: str     # labels, secondary text
    faint: str     # rules, the sparsest ASCII tone
    accent: str    # moonlight: links, highlights
    seal: str      # vermilion hanko, used once per card
    live: str      # "online" dot
    bloom: str     # the spider lily's red


DARK = Theme(
    name="dark",
    page="#0d1117",
    surface="#0b0f16",
    border="#1e2430",
    ink="#e6e9f2",
    muted="#7d8699",
    faint="#2e3545",
    accent="#a9b8ff",
    seal="#d9543f",
    live="#6fd3a1",
    bloom="#f0424f",
)

LIGHT = Theme(
    name="light",
    page="#ffffff",
    surface="#fbfbfd",
    border="#e3e6ee",
    ink="#171b26",
    muted="#667085",
    faint="#d5dae4",
    accent="#3346c8",
    seal="#c2412d",
    live="#1f8f5f",
    bloom="#c01f30",
)

THEMES = (DARK, LIGHT)

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"


def mix(a: str, b: str, t: float) -> str:
    """Blend two hex colours; t=0 gives a, t=1 gives b."""
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(ca, cb))
