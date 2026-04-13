# Score Prep

A terminal UI app that presents measures from a musical score in random order for practice. Ensures every measure gets covered exactly once — no repeats, no gaps.

![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)

## Usage

```
uv run python score_prep.py
```

1. Enter the total number of measures in your piece
2. Press **Space** to get the next random measure
3. Play from that measure until you're comfortable
4. Repeat until all measures are covered

### Keybindings

| Key     | Action        |
|---------|---------------|
| `Space` | Next measure  |
| `R`     | Reset session |
| `Q`     | Quit          |

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12+.

```
uv sync
```
