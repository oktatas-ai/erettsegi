from describe import open_pdf_to_buffer, remove_headers_and_footers
from tqdm import tqdm
from glob import glob


for file in tqdm(sorted(glob(".erettsegi/*_fl.pdf"))):
    buffer = open_pdf_to_buffer(file)

    buffer = remove_headers_and_footers(buffer)
