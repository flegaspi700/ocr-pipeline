from PIL import Image


def to_grayscale(image: Image.Image) -> Image.Image:
    return image.convert("L")


def binarize(image: Image.Image, threshold: int = 128) -> Image.Image:
    gray = to_grayscale(image)
    return gray.point(lambda p: 255 if p >= threshold else 0, mode="1").convert("L")


def resize_to_fit(
    image: Image.Image, max_width: int = 2200, max_height: int = 3200
) -> Image.Image:
    width, height = image.size
    ratio = min(max_width / width, max_height / height, 1.0)
    if ratio < 1.0:
        return image.resize(
            (int(width * ratio), int(height * ratio)), Image.Resampling.LANCZOS
        )
    return image


def preprocess_image(image: Image.Image, threshold: int = 128) -> Image.Image:
    processed = resize_to_fit(image)
    return binarize(processed, threshold=threshold)


def deskew(image: Image.Image) -> Image.Image:
    # Placeholder for deskew functionality. A future version can use OpenCV or other algorithms.
    return image
