"""
Advanced ATS Analyzer - Flask Application
This project implements an ATS-style resume analysis system using:

- PDF text extraction (PyMuPDF + OCR fallback).
- TF-IDF vectorization for semantic similarity between resume & job description.
- Fuzzy skill matching (partial_ratio) for robust skill detection
- Weighted scoring system (TF-IDF + skill coverage + skill weights).
- Extraction of common overlapping TF-IDF terms.
- Flask web interface for uploading resumes and displaying results.

This file represents the improved version of the ATS system, extending
the baseline by adding semantic similarity, fuzzy matching, and weighted scoring.
"""
import re
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# Flask Configuration
app = Flask(__name__)
app.secret_key = "dev-secret"
# Directory for temporarily storing uploaded resumes
BASE_DIR = Path(__file__).parent.resolve()
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)



# Large Skill Dictionary (90+ Skills)
SKILLS = {
    # Core Programming
    "python": 5,
    "java": 3,
    "c++": 3,
    
    # Data Analysis & Processing
    "pandas": 5,
    "numpy": 5,
    "data analysis": 5,
    "data cleaning": 4,
    "data preprocessing": 4,
    
    # Machine Learning
    "machine learning": 5,
    "ml": 5,
    "deep learning": 4,
    "neural networks": 4,
    "scikit-learn": 4,
    "sklearn": 4,

    # Visualization Tools
    "matplotlib": 3,
    "seaborn": 3,
    "power bi": 4,
    "tableau": 4,
    "data visualization": 4,
    "dashboard": 3,
    
    # Databases
    "sql": 5,
    "mysql": 3,
    "postgresql": 3,
    "postgres": 3,
    "sql server": 4,
    "database": 3,
    
    # BI / Analysis
    "excel": 3,
    "advanced excel": 4,
    "vlookup": 2,
    "pivot table": 2,
    
    # Cloud & Deployment
    "aws": 3,
    "azure": 3,
    "gcp": 2,
    "api": 2,
    "rest api": 3,
    "flask": 3,
    
    # Notebooks & Version Control
    "jupyter": 2,
    "jupyter notebook": 2,
    "git": 3,
    "github": 2,
    
    # AI / NLP (Light)
    "nlp": 3,
    "computer vision": 3,
    
    # Soft & Supportive Skills
    "communication": 1,
    "teamwork": 1,
    "problem solving": 2,
    "critical thinking": 2,
}



# Clean and normalize text for NLP processing.
##steps: Ensure text is not none, convert to lowercase, remove extra spaces
def preprocess(text: str) -> str:
    
    if not text:
        return ""
    return " ".join(text.lower().split())



###Extract text from a PDF resume.
def extract_text(path: str) -> str:
    
    text = ""

    # Step 1 — Try PyMuPDF
    try:
        doc = fitz.open(path)
        for page in doc:
            text += page.get_text()
    except:
        text = ""

    text = preprocess(text)

    # If text seems enough → good PDF
    if len(text) > 200:
        return text

    # Step 2 — OCR fallback
    print("Low text detected, switching to OCR...")
    ocr_text = ""
    try:
        images = convert_from_path(path, dpi=200)
        for img in images:
            ocr_text += pytesseract.image_to_string(img)
    except Exception as e:
        print("OCR error:", e)

    return preprocess(ocr_text)


# TF-IDF Similarity

def tfidf_ats_score(resume_text: str, jd_text: str) -> dict:
    """
    Compute semantic similarity between resume and job description using TF-IDF.

    Process:Clean text,Use TfidfVectorizer with unigrams + bigrams,Fit vectorizer on both texts together,Compute cosine similarity,Extract common TF-IDF terms that appear in both texts
    Returns:
        {
            "score": similarity * 100,
            "raw_score": cosine similarity (0-1),
            "common_terms": list of shared important terms
        }
    """
    resume_clean = preprocess(resume_text)
    jd_clean = preprocess(jd_text)

    if not resume_clean or not jd_clean:
        return {"score": 0.0, "raw_score": 0.0, "common_terms": []}

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([jd_clean, resume_clean])

    jd_vec = tfidf_matrix[0:1]
    res_vec = tfidf_matrix[1:2]

    sim = cosine_similarity(jd_vec, res_vec)[0][0]
    score_percent = round(float(sim) * 100, 2)

    # Extract important common words
    feature_names = np.array(vectorizer.get_feature_names_out())
    jd_weights = jd_vec.toarray()[0]
    res_weights = res_vec.toarray()[0]

    mask = (jd_weights > 0) & (res_weights > 0)
    terms = feature_names[mask]
    jd_w = jd_weights[mask]
    res_w = res_weights[mask]

    idx = np.argsort(-jd_w)

    common = []
    for i in idx[:15]:
        common.append((terms[i], round(float(jd_w[i]), 4), round(float(res_w[i]), 4)))

    return {"score": score_percent, "raw_score": float(sim), "common_terms": common}



# Skill Extraction
def extract_skills_from_text(text: str, threshold: int = 75) -> set:
    """
    Identify skills present in text using two methods:

    1. Exact match (e.g., "python" in text)
    2. Fuzzy partial matching using fuzz.partial_ratio()

    threshold:
        Minimum fuzzy score required to consider a skill matched.
        Default = 75 for balanced precision/recall.

    Returns:
        A set of detected skills as strings.
    """    
    text = text.lower()
    found = set()

    for skill in SKILLS:
        # Exact match
        if skill in text:
            found.add(skill)
            continue

        # Fuzzy match (partial ratio)
        ratio = fuzz.partial_ratio(skill, text)
        if ratio >= threshold:
            found.add(skill)

    return found





# Skill Match Score

def skill_match_score(resume_skills: set, jd_skills: set) -> float:
    """
    Calculate the % of JD-required skills present in the resume.

    Formula:
        (matched_skills / total_jd_skills) * 100

    This gives a simple but informative measure of keyword alignment.
    """
    if not jd_skills:
        return 0.0
    matched = resume_skills.intersection(jd_skills)
    return round((len(matched) / len(jd_skills)) * 100, 2)



# Compute a weighted skill boost score.Uses the weight dictionary

def weighted_boost(resume_skills: set) -> float:
    boost = sum(SKILLS.get(skill, 0) for skill in resume_skills)
    return min(boost, 100)



# Final Advanced ATS Score

def advanced_score(tfidf_score, skill_score, boost_score):
    """
    Combine all three scoring components:

    TF-IDF similarity   → 30%
    Skill match %       → 50%
    Skill weight boost  → 20%

    This weighted sum gives the final ATS score (0–100).
    """
    return round(
        (tfidf_score * 0.3) +
        (skill_score * 0.5) +
        (boost_score * 0.2),
        2
    )

# --------------------------
# BAR CHART (Matched vs Missing)
# --------------------------
def plot_skill_barchart(matched, missing):
    labels = ["Matched", "Missing"]
    values = [len(matched), len(missing)]

    plt.figure(figsize=(5,4))
    plt.bar("Matched", len(matched), color="green")
    plt.bar("Missing", len(missing), color="red")
    plt.title("Matched vs Missing Skills")
    plt.ylabel("Count")
    plt.tight_layout()

    # Ensure static/charts exists
    charts_dir = BASE_DIR / "static" / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    # Save chart
    chart_path = charts_dir / "skills_chart.png"
    plt.savefig(chart_path)
    plt.close()

    # Return relative path for Flask
    return "charts/skills_chart.png"



# Flask Routes

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Handle resume upload + ATS analysis.

    Steps:
    1. Validate resume PDF + JD text
    2. Save uploaded file
    3. Extract text from PDF
    4. Compute TF-IDF similarity
    5. Extract skills from resume and JD
    6. Compute:
        - skill match %
        - weighted boost score
        - final ATS score
    7. Render result.html with all results

    This is the main endpoint used by the web interface.
    """

    if "resume" not in request.files or request.files["resume"].filename == "":
        flash("Please upload a PDF resume.")
        return redirect(url_for("index"))

    resume_file = request.files["resume"]
    jd_text = request.form.get("job_description", "").strip()

    if not jd_text:
        flash("Please paste a job description.")
        return redirect(url_for("index"))

    filename = resume_file.filename
    save_path = UPLOAD_DIR / filename
    resume_file.save(str(save_path))

    # Extract text##
    resume_text = extract_text(str(save_path))
    

    # TF-IDF Score
    tfidf_result = tfidf_ats_score(resume_text, jd_text)
    tfidf_score = tfidf_result["score"]

    # Skills
    resume_skills = extract_skills_from_text(resume_text)
    jd_skills = extract_skills_from_text(jd_text)
    matched_skills = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills
    chart_url = plot_skill_barchart(matched_skills, missing)
   
    # Skill Matching Score
    skill_score = skill_match_score(resume_skills, jd_skills)

    # Weight Boost
    boost_score = weighted_boost(resume_skills)

    # Final Score
    final_score = advanced_score(tfidf_score, skill_score, boost_score)

    # Render Result Page
    return render_template(
        "result.html",
        final_score=final_score,
        tfidf_score=tfidf_score,
        skill_score=skill_score,
        boost_score=boost_score,
        resume_skills=resume_skills,
        common_terms=tfidf_result["common_terms"],
        resume_preview=resume_text[:800],
        jd_text=jd_text,
        chart_url=chart_url,
      
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
