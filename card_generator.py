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
        "game_dir",
        type=str,
        help="Path to the game directory containing cards.csv, card_template.html, and styles.css",
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


# Setup parser for newlines in text
def nl2br(value):
    result = value.replace("\n", "<br>")
    return result


def get_style_links(base_dir, card_dict):
    """Generate style link tags based on the card's style configuration"""
    style_links = []

    # Add base stylesheet if specified
    if "style_path" in card_dict and card_dict["style_path"]:
        style_path = os.path.join(base_dir, card_dict["style_path"])
        if os.path.exists(style_path):
            style_links.append(
                f'<link rel="stylesheet" href="file://{os.path.abspath(style_path)}">'
            )
        else:
            print(f"Warning: Style file not found: {style_path}")

    # Add supplementary stylesheet if specified
    if "supplementary_style" in card_dict and card_dict["supplementary_style"]:
        supp_style_path = os.path.join(base_dir, card_dict["supplementary_style"])
        if os.path.exists(supp_style_path):
            style_links.append(
                f'<link rel="stylesheet" href="file://{os.path.abspath(supp_style_path)}">'
            )
        else:
            print(f"Warning: Supplementary style file not found: {supp_style_path}")

    # If no valid styles found, fall back to default styles.css
    if not style_links:
        default_style = os.path.join(base_dir, "styles.css")
        if os.path.exists(default_style):
            style_links.append(
                f'<link rel="stylesheet" href="file://{os.path.abspath(default_style)}">'
            )
        else:
            print("Warning: No valid stylesheets found, card may not render correctly")

    return "\n".join(style_links)


def main():
    args = parse_args()
    game_dir = Path(args.game_dir)

    # Check required files exist
    required_files = {
        "CSV": game_dir / "cards.csv",
        "Template": game_dir / "card_template.html",
    }

    for name, path in required_files.items():
        if not path.exists():
            raise FileNotFoundError(f"{name} file not found: {path}")

    # Set up paths
    base_dir = str(game_dir)
    cards_dir = game_dir / "cards"
    cards_dir.mkdir(exist_ok=True)

    # Set up Jinja environment
    env = Environment(loader=FileSystemLoader(base_dir))
    env.filters["nl2br"] = nl2br
    template = env.get_template("card_template.html")

    # Read and process the CSV file
    df = pd.read_csv(required_files["CSV"], lineterminator="\n")
    df = df.dropna(subset=["id"])  # Drop rows without an id
    df["serial_number"] = df.index + 1  # Add serial number based on index

    # Initialize webdriver
    driver = setup_webdriver(args.browser)

    try:
        # Process each card
        for _, card_data in df.iterrows():
            try:
                # Convert row to dict and handle image path
                card_dict = card_data.to_dict()

                card_dict["total_cards"] = len(df)

                # Ensure cost is an integer
                for key in ["cost", "serial_number"]:
                    val = card_dict.get(key, None)
                    if val is not None:
                        card_dict[key] = int(val)

                # Use image_path from CSV and make it absolute
                if card_dict.get("image_path"):
                    card_dict["image_url"] = os.path.abspath(
                        os.path.join(base_dir, card_dict["image_path"])
                    )
                else:
                    print(
                        f"Warning: No image path specified for card {card_dict['id']}"
                    )

                # Get style links for this card
                style_links = get_style_links(base_dir, card_dict)

                # Render the card HTML
                card_html = template.render(card=card_dict)

                # Create full HTML with CSS
                full_html_string = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <base href="file://{os.path.abspath(base_dir)}/">
                    {style_links}
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
