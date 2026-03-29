# Sprite Generator

Procedural character sprite generator using the Universal LPC spritesheet system.

## Features

- deterministic seed-based sprite generation
- automatic item classification filtering
- variant randomization per item
- automated spritesheet PNG download via Playwright
- reproducible URLs

---

## Installation

```bash
git clone <repo>
cd sprite-generator

python -m venv .venv
source .venv/bin/activate

pip install -e .

export PLAYWRIGHT_BROWSERS_PATH=.playwright
playwright install chromium
```

---

## Project Structure

```sh
.
├── generated_spritesheets
│   ├── male_Non-Humanoid_1.png
│   ├── male_Non-Humanoid_2.png
│   └── male_Non-Humanoid_2.png
├── pyproject.toml
├── README.md
└── src
    │  
    └── spriter
        ├── __init__.py
        ├── __main__.py
        ├── config.json
        ├── classified_items.csv
        ├── item-metadata.json
        ├── item_selector.py
        └── playwright_wrapper.py
```
---

## Usage

### 1. Start sprite generator service

```bash
python -m http.server 8000
```

or use hosted version:

https://liberatedpixelcup.github.io/Universal-LPC-Spritesheet-Character-Generator/

---

### 2. Generate sprite URL

```sh

python -m spriter

```

## Configuration

### Base frames

child
female
male
muscular
pregnant
teen

### Modes

Humanoid
Non-Humanoid
Universal
