from __future__ import annotations

from PIL import Image

RESET = "\033[0m"

# ASCII ramp, dark → light (10 levels)
_RAMP = " .:-=+*#%@"


def _fg(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"


def _bg(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"


def image_to_ansi(path: str, width: int = 40) -> list[str]:
    """Convert an image file to a list of ANSI half-block art strings."""
    img = Image.open(path).convert("RGBA")

    # Terminal chars are ~2× taller than wide, but each half-block covers
    # 2 pixel rows per char row — the two factors cancel out exactly.
    aspect = img.height / img.width
    height = int(width * aspect)
    if height % 2 != 0:
        height += 1

    img = img.resize((width, height), Image.LANCZOS)
    pixels = img.load()

    lines = []
    for y in range(0, height, 2):
        line = ""
        for x in range(width):
            tr, tg, tb, ta = pixels[x, y]
            br, bg, bb, ba = pixels[x, y + 1] if y + 1 < height else (0, 0, 0, 0)

            # Treat pixels below 50% alpha as transparent to avoid the
            # coloured halo that LANCZOS resampling introduces at edges.
            top_vis = ta >= 128
            bot_vis = ba >= 128

            if not top_vis and not bot_vis:
                line += " "
            elif not top_vis:
                line += _fg(br, bg, bb) + "▄" + RESET
            elif not bot_vis:
                line += _fg(tr, tg, tb) + "▀" + RESET
            else:
                line += _bg(tr, tg, tb) + _fg(br, bg, bb) + "▄" + RESET

        lines.append(line)

    return lines


def image_to_ascii(path: str, width: int = 40) -> list[str]:
    """Convert an image file to ASCII dot art (grayscale brightness → chars)."""
    img = Image.open(path).convert("L")  # grayscale

    # Terminal chars are ~2× taller than wide, so halve the height to preserve
    # the apparent aspect ratio.
    aspect = img.height / img.width
    height = max(1, int(width * aspect / 2))

    img = img.resize((width, height), Image.LANCZOS)
    pixels = img.load()

    lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            brightness = pixels[x, y]  # 0–255
            idx = int(brightness / 255 * (len(_RAMP) - 1))
            line += _RAMP[idx]
        lines.append(line)

    return lines
