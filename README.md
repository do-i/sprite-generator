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

playwright install chromium
```

---

## Project Structure

.
├── item_selector.py
├── playwright_wrapper.py
├── classified_items.csv
├── item-metadata.json
├── pyproject.toml
└── README.md

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

```python
from item_selector import generate_sprite, create_url, quick_dict

seed = 42

items = generate_sprite(
    base_frame="male",
    mode="Humanoid",
    seed=seed
)

url = create_url(quick_dict["male"], items)

print(url)
```

Same seed → same sprite.

---

### 3. Render spritesheet PNG automatically

```bash
python playwright_wrapper.py
```

Outputs:

generated_spritesheets/<name>.png

---

## Deterministic Generation

Controlled by seed:

| component | deterministic |
|----------|--------------|
| mandatory categories | yes |
| optional category count | yes |
| optional category selection | yes |
| item selection | yes |
| variant selection | yes |
| final URL | yes |

Example:

```python
for seed in range(5):
    items = generate_sprite("female", seed=seed)
```

---

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

---

## Roadmap ideas

- CLI interface
- batch dataset generation
- sprite preview grid
- rarity weighting
- multi-agent outfit constraints
- SVG export pipeline