import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageTk


class WatermarkApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Image Watermarker")
        self.geometry("1100x700")
        self.minsize(900, 600)

        # Image state
        self.original_image: Image.Image | None = None
        self.logo_image: Image.Image | None = None
        self.display_photo: ImageTk.PhotoImage | None = None
        self.open_image_path: Path | None = None

        # UI state
        self.watermark_text_var = tk.StringVar(value="Sample Watermark")
        self.opacity_var = tk.DoubleVar(value=70.0)  # 0-100
        self.font_size_var = tk.IntVar(value=40)
        self.position_var = tk.StringVar(value="bottom_right")
        self.logo_scale_var = tk.DoubleVar(value=30.0)  # percentage of image width

        self._build_ui()

    # UI setup ---------------------------------------------------------------
    def _build_ui(self) -> None:
        root_frame = ttk.Frame(self, padding=10)
        root_frame.pack(fill=tk.BOTH, expand=True)

        root_frame.columnconfigure(0, weight=0)
        root_frame.columnconfigure(1, weight=1)
        root_frame.rowconfigure(0, weight=1)

        controls = ttk.Frame(root_frame)
        controls.grid(row=0, column=0, sticky="nsw", padx=(0, 10))

        preview = ttk.Frame(root_frame)
        preview.grid(row=0, column=1, sticky="nsew")
        preview.rowconfigure(0, weight=1)
        preview.columnconfigure(0, weight=1)

        self._build_controls(controls)
        self._build_preview(preview)

    def _build_controls(self, parent: ttk.Frame) -> None:
        # File section
        file_label = ttk.Label(parent, text="Image Files", font=("TkDefaultFont", 10, "bold"))
        file_label.grid(row=0, column=0, sticky="w", pady=(0, 4))

        open_image_btn = ttk.Button(parent, text="Open Base Image...", command=self._open_image)
        open_image_btn.grid(row=1, column=0, sticky="ew", pady=2)

        open_logo_btn = ttk.Button(parent, text="Open Logo (optional)...", command=self._open_logo)
        open_logo_btn.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(row=3, column=0, sticky="ew", pady=8)

        # Text watermark controls
        text_label = ttk.Label(parent, text="Text Watermark", font=("TkDefaultFont", 10, "bold"))
        text_label.grid(row=4, column=0, sticky="w", pady=(0, 4))

        text_entry = ttk.Entry(parent, textvariable=self.watermark_text_var, width=28)
        text_entry.grid(row=5, column=0, sticky="ew", pady=(0, 6))

        font_row = ttk.Frame(parent)
        font_row.grid(row=6, column=0, sticky="ew", pady=(0, 6))
        ttk.Label(font_row, text="Font size:").pack(side=tk.LEFT)
        font_spin = ttk.Spinbox(
            font_row,
            from_=10,
            to=200,
            textvariable=self.font_size_var,
            width=5,
            command=self._update_preview,
        )
        font_spin.pack(side=tk.LEFT, padx=(4, 0))

        # Logo controls
        logo_label = ttk.Label(parent, text="Logo Watermark", font=("TkDefaultFont", 10, "bold"))
        logo_label.grid(row=7, column=0, sticky="w", pady=(6, 4))

        scale_row = ttk.Frame(parent)
        scale_row.grid(row=8, column=0, sticky="ew")
        ttk.Label(scale_row, text="Logo size (% width):").pack(side=tk.TOP, anchor="w")

        logo_scale = ttk.Scale(
            scale_row,
            from_=5,
            to=60,
            variable=self.logo_scale_var,
            command=lambda _v: self._update_preview(),
        )
        logo_scale.pack(fill=tk.X)

        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(row=9, column=0, sticky="ew", pady=8)

        # Shared controls
        pos_label = ttk.Label(parent, text="Position", font=("TkDefaultFont", 10, "bold"))
        pos_label.grid(row=10, column=0, sticky="w", pady=(0, 4))

        pos_menu = ttk.OptionMenu(
            parent,
            self.position_var,
            "bottom_right",
            "bottom_right",
            "bottom_left",
            "top_right",
            "top_left",
            "center",
            command=lambda _v: self._update_preview(),
        )
        pos_menu.grid(row=11, column=0, sticky="ew", pady=(0, 6))

        opacity_row = ttk.Frame(parent)
        opacity_row.grid(row=12, column=0, sticky="ew", pady=(0, 6))
        ttk.Label(opacity_row, text="Opacity:").pack(side=tk.TOP, anchor="w")

        opacity_scale = ttk.Scale(
            opacity_row,
            from_=10,
            to=100,
            variable=self.opacity_var,
            command=lambda _v: self._update_preview(),
        )
        opacity_scale.pack(fill=tk.X)

        # Save button
        self.save_btn = ttk.Button(parent, text="Save Watermarked Image...", command=self._save_image, state=tk.DISABLED)
        self.save_btn.grid(row=13, column=0, sticky="ew", pady=(10, 0))

        # Make controls column expand horizontally
        parent.columnconfigure(0, weight=1)

        # Live updates when text changes
        self.watermark_text_var.trace_add("write", lambda *_: self._update_preview())
        self.font_size_var.trace_add("write", lambda *_: self._update_preview())

    def _build_preview(self, parent: ttk.Frame) -> None:
        self.preview_canvas = tk.Label(parent, text="Open an image to preview.", anchor="center", bg="#dddddd")
        self.preview_canvas.grid(row=0, column=0, sticky="nsew")

    # Image loading ----------------------------------------------------------
    def _open_image(self) -> None:
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(title="Select base image", filetypes=filetypes)
        if not filename:
            return

        try:
            img = Image.open(filename).convert("RGBA")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Error", f"Could not open image:\n{exc}")
            return

        self.original_image = img
        self.open_image_path = Path(filename)
        self.save_btn.config(state=tk.NORMAL)
        self._update_preview()

    def _open_logo(self) -> None:
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(title="Select logo image", filetypes=filetypes)
        if not filename:
            return

        try:
            logo = Image.open(filename).convert("RGBA")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Error", f"Could not open logo image:\n{exc}")
            return

        self.logo_image = logo
        self._update_preview()

    # Watermark logic --------------------------------------------------------
    def _get_font(self, font_size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        font_candidates = [
            "arial.ttf",
            "DejaVuSans.ttf",
        ]
        for font_name in font_candidates:
            try:
                return ImageFont.truetype(font_name, font_size)
            except Exception:  # noqa: BLE001
                continue
        return ImageFont.load_default()

    def _compute_position(self, base_size: tuple[int, int], overlay_size: tuple[int, int]) -> tuple[int, int]:
        img_w, img_h = base_size
        obj_w, obj_h = overlay_size
        margin = max(int(min(img_w, img_h) * 0.02), 10)

        pos_key = self.position_var.get()

        if pos_key == "top_left":
            return margin, margin
        if pos_key == "top_right":
            return img_w - obj_w - margin, margin
        if pos_key == "bottom_left":
            return margin, img_h - obj_h - margin
        if pos_key == "center":
            return (img_w - obj_w) // 2, (img_h - obj_h) // 2

        # default: bottom_right
        return img_w - obj_w - margin, img_h - obj_h - margin

    def _apply_text_watermark(self, base: Image.Image) -> Image.Image:
        text = self.watermark_text_var.get().strip()
        if not text:
            return base

        font_size = max(int(self.font_size_var.get()), 8)
        opacity = max(10.0, min(100.0, float(self.opacity_var.get()))) / 100.0

        txt_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(txt_layer)
        font = self._get_font(font_size)

        # Measure text size
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except Exception:  # noqa: BLE001
            text_w, text_h = draw.textsize(text, font=font)

        position = self._compute_position(base.size, (text_w, text_h))
        fill = (255, 255, 255, int(255 * opacity))

        draw.text(position, text, font=font, fill=fill)
        return Image.alpha_composite(base, txt_layer)

    def _apply_logo_watermark(self, base: Image.Image) -> Image.Image:
        if self.logo_image is None:
            return base

        opacity = max(10.0, min(100.0, float(self.opacity_var.get()))) / 100.0
        logo_scale_percent = max(5.0, min(60.0, float(self.logo_scale_var.get())))

        base_w, base_h = base.size
        target_w = int(base_w * (logo_scale_percent / 100.0))

        logo = self.logo_image.copy()
        if target_w > 0 and logo.width > target_w:
            ratio = target_w / logo.width
            new_size = (target_w, int(logo.height * ratio))
            logo = logo.resize(new_size, Image.LANCZOS)

        # Apply opacity to logo
        r, g, b, a = logo.split()
        a = a.point(lambda v: int(v * opacity))
        logo.putalpha(a)

        logo_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        position = self._compute_position(base.size, logo.size)
        logo_layer.paste(logo, position, logo)

        return Image.alpha_composite(base, logo_layer)

    def _build_watermarked_image(self) -> Image.Image | None:
        if self.original_image is None:
            return None

        base = self.original_image.convert("RGBA").copy()
        base = self._apply_text_watermark(base)
        base = self._apply_logo_watermark(base)
        return base

    # Preview & saving -------------------------------------------------------
    def _update_preview(self) -> None:
        if self.original_image is None:
            self.preview_canvas.config(text="Open an image to preview.", image="")
            self.display_photo = None
            return

        watermarked = self._build_watermarked_image()
        if watermarked is None:
            return

        # Resize for preview while keeping aspect ratio
        max_w, max_h = 900, 650
        img_w, img_h = watermarked.size
        scale = min(max_w / img_w, max_h / img_h, 1.0)
        if scale < 1.0:
            new_size = (int(img_w * scale), int(img_h * scale))
            preview_img = watermarked.resize(new_size, Image.LANCZOS)
        else:
            preview_img = watermarked

        self.display_photo = ImageTk.PhotoImage(preview_img)
        self.preview_canvas.config(image=self.display_photo, text="")

    def _save_image(self) -> None:
        if self.original_image is None:
            messagebox.showwarning("No image", "Please open an image first.")
            return

        watermarked = self._build_watermarked_image()
        if watermarked is None:
            messagebox.showwarning("Nothing to save", "There is no watermarked image to save.")
            return

        initial_dir = str(self.open_image_path.parent) if self.open_image_path else ""
        initial_name = (
            f"{self.open_image_path.stem}_watermarked{self.open_image_path.suffix}"
            if self.open_image_path
            else "watermarked.png"
        )

        filetypes = [
            ("PNG image", "*.png"),
            ("JPEG image", "*.jpg;*.jpeg"),
            ("Bitmap image", "*.bmp"),
            ("All files", "*.*"),
        ]

        out_path = filedialog.asksaveasfilename(
            title="Save watermarked image",
            defaultextension=".png",
            initialdir=initial_dir,
            initialfile=initial_name,
            filetypes=filetypes,
        )
        if not out_path:
            return

        try:
            ext = Path(out_path).suffix.lower()
            if ext in {".jpg", ".jpeg", ".bmp"}:
                watermarked.convert("RGB").save(out_path)
            else:
                watermarked.save(out_path)
            messagebox.showinfo("Saved", f"Watermarked image saved to:\n{out_path}")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Error", f"Could not save image:\n{exc}")


def main() -> None:
    app = WatermarkApp()
    app.mainloop()


if __name__ == "__main__":
    main()
