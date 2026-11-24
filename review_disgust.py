
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
import math

DATASET = Path("Dataset/disgust/fer2013/train")
OUTPUT = Path("review_outputs")
OUTPUT.mkdir(exist_ok=True)

images = sorted(DATASET.glob("*.jpg"))
print(f"Found {len(images)} images")

COLS = 8
ROWS = 6
PER_PAGE = COLS * ROWS
CELL_W = 160
CELL_H = 155

pages = math.ceil(len(images) / PER_PAGE)

for page in range(pages):
    sheet = Image.new(
        "RGB", (COLS * CELL_W, ROWS * CELL_H), "white"
    )
    draw = ImageDraw.Draw(sheet)

    batch = images[page * PER_PAGE:(page + 1) * PER_PAGE]

    for i, path in enumerate(batch):
        x = (i % COLS) * CELL_W
        y = (i // COLS) * CELL_H

        try:
            with Image.open(path) as img:
                img = ImageOps.contain(
                    img.convert("RGB"), (125, 125)
                )
                # Enlarge 48x48 image for easier review
                img = img.resize((120, 120))
                sheet.paste(img, (x + 20, y + 5))

            draw.text(
                (x + 5, y + 133),
                path.name,
                fill="black"
            )

        except Exception as e:
            print(f"Cannot read {path.name}: {e}")

    filename = OUTPUT / f"disgust_page_{page + 1:02d}.jpg"
    sheet.save(filename, quality=95)
    print(f"Created: {filename}")

print("Done! Original images were not modified.")
