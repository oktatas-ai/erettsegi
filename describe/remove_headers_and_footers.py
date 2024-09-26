import fitz
import io


LAYOUT_HEIGHT = 72


def remove_headers_and_footers(pdf_buffer):
    doc = fitz.open(stream=pdf_buffer, filetype="pdf")

    for page in doc:
        page_rect = page.rect
        shape = page.new_shape()

        shape.draw_rect(
            fitz.Rect(
                page_rect.x0,
                page_rect.y0,
                page_rect.x1,
                page_rect.y0 + LAYOUT_HEIGHT,
            )
        )
        shape.finish(color=None, fill=(1, 0, 0), fill_opacity=0.5)

        shape.draw_rect(
            fitz.Rect(
                page_rect.x0,
                page_rect.y1 - LAYOUT_HEIGHT,
                page_rect.x1,
                page_rect.y1,
            )
        )
        shape.finish(color=None, fill=(0, 0, 1), fill_opacity=0.5)

        shape.commit()

    output_buffer = io.BytesIO()
    doc.save(output_buffer)
    doc.close()
    output_buffer.seek(0)

    return output_buffer
