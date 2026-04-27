from src.semantic_matcher import semantic_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# NORMALIZATION
# =========================
def normalize_skill_text(text):
    text = str(text).lower()

    text = text.replace("scikit learn", "scikit-learn")
    text = text.replace("sci-kit-learn", "scikit-learn")
    text = text.replace("sklearn", "scikit-learn")

    return text


# =========================
# TF-IDF + SEMANTIC
# =========================
def similarity_with_explanation(text1, text2):

    text1 = str(text1)
    text2 = str(text2)

    if not text1.strip() or not text2.strip():
        return 0.0, []

    text1 = normalize_skill_text(text1)
    text2 = normalize_skill_text(text2)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1
    )

    try:
        tfidf = vectorizer.fit_transform([text1, text2])
    except ValueError:
        return 0.0, []

    tfidf_score = cosine_similarity(tfidf[0], tfidf[1])[0][0]
    tfidf_score = max(0.0, min(1.0, float(tfidf_score)))

    semantic_score = semantic_similarity(text1, text2)

    score = 0.5 * tfidf_score + 0.5 * semantic_score

    feature_names = vectorizer.get_feature_names_out()
    vec1 = tfidf[0].toarray()[0]
    vec2 = tfidf[1].toarray()[0]

    contributions = []

    for i, word in enumerate(feature_names):
        if vec1[i] > 0 and vec2[i] > 0:
            if word in ["learning", "data", "model", "system"]:
                continue
            contributions.append((word, vec1[i] * vec2[i]))

    contributions.sort(key=lambda x: x[1], reverse=True)

    return score, contributions[:6]


# =========================
# SKILLS
# =========================
KNOWN_SKILLS = {
    "python","java","c++","sql",
    "numpy","pandas","matplotlib","seaborn",
    "scikit-learn","tensorflow","pytorch",
    "git","jupyter","opencv","xgboost",
    "machine learning","deep learning",
    "natural language processing","computer vision"
}

SKILL_ALIASES = {
    "machine learning": ["ml"],
    "deep learning": ["dl"],
    "natural language processing": ["nlp"]
}

def apply_skill_aliases(text):
    text = str(text).lower()

    for canonical, variants in SKILL_ALIASES.items():
        for v in variants:
            text = text.replace(v, canonical)

    return text

def extract_real_skills(text):
    text = normalize_skill_text(text)
    text = apply_skill_aliases(text)
    found = set()

    for skill in KNOWN_SKILLS:
        if skill in text:
            found.add(skill)

    return list(found)


# =========================
# EXPERIENCE
# =========================
ACTION_VERBS = [
    "developed", "built", "designed", "implemented", "created",
    "led", "improved", "increased", "reduced", "optimized",
    "collaborated", "deployed", "trained", "analyzed", "published"
]


def experience_signal(text):
    text = str(text).lower()

    score = 0
    hits = []

    for verb in ACTION_VERBS:
        if verb in text:
            score += 1
            hits.append(verb)

    if score == 0:
        return 0.0, []

    return min(score / 5, 1.0), hits[:6]


# =========================
# PROJECTS
# =========================
PROJECT_KEYWORDS = [
    "project", "model", "system", "pipeline",
    "classification", "prediction", "detection",
    "nlp", "machine learning", "ai"
]


def project_signal(text):
    text = str(text).lower()

    hits = []

    for word in PROJECT_KEYWORDS:
        if word in text:
            hits.append(word)

    if not hits:
        return 0.0, []

    return min(len(hits) / 5, 1.0), hits[:6]


# =========================
# BASELINE (KEEP FOR PIPELINE)
# =========================
DEFAULT_WEIGHTS = {
    "skills": 0.5,
    "experience": 0.25,
    "projects": 0.25
}


def baseline_score_resume(resume_sections, jd_sections, weights=DEFAULT_WEIGHTS):
    explanation = {}
    final_score = 0.0

    for section, weight in weights.items():

        score, words = similarity_with_explanation(
            resume_sections.get(section, ""),
            jd_sections.get(section, "")
        )

        explanation[section] = {
            "score": score,
            "top_matches": words
        }

        final_score += weight * score

    final_score = max(0.0, min(1.0, float(final_score)))
    return final_score, explanation


# =========================
# HYBRID (MAIN MODEL)
# =========================
def hybrid_score_resume(resume_sections, jd_sections, weights=DEFAULT_WEIGHTS):

    explanation = {}
    final_score = 0.0

    # -------------------
    # SKILLS (FIXED)
    # -------------------
    skills_text = resume_sections.get("skills", "")

    # SMART fallback
    if len(skills_text.strip()) < 30:
        skills_text = (
            resume_sections.get("skills", "") + " " +
            resume_sections.get("projects", "") + " " +
            resume_sections.get("experience", "")
        )

    jd_skills_text = jd_sections.get("skills", "")

    resume_skills = extract_real_skills(skills_text)
    jd_skills = extract_real_skills(jd_skills_text)

    overlap = list(set(resume_skills) & set(jd_skills))

    missing_skills = list(set(jd_skills) - set(resume_skills))


    if jd_skills:
        matched = len(overlap)
        total = len(jd_skills)
        missing = total - matched

        match_ratio = matched / total 
        missing_ratio = missing / total

        penalty = 0.3

        skill_score = match_ratio - penalty * missing_ratio
        skill_score = max(0.0, min(1.0, skill_score))
    else:
        skill_score = 0.0
        

    explanation["skills"] = {
        "score": skill_score,
        "matched": overlap[:8],
        "missing": missing_skills[:8]
    }

    final_score += weights["skills"] * skill_score

    # -------------------
    # EXPERIENCE
    # -------------------
    exp_text = resume_sections.get("experience", "")
    exp_score, exp_hits = experience_signal(exp_text)

    explanation["experience"] = {
        "score": exp_score,
        "top_matches": exp_hits
    }

    final_score += weights["experience"] * exp_score

    # -------------------
    # PROJECTS
    # -------------------
    proj_text = resume_sections.get("projects", "")
    proj_score, proj_hits = project_signal(proj_text)

    explanation["projects"] = {
        "score": proj_score,
        "top_matches": proj_hits
    }

    final_score += weights["projects"] * proj_score

    final_score = max(0.0, min(1.0, float(final_score)))
    return final_score, explanation