import re
from .text_cleaning import normalize_text, clean_text


SECTION_ALIASES = {
    "summary": ["summary", "profile", "about"],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships",
        "employment"
    ],
    "projects": [
        "projects",
        "project",
        "project experience",
        "academic projects"
    ],
    "skills": [
        "skills",
        "technical skills",
        "tech stack",
        "technologies",
        "tools",
        "frameworks",
        "libraries"
    ]
}


def extract_sections(raw_text: str):
    text = normalize_text(raw_text.lower())

    # Add newline start to stabilize regex
    text = "\n" + text

    matches = []

    # ---------------------------------------------------
    # FIND ALL SECTION HEADERS
    # ---------------------------------------------------
    for section, aliases in SECTION_ALIASES.items():
        for alias in aliases:

            # matches:
            # skills
            # skills:
            # skills -
            # skills\n
            pattern = rf"\n\s*{alias}\s*[:\-]?\s*\n?"

            for m in re.finditer(pattern, text):
                matches.append((section, m.start(), m.end()))

    # sort by position
    matches.sort(key=lambda x: x[1])

    extracted = {
        "summary": "",
        "experience": "",
        "projects": "",
        "skills": ""
    }

    # ---------------------------------------------------
    # CUT TEXT BETWEEN HEADERS
    # ---------------------------------------------------
    for i, (section, start, end) in enumerate(matches):

        next_start = matches[i + 1][1] if i + 1 < len(matches) else len(text)

        section_text = text[end:next_start].strip()
        extracted[section] += " " + section_text

    # ---------------------------------------------------
    # HARD FALLBACK (if extraction weak)
    # ---------------------------------------------------
    if len(extracted["skills"].strip()) < 20:
        extracted["skills"] = text

    if len(extracted["experience"].strip()) < 20:
        extracted["experience"] = text

    if len(extracted["projects"].strip()) < 20:
        extracted["projects"] = text

    # ---------------------------------------------------
    # CLEAN EACH SECTION
    # ---------------------------------------------------
    for k in extracted:
        extracted[k] = clean_text(extracted[k])

    return extracted