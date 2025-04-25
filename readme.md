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

1. Create a game directory with the following required files:
   - `cards.csv` - Card data with columns: id, name, type, cost, effect, quote, source
   - `card_template.html` - HTML template using Jinja2 syntax
   - `styles.css` - CSS styling for cards
2. Place card images in `img/cards/` directory (supports .jpg and .png)
3. Run the generator:
   ```bash
   python card_generator.py games/your_game
   ```

## File Structure

Your game directory should follow this structure:
```
your_game/
    card_template.html  # HTML template for cards
    cards.csv          # Card data
    styles.css         # Card styling
    img/
        cards/        # Card images
            image1.jpg
            image2.png
    fonts/           # Custom fonts (optional)
    cards/          # Generated output (created automatically)
```

### Required Files

1. `cards.csv`: Contains card data with the following columns:
   - id: Unique identifier (matches image filename)
   - name: Card name
   - type: Card type
   - cost: Card cost
   - effect: Card effect/description
   - quote: Flavor text (optional)
   - source: Quote source (optional)

2. `card_template.html`: HTML template using Jinja2 syntax
3. `styles.css`: CSS styling for cards
4. Card images in `img/cards/` directory (jpg or png)

## CLI Options

```
python card_generator.py [GAME_DIR] [OPTIONS]

Arguments:
  GAME_DIR        Path to the game directory containing cards.csv, card_template.html, and styles.css

Options:
  --browser TEXT  Browser to use for rendering: firefox|chrome|edge (default: firefox)
```

## Output

The generator creates two files for each card in the `cards/` subdirectory:
1. An HTML file for debugging and style adjustments
2. A PNG file of the rendered card