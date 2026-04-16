from __future__ import annotations

import argparse
import sys
from itertools import zip_longest

from .bubble import make_comic_bubble
from .image import image_to_ansi, image_to_ascii

# Gap (plain spaces) between the right edge of the image and the bubble tail
_GAP = 2


def _side_by_side(image_lines: list[str], bubble_lines: list[str], img_width: int) -> list[str]:
    """Combine image and bubble lines side-by-side, bubble centred vertically."""
    n_img = len(image_lines)
    n_bub = len(bubble_lines)

    # Offset that centres the shorter block relative to the taller one
    img_start  = max(0, (n_bub - n_img) // 2)
    bub_start  = max(0, (n_img - n_bub) // 2)

    total = max(n_img, n_bub)
    gap   = " " * _GAP
    blank = " " * img_width

    result: list[str] = []
    for i in range(total):
        img_i = i - img_start
        bub_i = i - bub_start

        img_part = image_lines[img_i] if 0 <= img_i < n_img else blank
        bub_part = bubble_lines[bub_i] if 0 <= bub_i < n_bub else ""

        result.append(img_part + gap + bub_part)

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="cirnosay",
        description="cowsay, but with any image rendered in ANSI true-color.",
    )
    parser.add_argument("message", nargs="?", help="Text to say (reads stdin if omitted)")
    parser.add_argument("-i", "--image", required=True, metavar="PATH", help="Image file to use as avatar")
    parser.add_argument(
        "-w", "--width",
        type=int, default=None, metavar="COLS",
        help="Width of the rendered image in terminal columns (default: auto)",
    )
    parser.add_argument(
        "--bubble-width",
        type=int, default=35, metavar="COLS",
        help="Max text width inside the speech bubble (default: 35)",
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["blocks", "ascii"],
        default="blocks",
        help="Image rendering mode: 'blocks' (ANSI color half-blocks) or 'ascii' (grayscale ASCII) (default: blocks)",
    )

    args = parser.parse_args()

    if args.message is None:
        if sys.stdin.isatty():
            parser.error("provide a message as an argument or pipe text via stdin")
        text = sys.stdin.read().rstrip("\n")
    else:
        text = args.message

    img_width = args.width if args.width is not None else 60

    try:
        if args.mode == "ascii":
            image_lines = image_to_ascii(args.image, width=img_width)
        else:
            image_lines = image_to_ansi(args.image, width=img_width)
    except FileNotFoundError:
        parser.error(f"image not found: {args.image}")
    except Exception as exc:
        parser.error(f"could not load image: {exc}")

    bubble_lines = make_comic_bubble(text, max_width=args.bubble_width)

    for line in _side_by_side(image_lines, bubble_lines, img_width):
        print(line)


if __name__ == "__main__":
    main()
