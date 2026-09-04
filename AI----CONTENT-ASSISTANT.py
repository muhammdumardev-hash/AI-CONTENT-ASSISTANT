import os
import streamlit as st
from groq import Groq

# ============================================================
# CONFIG
# ============================================================
GROQ_MODEL = "openai/gpt-oss-120b"

st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered",
)

# ============================================================
# STYLING — Premium Glassmorphism UI
# ============================================================
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Animated gradient background */
        .stApp {
            background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
            background-size: 400% 400%;
            animation: gradientShift 18s ease infinite;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Floating glow orbs */
        .stApp::before {
            content: "";
            position: fixed;
            top: -10%;
            left: -10%;
            width: 40%;
            height: 40%;
            background: radial-gradient(circle, rgba(139,92,246,0.25) 0%, transparent 70%);
            filter: blur(60px);
            z-index: 0;
            pointer-events: none;
            animation: floatOrb1 12s ease-in-out infinite;
        }

        .stApp::after {
            content: "";
            position: fixed;
            bottom: -10%;
            right: -10%;
            width: 45%;
            height: 45%;
            background: radial-gradient(circle, rgba(236,72,153,0.2) 0%, transparent 70%);
            filter: blur(70px);
            z-index: 0;
            pointer-events: none;
            animation: floatOrb2 14s ease-in-out infinite;
        }

        @keyframes floatOrb1 {
            0%, 100% { transform: translate(0, 0); }
            50% { transform: translate(30px, 40px); }
        }

        @keyframes floatOrb2 {
            0%, 100% { transform: translate(0, 0); }
            50% { transform: translate(-30px, -30px); }
        }

        .block-container {
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 760px;
            position: relative;
            z-index: 1;
        }

        /* Hero header */
        .hero-wrap {
            text-align: center;
            padding: 30px 20px 10px 20px;
        }

        .hero-badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 999px;
            background: rgba(139, 92, 246, 0.15);
            border: 1px solid rgba(139, 92, 246, 0.35);
            color: #c4b5fd;
            font-size: 12.5px;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 18px;
            backdrop-filter: blur(10px);
        }

        .main-title {
            font-family: 'Poppins', sans-serif;
            font-size: 46px;
            font-weight: 800;
            margin-bottom: 6px;
            background: linear-gradient(90deg, #a78bfa, #f472b6, #60a5fa);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: shine 6s linear infinite;
        }

        @keyframes shine {
            to { background-position: 200% center; }
        }

        .subtitle {
            color: rgba(255,255,255,0.65);
            font-size: 16.5px;
            margin-bottom: 10px;
            font-weight: 400;
        }

        /* Glass card wrapper for containers */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(18px) !important;
            -webkit-backdrop-filter: blur(18px) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 20px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35) !important;
            padding: 8px !important;
        }

        /* Section labels */
        .section-label {
            font-family: 'Poppins', sans-serif;
            font-size: 15px;
            font-weight: 700;
            color: #e9d5ff;
            margin-top: 4px;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Inputs styling */
        .stTextInput input, .stTextArea textarea {
            background: rgba(255,255,255,0.06) !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            border-radius: 12px !important;
            color: #f1f5f9 !important;
        }

        .stTextInput input:focus, .stTextArea textarea:focus {
            border: 1px solid rgba(167, 139, 250, 0.7) !important;
            box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15) !important;
        }

        .stTextArea textarea::placeholder, .stTextInput input::placeholder {
            color: rgba(255,255,255,0.35) !important;
        }

        div[data-baseweb="select"] > div {
            background: rgba(255,255,255,0.06) !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            border-radius: 12px !important;
            color: #f1f5f9 !important;
        }

        label, .stSelectbox label, .stTextArea label, .stTextInput label {
            color: rgba(255,255,255,0.85) !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }

        /* Primary button */
        .stButton > button {
            background: linear-gradient(90deg, #8b5cf6, #ec4899) !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 0.75rem 1rem !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            letter-spacing: 0.3px;
            box-shadow: 0 6px 22px rgba(139, 92, 246, 0.45) !important;
            transition: all 0.25s ease !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) scale(1.01);
            box-shadow: 0 10px 28px rgba(236, 72, 153, 0.5) !important;
        }

        .stButton > button:active {
            transform: translateY(0px) scale(0.99);
        }

        /* Download button */
        .stDownloadButton > button {
            background: rgba(255,255,255,0.08) !important;
            color: #e9d5ff !important;
            border: 1px solid rgba(167, 139, 250, 0.4) !important;
            border-radius: 14px !important;
            font-weight: 700 !important;
            padding: 0.7rem 1rem !important;
            transition: all 0.2s ease !important;
        }

        .stDownloadButton > button:hover {
            background: rgba(167, 139, 250, 0.15) !important;
            border-color: rgba(167, 139, 250, 0.8) !important;
        }

        /* Result box */
        .result-card {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(18px);
            border: 1px solid rgba(255,255,255,0.14);
            border-radius: 20px;
            padding: 26px 28px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.35);
            color: #f1f5f9;
            line-height: 1.7;
            animation: fadeInUp 0.5s ease;
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(14px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Success / info / warning / error boxes */
        div[data-testid="stAlert"] {
            border-radius: 14px !important;
            backdrop-filter: blur(10px);
        }

        /* Divider */
        hr {
            border-color: rgba(255,255,255,0.1) !important;
        }

        /* Footer caption */
        .footer-caption {
            text-align: center;
            color: rgba(255,255,255,0.4);
            font-size: 13px;
            margin-top: 6px;
            letter-spacing: 0.3px;
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(167,139,250,0.4); border-radius: 10px; }

        /* Spinner text */
        .stSpinner > div > div {
            border-top-color: #a78bfa !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================
st.markdown(
    """
    <div class="hero-wrap">
        <span class="hero-badge">⚡ POWERED BY GROQ AI</span>
        <div class="main-title">✍️ AI Content Assistant</div>
        <div class="subtitle">Create complete social media content with a caption and relevant hashtags.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# API KEY
# ============================================================
api_key = None

try:
    api_key = st.secrets.get("GROQ_API_KEY")
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    with st.container(border=True):
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="Enter your Groq API key",
            help="You can also store GROQ_API_KEY in Streamlit Secrets.",
        )

if not api_key:
    st.info("Enter your Groq API key to start generating content.")
    st.stop()

# ============================================================
# INPUTS
# ============================================================
with st.container(border=True):
    st.markdown('<div class="section-label">⚙️ Content Settings</div>', unsafe_allow_html=True)

    content_type = st.selectbox(
        "Content Type",
        [
            "Social Media Post",
            "LinkedIn Post",
            "Instagram Post",
            "Facebook Post",
            "X (Twitter) Post",
            "Product Promotion",
            "Educational Post",
            "Blog Introduction",
            "Marketing Copy",
        ],
    )

    platform = st.selectbox(
        "Platform",
        [
            "LinkedIn",
            "Instagram",
            "Facebook",
            "X (Twitter)",
            "TikTok",
            "YouTube",
            "General / Multi-platform",
        ],
    )

    topic = st.text_area(
        "Topic",
        placeholder="Example: Benefits of learning Python for beginners",
        height=100,
    )

    target_audience = st.selectbox(
        "Target Audience",
        [
            "General Audience",
            "Students",
            "Developers / Programmers",
            "Business Professionals",
            "Entrepreneurs",
            "Job Seekers",
            "Content Creators",
            "Marketing Professionals",
            "Tech Enthusiasts",
        ],
    )

    tone = st.selectbox(
        "Tone",
        [
            "Professional",
            "Friendly",
            "Casual",
            "Educational",
            "Persuasive",
            "Inspirational",
            "Humorous",
            "Confident",
        ],
    )

    additional_instructions = st.text_area(
        "Additional Instructions (Optional)",
        placeholder="Example: Keep it concise, include a call-to-action, and avoid emojis.",
        height=80,
    )

st.write("")

# ============================================================
# GENERATION
# ============================================================
if st.button("✨ Generate Content", type="primary", use_container_width=True):

    if not topic.strip():
        st.warning("Please enter a topic first.")
        st.stop()

    prompt = f"""
You are an expert social media content writer.

Create high-quality content using the following requirements:

Content Type: {content_type}
Platform: {platform}
Topic: {topic}
Target Audience: {target_audience}
Tone: {tone}
Additional Instructions: {additional_instructions or "None"}

Return the result in EXACTLY this structure:

POST:
[Write the complete post here.]

CAPTION:
[Write a polished caption suitable for the selected platform.]

HASHTAGS:
[Provide 8-15 relevant hashtags in one line.]

Requirements:
- Make the content natural and human-sounding.
- Match the selected platform and audience.
- Keep the tone consistent.
- Do not invent statistics, studies, quotes, or facts unless they are provided in the topic.
- Make the post engaging and useful.
- Avoid unnecessary filler.
"""

    try:
        client = Groq(api_key=api_key)

        with st.spinner("Generating your content..."):
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional AI content assistant. "
                            "Follow the user's requested output format exactly."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1800,
            )

        result = response.choices[0].message.content

        st.success("Content generated successfully!")

        # ----------------------------------------------------
        # DISPLAY RESULT
        # ----------------------------------------------------
        st.markdown('<div class="section-label">📄 Generated Content</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-card">{result}</div>', unsafe_allow_html=True)

        st.write("")

        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------
        st.download_button(
            label="⬇️ Download Content",
            data=result,
            file_name="ai_content.txt",
            mime="text/plain",
            use_container_width=True,
        )

    except Exception as e:
        st.error("Something went wrong while generating the content.")
        st.code(str(e))

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown(
    f'<div class="footer-caption">Powered by Groq • Model: {GROQ_MODEL}</div>',
    unsafe_allow_html=True,
)
