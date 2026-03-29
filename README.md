# 🚀 AI Resume Matcher (Advanced)

An intelligent AI-powered system that analyzes resumes against job descriptions using **hybrid scoring, section-based parsing, and semantic matching**.

---

## 🔥 Key Features

* 📄 **Resume Parsing (PDF + OCR support)**
* 🧠 **Section-Based Analysis**

  * Skills
  * Experience
  * Projects
* ⚡ **Hybrid Scoring System**

  * Keyword Matching
  * Semantic Similarity
* 🤖 **NLP-powered Matching**
* 📊 **Final Match Score with Insights**
* ❗ **Missing Skills Detection**
* 🎯 Clean and Interactive **Streamlit UI**

---

## 🧠 How It Works

1. Extract text from resume (PDF / OCR fallback)
2. Clean and preprocess text
3. Extract structured sections:

   * Skills
   * Experience
   * Projects
4. Compare with Job Description using:

   * Keyword overlap
   * Semantic similarity (Sentence Transformers)
5. Generate:

   * Final Score
   * Match Summary
   * Missing Skills

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Scikit-learn
* Sentence Transformers
* Pandas, NumPy
* PDFPlumber
* PyTesseract (OCR)

---

## 📂 Project Structure

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
git clone (https://github.com/subesh-cse/ai-resume-matcher-advanced.git)
cd ai-resume-matcher-advanced

pip install -r requirements.txt
streamlit run app.py



## 🔥 Future Improvements

* Deep Learning-based scoring
* Fine-tuned embeddings for hiring
* ATS-style ranking system
* Multi-resume comparison
* Deploy with API backend

---

## 💡 Why This Project?

Most resume matchers rely only on keyword matching (fragile).
This system improves accuracy using:

* Section-aware parsing
* Hybrid scoring
* Semantic understanding

---

## 👨‍💻 Author

**Subesh**
Machine Learning Enthusiast | Building real-world AI systems 🚀
