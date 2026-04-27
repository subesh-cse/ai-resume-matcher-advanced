from src.section_extractor import extract_sections
from src.scorer import (
    baseline_score_resume,
    hybrid_score_resume,
    similarity_with_explanation,
)


def analyze_resume(resume_text, jd_text, mode="hybrid"):
    """
    Main pipeline:
    - Extract sections
    - Score resume vs JD
    - Blend section score + global similarity
    """

    # ------------------------------
    # SAFETY CHECK
    # ------------------------------
    if not resume_text or not jd_text:
        return 0.0, {"error": "Empty resume or job description"}

    resume_text = str(resume_text)
    jd_text = str(jd_text)

    # ------------------------------
    # RAW TEXT (for global similarity)
    # ------------------------------
    raw_resume = resume_text
    raw_jd = jd_text

    # ------------------------------
    # SECTION EXTRACTION
    # (Do NOT clean before this)
    # ------------------------------
    resume_sections = extract_sections(resume_text)
    jd_sections = extract_sections(jd_text)

    # ------------------------------
    # FALLBACK if extraction failed
    # ------------------------------
    if all(len(v.strip()) == 0 for v in resume_sections.values()):
        resume_sections["skills"] = resume_text
        resume_sections["experience"] = resume_text
        resume_sections["projects"] = resume_text

    # ------------------------------
    # SCORING
    # ------------------------------
    if mode == "baseline":
        section_score, explanation = baseline_score_resume(
            resume_sections, jd_sections
        )
    else:
        section_score, explanation = hybrid_score_resume(
            resume_sections, jd_sections
        )

    # ------------------------------
    # GLOBAL SIMILARITY
    # ------------------------------
    global_score, _ = similarity_with_explanation(raw_resume, raw_jd)

    # ------------------------------
    # FINAL BLEND
    # ------------------------------
    final_score = 0.7 * section_score + 0.3 * global_score
    final_score = max(0.0, min(1.0, float(final_score)))

    return final_score, explanation