from pdf2image import convert_from_bytes
from typing import List
from PIL import Image
from io import BytesIO


def convert_pdf_to_images(pdf_buffer: BytesIO) -> List[Image.Image]:
    return convert_from_bytes(pdf_buffer.read())
