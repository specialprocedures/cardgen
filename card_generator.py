import os

# HTML templating
from jinja2 import Environment, FileSystemLoader


# import webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

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
    "image_url": os.path.abspath("img/input/action1_bushtroops.jpg"),
}

# Render the Jinja template for the single card
card_html = template.render(card=single_card_data)

css_path = os.path.abspath("styles.css")
output_path = os.path.abspath("output_card.png")

# Combine HTML and CSS and generate PDF for the single card
# We wrap the card HTML in a basic HTML structure
full_html_string = f'<html><head><link rel="stylesheet" href="file://{css_path}"></head><body>{card_html}</body></html>'

# Write the HTML to a file
with open("output_card.html", "w") as f:
    f.write(full_html_string)


# the interface for turning on headless mode
options = Options()
options.add_argument("-headless")

driver = webdriver.Firefox(options=options)

# Load the HTML file
driver.get("file:///home/ian/Projects/cardgen/games/risk_2025/output_card.html")
driver.execute_script('document.body.style.MozTransform = "scale(5)";')
driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')

# get the element by class
element = driver.find_element("class name", "trading-card")
# Set the size of the window to match the card size
# driver.set_window_size(4 * 400, 4 * 600)
# Take a screenshot of the element
element.screenshot("foo.png")
# Close the browser
driver.quit()
