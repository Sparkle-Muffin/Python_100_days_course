from io import BytesIO
import base64

from flask import Flask, flash, redirect, render_template, request, url_for
import numpy as np
from PIL import Image, UnidentifiedImageError

# cd day92
# flask --app main run --debug

app = Flask(__name__)
app.secret_key = "change-me-in-production"
MAX_COLORS = 10
MAX_ANALYSIS_PIXELS = 250_000
BIN_SIZE = 24


def rgb_to_hex(color):
    """Convert an RGB tuple to HEX string."""
    return "#{:02x}{:02x}{:02x}".format(*color)


def top_colors_from_image(image_bytes, top_n=10):
    """
    Return top N dominant RGB colors with counts.

    Strategy:
    - Resize very large images for speed.
    - Snap channels to fixed bins (24) to merge near shades consistently.
    - Count resulting colors and return the most frequent ones.

    This produces "web extractor style" palettes closer to tools that use
    fixed bucket quantization rather than adaptive palettes.
    """
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    # Keep processing quick for large images while preserving aspect ratio.
    if image.width * image.height > MAX_ANALYSIS_PIXELS:
        image.thumbnail((1000, 1000))

    pixel_array = np.array(image, dtype=np.float32)
    binned = np.clip(np.round(pixel_array / BIN_SIZE) * BIN_SIZE, 0, 255).astype(np.uint8)

    flat_pixels = binned.reshape(-1, 3)
    unique_colors, counts = np.unique(flat_pixels, axis=0, return_counts=True)
    sorted_idx = np.argsort(counts)[::-1][:top_n]
    total_pixels = flat_pixels.shape[0]

    return [
        {
            "rank": idx + 1,
            "rgb": tuple(map(int, unique_colors[color_idx])),
            "hex": rgb_to_hex(tuple(map(int, unique_colors[color_idx]))),
            "count": int(counts[color_idx]),
            "percentage": (count / total_pixels) * 100,
        }
        for idx, color_idx in enumerate(sorted_idx)
        for count in [int(counts[color_idx])]
    ]


@app.route("/", methods=["GET", "POST"])
def index():
    colors = None
    filename = None
    image_data_url = None

    if request.method == "POST":
        uploaded_file = request.files.get("image")

        if not uploaded_file or uploaded_file.filename == "":
            flash("Please choose an image file first.", "warning")
            return redirect(url_for("index"))

        try:
            image_bytes = uploaded_file.read()
            colors = top_colors_from_image(image_bytes, top_n=MAX_COLORS)
            filename = uploaded_file.filename
            encoded = base64.b64encode(image_bytes).decode("utf-8")
            image_data_url = f"data:{uploaded_file.mimetype};base64,{encoded}"
        except UnidentifiedImageError:
            flash("That file is not a valid image.", "danger")
            return redirect(url_for("index"))
        except Exception:
            flash("Something went wrong while processing the image.", "danger")
            return redirect(url_for("index"))

    return render_template(
        "index.html",
        colors=colors,
        filename=filename,
        image_data_url=image_data_url,
    )


if __name__ == "__main__":
    app.run(debug=True)
