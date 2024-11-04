from describe.convert_pdf_to_images import convert_pdf_to_images
from describe.open_pdf_to_buffer import open_pdf_to_buffer
from describe.remove_headers_and_footers import remove_headers_and_footers
from describe.extract_images import extract_images
from describe.merge_adjacent_images import merge_adjacent_images
from describe.split_pdf_to_page_buffers import split_pdf_to_page_buffers
from describe.describe_rendering import describe_rendering

from tqdm import tqdm
from glob import glob
import os

for file in tqdm(sorted(glob(".erettsegi/e_tort_19okt_fl.pdf"))):
    filename = os.path.basename(file)

    pdf_buffer = open_pdf_to_buffer(file)

    pdf_buffer = remove_headers_and_footers(pdf_buffer)

    page_buffers = split_pdf_to_page_buffers(pdf_buffer)
    renderings = convert_pdf_to_images(pdf_buffer)

    for i, (page_buffer, rendering) in tqdm(
        enumerate(zip(page_buffers[3:4], renderings[3:4])), total=len(page_buffers)
    ):
        images = extract_images(page_buffer)

        for img_data in images:
            img_data["page"] = i + 1

        images = merge_adjacent_images(images)

        for j, img_data in enumerate(images):
            img_data["index"] = j + 1

        description = describe_rendering(filename, rendering, images)

        rendering.save(f"_rendering_{i + 1}.png")

        with open(f"_description_{i + 1}.txt", "w") as f:
            f.write(description)

    break
