from jinja2 import Environment, FileSystemLoader

# import imgkit

# Set up Jinja environment
env = Environment(
    loader=FileSystemLoader(".")
)  # Assuming template and css are in the current directory
template = env.get_template("card_template.html")

# Data for a single card (example)
single_card_data = {
    "id": "001",
    "name": "Forest Guardian",
    "type": "Creature",
    "cost": 3,
    "count": 1,
    "effect": "When this card enters the battlefield, gain 5 life.",
    "quote": '"Protector of the ancient woods."',
    "source": "Elder Scrolls Series",
    "image_url": "img/input/action1_bushtroops.jpg",  # Make sure this image exists or use a placeholder
}

# Render the Jinja template for the single card
card_html = template.render(card=single_card_data)

# Combine HTML and CSS and generate PDF for the single card
# We wrap the card HTML in a basic HTML structure
full_html_string = f'<html><head><link rel="stylesheet" href="styles.css"></head><body>{card_html}</body></html>'

# Use imgkit to convert HTML to png
options = {
    "format": "png",
    "width": 300,
    "height": 400,
    "quality": 300,
}

with open("output_card.html", "w") as f:
    f.write(full_html_string)
# imgkit.from_string(full_html_string, "output_card.png", options=options)
