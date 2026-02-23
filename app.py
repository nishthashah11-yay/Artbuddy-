

# =========================================================
# 🎨 ArtRestorer AI - Smart Assistance for Art Restoration
# Scenario 1 - Generative AI Summative Assessment
# =========================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="ArtRestorer AI 🎨",
    page_icon="🖌️",
    layout="wide"
)

st.markdown("""
<style>

/* Historic Background Image */
.stApp {
   background-image: url("https://images.pexels.com/photos/15727855/pexels-photo-15727855.jpeg");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}

</style>
""", unsafe_allow_html=True)





st.markdown("""
<style>

/* Dark Box Style */
.dark-box {
    background-color: #1e1e1e;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.6);
}

/* Make text white inside dark boxes */
.dark-box h1,
.dark-box h2,
.dark-box h3,
.dark-box h4,
.dark-box h5,
.dark-box h6,
.dark-box p {
    color: white;
}

</style>
""", unsafe_allow_html=True)





# ---------------- GEMINI CLIENT ----------------


# ---------------- SESSION STATE ----------------
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- SPLASH SCREEN ----------------
if not st.session_state.splash_done:

    splash_html = """
    <html>
    <head>
    <style>
    body {
        margin:0;
        background: linear-gradient(180deg,#f3e5f5,#e1bee7,#ce93d8);
        font-family:Segoe UI;
        text-align:center;
    }
    .title {margin-top:200px;font-size:60px;font-weight:bold;color:#4a148c;}
    .subtitle {font-size:22px;color:#6a1b9a;margin-top:10px;}
    </style>
    </head>
    <body>
        <div class="title">🎨 ArtRestorer AI</div>
        <div class="subtitle">Reviving Heritage with Digital Intelligence</div>
    </body>
    </html>
    """

    st.components.v1.html(splash_html, height=600)
    time.sleep(4)
    st.session_state.splash_done = True
    st.rerun()

# ---------------- LANDING PAGE ----------------
if st.session_state.page == "landing":

    st.markdown("""
    <div style="text-align:center;padding-top:120px;">
        <h1 style="font-size:52px;color:#4a148c;">AI-Powered Art Restoration Assistant</h1>
        <p style="font-size:20px;color:#6a1b9a;">
        Analyze artwork descriptions and generate intelligent restoration suggestions.
        </p>
    </div>
    """, unsafe_allow_html=True) 
    

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🎨 Get Started"):
            st.session_state.page = "profile"
            st.rerun()

# ---------------- PROFILE PAGE ----------------
elif st.session_state.page == "profile":

    st.title("🖌️ Create Your Curator Profile")

    name = st.text_input("👤 Name")
    institution = st.text_input("🏛️ Institution / Museum")
    country = st.text_input("🌍 Country")

    if st.button("Continue to Dashboard"):
        if not name:
            st.warning("Please enter your name.")
        else:
            st.session_state.name = name
            st.session_state.institution = institution
            st.session_state.country = country
            st.session_state.page = "dashboard"
            st.rerun()

# ---------------- DASHBOARD ----------------
elif st.session_state.page == "dashboard":

    # HEADER
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#4a148c,#6a1b9a);
                padding:20px;border-radius:15px;color:white;">
        <h1>🎨 ArtRestorer AI</h1>
        <p>Welcome {st.session_state.name} | {st.session_state.institution}</p>
    </div>
    """, unsafe_allow_html=True)

    tab_restore, tab_prompts, tab_feedback, tab_usage, tab_settings = st.tabs(
        ["🖌️ Restoration Assistant", 
         "📜 Prompt Library (10+)", 
         "📊 Feedback",
         "📈 Usage",
         "⚙️ Settings"]
    )

    # =====================================================
    # TAB 1 - RESTORATION ASSISTANT
    # =====================================================
    with tab_restore:

        st.subheader("Describe the Artwork")

        col1, col2 = st.columns(2)

        with col1:
            artwork_type = st.selectbox(
                "Artwork Type",
                ["Oil Painting","Sculpture","Textile","Mural",
                 "Manuscript","Mosaic","Pottery"]
            )

            art_period = st.text_input("Art Period / Style (e.g., Renaissance, Mughal, Gothic)")

            artist = st.text_input("Artist (if known)")

        with col2:
            damage = st.text_area("Damage Description")

            output_format = st.selectbox(
                "Desired Output",
                ["Restoration Technique",
                 "Narrative Reconstruction",
                 "Symbol Interpretation",
                 "Complete Analysis"]
            )

            temperature = st.slider(
                "Creativity Level (Temperature)",
                0.1, 1.0, 0.6
            )

        if st.button("Generate AI Restoration Suggestion"):

            prompt = f"""
You are a senior art restoration expert.

Artwork Type: {artwork_type}
Period/Style: {art_period}
Artist: {artist}
Damage Description: {damage}
Output Type: {output_format}

Provide:
1. Restoration Strategy
2. Implementation Steps
3. Cultural and Historical Justification
4. Risk Mitigation Advice
5. Final Professional Recommendation

Maintain cultural sensitivity and artistic accuracy.
"""

            with st.spinner("Analyzing artwork and generating restoration strategy..."):
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt,
                    config={
                        "temperature": temperature,
                        "max_output_tokens": 2048
                    }
                )

            st.markdown("### 🎨 AI Restoration Output")
            st.markdown(response.text)

    # =====================================================
    # TAB 2 - 10+ PROMPT LIBRARY
    # =====================================================
    with tab_prompts:

        st.subheader("Compulsory 10 AI Restoration Prompts")

        prompts = [
            "Baroque painting missing upper-left corner — restore dramatic shadows.",
            "Mughal miniature with faded floral borders — enhance detailing.",
            "12th century sandstone sculpture with eroded face — reconstruct symmetrically.",
            "18th century silk tapestry torn near emblem — restore embroidery consistency.",
            "Abstract Expressionist canvas lost texture — recreate chaotic brushstroke feel.",
            "Ajanta cave mural with sun fading — digitally revive mineral pigments.",
            "Mayan glyph carvings partially eroded — reconstruct symbolic inscriptions.",
            "Japanese Ukiyo-e woodblock faded — enhance wave and ink precision.",
            "Gothic cathedral mosaic cracked — restore stained glass symmetry.",
            "Medieval manuscript ink erosion — recreate script and floral margins."
        ]

        for i, p in enumerate(prompts, 1):
            st.markdown(f"**{i}.** {p}")

    # =====================================================
    # TAB 3 - FEEDBACK
    # =====================================================
    with tab_feedback:

        st.subheader("AI Output Evaluation")

        with st.form("feedback_form"):
            f1 = st.checkbox("Culturally accurate")
            f2 = st.checkbox("Technically useful")
            f3 = st.checkbox("Historically aligned")
            f4 = st.checkbox("Creative but realistic")
            f5 = st.checkbox("Clear and understandable")

            submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            score = sum([f1,f2,f3,f4,f5])
            percentage = int((score/5)*100)
            st.progress(percentage/100)
            st.success(f"Quality Score: {percentage}%")

    # =====================================================
    # TAB 4 - USAGE
    # =====================================================
    with tab_usage:

        usage_data = {
            "Name": st.session_state.name,
            "Institution": st.session_state.institution,
            "Country": st.session_state.country,
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        st.dataframe(pd.DataFrame([usage_data]))

    # =====================================================
    # TAB 5 - SETTINGS
    # =====================================================
    with tab_settings:

        st.write("### Profile Information")
        st.write(f"Name: {st.session_state.name}")
        st.write(f"Institution: {st.session_state.institution}")
        st.write(f"Country: {st.session_state.country}")

        if st.button("Sign Out"):
            st.session_state.page = "landing"
            st.rerun()

# ---------------- FOOTER ----------------
st.markdown("<hr><p style='text-align:center;'>CRS Generative AI | 2026</p>", unsafe_allow_html=True)



