from describe import open_pdf_to_buffer
from tqdm import tqdm
from glob import glob


for file in tqdm(sorted(glob(".erettsegi/*_fl.pdf"))):
    buffer = open_pdf_to_buffer(file)
