#!/usr/bin/env python3

import os
import csv
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
import argparse
from PIL import Image

# A4 size in mm
A4_WIDTH = 210
A4_HEIGHT = 297

# Card dimensions from base.css (69mm x 94mm)
CARD_WIDTH = 69
CARD_HEIGHT = 94

# Margin in mm
MARGIN = 5


def calculate_card_positions():
    """Calculate positions where cards can be placed on the page"""
    # Available space after margins
    available_width = A4_WIDTH - (2 * MARGIN)
    available_height = A4_HEIGHT - (2 * MARGIN)

    # Calculate how many cards fit in each direction
    cards_across = int(available_width // CARD_WIDTH)
    cards_down = int(available_height // CARD_HEIGHT)

    # Calculate spacing between cards to center them
    x_spacing = (
        (available_width - (cards_across * CARD_WIDTH)) / (cards_across - 1)
        if cards_across > 1
        else 0
    )
    y_spacing = (
        (available_height - (cards_down * CARD_HEIGHT)) / (cards_down - 1)
        if cards_down > 1
        else 0
    )

    positions = []
    for row in range(cards_down):
        for col in range(cards_across):
            x = MARGIN + (col * (CARD_WIDTH + x_spacing))
            # Start from top of page
            y = A4_HEIGHT - MARGIN - CARD_HEIGHT - (row * (CARD_HEIGHT + y_spacing))
            positions.append((x * mm, y * mm))

    return positions


def get_cards_in_order(game_dir: str) -> list:
    """Read the CSV file and return cards in order with their counts"""
    csv_path = Path(game_dir) / "cards.csv"
    cards = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["id"].startswith(("action_", "event_")):  # Only process actual cards
                card_id = row["id"]
                count = int(row["count"]) if row["count"] else 1
                card_type = "action" if card_id.startswith("action_") else "event"
                cards.extend([{"id": card_id, "type": card_type}] * count)

    return cards


def create_print_layout(game_dir: str, output_pdf: str):
    """Create a print layout PDF with cards from the game directory"""
    cards_dir = Path(game_dir) / "cards"

    # Get cards in CSV order with their counts
    ordered_cards = get_cards_in_order(game_dir)

    # Get all card images
    image_files = {f.stem: f for f in cards_dir.glob("*.png")}
    back_action = image_files.get("back_action")
    back_event = image_files.get("back_event")

    # Create PDF
    c = canvas.Canvas(output_pdf, pagesize=A4)

    # Calculate card positions
    positions = calculate_card_positions()
    cards_per_page = len(positions)

    # Process front faces in CSV order
    current_pos = 0
    for card in ordered_cards:
        img_path = image_files.get(card["id"])
        if img_path:
            if current_pos >= cards_per_page:
                c.showPage()  # Start new page
                current_pos = 0

            # Add card to PDF
            x, y = positions[current_pos]
            c.drawImage(str(img_path), x, y, CARD_WIDTH * mm, CARD_HEIGHT * mm)
            current_pos += 1

    # Start new page if needed
    if current_pos > 0:
        c.showPage()

    # Process card backs in same order
    current_pos = 0
    for card in ordered_cards:
        back_image = back_action if card["type"] == "action" else back_event
        if back_image:
            if current_pos >= cards_per_page:
                c.showPage()
                current_pos = 0

            x, y = positions[current_pos]
            c.drawImage(str(back_image), x, y, CARD_WIDTH * mm, CARD_HEIGHT * mm)
            current_pos += 1

    # Save PDF
    c.save()
    print(f"Created print layout at {output_pdf}")
    print(
        f"Total cards: {len(ordered_cards)} ({sum(1 for c in ordered_cards if c['type'] == 'action')} action cards, {sum(1 for c in ordered_cards if c['type'] == 'event')} event cards)"
    )


def main():
    parser = argparse.ArgumentParser(description="Generate print layout for cards")
    parser.add_argument(
        "game_dir",
        type=str,
        help="Path to the game directory containing the cards folder",
    )
    parser.add_argument(
        "--output", type=str, default="print_layout.pdf", help="Output PDF file path"
    )

    args = parser.parse_args()
    create_print_layout(args.game_dir, args.output)


if __name__ == "__main__":
    main()
