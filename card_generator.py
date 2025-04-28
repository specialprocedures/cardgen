import os
import pandas as pd
from pathlib import Path
import argparse
from jinja2 import Environment, FileSystemLoader
from html2png import setup_webdriver, html2png


def parse_args():
    parser = argparse.ArgumentParser(description="Generate trading cards from CSV data")
    parser.add_argument(
        "game_dir",
        type=str,
        help="Path to the game directory containing cards.csv and card_template.html",
    )
    parser.add_argument(
        "--browser",
        type=str,
        choices=["firefox", "chrome", "edge"],
        default="firefox",
        help="Browser to use for rendering",
    )
    return parser.parse_args()


# Setup parser for newlines in text
def nl2br(value):
    result = value.replace("\n", "<br>")
    return result


def get_style_links(base_dir, card_dict):
    """Generate style link tags based on the card's style configuration"""
    style_links = []

    # Add base stylesheet if specified
    if "style_path" in card_dict and pd.notna(card_dict["style_path"]):
        style_path = os.path.join(base_dir, str(card_dict["style_path"]))
        if os.path.exists(style_path):
            style_links.append(
                f'<link rel="stylesheet" href="file://{os.path.abspath(style_path)}">'
            )
        else:
            print(f"Warning: Style file not found: {style_path}")

    # Add supplementary stylesheet if specified
    if "supplementary_style" in card_dict and pd.notna(
        card_dict["supplementary_style"]
    ):
        supp_style_path = os.path.join(base_dir, str(card_dict["supplementary_style"]))
        if os.path.exists(supp_style_path):
            style_links.append(
                f'<link rel="stylesheet" href="file://{os.path.abspath(supp_style_path)}">'
            )
        else:
            print(f"Warning: Supplementary style file not found: {supp_style_path}")

    # If no valid styles found, fall back to default styles.css
    if not style_links:
        default_style = os.path.join(base_dir, "base.css")
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
        "Template": game_dir / "templates" / "card_template.html",
    }

    for name, path in required_files.items():
        if not path.exists():
            raise FileNotFoundError(f"{name} file not found: {path}")

    # Set up paths
    base_dir = str(game_dir)
    cards_dir = game_dir / "cards"
    cards_dir.mkdir(exist_ok=True)

    # Set up Jinja environment with templates directory
    templates_dir = game_dir / "templates"
    env = Environment(loader=FileSystemLoader(templates_dir))
    env.filters["nl2br"] = nl2br

    # Read and process the CSV file
    df = pd.read_csv(required_files["CSV"], lineterminator="\n")
    df = df.dropna(subset=["id"])  # Drop rows without an id
    df["serial_number"] = df.index + 1  # Add serial number based on index

    # Initialize webdriver once for all cards
    driver = setup_webdriver(args.browser)

    try:
        # Generate back templates first (only once per type)
        generated_backs = set()
        for card_type in df["type"].unique():
            card_type = card_type.lower()
            if card_type not in generated_backs:
                # Generate card back
                back_template_name = f"back_{card_type}.html"
                back_template = env.get_template(back_template_name)
                back_html = back_template.render()

                # Create full HTML for back
                style_links = get_style_links(base_dir, {"type": card_type})
                back_html_string = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <base href="file://{os.path.abspath(base_dir)}/">
                    {style_links}
                </head>
                <body>
                {back_html}
                </body>
                </html>
                """

                # Save back HTML file
                back_html_path = cards_dir / f"back_{card_type}.html"
                with open(back_html_path, "w") as f:
                    f.write(back_html_string)

                # Generate back PNG
                back_png_path = cards_dir / f"back_{card_type}.png"
                html2png(
                    back_html_path,
                    back_png_path,
                    element_class="trading-card",
                    driver=driver,
                )

                # Clean up back HTML file
                if back_html_path.exists():
                    os.remove(back_html_path)

                generated_backs.add(card_type)
                print(f"Generated {card_type} back template")

        # Process each card front using the same browser session
        for _, card_data in df.iterrows():
            process_card(card_data, env, base_dir, cards_dir, driver, len(df))
    finally:
        # Close the browser
        driver.quit()


def process_card(card_data, env, base_dir, cards_dir, driver, total_cards):
    try:
        # Convert row to dict and handle image path
        card_dict = card_data.to_dict()
        card_dict["total_cards"] = total_cards

        # Handle cost - convert to int if present, otherwise empty string
        if pd.notna(card_dict.get("cost")):
            card_dict["cost"] = int(card_dict["cost"])
        else:
            card_dict["cost"] = ""

        # Handle null quotes and sources
        for key in ["quote", "source"]:
            if pd.notna(card_dict.get(key)):
                card_dict[key] = str(card_dict[key])
            else:
                card_dict[key] = ""

        # Handle serial number
        card_dict["serial_number"] = int(card_dict["serial_number"])

        # Use image_path from CSV and make it absolute
        if pd.notna(card_dict.get("image_path")):
            card_dict["image_url"] = os.path.abspath(
                os.path.join(base_dir, str(card_dict["image_path"]))
            )
        else:
            print(f"Warning: No image path specified for card {card_dict['id']}")

        # Get style links for this card
        style_links = get_style_links(base_dir, card_dict)

        # Render the front card HTML
        template = env.get_template("card_template.html")
        card_html = template.render(card=card_dict)

        # Create full HTML with styles
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
        try:
            with open(html_path, "w") as f:
                f.write(full_html_string)

            # Generate PNG using existing browser session
            png_path = cards_dir / f"{card_dict['id']}.png"
            html2png(html_path, png_path, element_class="trading-card", driver=driver)

            print(f"Generated card {card_dict['id']}")
        finally:
            # Clean up HTML file after PNG is generated
            if html_path.exists():
                os.remove(html_path)

    except Exception as e:
        print(f"Error processing card {card_dict['id']}: {e}")


if __name__ == "__main__":
    main()
