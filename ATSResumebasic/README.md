## ATS Resume Analyzer (Flask Application)

This project is an ATS-style resume analysis system built using Python, NLP techniques, TF-IDF similarity, fuzzy skill matching, and a weighted scoring model. It evaluates how well a candidate’s resume matches a given Job Description (JD) and generates a detailed compatibility score.

This improved version extends a simple baseline system by adding semantic similarity, weighted scoring, OCR handling, and richer skill detection.

🚀 Features
## 1. PDF Text Extraction

Extracts text from digital PDFs using PyMuPDF

Automatically falls back to OCR (Tesseract) for scanned PDFs

## 2. TF-IDF Semantic Similarity

Measures semantic similarity between resume and JD

Uses unigrams & bigrams

Displays shared TF-IDF keywords

Outputs similarity score (0–100%)

## 3. Fuzzy Skill Matching

Detects skills even with typos or wording variations

Uses fuzzy.partial_ratio

Extracts and compares skills from resume + JD

## 4. Weighted Skill Scoring

Technical & soft skills have different weights

Important skills (Python, SQL, ML, etc.) increase score more

Produces a Boost Score (0–100)

## 5. Final ATS Score

A combined score based on:

Component	Weight
TF-IDF Similarity	30%
Skill Match %	50%
Weighted Boost Score	20%

Final output → 0–100 ATS Match Score

## 6. Flask Web Interface

Upload a PDF resume

Paste a Job Description

View results:

TF-IDF similarity

Matched & missing skills

Weighted scoring

Boost score

Final ATS Score

Common terms

 # Project Structure
ats_project/
│── app1.py
│── requirements.txt
│── README.md
│
├── templates/
│     ├── index.html
│     └── result.html
│
├── static/
│
├── uploads/          # auto-created for uploaded PDFs
│
└── datasets/
      ├── weak_resume.pdf
      ├── average_resume.pdf
      ├── strong_resume.pdf
      └── job_description.pdf

🛠️ How the System Works (Pipeline)

User uploads resume (PDF)

Text extracted (direct or OCR)

JD text is cleaned + normalized

TF-IDF similarity calculation

Skills extracted + fuzzy-matched

Weighted scoring applied

Final ATS Score computed

All results shown in browser

## Installation
Clone the project
git clone <your-repo-url>
cd ats_project

## Install dependencies
pip install -r requirements.txt

Run the Flask app
python app1.py

## Open in browser
http://127.0.0.1:5000

## Datasets

This project uses example resumes and a sample job description for testing.
All dataset files are stored in the datasets/ folder.

Included Files

# weak_resume.pdf

# average_resume.pdf

# strong_resume.pdf

# job_description.pdf

You can add your own resumes or job descriptions to test the ATS model.