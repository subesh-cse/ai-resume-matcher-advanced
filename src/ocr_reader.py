import pytesseract
from pdf2image import convert_from_path
import tempfile
import os

# =====================================================
# LOCAL PATHS (for your system)
# These will be used ONLY if they exist on the machine
# =====================================================

LOCAL_TESSERACT_PATH = r"C:\Users\subes\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
LOCAL_POPPLER_PATH = r"C:\poppler\poppler-25.12.0\Library\bin"

# Use local tesseract if present
if os.path.exists(LOCAL_TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = LOCAL_TESSERACT_PATH

# If poppler exists locally, use it
if os.path.exists(LOCAL_POPPLER_PATH):
    POPPLER_PATH = LOCAL_POPPLER_PATH
else:
    POPPLER_PATH = None


# =====================================================
# OCR FUNCTION
# =====================================================
def read_image_pdf(uploaded_file):
    text_output = ""

    # Reset file pointer (important for Streamlit uploads)
    uploaded_file.seek(0)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        pages = convert_from_path(
            tmp_path,
            poppler_path=POPPLER_PATH if POPPLER_PATH else None
        )

        for page in pages:
            text_output += pytesseract.image_to_string(page)

    finally:
        os.remove(tmp_path)

    return text_output