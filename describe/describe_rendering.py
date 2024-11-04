from pdf2image import convert_from_path
from dotenv import load_dotenv
from base64 import b64encode
from openai import OpenAI
from io import BytesIO
import os
from describe.generate_alt_text import generate_alt_text

import fitz


def get_text_from_page_buffer(page_buffer):
    doc = fitz.open("pdf", page_buffer)
    text = "".join(page.get_text() for page in doc)
    return text


from pydantic import BaseModel


class Schema(BaseModel):
    digitalized_document: str


load_dotenv()
client = OpenAI()


def generate_image_filename(filename, image):
    index = image["index"]
    x = int(image["position"]["x"])
    y = int(image["position"]["y"])
    w = int(image["position"]["w"])
    h = int(image["position"]["h"])
    extension = image["extension"]

    name = f"file-{filename}-index-{index}-x-{x}-y-{y}-w-{w}-h-{h}.{extension}"
    alt = generate_alt_text(image["image"])

    print(f"Saving image to {name}")
    print(f"Alt text: {alt}")

    image["image"].save(name)

    return f"![{alt}]({name})"


def describe_rendering(filename, rendering, images):
    image_filenames = ""
    for image in images:
        image_filenames += generate_image_filename(filename, image) + "\n"

    rendering_buffer = BytesIO()
    rendering.save(rendering_buffer, format="PNG")
    rendering_bytes = b64encode(rendering_buffer.getvalue())
    rendering_string = rendering_bytes.decode("utf-8")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "digitalize this document. digitalize it as it is, dont translate anything.\n"
                            + "make sure that everything has the same formatting as the original document. bold, italic, underline, etc.\n"
                            + f"for images, choose one of the following markdown-formatted images:\n{image_filenames}"
                            if image_filenames
                            else ""
                            + "ignore the gray background parts of the image. including 'number of points' for example.\n"
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{rendering_string}"
                        },
                    },
                ],
            },
        ],
        response_format=Schema,
    )

    return completion.choices[0].message.parsed.digitalized_document
