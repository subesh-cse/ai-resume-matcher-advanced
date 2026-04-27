# 🧠 Intelligent AI Resume Analyzer

An advanced AI-powered system that analyzes resumes against job descriptions using **hybrid scoring**, **section extraction**, and **semantic matching**.

---

## 🚀 Features

- 📄 Resume parsing (PDF + text)
- 🧠 Hybrid scoring (skills + projects + experience)
- 🔍 Section-wise analysis (skills, projects, experience)
- ⚡ Semantic matching for deeper understanding
- ❌ Missing skills detection
- 📊 Final match score with explanation
- 🌐 Streamlit web interface

---

## 🧱 Tech Stack

- Python
- Streamlit
- Scikit-learn
- NLP techniques (TF-IDF, similarity)
- PyMuPDF (fitz)
- EasyOCR

---

## ⚙️ How It Works

1. Resume is parsed and cleaned
2. Sections are extracted (skills, projects, experience)
3. Job description is processed
4. Hybrid scoring is applied:
   - Skill matching
   - Project relevance
   - Experience signals
5. Final score is generated
6. Missing skills are identified

---

## 📊 Output

- Final match score
- Match summary
- Matched skills
- Missing skills
- Project & experience insights

---

## 🌐 Live Demo

👉 [Add your deployed link here]

---

## 📁 Project Structure

```bash
ai-resume-matcher-advanced/
│
├── app.py
├── requirements.txt
├── src/
│   ├── scorer.py
│   ├── section_extractor.py
│   ├── semantic_matcher.py
│   ├── pipeline.py
│   ├── pdf_reader.py
│   ├── ocr_reader.py
│   └── text_cleaning.py
```


---

## 📌 Future Improvements

- Better resume parsing for complex formats
- More robust skill extraction
- Model-based semantic matching (LLMs)
- Resume feedback suggestions

---

## 👨‍💻 Author

Subesh  
