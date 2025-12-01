# utils_image.py
import hashlib
import urllib.parse
from textwrap import wrap


def _color_from_hash(prompt: str) -> tuple[int, int, int]:
    """Deterministically derive an RGB color from the prompt."""
    h = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    return r, g, b


def _build_svg(prompt: str, width: int = 1024, height: int = 576) -> str:
    """
    Build a tiny SVG (<5KB) that symbolically represents the paragraph:
    - gradient-ish background derived from text hash
    - a few simple shapes
    - very short text label
    """
    r, g, b = _color_from_hash(prompt)
    bg_color = f"rgb({r},{g},{b})"
    accent_color = f"rgb({255 - r},{255 - g},{255 - b})"

    # Short descriptive label
    text = " ".join(prompt.strip().split())
    max_chars = 60
    if len(text) > max_chars:
        text = text[: max_chars - 3] + "..."

    # Crude multi-line wrapping for 2–3 lines max
    lines = wrap(text, width=30)[:3]

    # Basic SVG with a rect, circle, and up to 3 lines of text
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'  <rect width="100%" height="100%" fill="{bg_color}" />',
        f'  <circle cx="{width//2}" cy="{height//3}" r="{min(width, height)//6}" fill="{accent_color}" fill-opacity="0.35" />',
    ]

    start_y = height * 2 // 3
    for idx, line in enumerate(lines):
        y = start_y + idx * 28
        svg_lines.append(
            f'  <text x="50%" y="{y}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="20" fill="white">{line}</text>'
        )

    svg_lines.append("</svg>")
    svg = "\n".join(svg_lines)
    # Safety: ensure it's small (truncate if ever larger, though it's unlikely)
    return svg[:4096]


async def generate_image(prompt: str, dest_path: str | None = None) -> str:
    """
    Generate a tiny, lightweight SVG placeholder encoded as a data: URL that
    symbolically represents the scene. No filesystem, no GPU.
    """
    svg = _build_svg(prompt)
    encoded = urllib.parse.quote(svg)
    return f"data:image/svg+xml;utf8,{encoded}"
