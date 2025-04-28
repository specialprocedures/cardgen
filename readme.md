# Card Generator

A Python-based tool for generating high-quality trading cards from CSV data using HTML templates and browser rendering. 

Generate print-ready card assets from a csv with css and jinja.

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
3. Create your HTML templates in the templates directory
4. Run the generator:
   ```bash
   python card_generator.py games/your_game
   ```

## File Structure

To create your own card set, follow this structure:
```
games/
    your_game/
        templates/        # Directory for HTML templates
            card_template.html  # Main card template
            back_template.html  # Card back template (optional)
        cards.csv        # Card data
        styles/         # Directory for CSS files (optional)
            base.css    # Base styles
            custom.css  # Additional styles
        styles.css      # Default CSS file (optional if using styles directory)
        img/            # Image directory (can be organized as needed)
        fonts/         # Custom fonts (optional)
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
   - style_path: Path to the card's base CSS file (optional)
   - supplementary_style: Path to additional CSS file for this card (optional)

2. `templates/card_template.html`: HTML template using Jinja2 syntax
3. CSS file(s): At least one CSS file is required. The system will look for CSS files in the following order:
   1. Per-card style files specified in the CSV (style_path and supplementary_style)
   2. Default base.css in the game directory

## CSV Data Handling

- Empty cells in the CSV are handled gracefully
- Optional columns (quote, source, style_path, supplementary_style) can be left blank
- Numeric values (cost) are automatically converted to integers
- Each card is assigned a serial number based on its position in the CSV

## CLI Options

```
python card_generator.py [GAME_DIR] [OPTIONS]

Arguments:
  GAME_DIR          Path to the game directory containing cards.csv and templates/card_template.html

Options:
  --browser TEXT    Browser to use for rendering: firefox|chrome|edge (default: firefox)
```

### Examples

Basic usage:
```bash
python card_generator.py games/my_game
```

Using Chrome for rendering:
```bash
python card_generator.py games/my_game --browser chrome
```