import os
import re
import pandas as pd
from pathlib import Path
import argparse

# HTML templating
from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


def parse_args():
    parser = argparse.ArgumentParser(description="Generate trading cards from CSV data")
    parser.add_argument(
        "--csv",
        type=str,
        default="cards.csv",
        help="Path to the CSV file containing card data",
    )
    parser.add_argument(
        "--template",
        type=str,
        default="card_template.html",
        help="Path to the HTML template file",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="cards",
        help="Directory to output generated cards",
    )
    parser.add_argument(
        "--styles", type=str, default="styles.css", help="Path to CSS styles file"
    )
    parser.add_argument(
        "--browser",
        type=str,
        choices=["firefox", "chrome", "edge"],
        default="firefox",
        help="Browser to use for rendering",
    )
    return parser.parse_args()


def setup_webdriver(browser_name):
    if browser_name == "firefox":
        options = Options()
        options.add_argument("-headless")
        return webdriver.Firefox(options=options)
    elif browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless")
        return webdriver.Chrome(options=options)
    elif browser_name == "edge":
        options = EdgeOptions()
        options.add_argument("--headless")
        return webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")


def get_image_path(card_id, base_dir):
    """Try both .jpg and .png extensions"""
    jpg_path = os.path.join(base_dir, f"img/cards/{card_id}.jpg")
    png_path = os.path.join(base_dir, f"img/cards/{card_id}.png")

    if os.path.exists(jpg_path):
        return os.path.abspath(jpg_path)
    elif os.path.exists(png_path):
        return os.path.abspath(png_path)
    else:
        raise FileNotFoundError(f"No image found for {card_id}")


# Setup parser for newlines in text
def nl2br(value):
    result = value.replace("\n\n", "<br>")
    return result


def main():
    args = parse_args()

    # Set up paths
    base_dir = os.path.dirname(os.path.abspath(args.csv))
    cards_dir = Path(args.output_dir)
    cards_dir.mkdir(exist_ok=True)

    # Set up Jinja environment
    template_dir = os.path.dirname(os.path.abspath(args.template))
    env = Environment(loader=FileSystemLoader(template_dir))
    env.filters["nl2br"] = nl2br
    template = env.get_template(os.path.basename(args.template))

    # Read and process the CSV file
    df = pd.read_csv(args.csv, lineterminator="\n")
    df = df.dropna(subset=["id"])  # Drop rows without an id

    # Handle newlines in text fields
    text_columns = ["effect", "quote", "source"]
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].str.replace("\n", "\n\n")

    # Initialize webdriver
    driver = setup_webdriver(args.browser)
    css_path = os.path.abspath(args.styles)

    try:
        # Process each card
        for _, card_data in df.iterrows():
            try:
                # Convert row to dict and handle image path
                card_dict = card_data.to_dict()

                # Ensure cost is an integer
                cost = card_dict.get("cost", None)
                if cost is not None:
                    card_dict["cost"] = int(cost)

                card_dict["image_url"] = get_image_path(card_dict["id"], base_dir)

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
    finally:
        # Close the browser
        driver.quit()


if __name__ == "__main__":
    main()
