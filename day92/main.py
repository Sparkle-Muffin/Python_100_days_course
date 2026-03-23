from collections import Counter
from io import BytesIO

from flask import Flask, flash, redirect, render_template, request, url_for
from PIL import Image, UnidentifiedImageError

# cd day92
# flask --app main run --debug

app = Flask(__name__)
app.secret_key = "change-me-in-production"
MAX_COLORS = 10
PALETTE_SIZE = 32
MAX_ANALYSIS_PIXELS = 250_000


def rgb_to_hex(color):
    """Convert an RGB tuple to HEX string."""
    return "#{:02x}{:02x}{:02x}".format(*color)


def top_colors_from_image(image_bytes, top_n=10):
    """
    Return top N dominant RGB colors with counts.

    Why quantize first:
    Exact pixel counting overweights tiny shade differences (e.g. subtitle antialiasing),
    which often produces mostly white/gray/black output.
    """
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    # Keep processing quick for large images while preserving aspect ratio.
    if image.width * image.height > MAX_ANALYSIS_PIXELS:
        image.thumbnail((1000, 1000))

    # Cluster similar shades into a limited adaptive palette.
    quantized = image.quantize(colors=PALETTE_SIZE, method=Image.Quantize.MEDIANCUT)
    clustered_rgb = quantized.convert("RGB")

    color_counts = Counter(clustered_rgb.getdata())
    most_common = color_counts.most_common(top_n)
    total_pixels = clustered_rgb.width * clustered_rgb.height

    return [
        {
            "rank": idx + 1,
            "rgb": rgb,
            "hex": rgb_to_hex(rgb),
            "count": count,
            "percentage": (count / total_pixels) * 100,
        }
        for idx, (rgb, count) in enumerate(most_common)
    ]


@app.route("/", methods=["GET", "POST"])
def index():
    colors = None
    filename = None

    if request.method == "POST":
        uploaded_file = request.files.get("image")

        if not uploaded_file or uploaded_file.filename == "":
            flash("Please choose an image file first.", "warning")
            return redirect(url_for("index"))

        try:
            image_bytes = uploaded_file.read()
            colors = top_colors_from_image(image_bytes, top_n=MAX_COLORS)
            filename = uploaded_file.filename
        except UnidentifiedImageError:
            flash("That file is not a valid image.", "danger")
            return redirect(url_for("index"))
        except Exception:
            flash("Something went wrong while processing the image.", "danger")
            return redirect(url_for("index"))

    return render_template("index.html", colors=colors, filename=filename)


if __name__ == "__main__":
    app.run(debug=True)
