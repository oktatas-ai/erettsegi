from io import BytesIO
from PIL import Image
import fitz


def extract_images(pdf_buffer):
    doc = fitz.open(stream=pdf_buffer, filetype="pdf")
    images = []

    for page_num, page in enumerate(doc):
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            rect = page.get_image_bbox(img)

            pil_image = Image.open(BytesIO(image_bytes))

            images.append(
                {
                    "page": page_num + 1,
                    "index": img_index + 1,
                    "image": pil_image,
                    "extension": image_ext,
                    "position": {
                        "x": rect.x0,
                        "y": rect.y0,
                        "w": rect.width,
                        "h": rect.height,
                    },
                }
            )

    return images
