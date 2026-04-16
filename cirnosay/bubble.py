from __future__ import annotations

import textwrap

_PAD = "    "  # 4-space left indent so the tail can step leftward


def make_comic_bubble(text: str, max_width: int = 35) -> list[str]:
    """
    Rounded speech bubble with a stepped tail pointing left toward the image.

    Structure (W = inner + 6, min 20):

        ╭─────────────────────────╮
        │                         │
        │  Hello world!           │
        │                         │
        ╰─────────────────────────╯
       ─╯
    """
    wrapped: list[str] = []
    for para in text.splitlines():
        lines = textwrap.wrap(para, max_width)
        wrapped.extend(lines if lines else [""])
    if not wrapped:
        wrapped = [""]

    inner = max(len(l) for l in wrapped)
    # W = inner + 6  (1 border + 2 spaces each side)
    W = max(inner + 6, 20)
    inner = W - 6  # recalc in case W was bumped

    result: list[str] = []

    # ── Top border ────────────────────────────────────────────────────────────
    result.append(_PAD + "╭" + "─" * (W - 2) + "╮")

    # ── Content rows ──────────────────────────────────────────────────────────
    blank = _PAD + "│" + " " * (W - 2) + "│"
    result.append(blank)
    for line in wrapped:
        result.append(_PAD + "│  " + line.ljust(inner) + "  │")
    result.append(blank)

    # ── Bottom border (clean, no notch — tail is separate) ────────────────────
    result.append(_PAD + "╰" + "─" * (W - 2) + "╯")

    # ── Stepped tail, each row 2 cols left of the previous ────────────────────
    # Bubble body starts at col 4 (_PAD), tail steps: col 2 → col 0
    result.append("  ╭─╯")
    result.append("──╯")

    return result
