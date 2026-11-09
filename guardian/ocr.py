"""Segunda lectura de la factura con OCR (Tesseract), independiente de la IA.

Es opcional: si Tesseract no está instalado, la revisión se marca como "no disponible" y no
cuenta como falla. En Colab se instala con:
    !apt-get install -y tesseract-ocr tesseract-ocr-spa && pip install pytesseract
"""

from pathlib import Path


def ocr_disponible() -> bool:
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False


def leer_texto(ruta_png: Path) -> str | None:
    """Texto de la imagen, o None si no hay OCR."""
    if not ocr_disponible():
        return None
    import pytesseract
    from PIL import Image
    return pytesseract.image_to_string(Image.open(ruta_png), lang="spa")
