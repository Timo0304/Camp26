import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from reportlab.pdfgen import canvas
from datetime import datetime
import os

from flyer_generator import generate_flyer, THEMES

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
    font-size: clamp(2rem, 6vw, 3.6rem) !important;
    color: white !important;
    text-shadow: 3px 3px 0px rgba(0,0,0,0.2);
    margin: 16px 0 8px;
    letter-spacing: 1px;
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
div[data-baseweb="input"] input,
div[data-baseweb="select"] div {
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
</style>
""", unsafe_allow_html=True)


# ------------------------------------
# HEADER BANNER
# ------------------------------------

st.markdown("""
<div class="rainbow-banner">
    <h1>⛺ Sunday School Camp '26 ⛺</h1>
    <h2>🙏 Theme: God Answers Prayers 🙏</h2>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sticker-row">🎉 ✝️ 🎊 🌟 🎈 🙌 🎵 💛 🎠 ⭐</div>', unsafe_allow_html=True)


# ------------------------------------
# COUNTDOWN TIMER
# ------------------------------------

event_date = datetime(2026, 8, 13)
now = datetime.now()
time_left = event_date - now
days = time_left.days
hours = time_left.seconds // 3600
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


# ------------------------------------
# ABOUT THE PROGRAM
# ------------------------------------

st.markdown("### 🎒 What's This Camp About?")

st.markdown("""
<div class="about-card">
    <p style="font-size:1.1rem; font-weight:700; color:#555; margin:0 0 8px;">
        Get ready for the most AMAZING Biannual Retreat ever!
        Come and experience God's power with fellow Sunday School kids and teens! 🎉
    </p>
    <ul class="emoji-list">
        <li>🔥 Powerful teachings that light up your heart</li>
        <li>🙏 Life-changing testimonies & miracles</li>
        <li>🤝 Make new friends & awesome connections</li>
        <li>🚀 Practical sessions to grow as a leader</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="fun-divider">⭐ ⭐ ⭐</div>', unsafe_allow_html=True)


# ------------------------------------
# EVENT DETAILS
# ------------------------------------

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

st.markdown('<div class="fun-divider">💛 💛 💛</div>', unsafe_allow_html=True)


# ------------------------------------
# TESTIMONIES
# ------------------------------------

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
        <div class="author">— Love 2024; ⭐⭐⭐⭐⭐</div>
    </div>
    <div class="testimony-card">
        <span class="tag">🔥 Highlight</span>
        <span class="bubble-icon">🥳</span>
        <div class="speech-text">"Yes! I enjoyed myself in the camp"</div>
        <div class="author">— Mosope 2024; ⭐⭐⭐⭐⭐</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="fun-divider">📸 📸 📸</div>', unsafe_allow_html=True)


# ------------------------------------
# PHOTO GALLERY
# ------------------------------------

st.markdown("### 🖼️ Pictures From Last Edition")

col1, col2, col3 = st.columns(3)

with col1:
    if os.path.exists("images/photo1.jpg"):
        st.image("images/photo1.jpg", caption="🎤 Opening Session", use_column_width=True)
    else:
        st.info("📷 Opening session photo coming soon!")

with col2:
    if os.path.exists("images/photo2.jpg"):
        st.image("images/photo2.jpg", caption="🤝 Participants", use_column_width=True)
    else:
        st.info("📷 Participants photo coming soon!")

with col3:
    if os.path.exists("images/photo3.jpg"):
        st.image("images/photo3.jpg", caption="🙏 Prayer Session", use_column_width=True)
    else:
        st.info("📷 Prayer session photo coming soon!")

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
        📸 View All Photos and Videos from Camp' 24 edition on Google Drive 📸
    </a>
</div>
""", unsafe_allow_html=True)

# ------------------------------------
# BULLETIN
# ------------------------------------

st.markdown("### 📄 Bulletin From Last Edition")

with open("bulletin.pdf", "rb") as f:
    pdf_data = f.read()

st.download_button(
    label="📥 Download Last Edition Bulletin",
    data=pdf_data,
    file_name="camp24_bulletin.pdf",
    mime="application/pdf"
)

st.markdown('<div class="fun-divider">📞 📞 📞</div>', unsafe_allow_html=True)

# ------------------------------------
# ENQUIRIES
# ------------------------------------

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

st.markdown('<div class="fun-divider">🎨 🎨 🎨</div>', unsafe_allow_html=True)

# ------------------------------------
# FLYER GENERATOR
# ------------------------------------

st.markdown("### 🎨 Make Your 'I Will Be Attending' Flyer!")

st.markdown('<div class="flyer-form">', unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1])

with col_left:
    name = st.text_input("✏️ Enter your name", placeholder="e.g. Favour")
    template_choice = st.selectbox(
        "🖼️ Choose a flyer version",
        list(THEMES.keys())
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
            border:2px dashed #C77DFF;
            color:#888;font-weight:700;">
            🌟 Upload your best smile photo!<br>
            <small>We'll put it on your awesome flyer 🎉</small>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------
# FLYER GENERATION
# ------------------------------------

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
                photo_img=photo_img
            )
            flyer_buf.seek(0)
            st.session_state.flyer_png = flyer_buf.read()
            st.session_state.flyer_name = name or "attendee"
        except Exception as e:
            st.error(f"Oops! Something went wrong: {e}")

if st.session_state.flyer_png:
    png_bytes = st.session_state.flyer_png
    flyer_name = st.session_state.flyer_name

    st.markdown("### 🎉 Your Flyer is Ready!")
    st.image(png_bytes, use_column_width=True)

    dl_col1, dl_col2, dl_col3 = st.columns(3)

    # PNG DOWNLOAD
    with dl_col1:
        st.download_button(
            "⬇️ Download PNG",
            png_bytes,
            f"camp26_flyer_{flyer_name}.png",
            "image/png"
        )

    # PDF DOWNLOAD
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

    # WHATSAPP SHARE
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

# ------------------------------------
# FOOTER
# ------------------------------------

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
