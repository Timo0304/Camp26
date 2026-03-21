import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from reportlab.pdfgen import canvas
from datetime import datetime
import os

from flyer_generator import generate_flyer, THEMES
from bible_game import QUESTIONS, LEVEL_COLORS, SCORE_MESSAGES, TIME_UP_VERSES
import time

try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=1000, key="countdown")
except ImportError:
    pass

st.set_page_config(page_title="Camp '26 🎉", layout="wide", page_icon="⛺")

# ------------------------------------
# CUSTOM CSS - COLORFUL & CHILD-FRIENDLY
# ------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700;800&display=swap');

/* ---- ROOT VARIABLES ---- */
:root {
    --yellow:  #FFD93D;
    --orange:  #FF6B35;
    --pink:    #FF6B9D;
    --purple:  #C77DFF;
    --blue:    #4CC9F0;
    --green:   #06D6A0;
    --red:     #FF4D6D;
    --white:   #FFFFFF;
    --bg:      #FFF8F0;
}

/* ---- GLOBAL ---- */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
    background-color: var(--bg) !important;
}

/* ---- HEADER BANNER ---- */
.rainbow-banner {
    background: linear-gradient(135deg, #1A73E8 0%, #0D47A1 60%, #FFD93D 100%);
    border-radius: 24px;
    padding: 36px 20px 28px;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(255,107,53,0.25);
    position: relative;
    overflow: hidden;
}
.rainbow-banner::before {
    content: "⭐ ✨ 🌟 ✨ ⭐";
    position: absolute;
    top: 10px; left: 50%;
    transform: translateX(-50%);
    font-size: 20px;
    letter-spacing: 8px;
}
.rainbow-banner h1 {
    font-family: 'Fredoka One', cursive !important;
    font-size: clamp(1.2rem, 4vw, 3.6rem) !important;
    color: white !important;
    text-shadow: 3px 3px 0px rgba(0,0,0,0.2);
    margin: 16px 0 8px;
    letter-spacing: 1px;
}
.banner-logo {
    height: clamp(28px, 4vw, 56px);
    vertical-align: middle;
    flex-shrink: 0;
    filter: drop-shadow(0 2px 6px rgba(0,0,0,0.3));
    border-radius: 8px;
}
.rainbow-banner h2 {
    font-family: 'Nunito', sans-serif !important;
    font-size: clamp(1rem, 3vw, 1.4rem) !important;
    color: #FFF8E1 !important;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 0;
}

/* ---- SECTION HEADERS ---- */
h2, h3 {
    font-family: 'Fredoka One', cursive !important;
    color: var(--orange) !important;
}

/* ---- COUNTDOWN BOXES ---- */
.countdown-container {
    display: flex;
    gap: 16px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 20px 0;
}
.countdown-box {
    background: white;
    border-radius: 20px;
    padding: 20px 30px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    border: 4px solid;
    min-width: 130px;
    transition: transform 0.2s;
}
.countdown-box:hover { transform: scale(1.06) rotate(-1deg); }
.countdown-box:nth-child(1) { border-color: var(--orange); }
.countdown-box:nth-child(2) { border-color: var(--blue); }
.countdown-box:nth-child(3) { border-color: var(--green); }
.countdown-box:nth-child(4) { border-color: var(--pink); }
.countdown-box .num {
    font-family: 'Fredoka One', cursive;
    font-size: 3rem;
    line-height: 1;
    display: block;
}
.countdown-box:nth-child(1) .num { color: var(--orange); }
.countdown-box:nth-child(2) .num { color: var(--blue); }
.countdown-box:nth-child(3) .num { color: var(--green); }
.countdown-box:nth-child(4) .num { color: var(--pink); }
.countdown-box .label {
    font-weight: 800;
    font-size: 0.85rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #888;
    margin-top: 4px;
    display: block;
}

/* ---- ABOUT CARD ---- */
.about-card {
    background: linear-gradient(135deg, #fff9e6, #fff0fb);
    border-radius: 24px;
    padding: 32px;
    border: 3px dashed var(--yellow);
    position: relative;
}
.about-card .emoji-list {
    list-style: none;
    padding: 0;
    margin: 16px 0 0;
}
.about-card .emoji-list li {
    font-size: 1.1rem;
    font-weight: 700;
    color: #444;
    padding: 8px 0;
    border-bottom: 2px dotted #FFD93D44;
}

/* ---- EVENT DETAILS CARD ---- */
.event-card {
    background: linear-gradient(135deg, #e8f9ff, #f0e8ff);
    border-radius: 24px;
    padding: 32px;
    border: 3px solid var(--blue);
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}
.event-item {
    text-align: center;
    padding: 16px;
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(76,201,240,0.15);
}
.event-item .icon { font-size: 2.2rem; }
.event-item .etitle {
    font-family: 'Fredoka One', cursive;
    font-size: 1rem;
    color: var(--purple);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 6px 0 2px;
}
.event-item .evalue {
    font-weight: 800;
    color: #333;
    font-size: 1rem;
}

/* ---- TESTIMONY CARDS ---- */
.testimony-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px,1fr));
    gap: 28px;
    margin-top: 20px;
}
.testimony-card {
    border-radius: 24px;
    padding: 28px 24px 20px;
    color: #333;
    font-weight: 700;
    font-size: 1rem;
    line-height: 1.7;
    position: relative;
    background: white;
    border: 4px solid;
    box-shadow: 6px 6px 0px;
    transition: transform 0.2s, box-shadow 0.2s;
}
.testimony-card:hover {
    transform: translate(-3px, -3px);
    box-shadow: 9px 9px 0px;
}
.testimony-card:nth-child(1) { border-color: var(--orange); box-shadow-color: var(--orange); }
.testimony-card:nth-child(1) { box-shadow: 6px 6px 0px var(--orange); }
.testimony-card:nth-child(1):hover { box-shadow: 9px 9px 0px var(--orange); }
.testimony-card:nth-child(2) { border-color: var(--purple); box-shadow: 6px 6px 0px var(--purple); }
.testimony-card:nth-child(2):hover { box-shadow: 9px 9px 0px var(--purple); }
.testimony-card:nth-child(3) { border-color: var(--green); box-shadow: 6px 6px 0px var(--green); }
.testimony-card:nth-child(3):hover { box-shadow: 9px 9px 0px var(--green); }
.testimony-card .bubble-icon {
    font-size: 2.4rem;
    display: block;
    margin-bottom: 10px;
}
.testimony-card .speech-text {
    font-size: 1rem;
    color: #444;
    font-weight: 700;
    font-style: italic;
}
.testimony-card .author {
    margin-top: 14px;
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding-top: 10px;
    border-top: 2px dashed #eee;
}
.testimony-card:nth-child(1) .author { color: var(--orange); }
.testimony-card:nth-child(2) .author { color: var(--purple); }
.testimony-card:nth-child(3) .author { color: var(--green); }
.testimony-card .tag {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 10px;
    text-transform: uppercase;
    color: white;
}
.testimony-card:nth-child(1) .tag { background: var(--orange); }
.testimony-card:nth-child(2) .tag { background: var(--purple); }
.testimony-card:nth-child(3) .tag { background: var(--green); }

/* ---- SECTION DIVIDER ---- */
.fun-divider {
    text-align: center;
    font-size: 1.5rem;
    letter-spacing: 10px;
    color: var(--yellow);
    margin: 30px 0;
}

/* ---- FLYER SECTION ---- */
.flyer-form {
    background: linear-gradient(135deg, #fff0f7, #f0f4ff);
    border-radius: 24px;
    padding: 32px;
    border: 3px solid var(--pink);
}

/* ---- STREAMLIT WIDGET OVERRIDES ---- */
div[data-baseweb="input"] input {
    border-radius: 12px !important;
    border: 2.5px solid var(--blue) !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    background: white !important;
    color: #333333 !important;
    -webkit-text-fill-color: #333333 !important;
}
div[data-baseweb="input"] input::placeholder {
    color: #aaaaaa !important;
    -webkit-text-fill-color: #aaaaaa !important;
}
div[data-baseweb="input"] input:focus {
    border-color: var(--pink) !important;
    box-shadow: 0 0 0 3px rgba(255,107,157,0.2) !important;
}

/* ---- SELECTBOX OVERRIDES ---- */
div[data-baseweb="select"] {
    border-radius: 12px !important;
}
div[data-baseweb="select"] > div {
    border: 2.5px solid var(--blue) !important;
    border-radius: 12px !important;
    background: white !important;
    min-height: 48px !important;
    height: auto !important;
    padding-top: 8px !important;
    padding-bottom: 8px !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div[class*="ValueContainer"],
div[data-baseweb="select"] div[class*="singleValue"],
div[data-baseweb="select"] div[class*="placeholder"],
div[data-baseweb="select"] * {
    color: #333333 !important;
    -webkit-text-fill-color: #333333 !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    white-space: normal !important;
    overflow: visible !important;
    line-height: 1.4 !important;
}

/* ---- FILE UPLOADER — FUN STYLE ---- */
[data-testid="stFileUploader"] {
    border-radius: 20px !important;
    padding: 4px !important;
}
[data-testid="stFileUploader"] > div {
    border: 3px dashed var(--pink) !important;
    border-radius: 20px !important;
    background: linear-gradient(135deg, #fff0f7, #f0f4ff) !important;
    padding: 20px !important;
    text-align: center !important;
    transition: all 0.3s !important;
    animation: pulse-border 2s ease-in-out infinite !important;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: var(--orange) !important;
    background: linear-gradient(135deg, #fff4e6, #fff0f7) !important;
    transform: scale(1.01) !important;
}
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] small {
    color: #FF6B35 !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
}
[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, var(--orange), var(--pink)) !important;
    color: white !important;
    font-family: 'Fredoka One', cursive !important;
    border-radius: 50px !important;
    border: none !important;
    padding: 8px 24px !important;
    font-size: 0.95rem !important;
    box-shadow: 0 4px 12px rgba(255,107,53,0.3) !important;
}
@keyframes pulse-border {
    0%,100% { border-color: var(--pink) !important; }
    50%      { border-color: var(--purple) !important; }
}

/* ---- BUTTONS ---- */
.stDownloadButton > button, .stButton > button {
    background: linear-gradient(135deg, var(--orange), var(--pink)) !important;
    color: white !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 1.1rem !important;
    border-radius: 50px !important;
    border: none !important;
    padding: 12px 32px !important;
    box-shadow: 0 6px 20px rgba(255,107,53,0.35) !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    letter-spacing: 1px;
}
.stDownloadButton > button:hover, .stButton > button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 10px 28px rgba(255,107,53,0.45) !important;
}

/* ---- FILE UPLOADER ---- */
[data-testid="stFileUploader"] {
    border: 3px dashed var(--purple) !important;
    border-radius: 16px !important;
    background: #faf5ff !important;
    padding: 12px !important;
}

/* ---- METRICS ---- */
[data-testid="stMetric"] {
    background: white;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}

/* ---- STICKERS ROW ---- */
.sticker-row {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    font-size: 2.2rem;
    margin: 10px 0 20px;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-6px); }
}

/* ---- PHOTO GALLERY ---- */
[data-testid="stImage"] img {
    border-radius: 20px !important;
    border: 4px solid var(--yellow) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1) !important;
}

/* ---- INFO / ALERT BOXES ---- */
.stAlert {
    border-radius: 16px !important;
}

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff3e0, #fce4ff) !important;
}

/* ======== RESPONSIVE / MOBILE ======== */
@media (max-width: 768px) {
    .rainbow-banner h1 { font-size: clamp(1.2rem, 4vw, 3.6rem) !important; }
    .rainbow-banner h2 { font-size: 0.85rem !important; letter-spacing: 1px !important; }
    .countdown-container { gap: 8px !important; }
    .countdown-box { padding: 12px 16px !important; min-width: 70px !important; }
    .countdown-box .num { font-size: 2rem !important; }
    .event-card { grid-template-columns: 1fr !important; padding: 16px !important; }
    .testimony-grid { grid-template-columns: 1fr !important; }
    .about-card { padding: 18px !important; }
    .flyer-form { padding: 16px !important; }
    [data-testid="stImage"] img { border-radius: 12px !important; }
    .sticker-row { font-size: 1.4rem !important; gap: 6px !important; }
    h2, h3 { font-size: 1.3rem !important; }
}
@media (max-width: 480px) {
    .rainbow-banner { padding: 20px 12px 16px !important; border-radius: 14px !important; }
    .rainbow-banner h1 { font-size: clamp(1rem, 3.5vw, 1.4rem) !important; gap: 6px !important; }
    .countdown-box { min-width: 60px !important; padding: 10px 12px !important; }
    .countdown-box .num { font-size: 1.6rem !important; }
    .fun-divider { font-size: 1rem !important; letter-spacing: 6px !important; }
}

/* ---- MAIN CONTENT MAX-WIDTH FOR LARGE SCREENS ---- */
.block-container {
    max-width: 900px !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}

/* ---- GAME LEVEL CARDS — centre button under card ---- */
.game-level-col {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

/* ---- CAMP 26 BADGE TEXT FIX ---- */
.camp26-badge {
    font-family: 'Fredoka One', cursive;
    font-size: 1.1rem;
    color: #FF6B35 !important;
    margin-top: 12px;
    padding: 8px 20px;
    background: #fff8f0;
    border: 2px solid #FF6B35;
    border-radius: 50px;
    display: inline-block;
    font-weight: 700;
}

/* ---- TABS STYLING ---- */
[data-baseweb="tab-list"] {
    background: white !important;
    border-radius: 20px !important;
    padding: 8px !important;
    gap: 6px !important;
    border: 3px solid #FFD93D !important;
    flex-wrap: wrap !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
}
[data-baseweb="tab"] {
    border-radius: 14px !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    padding: 16px 26px !important;
    color: #666 !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.2s !important;
    white-space: nowrap !important;
    min-height: 56px !important;
}
[data-baseweb="tab"]:hover {
    background: #FFF8F0 !important;
    color: #FF6B35 !important;
    transform: scale(1.03) !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: linear-gradient(135deg, #FF6B35, #FF6B9D) !important;
    color: white !important;
    box-shadow: 0 6px 18px rgba(255,107,53,0.4) !important;
    transform: scale(1.05) !important;
}
[data-baseweb="tab-highlight"] { display: none !important; }
[data-baseweb="tab-border"]    { display: none !important; }
[data-baseweb="tab-panel"] {
    padding-top: 28px !important;
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------
# HEADER BANNER
# ------------------------------------

# Load logo as base64 so it works on Streamlit Cloud
import base64
logo_b64 = ""
if os.path.exists("logo.png"):
    with open("logo.png", "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()

logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="banner-logo">' if logo_b64 else ""

st.markdown(f"""
<div class="rainbow-banner">
    <h1 style="display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:nowrap;white-space:nowrap;">
        {logo_html} Sunday School Camp &#39;26 {logo_html}
    </h1>
    <h2>&#128591; Theme: God Answers Prayers &#128591;</h2>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sticker-row">🎉 ✝️ 🎊 🌟 🎈 🙌 🎵 💛 🎠 ⭐</div>', unsafe_allow_html=True)

# ── COUNTDOWN (always visible under banner) ────────────────────────────────
event_date = datetime(2026, 8, 13)
now = datetime.now()
time_left = event_date - now
days    = time_left.days
hours   = time_left.seconds // 3600
minutes = (time_left.seconds % 3600) // 60
seconds = time_left.seconds % 60

st.markdown("### ⏳ Counting Down to the BIG Day!")
st.markdown(f"""
<div class="countdown-container">
    <div class="countdown-box">
        <span class="num">{days}</span>
        <span class="label">🌅 Days</span>
    </div>
    <div class="countdown-box">
        <span class="num">{hours}</span>
        <span class="label">⏰ Hours</span>
    </div>
    <div class="countdown-box">
        <span class="num">{minutes}</span>
        <span class="label">⚡ Minutes</span>
    </div>
    <div class="countdown-box">
        <span class="num">{seconds}</span>
        <span class="label">🔥 Seconds</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="fun-divider">⭐ ⭐ ⭐ ⭐ ⭐</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Home",
    "💬 Testimonies",
    "📸 Gallery",
    "📞 Contact",
    "🎮 Bible Quiz",
    "🎨 My Flyer",
])

# ─────────────────────────────────────────
# TAB 1 — HOME
# ─────────────────────────────────────────
with tab1:
    st.markdown("### 🎒 What's This Camp About?")
    st.markdown("""
<div class="about-card">
    <p style="font-size:1.1rem; font-weight:700; color:#555; margin:0 0 8px;">
        Get ready for the most AMAZING Biannual Retreat ever!
        Come and experience God's power with fellow Sunday School kids and teens! 🎉
    </p>
    <ul class="emoji-list">
        <li>🔥 Powerful teachings that light up your heart</li>
        <li>🙏 Life-changing testimonies &amp; miracles</li>
        <li>🤝 Make new friends &amp; awesome connections</li>
        <li>🚀 Practical sessions to grow as a leader</li>
    </ul>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="fun-divider">⭐ ⭐ ⭐</div>', unsafe_allow_html=True)

    st.markdown("### 📌 Event Details")
    st.markdown("""
<div class="event-card">
    <div class="event-item">
        <div class="icon">📅</div>
        <div class="etitle">Dates</div>
        <div class="evalue">Aug 13–16, 2026</div>
    </div>
    <div class="event-item">
        <div class="icon">📍</div>
        <div class="etitle">Venue</div>
        <div class="evalue">All Souls' Chapel OAU, Ile-Ife</div>
    </div>
    <div class="event-item">
        <div class="icon">⏰</div>
        <div class="etitle">Time</div>
        <div class="evalue">9:00 AM Daily</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# TAB 2 — TESTIMONIES
# ─────────────────────────────────────────
with tab2:
    st.markdown("### 💬 What Kids Are Saying!")
    st.markdown("""
<div class="testimony-grid">
    <div class="testimony-card">
        <span class="tag">✨ Testimony</span>
        <span class="bubble-icon">😄</span>
        <div class="speech-text">"I really enjoyed the power point presentation and I had so much fun!"</div>
        <div class="author">— Ehud 2024 ⭐⭐⭐⭐⭐</div>
    </div>
    <div class="testimony-card">
        <span class="tag">🔥 Highlight</span>
        <span class="bubble-icon">🤩</span>
        <div class="speech-text">"I had so much fun and I want to do this again!"</div>
        <div class="author">— Love 2024 ⭐⭐⭐⭐⭐</div>
    </div>
    <div class="testimony-card">
        <span class="tag">🔥 Highlight</span>
        <span class="bubble-icon">🥳</span>
        <div class="speech-text">"Yes! I enjoyed myself in the camp"</div>
        <div class="author">— Mosope 2024 ⭐⭐⭐⭐⭐</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# TAB 3 — GALLERY
# ─────────────────────────────────────────
with tab3:
    st.markdown("### 🖼️ Pictures From Last Edition")
    st.markdown("""
<div style="text-align:center; margin-top:24px;">
    <a href="https://drive.google.com/drive/folders/1xyzN4B2IIBViAlStN09XVayf2_cq76Zc"
    target="_blank"
    style="
        display:inline-block;
        background: linear-gradient(135deg, #1A73E8, #0D47A1);
        color: white;
        font-family: 'Fredoka One', cursive;
        font-size: 1.1rem;
        border-radius: 50px;
        padding: 14px 32px;
        text-decoration: none;
        box-shadow: 0 6px 20px rgba(26,115,232,0.35);
        letter-spacing: 1px;
    ">
        📸 View All Photos and Videos from Camp '24 on Google Drive 📸
    </a>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="fun-divider">📄 📄 📄</div>', unsafe_allow_html=True)

    st.markdown("### 📄 Bulletin From Last Edition")
    if os.path.exists("bulletin.pdf"):
        with open("bulletin.pdf", "rb") as _bf:
            _pdf_data = _bf.read()
        st.download_button(
            label="📥 Download Last Edition Bulletin",
            data=_pdf_data,
            file_name="camp24_bulletin.pdf",
            mime="application/pdf"
        )
    else:
        st.info("📄 Bulletin will be available soon!")

# ─────────────────────────────────────────
# TAB 4 — CONTACT
# ─────────────────────────────────────────
with tab4:
    st.markdown("### 📞 For Further Enquiries")
    st.markdown(
        """
        <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:20px; margin-top:16px;">
            <div style="background:white; border-radius:20px; padding:24px; border:3px solid #4CC9F0; box-shadow:5px 5px 0px #4CC9F0; text-align:center;">
                <div style="font-size:2.5rem;">👨‍💼</div>
                <div style="font-family:Arial; font-size:1.1rem; color:#FF6B35; margin:8px 0 4px;"><b>Dr. Olatomide Fadare</b></div>
                <div style="font-weight:700; color:#555; font-size:0.9rem;">Chairman Organizing Committee</div>
                <a href="tel:+2347054075459" style="display:block; margin-top:10px; color:#1A73E8; font-weight:800; text-decoration:none;">📱 +234 705 407 5459</a>
                <a href="https://wa.me/2347054075459" target="_blank" style="display:inline-block; margin-top:8px; background:#25D366; color:white; padding:6px 18px; border-radius:50px; font-weight:800; text-decoration:none; font-size:0.85rem;">💬 WhatsApp</a>
            </div>
            <div style="background:white; border-radius:20px; padding:24px; border:3px solid #C77DFF; box-shadow:5px 5px 0px #C77DFF; text-align:center;">
                <div style="font-size:2.5rem;">👩‍💼</div>
                <div style="font-family:Arial; font-size:1.1rem; color:#FF6B35; margin:8px 0 4px;"><b>Mrs. Rachael Talabi</b></div>
                <div style="font-weight:700; color:#555; font-size:0.9rem;">Sunday School Superintendent</div>
                <a href="tel:+2348034464183" style="display:block; margin-top:10px; color:#1A73E8; font-weight:800; text-decoration:none;">📱 +234 803 446 4183</a>
                <a href="https://wa.me/2348034464183" target="_blank" style="display:inline-block; margin-top:8px; background:#25D366; color:white; padding:6px 18px; border-radius:50px; font-weight:800; text-decoration:none; font-size:0.85rem;">💬 WhatsApp</a>
            </div>
            <div style="background:white; border-radius:20px; padding:24px; border:3px solid #06D6A0; box-shadow:5px 5px 0px #06D6A0; text-align:center;">
                <div style="font-size:2.5rem;">👨🏾‍🏫</div>
                <div style="font-family:Arial; font-size:1.1rem; color:#FF6B35; margin:8px 0 4px;"><b>Rev. Dr. Olusegun Babalola</b></div>
                <div style="font-weight:700; color:#555; font-size:0.9rem;">Chaplain</div>
                <a href="tel:+2348062262318" style="display:block; margin-top:10px; color:#1A73E8; font-weight:800; text-decoration:none;">📱 +234 806 226 2318</a>
                <a href="https://wa.me/2348062262318" target="_blank" style="display:inline-block; margin-top:8px; background:#25D366; color:white; padding:6px 18px; border-radius:50px; font-weight:800; text-decoration:none; font-size:0.85rem;">💬 WhatsApp</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="fun-divider">💰 💰 💰</div>', unsafe_allow_html=True)

    st.markdown("### 💛 Support the Camp")
    st.markdown("""
<div style="background:linear-gradient(135deg,#fff9e6,#fff0fb); border-radius:24px;
padding:32px; border:3px dashed #FFD93D; text-align:center; max-width:500px; margin:auto;">
    <div style="font-size:2.5rem;">🙏</div>
    <div style="font-family:'Fredoka One',cursive; font-size:1.3rem; color:#FF6B35; margin:10px 0 6px;">
        Make a Donation
    </div>
    <p style="color:#555; font-weight:700; margin-bottom:20px;">
        Your giving supports children attending Camp '26. God bless you! 💛
    </p>
    <div style="background:white; border-radius:16px; padding:20px; border:2px solid #FFD93D;">
        <div style="font-weight:800; color:#888; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;">Bank Name</div>
        <div style="font-family:'Fredoka One',cursive; font-size:1.2rem; color:#333; margin:4px 0 16px;">Access Bank</div>
        <div style="font-weight:800; color:#888; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;">Account Name</div>
        <div style="font-family:'Fredoka One',cursive; font-size:1.2rem; color:#333; margin:4px 0 16px;">Mrs. Kehinde Taiwo</div>
        <div style="font-weight:800; color:#888; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;">Account Number</div>
        <div style="font-family:'Fredoka One',cursive; font-size:2rem; color:#1A73E8; letter-spacing:4px; margin:4px 0;">0817884022</div>
    </div>
    <p style="color:#555; font-weight:700; margin-bottom:20px;">
        "Every seed sown helps a child grow". God bless you! 💛
    </p>
    <div style="background:white; border-radius:16px; padding:20px; border:2px solid #FFD93D;">
        <div style="font-weight:800; color:#888; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;">Bank Name</div>
        <div style="font-family:'Fredoka One',cursive; font-size:1.2rem; color:#333; margin:4px 0 16px;">Union Bank</div>
        <div style="font-weight:800; color:#888; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;">Account Name</div>
        <div style="font-family:'Fredoka One',cursive; font-size:1.2rem; color:#333; margin:4px 0 16px;">Mrs. Kehinde Taiwo</div>
        <div style="font-weight:800; color:#888; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;">Account Number</div>
        <div style="font-family:'Fredoka One',cursive; font-size:2rem; color:#1A73E8; letter-spacing:4px; margin:4px 0;">0007008895</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# TAB 5 — BIBLE QUIZ
# ─────────────────────────────────────────
with tab5:
    st.markdown("### 🎮 Bible Quiz Challenge!")
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#fff9e6,#f0f4ff);border-radius:24px;
        padding:20px 28px;border:3px solid #FFD93D;margin-bottom:16px;">
            <p style="font-size:1.05rem;font-weight:700;color:#555;margin:0;">
                🌟 Test your Bible knowledge! Pick your level, answer 5 questions,
                and see how many you get right. Can you score 5 out of 5? 🏆
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── Session state init
    for _k, _v in [
        ("game_active", False), ("q_index", 0), ("score", 0),
        ("answered", False), ("selected", None), ("game_level", None),
        ("game_questions", []), ("game_over", False),
        ("timed_out", False), ("q_start_time", None), ("timeout_verse", None),
    ]:
        if _k not in st.session_state:
            st.session_state[_k] = _v

    # ── Level picker
    if not st.session_state.game_active and not st.session_state.game_over:
        st.markdown("#### 👇 Choose your level to start!")
        _cols = st.columns(3)
        _level_list = list(QUESTIONS.keys())
        _icons = ["🌱", "🔥", "👑"]
        _descs = ["Perfect for younger kids", "For teens and youth", "For Bible pros!"]
        for _i, (_col, _level, _icon, _desc) in enumerate(zip(_cols, _level_list, _icons, _descs)):
            _c = LEVEL_COLORS[_level]
            with _col:
                st.markdown(
                    f"""
                    <div style="background:{_c['bg']};border:3px solid {_c['border']};
                    border-radius:20px;padding:20px;text-align:center;
                    box-shadow:4px 4px 0 {_c['border']};margin-bottom:12px;">
                        <div style="font-size:2rem;">{_icon}</div>
                        <div style="font-family:'Fredoka One',cursive;font-size:1.1rem;
                        color:{_c['badge']};margin:6px 0 4px;">{_level}</div>
                        <div style="font-size:0.85rem;font-weight:700;color:#777;">{_desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button(f"Play {_level}", key=f"start_{_i}", use_container_width=True):
                    import random as _random
                    _qs = QUESTIONS[_level].copy()
                    _random.shuffle(_qs)
                    st.session_state.game_questions = _qs[:5]
                    st.session_state.game_level     = _level
                    st.session_state.game_active    = True
                    st.session_state.q_index        = 0
                    st.session_state.score          = 0
                    st.session_state.answered       = False
                    st.session_state.selected       = None
                    st.session_state.game_over      = False
                    st.session_state.q_start_time   = None
                    st.session_state.timed_out      = False
                    st.session_state.timeout_verse  = None
                    st.rerun()

    # ── Active game
    elif st.session_state.game_active and not st.session_state.game_over:
        _level = st.session_state.game_level
        _c     = LEVEL_COLORS[_level]
        _qi    = st.session_state.q_index
        _qs    = st.session_state.game_questions
        _q     = _qs[_qi]
        _total = len(_qs)
        _prog  = int((_qi / _total) * 100)
        _TIME_LIMIT = 15

        if st.session_state.q_start_time is None:
            st.session_state.q_start_time = time.time()

        _elapsed   = time.time() - st.session_state.q_start_time
        _remaining = max(0, _TIME_LIMIT - int(_elapsed))

        if _remaining == 0 and not st.session_state.answered and not st.session_state.timed_out:
            import random as _rnd
            st.session_state.timed_out    = True
            st.session_state.game_active  = False
            st.session_state.game_over    = True
            st.session_state.timeout_verse = _rnd.choice(TIME_UP_VERSES)
            st.rerun()

        if _remaining > 10:
            _tcol = "#06D6A0"
        elif _remaining > 5:
            _tcol = "#FF6B35"
        else:
            _tcol = "#FF4D6D"

        _timer_pct = int((_remaining / _TIME_LIMIT) * 100)

        st.markdown(
            f"""
            <div style="background:#eee;border-radius:50px;height:14px;margin-bottom:6px;overflow:hidden;">
                <div style="background:linear-gradient(90deg,{_c['badge']},{_c['border']});
                width:{_prog}%;height:100%;border-radius:50px;transition:width 0.5s;"></div>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <span style="font-weight:800;color:{_c['badge']};">Question {_qi+1} of {_total}</span>
                <span style="font-weight:800;color:#FF6B35;">Score: {st.session_state.score} ⭐</span>
            </div>
            <div style="margin-bottom:6px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                    <span style="font-size:0.85rem;font-weight:800;color:{_tcol};">
                        {'⏱️' if _remaining > 5 else '🚨'} {_remaining}s remaining
                    </span>
                    <span style="font-size:0.75rem;font-weight:700;color:#aaa;">15 sec per question</span>
                </div>
                <div style="background:#eee;border-radius:50px;height:10px;overflow:hidden;">
                    <div style="background:{_tcol};width:{_timer_pct}%;height:100%;
                    border-radius:50px;transition:width 1s linear;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="background:{_c['bg']};border:3px solid {_c['border']};
            border-radius:24px;padding:28px;margin-bottom:20px;
            box-shadow:5px 5px 0 {_c['border']};">
                <div style="font-size:2.5rem;text-align:center;margin-bottom:12px;">{_q['emoji']}</div>
                <div style="font-family:'Fredoka One',cursive;font-size:1.3rem;
                color:#333;text-align:center;line-height:1.4;">{_q['question']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        _nav1, _nav2 = st.columns(2)
        with _nav1:
            if st.button("🏠 Home", key="home_mid", use_container_width=True):
                st.session_state.game_active = False
                st.session_state.game_over   = False
                st.session_state.q_index     = 0
                st.session_state.score       = 0
                st.session_state.answered    = False
                st.session_state.selected    = None
                st.session_state.game_level  = None
                st.session_state.q_start_time = None
                st.rerun()
        with _nav2:
            if st.button("🔄 New Game", key="new_game_mid", use_container_width=True):
                st.session_state.game_active = False
                st.session_state.game_over   = False
                st.session_state.q_index     = 0
                st.session_state.score       = 0
                st.session_state.answered    = False
                st.session_state.selected    = None
                st.session_state.game_level  = None
                st.session_state.q_start_time = None
                st.rerun()

        if not st.session_state.answered:
            _bcols = st.columns(2)
            for _i, _opt in enumerate(_q["options"]):
                with _bcols[_i % 2]:
                    if st.button(f"  {_opt}  ", key=f"opt_{_qi}_{_i}", use_container_width=True):
                        st.session_state.selected = _opt
                        st.session_state.answered = True
                        if _opt == _q["answer"]:
                            st.session_state.score += 1
                        st.rerun()
        else:
            _selected = st.session_state.selected
            _correct  = _q["answer"]
            _is_right = _selected == _correct

            if _is_right:
                st.markdown(
                    f"""
                    <div style="background:#e8fff5;border:3px solid #06D6A0;border-radius:20px;
                    padding:20px;text-align:center;box-shadow:4px 4px 0 #06D6A0;margin-bottom:12px;">
                        <div style="font-size:2rem;">🎉</div>
                        <div style="font-family:'Fredoka One',cursive;font-size:1.3rem;color:#06D6A0;">
                            Correct! Well done!</div>
                        <div style="font-size:0.9rem;font-weight:700;color:#555;margin-top:8px;">
                            💡 {_q['fun_fact']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="background:#fff0f0;border:3px solid #FF4D6D;border-radius:20px;
                    padding:20px;text-align:center;box-shadow:4px 4px 0 #FF4D6D;margin-bottom:12px;">
                        <div style="font-size:2rem;">😅</div>
                        <div style="font-family:'Fredoka One',cursive;font-size:1.3rem;color:#FF4D6D;">
                            Not quite! The answer was:</div>
                        <div style="font-family:'Fredoka One',cursive;font-size:1.5rem;
                        color:#333;margin:6px 0;">{_correct}</div>
                        <div style="font-size:0.9rem;font-weight:700;color:#555;margin-top:4px;">
                            💡 {_q['fun_fact']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            if _qi + 1 < _total:
                if st.button("Next Question ➡️", use_container_width=True):
                    st.session_state.q_index      += 1
                    st.session_state.answered      = False
                    st.session_state.selected      = None
                    st.session_state.q_start_time  = None
                    st.rerun()
            else:
                if st.button("See My Score! 🏆", use_container_width=True):
                    st.session_state.game_over   = True
                    st.session_state.game_active = False
                    st.rerun()

    # ── TIME'S UP screen
    elif st.session_state.game_over and st.session_state.timed_out:
        _verse  = st.session_state.timeout_verse or {"verse": "Psalm 119:11", "text": "I have hidden your word in my heart."}
        _level  = st.session_state.game_level or "Kids (Easy)"
        _c      = LEVEL_COLORS[_level]
        _score  = st.session_state.score
        _total  = len(st.session_state.game_questions) if st.session_state.game_questions else 5

        st.markdown(
            f"""
            <div style="background:#fff0f0;border:4px solid #FF4D6D;border-radius:28px;
            padding:36px;text-align:center;box-shadow:6px 6px 0 #FF4D6D;">
                <div style="font-size:3.5rem;margin-bottom:8px;">⏰</div>
                <div style="font-family:'Fredoka One',cursive;font-size:2rem;color:#FF4D6D;margin-bottom:4px;">
                    Time's Up!
                </div>
                <div style="font-family:'Fredoka One',cursive;font-size:1.1rem;color:#555;margin-bottom:16px;">
                    Sorry, better luck next time! You scored {_score} out of {_total} before time ran out.
                </div>
                <div style="background:white;border:2.5px dashed #FF4D6D;border-radius:20px;
                padding:20px;margin:0 auto;max-width:480px;">
                    <div style="font-size:1.5rem;margin-bottom:8px;">📖</div>
                    <div style="font-family:'Fredoka One',cursive;font-size:1rem;color:#1A73E8;margin-bottom:8px;">
                        Go and read this Bible verse:</div>
                    <div style="font-family:'Fredoka One',cursive;font-size:1.4rem;color:#FF6B35;margin-bottom:8px;">
                        {_verse['verse']}</div>
                    <div style="font-style:italic;font-weight:700;color:#555;font-size:0.95rem;line-height:1.6;">
                        "{_verse['text']}"</div>
                </div>
                <div style="margin-top:16px;font-family:'Fredoka One',cursive;font-size:1rem;color:#888;">
                    Keep studying and come back stronger! 💪</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        _t1, _t2, _t3 = st.columns(3)
        with _t1:
            if st.button("🔄 Try Again!", key="timeout_retry", use_container_width=True):
                import random as _rnd2
                _qs2 = QUESTIONS[_level].copy()
                _rnd2.shuffle(_qs2)
                st.session_state.game_questions = _qs2[:5]
                st.session_state.q_index        = 0
                st.session_state.score          = 0
                st.session_state.answered       = False
                st.session_state.selected       = None
                st.session_state.game_over      = False
                st.session_state.game_active    = True
                st.session_state.timed_out      = False
                st.session_state.q_start_time   = None
                st.session_state.timeout_verse  = None
                st.rerun()
        with _t2:
            if st.button("🎯 Pick Level", key="timeout_level", use_container_width=True):
                st.session_state.game_active    = False
                st.session_state.game_over      = False
                st.session_state.timed_out      = False
                st.session_state.q_index        = 0
                st.session_state.score          = 0
                st.session_state.answered       = False
                st.session_state.selected       = None
                st.session_state.game_level     = None
                st.session_state.q_start_time   = None
                st.session_state.timeout_verse  = None
                st.rerun()
        with _t3:
            if st.button("🏠 Home", key="timeout_home", use_container_width=True):
                st.session_state.game_active    = False
                st.session_state.game_over      = False
                st.session_state.timed_out      = False
                st.session_state.q_index        = 0
                st.session_state.score          = 0
                st.session_state.answered       = False
                st.session_state.selected       = None
                st.session_state.game_level     = None
                st.session_state.q_start_time   = None
                st.session_state.timeout_verse  = None
                st.rerun()

    # ── Game over screen (normal)
    elif st.session_state.game_over:
        _score = st.session_state.score
        _level = st.session_state.game_level
        _c     = LEVEL_COLORS[_level]
        _total = len(st.session_state.game_questions)
        _msg   = next(m for threshold, m in SCORE_MESSAGES if _score >= threshold)
        _camp_msg = ""
        if _score == _total:
            _camp_msg = "🎉 See You at CAMP '26 — We can't wait!"
        elif _score >= int(_total * 0.6):
            _camp_msg = "⛺ See You at CAMP '26!"
        _pct   = int((_score / _total) * 100)
        _bar   = "#06D6A0" if _pct == 100 else "#1A73E8" if _pct >= 60 else "#FF6B35"
        _trophy = "🏆" if _score == _total else "🌟" if _score >= _total * 0.6 else "📖"

        st.markdown(
            f"""
            <div style="background:{_c['bg']};border:4px solid {_c['border']};
            border-radius:28px;padding:36px;text-align:center;
            box-shadow:6px 6px 0 {_c['border']};">
                <div style="font-size:3.5rem;margin-bottom:8px;">{_trophy}</div>
                <div style="font-family:'Fredoka One',cursive;font-size:2.5rem;color:{_c['badge']};">
                    {_score} / {_total}
                </div>
                <div style="background:#eee;border-radius:50px;height:18px;
                margin:12px auto;max-width:300px;overflow:hidden;">
                    <div style="background:linear-gradient(90deg,{_bar},{_c['border']});
                    width:{_pct}%;height:100%;border-radius:50px;"></div>
                </div>
                <div style="font-family:'Fredoka One',cursive;font-size:1.2rem;
                color:#444;margin-top:8px;">{_msg}</div>
                <div style="font-size:0.9rem;font-weight:700;color:#888;margin-top:8px;">
                    Level played: {_level}
                </div>
                {('<div style="font-family:Fredoka One,cursive;font-size:1.1rem;color:#FF6B35;font-weight:800;margin-top:12px;padding:10px 20px;background:#FFF8F0;border:2.5px solid #FF6B35;border-radius:50px;display:inline-block;">' + _camp_msg + '</div>') if _camp_msg else ""}
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        _rc1, _rc2, _rc3 = st.columns(3)
        with _rc1:
            if st.button("🔄 Play Again", use_container_width=True):
                import random as _random
                _qs = QUESTIONS[_level].copy()
                _random.shuffle(_qs)
                st.session_state.game_questions = _qs[:5]
                st.session_state.q_index        = 0
                st.session_state.score          = 0
                st.session_state.answered       = False
                st.session_state.selected       = None
                st.session_state.game_over      = False
                st.session_state.game_active    = True
                st.session_state.q_start_time   = None
                st.session_state.timed_out      = False
                st.session_state.timeout_verse  = None
                st.rerun()
        with _rc2:
            if st.button("🎯 Try Different Level", use_container_width=True):
                st.session_state.game_active = False
                st.session_state.game_over   = False
                st.session_state.q_index     = 0
                st.session_state.score       = 0
                st.session_state.answered    = False
                st.session_state.selected    = None
                st.session_state.game_level  = None
                st.session_state.q_start_time = None
                st.rerun()
        with _rc3:
            if st.button("🏠 Home", key="home_end", use_container_width=True):
                st.session_state.game_active = False
                st.session_state.game_over   = False
                st.session_state.q_index     = 0
                st.session_state.score       = 0
                st.session_state.answered    = False
                st.session_state.selected    = None
                st.session_state.game_level  = None
                st.session_state.q_start_time = None
                st.rerun()

# ─────────────────────────────────────────
# TAB 6 — MY FLYER
# ─────────────────────────────────────────
with tab6:
    st.markdown("### 🎨 Make Your 'I Will Be Attending' Flyer!")

    st.markdown('<div class="flyer-form">', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1])

    with col_left:
        name = st.text_input("✏️ Enter your name", placeholder="e.g. Favour")
        template_choice = st.selectbox(
            "🖼️ Choose a flyer version",
            list(THEMES.keys())
        )
        badge_choice = st.selectbox(
            "💬 Choose your flyer message",
            [
                "I Will Be Attending!",
                "I Look Forward to Camp '26!",
                "I Can't Wait to See You at Camp '26!",
            ]
        )

    with col_right:
        uploaded_file = st.file_uploader(
            "📸 Upload your photo here!",
            type=["jpg", "jpeg", "png"]
        )
        if not uploaded_file:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg,#fff0f7,#f0f4ff);
                border-radius:16px;padding:20px;
                text-align:center;
                border:3px dashed #C77DFF;
                animation: pulse-border 2s ease-in-out infinite;">
                <div style="font-size:2.5rem;margin-bottom:8px;">📸</div>
                <div style="font-family:'Fredoka One',cursive;font-size:1.2rem;color:#FF6B35;margin-bottom:4px;">
                    Drop Your Best Smile Here!
                </div>
                <div style="font-weight:800;color:#C77DFF;font-size:0.9rem;">
                    JPG, JPEG or PNG • Max 200MB
                </div>
                <div style="margin-top:8px;font-size:0.85rem;font-weight:700;color:#aaa;">
                    Your photo goes right on the flyer!
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if "flyer_png" not in st.session_state:
        st.session_state.flyer_png = None
    if "flyer_name" not in st.session_state:
        st.session_state.flyer_name = ""

    if st.button("🎨 Generate My Flyer!"):
        photo_img = None
        if uploaded_file:
            photo_img = Image.open(uploaded_file).convert("RGBA")
        with st.spinner("Creating your flyer... 🎉"):
            try:
                flyer_buf = generate_flyer(
                    theme_name=template_choice,
                    attendee_name=name,
                    photo_img=photo_img,
                    badge_text=badge_choice
                )
                flyer_buf.seek(0)
                st.session_state.flyer_png = flyer_buf.read()
                st.session_state.flyer_name = name or "attendee"
            except Exception as e:
                st.error(f"Oops! Something went wrong: {e}")

    if st.session_state.flyer_png:
        png_bytes  = st.session_state.flyer_png
        flyer_name = st.session_state.flyer_name

        st.markdown("### 🎉 Your Flyer is Ready!")
        st.image(png_bytes, use_column_width=True)

        dl_col1, dl_col2, dl_col3 = st.columns(3)

        with dl_col1:
            st.download_button(
                "⬇️ Download PNG",
                png_bytes,
                f"camp26_flyer_{flyer_name}.png",
                "image/png"
            )
        with dl_col2:
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=(540, 780))
            temp_path = "/tmp/flyer_temp.png"
            with open(temp_path, "wb") as f:
                f.write(png_bytes)
            c.drawImage(temp_path, 0, 0, 540, 780)
            c.save()
            st.download_button(
                "⬇️ Download PDF",
                pdf_buffer.getvalue(),
                f"camp26_flyer_{flyer_name}.pdf",
                "application/pdf"
            )
        with dl_col3:
            st.markdown(
                """
                <a href="https://wa.me/?text=I%20will%20be%20attending%20Sunday%20School%20Camp%2026!%20%F0%9F%8E%89%20God%20Answers%20Prayers!"
                target="_blank"
                style="
                    display:inline-block;
                    background:linear-gradient(135deg,#25D366,#128C7E);
                    color:white;
                    font-family:'Fredoka One',cursive;
                    font-size:1rem;
                    border-radius:50px;
                    padding:12px 24px;
                    text-decoration:none;
                    box-shadow:0 6px 20px rgba(37,211,102,0.35);
                    letter-spacing:1px;
                ">
                    📲 Share on WhatsApp
                </a>
                """,
                unsafe_allow_html=True
            )

# ─────────────────────────────────────────
# FOOTER (always visible)
# ─────────────────────────────────────────
st.markdown('<div class="fun-divider">🙏 🙏 🙏</div>', unsafe_allow_html=True)
st.markdown("""
<div style="
    text-align:center;
    background:linear-gradient(135deg,#1A73E8,#0D47A1);
    border-radius:20px;
    padding:24px;
    color:white;
    font-family:'Fredoka One',cursive;
    font-size:1.3rem;
    letter-spacing:1px;
    box-shadow:0 6px 24px rgba(0,0,0,0.1);
">
    🌟 See You at Camp '26! God Bless You! 🌟<br>
    <span style="font-family:'Nunito',sans-serif;font-size:0.9rem;font-weight:700;opacity:0.9;">
        August 13–16, 2026 • All Souls' Chapel OAU, Ile-Ife
    </span>
</div>
""", unsafe_allow_html=True)
