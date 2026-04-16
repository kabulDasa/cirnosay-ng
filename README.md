# cirnosay

cowsay, but with any image rendered in your terminal.

Renders an arbitrary image file as ANSI true-color half-block art alongside a speech bubble containing your message.

```
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⠇                                                    ⠘⣿⣿⣇
⣿⣿⣿  Hello!                                              ⣿⣿⣿
⢻⣿⣿⡀                                                    ⢀⣿⣿⡟
⠘⣿⣿⣧                                                    ⣼⣿⣿⠃
⠀⠘⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⠏⠀
...
```

## Requirements

- Python 3.9+
- [Pillow](https://pillow.readthedocs.io/)

## Setup

```bash
cd cirnosay-ng
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
```

## Usage

```
cirnosay -i <image> [options] [message]
```

If `message` is omitted, text is read from stdin.

```bash
# Basic usage
cirnosay -i avatar.png "Hello, world!"

# Pipe text in
echo "Hello from stdin" | cirnosay -i avatar.png

# Multi-line stdin
cat speech.txt | cirnosay -i avatar.png
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-i`, `--image PATH` | *(required)* | Image file to use as the avatar |
| `message` | stdin | Text to display in the speech bubble |
| `-w`, `--width COLS` | `60` | Width of the rendered image in terminal columns |
| `--bubble-width COLS` | `35` | Max text width inside the speech bubble before wrapping |
| `-m`, `--mode MODE` | `blocks` | Image rendering mode (see below) |

## Image Modes

### `blocks` (default)

Renders the image as ANSI 24-bit true-color half-block art using `▀` and `▄` Unicode characters. Each terminal cell covers two pixel rows, giving 2× vertical resolution. Transparent pixels (alpha < 50%) are rendered as spaces.

```bash
cirnosay -i avatar.png "Looks great in a color terminal!"
```

### `ascii`

Renders the image as grayscale ASCII art by mapping pixel brightness to the character ramp ` .:-=+*#%@`. Works in any terminal without color support.

```bash
cirnosay -i avatar.png -m ascii "Works everywhere!"
```

## Examples

```bash
# Larger image, wider bubble
cirnosay -i avatar.png -w 80 --bubble-width 50 "This is a longer message that will wrap nicely."

# ASCII mode with custom width
cirnosay -i avatar.png -m ascii -w 40 "ASCII art!"

# Pipe a file
cat README.md | cirnosay -i avatar.png --bubble-width 60
```
