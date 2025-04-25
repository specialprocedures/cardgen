# Card Generator

A Python-based tool for generating high-quality trading cards from CSV data using HTML templates and browser rendering. Perfect for prototyping card games, creating custom trading cards, or generating print-ready card assets.

## Prerequisites

- Python 3.6+
- A modern web browser (Firefox, Chrome, or Edge)

## Installation

1. Clone this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

1. Prepare your card data in a CSV file with columns: id, name, type, cost, effect, quote, source, image_path
2. Place card images in your preferred directory structure
3. Run the generator:
   ```bash
   python card_generator.py games/your_game
   ```

## File Structure

To create your own card set, follow this structure:
```
games/
    your_game/
        card_template.html  # HTML template for cards
        cards.csv          # Card data
        styles/           # Directory for CSS files (optional)
            base.css      # Base styles
            custom.css    # Additional styles
        styles.css        # Default CSS file (optional if using styles directory)
        img/              # Image directory (can be organized as needed)
        fonts/           # Custom fonts (optional)
```

### Required Files

1. `cards.csv`: Contains card data with the following columns:
   - id: Unique identifier for the card
   - name: Card name
   - type: Card type
   - cost: Card cost
   - effect: Card effect/description
   - quote: Flavor text (optional)
   - source: Quote source (optional)
   - image_path: Path to the card's image file, relative to the game directory

2. `card_template.html`: HTML template using Jinja2 syntax
3. CSS file(s): At least one CSS file is required, either in the styles/ directory or specified via command line

## CLI Options

```
python card_generator.py [GAME_DIR] [OPTIONS]

Arguments:
  GAME_DIR          Path to the game directory containing cards.csv and card_template.html

Options:
  --browser TEXT    Browser to use for rendering: firefox|chrome|edge (default: firefox)
  --styles TEXT...  CSS files to use for styling. Will look for files in the following order:
                    1. In the styles/ directory of the game directory
                    2. At the specified full path
                    3. In the game directory
                    (default: styles.css)
```

### Examples

Use the default styles.css:
```bash
python card_generator.py games/my_game
```

Use multiple CSS files:
```bash
python card_generator.py games/my_game --styles base.css custom.css
```

Use CSS files from different locations:
```bash
python card_generator.py games/my_game --styles styles/base.css /path/to/custom.css
```