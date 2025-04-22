import os
import re
import glob
from PIL import Image
import argparse

# Script to slice a single image of all cards into individual card images
# Assumes a grid of 4 rows (suits) and 10 columns (values) in the screenshot.
# Values order: 1,2,3,4,5,6,7,10,11,12
# Suits order: oros, copas, espadas, bastos

# Margins (pixels) to trim from screenshot edges if there are borders
MARGIN_LEFT = 0
MARGIN_TOP = 0
MARGIN_RIGHT = 0
MARGIN_BOTTOM = 0

def main():
    # Parse margin overrides if needed
    parser = argparse.ArgumentParser(description="Slice cards screenshot into individual images")
    parser.add_argument("--left", type=int, default=MARGIN_LEFT, help="Pixels to trim from left")
    parser.add_argument("--top", type=int, default=MARGIN_TOP, help="Pixels to trim from top")
    parser.add_argument("--right", type=int, default=MARGIN_RIGHT, help="Pixels to trim from right")
    parser.add_argument("--bottom", type=int, default=MARGIN_BOTTOM, help="Pixels to trim from bottom")
    args = parser.parse_args()
    left_margin = args.left
    top_margin = args.top
    right_margin = args.right
    bottom_margin = args.bottom
    # Directory for images
    images_dir = "images"
    # Gather all images in the directory
    files = glob.glob(os.path.join(images_dir, "*.*"))
    # Filter out card files matching the naming convention
    card_pattern = re.compile(r'^[0-9]+_[a-z]+\.png$')
    screenshots = [f for f in files if not card_pattern.match(os.path.basename(f))]
    if len(screenshots) != 1:
        print(f"Expected exactly one screenshot file, found {len(screenshots)}: {screenshots}")
        return
    screenshot = screenshots[0]
    print(f"Slicing screenshot: {screenshot}")
    img = Image.open(screenshot)
    w, h = img.size
    print(f"Screenshot size: {w}x{h}")
    print(f"Margins: left={left_margin}, top={top_margin}, right={right_margin}, bottom={bottom_margin}")
    rows, cols = 4, 10
    # Compute grid size after trimming margins
    grid_w = w - left_margin - right_margin
    grid_h = h - top_margin - bottom_margin
    cell_w = grid_w / cols
    cell_h = grid_h / rows
    print(f"Grid: {cols} columns, {rows} rows => cell size: {cell_w:.2f}x{cell_h:.2f}")

    values = [1,2,3,4,5,6,7,10,11,12]
    suits = ['oros','copas','espadas','bastos']

    for r, suit in enumerate(suits):
        for c, value in enumerate(values):
            crop_left = left_margin + int(c * cell_w)
            crop_upper = top_margin + int(r * cell_h)
            crop_right = left_margin + int((c+1) * cell_w)
            crop_lower = top_margin + int((r+1) * cell_h)
            box = (crop_left, crop_upper, crop_right, crop_lower)
            print(f"Cropping {value}_{suit}: box={box}")
            card = img.crop(box)
            out_path = os.path.join(images_dir, f"{value}_{suit}.png")
            card.save(out_path)
            print(f"Saved {out_path}")

if __name__ == "__main__":
    main()
