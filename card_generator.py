import os
import pandas as pd
from pathlib import Path

# HTML templating
from jinja2 import Environment, FileSystemLoader

# import webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Set up Jinja environment
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("card_template.html")

# Ensure cards directory exists
cards_dir = Path("cards")
cards_dir.mkdir(exist_ok=True)

# Read and process the CSV file
df = pd.read_csv("cards.csv")
df = df.dropna(subset=["id"])  # Drop rows without an id

# the interface for turning on headless mode
options = Options()
options.add_argument("-headless")

# Get the base directory for resources
base_dir = os.path.dirname(os.path.abspath(__file__))


def get_image_path(card_id):
    """Try both .jpg and .png extensions"""
    jpg_path = f"img/cards/{card_id}.jpg"
    png_path = f"img/cards/{card_id}.png"

    if os.path.exists(jpg_path):
        return os.path.abspath(jpg_path)
    elif os.path.exists(png_path):
        return os.path.abspath(png_path)
    else:
        raise FileNotFoundError(f"No image found for {card_id}")


# Process each card
driver = webdriver.Firefox(options=options)
css_path = os.path.abspath("styles.css")
for _, card_data in df.iterrows():
    try:
        # Convert row to dict and handle image path
        card_dict = card_data.to_dict()
        card_dict["image_url"] = get_image_path(card_dict["id"])

        # Render the card HTML
        card_html = template.render(card=card_dict)

        # Create full HTML with CSS
        full_html_string = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <base href="file://{base_dir}/">
            <link rel="stylesheet" href="file://{css_path}">
        </head>
        <body>
        {card_html}
        </body>
        </html>
        """

        # Save HTML file
        html_path = cards_dir / f"{card_dict['id']}.html"
        with open(html_path, "w") as f:
            f.write(full_html_string)

        # Generate PNG
        driver.get(f"file://{html_path.absolute()}")
        driver.execute_script('document.body.style.MozTransform = "scale(5)";')
        driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')

        # Get the card element and take screenshot
        element = driver.find_element("class name", "trading-card")
        png_path = cards_dir / f"{card_dict['id']}.png"
        element.screenshot(str(png_path))

        print(f"Generated card {card_dict['id']}")

    except Exception as e:
        print(f"Error processing card {card_dict['id']}: {e}")

# Close the browser
driver.quit()
