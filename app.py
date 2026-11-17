
from dotenv import load_dotenv
load_dotenv()

import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai


# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="ResumeIQ | ATS Resume Tracker",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ----------------------------------
# GEMINI CONFIGURATION
# ----------------------------------

API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)


def get_gemini_response(input_prompt, pdf_content, job_description):

    model = genai.GenerativeModel('gemini-3.8-flash')

    response = model.generate_content([
        input_prompt,
        pdf_content[0],
        job_description
    ])

    return response.text


# ----------------------------------
# PDF PROCESSING
# ----------------------------------

def input_pdf_setup(uploaded_file):

    if uploaded_file is not None:

        images = pdf2image.convert_from_bytes(
            uploaded_file.getvalue()
        )

        first_page = images[0]

        img_byte_arr = io.BytesIO()

        first_page.save(img_byte_arr, format='JPEG')

        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(
                    img_byte_arr
                ).decode()
            }
        ]

        return pdf_parts

    else:
        raise FileNotFoundError("No file uploaded")


# ----------------------------------
# CUSTOM CSS
# ----------------------------------

st.markdown("""
<style>

/* Main application background */

.stApp {
    background:
        radial-gradient(
            circle at 15% 10%,
            rgba(124, 58, 237, 0.12),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #0B1020 0%,
            #111827 55%,
            #101426 100%
        );

    color: #F8FAFC;
}

/* Main container */

.block-container {
    max-width: 900px;
    padding-top: 1rem;
    padding-bottom: 1rem;
}
/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Headings */

h1, h2, h3 {
    color: #F8FAFC !important;
    font-family: 'Inter', sans-serif;
}

/* Header */

.hero {
    text-align: center;
    padding: 20px 10px 30px 10px;
}

.brand-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin-bottom: 12px;
}

.logo-box {
    background: linear-gradient(135deg, #7C3AED, #A78BFA);
    width: 48px;
    height: 48px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 25px;
    margin: 0;
}

.hero-title {
    font-size: 38px;
    font-weight: 750;
    letter-spacing: -1.5px;
    color: #F8FAFC;
    margin: 0;
}

.hero-subtitle {
    color: #9CA3AF;
    font-size: 15px;
    margin-bottom: 12px;
}

.hero-tag {
    color: #C4B5FD;
    font-size: 12px;
    background: rgba(139, 92, 246, 0.12);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: 20px;
    padding: 6px 14px;
    display: inline-block;
}

/* Section headings */

.section-heading {
    color: #E5E7EB;
    font-size: 16px;
    font-weight: 650;
    margin-top: 18px;
    margin-bottom: 10px;
}

/* Input fields */

.stTextArea textarea {
    background-color: #171E30 !important;
    color: #F8FAFC !important;
    border: 1px solid #303B52 !important;
    border-radius: 12px !important;
    font-size: 14px !important;
}

.stTextArea textarea:focus {
    border: 1px solid #8B5CF6 !important;
    box-shadow: 0 0 0 1px #8B5CF6 !important;
}

/* File uploader */

[data-testid="stFileUploader"] {
    background: #171E30;
    border: 1px dashed #6D5BA6;
    border-radius: 14px;
    padding: 15px;
}

[data-testid="stFileUploader"] section {
    background: transparent;
}

[data-testid="stFileUploader"] label {
    color: #E5E7EB !important;
}

/* Buttons */

.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 10px;
    background: #171E30;
    border: 1px solid #39445C;
    color: #E5E7EB;
    font-weight: 600;
    font-size: 13px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #35245B;
    border-color: #8B5CF6;
    color: white;
    transform: translateY(-2px);
}

/* Analysis result */

.result-card {
    background: #171E30;
    border: 1px solid #39445C;
    border-radius: 14px;
    padding: 22px;
    margin-top: 15px;
    margin-bottom: 15px;
}

.result-heading {
    color: #C4B5FD;
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 12px;
}

/* Success messages */

.stAlert {
    border-radius: 10px;
}

/* Divider */

hr {
    border-color: #303B52 !important;
    margin-top: 25px;
    margin-bottom: 25px;
}

/* Footer */

.custom-footer {
    text-align: center;
    color: #6B7280;
    font-size: 12px;
    padding-top: 35px;
}

/* Compact layout */

.section-heading {
    margin-top: 8px;
    margin-bottom: 6px;
    font-size: 14px;
}

[data-testid="stFileUploader"] {
    padding: 8px;
}

.stButton > button {
    min-height: 42px;
}

hr {
    margin-top: 12px !important;
    margin-bottom: 12px !important;
}

.hero-subtitle {
    margin-bottom: 6px;
}
/* Keep Streamlit toolbar and Deploy button visible */
[data-testid="stHeader"] {
    background: transparent;
}

/* Remove excess top spacing */
.block-container {
    padding-top: 0.5rem !important;
}
</style>
""", unsafe_allow_html=True
)


# ----------------------------------
# HEADER
# ----------------------------------

st.markdown("""
<div style="text-align:center;padding:5px 0 12px 0;">

<div style="display:flex; align-items:center; justify-content:center; gap:14px; margin-bottom:15px;">

<div style="background:linear-gradient(135deg,#7C3AED,#A78BFA); width:48px; height:48px; border-radius:13px; display:flex; align-items:center; justify-content:center; font-size:25px;">
📄
</div>

<div style="font-size:38px; font-weight:750; color:#F8FAFC; letter-spacing:-1.5px;">
ResumeIQ
</div>

</div>

<div style="color:#9CA3AF; font-size:15px;">
Your AI-powered resume analysis companion.
</div>

<div style="color:#9CA3AF; font-size:15px; margin-top:5px;">
Get insights. Identify skill gaps. Get job-ready.
</div>

<div style="margin-top:18px;">
<span style="color:#C4B5FD; background:rgba(139,92,246,0.12); border:1px solid rgba(139,92,246,0.3); border-radius:20px; padding:7px 15px; font-size:11px;">
✦ POWERED BY GOOGLE GEMINI AI
</span>
</div>

</div>
""", unsafe_allow_html=True)






# ----------------------------------
# JOB DESCRIPTION
# ----------------------------------

st.markdown(
    '<div class="section-heading">01 &nbsp; Job Description</div>',
    unsafe_allow_html=True
)

input_text = st.text_area(
    "Job Description",
    placeholder="Paste the job description here...\n\nInclude the role, responsibilities, required skills and qualifications for a more useful analysis.",
    height=115,
    key="input",
    label_visibility="collapsed"
)


# ----------------------------------
# RESUME UPLOAD
# ----------------------------------

st.markdown(
    '<div class="section-heading">02 &nbsp; Upload Your Resume</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"],
    label_visibility="collapsed",
    help="Upload your resume in PDF format."
)

if uploaded_file is not None:

    st.success(
        f"✓ Resume uploaded successfully: {uploaded_file.name}"
    )


# ----------------------------------
# ANALYSIS OPTIONS
# ----------------------------------

st.markdown(
    '<div class="section-heading">03 &nbsp; Choose Your Analysis</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    submit1 = st.button(
        "📋 Resume Review",
        use_container_width=True
    )

with col2:
    submit2 = st.button(
        "💡 Skill Improvement",
        use_container_width=True
    )

with col3:
    submit3 = st.button(
        "📊 Match Score",
        use_container_width=True
    )


# ----------------------------------
# ORIGINAL GEMINI PROMPTS
# ----------------------------------

input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an experienced Technical Human Resource Manager and career advisor.
Your task is to review the provided resume against the job description.
Identify the skills and areas where the candidate needs improvement to better match the job requirements.
Mention the missing technical skills, tools, knowledge areas, and any other improvements that would help the candidate become a stronger fit for the role.
Provide your suggestions in a clear and practical manner.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
your task is to evaluate the resume against the provided job description. give me the percentage match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""


# ----------------------------------
# ANALYSIS EXECUTION
# ----------------------------------

analysis_options = {
    submit1: (input_prompt1, "Resume Evaluation"),
    submit2: (input_prompt2, "Skill Improvement Recommendations"),
    submit3: (input_prompt3, "Resume Match Analysis")
}

selected = None

if submit1:
    selected = (input_prompt1, "Resume Evaluation")

elif submit2:
    selected = (input_prompt2, "Skill Improvement Recommendations")

elif submit3:
    selected = (input_prompt3, "Resume Match Analysis")


if selected:

    if not API_KEY:

        st.error(
            "Google Gemini API key not found. "
            "Please check your .env file."
        )

    elif uploaded_file is None:

        st.warning("Please upload your resume before proceeding.")

    elif not input_text.strip():

        st.warning("Please enter the job description before proceeding.")

    else:

        prompt, result_title = selected

        try:

            with st.spinner(
                "Gemini AI is analysing your resume... Please wait."
            ):

                pdf_content = input_pdf_setup(uploaded_file)

                response = get_gemini_response(
                    prompt,
                    pdf_content,
                    input_text
                )

            st.markdown("---")

            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-heading">
                        ✦ {result_title}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(response)

        except Exception as e:

            st.error(
                f"Something went wrong during analysis: {str(e)}"
            )


# ----------------------------------
# FOOTER
# ----------------------------------

st.markdown("""
<div class="custom-footer">
    Built with Python, Streamlit & Google Gemini AI
    <br><br>
    ResumeIQ · AI-powered Resume Analysis
</div>
""", unsafe_allow_html=True)
