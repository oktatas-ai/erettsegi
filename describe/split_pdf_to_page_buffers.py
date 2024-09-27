from io import BytesIO
import fitz


def split_pdf_to_page_buffers(pdf_buffer):
    doc = fitz.open(stream=pdf_buffer, filetype="pdf")
    page_buffers = []
    for page_num in range(len(doc)):
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        page_buffer = BytesIO()
        new_doc.save(page_buffer)
        page_buffer.seek(0)
        page_buffers.append(page_buffer)
    return page_buffers
