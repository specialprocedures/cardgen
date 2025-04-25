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
        styles.css         # Card styling
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
3. `styles.css`: CSS styling for cards

## CLI Options

```
python card_generator.py [GAME_DIR] [OPTIONS]

Arguments:
  GAME_DIR          Path to the game directory containing cards.csv, card_template.html, and styles.css

Options:
  --browser TEXT    Browser to use for rendering: firefox|chrome|edge (default: firefox)
```

## Output

The generator creates two files for each card in the game directory's `cards` folder:
1. An HTML file for debugging and style adjustments
2. A PNG file of the rendered card