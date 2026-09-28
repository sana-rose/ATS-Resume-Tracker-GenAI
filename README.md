# ATS Resume Tracker – GenAI

An AI-powered resume analysis application built using Python, Streamlit, and Google's Gemini API. It analyzes a resume against a job description and provides AI-generated feedback.

## Features

- Upload a resume in PDF format
- Enter a job description
- Get an AI-based resume evaluation
- Identify skills that need improvement
- Generate an ATS-style percentage match
- Identify missing keywords

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- PDF2Image
- python-dotenv
- Pillow

## How It Works

Job Description + Resume PDF  
↓  
PDF Processing  
↓  
Gemini API  
↓  
AI Resume Analysis  
↓  
Evaluation / Skill Improvement / ATS Match

## Setup

Clone the repository and install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your Gemini API key:

```text
GOOGLE_API_KEY=your_gemini_api_key
```

Run the application:

```bash
streamlit run app.py
```

## Learning Outcomes

- Generative AI and LLM integration
- Gemini API
- Prompt engineering
- PDF processing
- Multimodal AI
- Streamlit application development
- API key management using environment variables

## Future Improvements

- Multi-page resume processing
- Improved ATS scoring
- Resume optimization suggestions
