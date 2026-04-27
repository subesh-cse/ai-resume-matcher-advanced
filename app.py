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

    def build_summary(score, explanation):
        
        if score >= 0.75:
            return "🟢 Strong alignment with job requirements. Candidate demonstrates relevant skills and solid project experience."
    
        elif score >= 0.60:
            return "🟡 Good alignment with key skills, but some important gaps are present."
    
        elif score >= 0.40:
            return "🟠 Partial match. Candidate has some relevant skills but lacks several required areas."
    
        else:
            return "🔴 Low alignment. Significant skill gaps for this role."
   

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
        st.info(build_summary(score, explanation))


        st.divider()

        if explanation["skills"]["matched"]:
            st.subheader("🧠 Matched Skills")
            for m in explanation["skills"]["matched"]:
                word = m[0] if isinstance(m, tuple) else m
                st.write("-", word)

        if explanation["skills"]["missing"]:
            st.subheader("❗ Missing Skills")
            for m in explanation["skills"]["missing"]:
                 st.write("-", m)

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
                for m in r["explanation"]["skills"]["matched"]:
                    word = m[0] if isinstance(m, tuple) else m
                    st.write("-", word)

                st.write("### ❗ Missing Skills")
                for m in r["explanation"]["skills"]["missing"]:
                    st.write("-", m)

                st.write("### Projects")
                for m in r["explanation"]["projects"]["top_matches"]:
                    st.write("-", m)