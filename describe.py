from describe.convert_pdf_to_images import convert_pdf_to_images
from describe.open_pdf_to_buffer import open_pdf_to_buffer
from describe.remove_headers_and_footers import remove_headers_and_footers
from describe.extract_images import extract_images
from describe.merge_adjacent_images import merge_adjacent_images
from describe.split_pdf_to_page_buffers import split_pdf_to_page_buffers

from tqdm import tqdm
from glob import glob

import os


for file in tqdm(sorted(glob(".erettsegi/e_tort_19okt_fl.pdf"))):
    pdf_buffer = open_pdf_to_buffer(file)

    pdf_buffer = remove_headers_and_footers(pdf_buffer)

    page_buffers = split_pdf_to_page_buffers(pdf_buffer)
    renderings = convert_pdf_to_images(pdf_buffer)

    for i, (page_buffer, rendering) in enumerate(zip(page_buffers, renderings)):
        images = extract_images(page_buffer)

        for img_data in images:
            img_data["page"] = i + 1

        images = merge_adjacent_images(images)

        for j, img_data in enumerate(images):
            img_data["index"] = j + 1

        for img_data in images:
            filename = os.path.splitext(os.path.basename(file))[0]

            image_filename_with_metadata = (
                f"file-{filename}"
                + f"-page-{img_data['page']}"
                + f"-index-{img_data['index']}"
                + f"-x-{int(img_data['position']['x'])}"
                + f"-y-{int(img_data['position']['y'])}"
                + f"-w-{int(img_data['position']['w'])}"
                + f"-h-{int(img_data['position']['h'])}"
                + f".{img_data['extension']}"
            )

            img_data["image"].save(image_filename_with_metadata)

    break
