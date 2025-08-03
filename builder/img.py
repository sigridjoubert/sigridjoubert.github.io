from PIL import Image
from pathlib import Path

from .logger import get_logger

LOGGER = get_logger()


def convert_and_resize_to_webp(path: Path, max_size=1920, quality=80):
    """
    Resize and convert an image to WebP format with optimal compression.
    Replaces fully transparent areas with white, deletes the original file,
    and saves the new one with a .webp extension.
    """
    if not path.is_file():
        return

    try:
        with Image.open(path) as img:
            img = img.convert("RGBA")  # Preserve alpha if present

            # Replace transparent pixels with white
            background = Image.new("RGBA", img.size, (255, 255, 255, 255))
            img = Image.alpha_composite(background, img).convert("RGB")

            width, height = img.size
            too_large = max(width, height) > max_size
            wrong_format = path.suffix.lower() != ".webp"
            if too_large or wrong_format:
                # Resize if larger than max_size
                if too_large:
                    scale = max_size / max(width, height)
                    new_size = (int(width * scale), int(height * scale))
                    img = img.resize(new_size, Image.LANCZOS)

                if wrong_format:
                    # Set output path
                    webp_path = path.with_suffix(".webp")

                    # Save as WebP
                    img.save(
                        webp_path,
                        format="WEBP",
                        quality=quality,
                        method=6,
                        optimize=True,
                    )

                    # Delete original file
                    path.unlink()

                    LOGGER.info(f"Converted {path.name} → {webp_path.name}")

    except Exception as e:
        LOGGER.error(f"❌ Failed to convert {path}: {e}")
