import streamlit as st
import os
import sys
import re

sys.path.append(os.path.abspath("."))

from src.pipeline import analyze_resume
from src.pdf_reader import read_pdf
from src.ocr_reader import read_image_pdf

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🧠 Intelligent Resume Hiring System")

# =========================================================
# TABS
# =========================================================
tab1, tab2 = st.tabs(["👤 Candidate Mode", "🏢 Recruiter Mode"])

# =========================================================
# 🟢 CANDIDATE MODE
# =========================================================
with tab1:

    st.subheader("📄 Resume Input")

    uploaded_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"],
        key="single_upload"
    )

    resume_text_input = st.text_area(
        "OR paste resume text",
        height=250,
        key="resume_text_input"
    )

    st.subheader("🧾 Job Description")

    jd_text = st.text_area(
        "Paste Job Description",
        height=200,
        key="candidate_jd"
    )

    mode = st.radio(
        "Scoring Mode",
        ["hybrid", "baseline"],
        index=0,
        key="scoring_mode"
    )

    # -------------------------
    # HELPERS
    # -------------------------
    def interpret_score(score):
        if score >= 0.75:
            return "🟢 Strong Match — Excellent fit"
        elif score >= 0.60:
            return "🟡 Good Match — Strong potential"
        elif score >= 0.45:
            return "🟠 Moderate Match — Some gaps"
        else:
            return "🔴 Low Match — Needs improvement"

    def build_summary(explanation):
        points = []

        if explanation["skills"]["score"] > 0.2:
            points.append("Strong skills overlap")
        if explanation["experience"]["score"] > 0.5:
            points.append("Relevant experience signals")
        if explanation["projects"]["score"] > 0.5:
            points.append("Project relevance detected")

        if not points:
            return "Limited alignment detected."

        return "Candidate shows: " + ", ".join(points) + "."

    # -------------------------
    # SKILL ENGINE
    # -------------------------
    TECH_PHRASES = [
        "machine learning",
        "deep learning",
        "data science",
        "natural language processing",
        "computer vision",
        "scikit-learn"
    ]

    TECH_SKILLS = {
        "python","sql","tensorflow","pytorch","sklearn","pandas","numpy",
        "aws","gcp","docker","kubernetes","flask","fastapi",
        "statistics","matplotlib","seaborn","xgboost","opencv",
        "git","jupyter","spark","airflow","llm","transformers"
    }

    def normalize_text(text):
        return re.sub(r'[^a-z0-9\s]', ' ', text.lower())

    def normalize_matched(matched_skills):
        clean = set()
        for m in matched_skills:
            if isinstance(m, tuple):
                clean.add(m[0].lower())
            else:
                clean.add(str(m).lower())
        return clean

    def find_missing_skills(jd_text, matched_skills):
        jd_clean = normalize_text(jd_text)
        matched = normalize_matched(matched_skills)

        missing = []

        for phrase in TECH_PHRASES:
            if phrase in jd_clean and phrase not in matched:
                missing.append(phrase)

        words = set(jd_clean.split())

        for word in words:
            if word in TECH_SKILLS and word not in matched:
                missing.append(word)

        return list(dict.fromkeys(missing))[:8]

    # -------------------------
    # ANALYZE BUTTON
    # -------------------------
    if st.button("Analyze Resume", key="analyze_single"):

        resume_text = ""

        if uploaded_file is not None:
            resume_text = read_pdf(uploaded_file)

            if len(resume_text.strip()) < 200:
                st.warning("Scanned PDF detected → running OCR...")
                uploaded_file.seek(0)
                resume_text = read_image_pdf(uploaded_file)

            st.success("Resume loaded successfully")

        elif resume_text_input.strip():
            resume_text = resume_text_input
        else:
            st.warning("Upload resume")
            st.stop()

        if not jd_text.strip():
            st.warning("Paste job description")
            st.stop()

        score, explanation = analyze_resume(resume_text, jd_text, mode=mode)

        st.subheader("🎯 Final Match Score")
        st.progress(min(score, 1.0))
        st.markdown(f"### {round(score,3)}")
        st.markdown(interpret_score(score))

        st.divider()

        st.subheader("📝 Match Summary")
        st.info(build_summary(explanation))

        matched = explanation["skills"]["top_matches"]
        missing = find_missing_skills(jd_text, matched)

        if missing:
            st.subheader("❗ Missing Skills")
            for m in missing:
                st.write("-", m)

        st.divider()

        if explanation["skills"]["top_matches"]:
            st.subheader("🧠 Skills Match")
            for m in explanation["skills"]["top_matches"]:
                word = m[0] if isinstance(m, tuple) else m
                st.write("-", word)

        if explanation["experience"]["top_matches"]:
            st.subheader("💼 Experience")
            for m in explanation["experience"]["top_matches"]:
                st.write("-", m)

        if explanation["projects"]["top_matches"]:
            st.subheader("🚀 Projects")
            for m in explanation["projects"]["top_matches"]:
                st.write("-", m)


# =========================================================
# 🔵 RECRUITER MODE (FIXED + PERSISTENT)
# =========================================================
with tab2:

    st.subheader("Upload Multiple Resumes")

    multi_files = st.file_uploader(
        "Upload multiple resumes",
        type=["pdf"],
        accept_multiple_files=True,
        key="multi_upload"
    )

    jd_multi = st.text_area(
        "Paste Job Description",
        height=200,
        key="recruiter_jd"
    )

    # Initialize session state
    if "ranking_results" not in st.session_state:
        st.session_state.ranking_results = None

    # Rank button
    if st.button("Rank Candidates", key="rank_button"):

        if not multi_files:
            st.warning("Upload resumes")
            st.stop()

        if not jd_multi.strip():
            st.warning("Paste job description")
            st.stop()

        results = []

        for file in multi_files:

            resume_text = read_pdf(file)

            if len(resume_text.strip()) < 200:
                file.seek(0)
                resume_text = read_image_pdf(file)

            score, explanation = analyze_resume(resume_text, jd_multi)

            results.append({
                "name": file.name,
                "score": score,
                "explanation": explanation
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)

        st.session_state.ranking_results = results

    # Display results if they exist
    if st.session_state.ranking_results:

        results = st.session_state.ranking_results

        st.subheader("🏆 Candidate Ranking")

        for idx, r in enumerate(results, 1):
            st.write(f"**{idx}. {r['name']} — Score: {round(r['score'],3)}**")

        st.divider()

        selected = st.selectbox(
            "View Candidate Details",
            [r["name"] for r in results],
            key="candidate_select"
        )

        for r in results:
            if r["name"] == selected:

                st.write("### Skills")
                for m in r["explanation"]["skills"]["top_matches"]:
                    word = m[0] if isinstance(m, tuple) else m
                    st.write("-", word)

                st.write("### Experience")
                for m in r["explanation"]["experience"]["top_matches"]:
                    st.write("-", m)

                st.write("### Projects")
                for m in r["explanation"]["projects"]["top_matches"]:
                    st.write("-", m)