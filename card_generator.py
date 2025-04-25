from jinja2 import Environment, FileSystemLoader

# import imgkit

# Set up Jinja environment
env = Environment(
    loader=FileSystemLoader(".")
)  # Assuming template and css are in the current directory
template = env.get_template("card_template.html")

# Data for a single card (example)
single_card_data = {
    "id": "action001",
    "name": "Conscription",
    "type": "Action",
    "cost": 2,
    "count": 4,
    "effect": "You gain 6 units, place them on any territory you control.",
    "quote": "If I were slightly younger and not employed here, I think it would be a fantastic experience to be on the front lines of helping this young democracy succeed.",
    "source": "George W. Bush, 2008",
    "image_url": "img/input/action1_bushtroops.jpg",
}

# Render the Jinja template for the single card
card_html = template.render(card=single_card_data)

# Combine HTML and CSS and generate PDF for the single card
# We wrap the card HTML in a basic HTML structure
full_html_string = f'<html><head><link rel="stylesheet" href="styles.css"></head><body>{card_html}</body></html>'

# Write the HTML to a file
with open("output_card.html", "w") as f:
    f.write(full_html_string)

# Use imgkit to convert HTML to png
# options = {
#     "format": "png",
#     "width": 300,
#     "height": 400,
#     "quality": 300,
# }

# imgkit.from_string(full_html_string, "output_card.png", options=options)
