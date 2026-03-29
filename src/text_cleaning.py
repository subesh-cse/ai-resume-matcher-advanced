import re

# ================================
# 🔹 NORMALIZATION LAYER
# ================================
def normalize_text(text: str) -> str:
    text = text.lower()

    # ---- OCR mistakes ----
    text = text.replace("al ", "ai ")
    text = text.replace("al-", "ai-")
    text = text.replace(" al", " ai")

    # ---- common ML variants ----
    replacements = {
        "scikit learn": "scikit-learn",
        "sci kit learn": "scikit-learn",
        "sci-kit-learn": "scikit-learn",
        "sk learn": "scikit-learn",
        "sklearn": "scikit-learn",

        "machine-learning": "machine learning",
        "deep-learning": "deep learning",
        "data-science": "data science",

        "a.i": "ai",
        "artificial intelligence": "ai",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


# ================================
# 🔹 MAIN CLEAN FUNCTION
# ================================
def clean_text(text: str) -> str:
    text = normalize_text(text)

    # IMPORTANT FIX:
    # Keep hyphen so "scikit-learn" stays intact
    text = re.sub(r"[^a-zA-Z\s\-]", " ", text)

    # collapse spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()