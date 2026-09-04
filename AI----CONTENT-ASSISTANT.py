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
# STYLING — "Ink & Paper" editorial theme
# ============================================================
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Solid ink-navy page background — no gradient noise */
        .stApp {
            background: #101a2e;
        }

        .block-container {
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 740px;
        }

        /* Hero header */
        .hero-wrap {
            padding: 12px 4px 26px 4px;
            border-bottom: 1px solid rgba(247, 241, 227, 0.12);
            margin-bottom: 28px;
        }

        .hero-top-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 16px;
        }

        .main-title-wrap {
            position: relative;
            display: inline-block;
        }

        .main-title {
            position: relative;
            z-index: 1;
            font-family: 'Fraunces', serif;
            font-size: 44px;
            font-weight: 600;
            color: #f7f1e3;
            margin: 0 0 8px 0;
            line-height: 1.1;
        }

        /* Highlighter-marker sweep behind the title, one-time reveal on load */
        .main-title-wrap::after {
            content: "";
            position: absolute;
            left: -8px;
            right: -8px;
            bottom: 10px;
            height: 16px;
            background: rgba(201, 162, 39, 0.4);
            z-index: 0;
            transform: scaleX(0);
            transform-origin: left center;
            animation: highlightSweep 0.9s cubic-bezier(0.65, 0, 0.35, 1) 0.3s forwards;
        }

        @keyframes highlightSweep {
            to { transform: scaleX(1); }
        }

        .subtitle {
            color: rgba(247, 241, 227, 0.6);
            font-size: 16px;
            font-weight: 400;
            max-width: 460px;
            line-height: 1.5;
        }

        /* Rubber-stamp badge */
        .stamp-badge {
            flex-shrink: 0;
            border: 2px solid #c1441f;
            color: #d9694a;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.6px;
            transform: rotate(4deg);
            white-space: nowrap;
            font-family: 'Inter', sans-serif;
        }

        /* Dark navy form panel — distinct from pure black, inputs stay light for typing */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #182643 !important;
            border: 1px solid rgba(247, 241, 227, 0.14) !important;
            border-radius: 10px !important;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.28) !important;
            padding: 10px !important;
        }

        /* Section labels inside the dark panel */
        .section-label {
            font-family: 'Fraunces', serif;
            font-size: 18px;
            font-weight: 600;
            color: #f7f1e3;
            margin-top: 4px;
            margin-bottom: 16px;
        }

        /* Inputs — paper-toned, dark ink text (no more black boxes) */
        .stTextInput input, .stTextArea textarea {
            background: #ffffff !important;
            border: 1px solid #d8cdae !important;
            border-radius: 6px !important;
            color: #1f2937 !important;
        }

        .stTextInput input:focus, .stTextArea textarea:focus {
            border: 1px solid #c1441f !important;
            box-shadow: 0 0 0 3px rgba(193, 68, 31, 0.12) !important;
        }

        .stTextArea textarea::placeholder, .stTextInput input::placeholder {
            color: #9c9484 !important;
        }

        div[data-baseweb="select"] > div {
            background: #ffffff !important;
            border: 1px solid #d8cdae !important;
            border-radius: 6px !important;
            color: #1f2937 !important;
        }

        div[data-baseweb="select"] span {
            color: #1f2937 !important;
        }

        label, .stSelectbox label, .stTextArea label, .stTextInput label {
            color: #f7f1e3 !important;
            font-weight: 600 !important;
            font-size: 13.5px !important;
        }

        /* Primary button — stamp red */
        .stButton > button {
            background: #c1441f !important;
            color: #fdf8ee !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 0.7rem 1rem !important;
            font-weight: 700 !important;
            font-size: 15.5px !important;
            transition: background 0.2s ease !important;
        }

        .stButton > button:hover {
            background: #a63a1a !important;
        }

        /* Download button */
        .stDownloadButton > button {
            background: transparent !important;
            color: #f7f1e3 !important;
            border: 1px solid rgba(247, 241, 227, 0.35) !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            padding: 0.65rem 1rem !important;
            transition: all 0.2s ease !important;
        }

        .stDownloadButton > button:hover {
            border-color: #c1441f !important;
            color: #d9694a !important;
        }

        /* Result box — paper card on the ink background */
        .result-card {
            background: #f7f1e3;
            border: 1px solid #e4dac2;
            border-left: 4px solid #c1441f;
            border-radius: 8px;
            padding: 26px 28px;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.28);
            color: #1f2937;
            line-height: 1.7;
        }

        /* Success / info / warning / error boxes */
        div[data-testid="stAlert"] {
            border-radius: 8px !important;
        }

        /* Divider */
        hr {
            border-color: rgba(247, 241, 227, 0.12) !important;
        }

        /* Footer caption */
        .footer-caption {
            text-align: center;
            color: rgba(247, 241, 227, 0.4);
            font-size: 13px;
            margin-top: 6px;
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(193, 68, 31, 0.4); border-radius: 10px; }

        /* Spinner */
        .stSpinner > div > div {
            border-top-color: #c1441f !important;
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
        <div class="hero-top-row">
            <div>
                <div class="main-title-wrap"><div class="main-title">The Content Desk</div></div>
                <div class="subtitle">Draft a complete post, caption, and hashtag set for any platform in one pass.</div>
            </div>
            <div class="stamp-badge">GROQ<br>POWERED</div>
        </div>
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
