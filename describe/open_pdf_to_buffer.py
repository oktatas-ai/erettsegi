import io


def open_pdf_to_buffer(input_pdf):
    with open(input_pdf, "rb") as file:
        return io.BytesIO(file.read())
