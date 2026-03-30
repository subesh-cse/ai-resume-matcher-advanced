# 🚀 AI Resume Matcher (Advanced)

[![Live App](https://img.shields.io/badge/🚀%20Live%20App-Click%20Here-brightgreen?style=for-the-badge)](https://ai-resume-matcher-advanced-vvbmj5aoxivw4kv83rnxv7.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge)]
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge)]
[![ML](https://img.shields.io/badge/Machine%20Learning-Enabled-orange?style=for-the-badge)]

---

## 🚀 Live Demo

👉 **[Try the Live App](https://ai-resume-matcher-advanced-vvbmj5aoxivw4kv83rnxv7.streamlit.app/)**

---

## 🧠 Overview

An intelligent AI-powered system that analyzes resumes against job descriptions using **hybrid scoring, section-based parsing, and semantic matching**.

Unlike traditional keyword matchers, this system combines **NLP + structured understanding** to produce more reliable and meaningful results.

> ⚡ Designed to simulate real-world hiring workflows with explainable AI scoring.

---

## 🔥 Key Features

- 📄 Resume Parsing (PDF + OCR support)
- 🧠 Section-Based Analysis
  - Skills
  - Experience
  - Projects
- ⚡ Hybrid Scoring System
  - Keyword Matching
  - Semantic Similarity (Sentence Transformers)
- 🤖 NLP-powered Matching
- 📊 Final Match Score with Explanation
- ❗ Missing Skills Detection
- 🎯 Recruiter + Candidate Modes

---

## ⚙️ How It Works

1. Extract text from resume (PDF / OCR fallback)  
2. Clean and preprocess text  
3. Extract structured sections:
   - Skills
   - Experience
   - Projects  
4. Compare with Job Description using:
   - Keyword overlap  
   - Semantic similarity  
5. Generate:
   - Final Score  
   - Match Summary  
   - Missing Skills  

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- Scikit-learn  
- Sentence Transformers  
- Pandas, NumPy  
- PDFPlumber  
- EasyOCR
- PyMuPDF  

---

## 📁 Project Structure

```
ai-resume-matcher-advanced/
│
├── app.py
├── requirements.txt
├── .gitignore
│
└── src/
    ├── pipeline.py
    ├── scorer.py
    ├── semantic_matcher.py
    ├── section_extractor.py
    ├── text_cleaning.py
    ├── pdf_reader.py
    └── ocr_reader.py
```

---

## 🚀 Run Locally

```bash
git clone https://github.com/subesh-cse/ai-resume-matcher-advanced.git
cd ai-resume-matcher-advanced

pip install -r requirements.txt
streamlit run app.py
```

---

## 💡 Why This Project?

Most resume matchers rely only on **keyword matching (fragile)**.

This system improves accuracy using:

- Section-aware parsing  
- Hybrid scoring  
- Semantic understanding  

---

## 🔮 Future Improvements

- Deep Learning-based scoring  
- Fine-tuned embeddings for hiring  
- ATS-style ranking system  
- Multi-resume comparison  
- Backend API deployment  

---

## 👨‍💻 Author

**Subesh**  
Aspiring ML Engineer | Building real-world AI systems 🚀  

---

⭐ If you found this useful, consider giving it a star!
