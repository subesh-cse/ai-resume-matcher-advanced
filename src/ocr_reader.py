import fitz  # PyMuPDF
import easyocr
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)


def read_image_pdf(uploaded_file):
    text_output = ""

    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    for page in pdf:
        pix = page.get_pixmap()
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, pix.n
        )

        results = reader.readtext(img, detail=0)
        text_output += " ".join(results) + "\n"

    return text_output