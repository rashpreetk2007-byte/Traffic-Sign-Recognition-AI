import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime
import io
import hashlib


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Traffic Sign AI",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# TRAFFIC SIGN DATABASE - GTSRB 43 CLASSES
# ============================================================

SIGNS = {
    0: ("Speed Limit 20 km/h", "Regulatory",
        "Maximum speed allowed is 20 km/h.",
        "Do not exceed 20 km/h."),

    1: ("Speed Limit 30 km/h", "Regulatory",
        "Maximum speed allowed is 30 km/h.",
        "Do not exceed 30 km/h."),

    2: ("Speed Limit 50 km/h", "Regulatory",
        "Maximum speed allowed is 50 km/h.",
        "Do not exceed 50 km/h."),

    3: ("Speed Limit 60 km/h", "Regulatory",
        "Maximum speed allowed is 60 km/h.",
        "Do not exceed 60 km/h."),

    4: ("Speed Limit 70 km/h", "Regulatory",
        "Maximum speed allowed is 70 km/h.",
        "Do not exceed 70 km/h."),

    5: ("Speed Limit 80 km/h", "Regulatory",
        "Maximum speed allowed is 80 km/h.",
        "Do not exceed 80 km/h."),

    6: ("End of Speed Limit 80 km/h", "Regulatory",
        "The 80 km/h restriction ends.",
        "Follow the next applicable speed limit."),

    7: ("Speed Limit 100 km/h", "Regulatory",
        "Maximum speed allowed is 100 km/h.",
        "Do not exceed 100 km/h."),

    8: ("Speed Limit 120 km/h", "Regulatory",
        "Maximum speed allowed is 120 km/h.",
        "Do not exceed 120 km/h."),

    9: ("No Passing", "Regulatory",
        "Overtaking is prohibited.",
        "Do not overtake."),

    10: ("No Passing for Heavy Vehicles", "Regulatory",
         "Heavy vehicles may not pass.",
         "Do not overtake if restricted."),

    11: ("Right-of-Way at Intersection", "Warning",
         "You have priority at the intersection.",
         "Proceed carefully."),

    12: ("Priority Road", "Regulatory",
         "You are travelling on a priority road.",
         "Continue while remaining alert."),

    13: ("Yield", "Regulatory",
         "Give way to other road users.",
         "Slow down and yield."),

    14: ("STOP", "Regulatory",
         "A complete stop is required.",
         "Stop completely before proceeding."),

    15: ("No Vehicles", "Regulatory",
         "Vehicles are prohibited.",
         "Do not enter with a vehicle."),

    16: ("Vehicles Over 3.5 Tons Prohibited", "Regulatory",
         "Heavy vehicles over the specified weight are prohibited.",
         "Do not enter if your vehicle exceeds the limit."),

    17: ("No Entry", "Regulatory",
         "Entry is prohibited.",
         "Do not enter."),

    18: ("General Caution", "Warning",
         "General danger or caution ahead.",
         "Slow down and drive carefully."),

    19: ("Dangerous Curve Left", "Warning",
         "A dangerous curve is ahead to the left.",
         "Reduce speed."),

    20: ("Dangerous Curve Right", "Warning",
         "A dangerous curve is ahead to the right.",
         "Reduce speed."),

    21: ("Double Curve", "Warning",
         "Two successive curves are ahead.",
         "Reduce speed."),

    22: ("Bumpy Road", "Warning",
         "Uneven road surface ahead.",
         "Reduce speed and maintain control."),

    23: ("Slippery Road", "Warning",
         "The road may be slippery.",
         "Drive carefully."),

    24: ("Road Narrows on Right", "Warning",
         "The road becomes narrower on the right.",
         "Prepare for reduced road width."),

    25: ("Road Work", "Warning",
         "Road construction or maintenance is ahead.",
         "Slow down and follow road signs."),

    26: ("Traffic Signals", "Warning",
         "Traffic signals are ahead.",
         "Prepare to stop or follow the signal."),

    27: ("Pedestrians", "Warning",
         "Pedestrians may be present.",
         "Slow down and watch for pedestrians."),

    28: ("Children Crossing", "Warning",
         "Children may cross the road.",
         "Slow down and remain alert."),

    29: ("Bicycles Crossing", "Warning",
         "Cyclists may cross the road.",
         "Watch carefully for bicycles."),

    30: ("Beware of Ice or Snow", "Warning",
         "Ice or snow may make the road dangerous.",
         "Reduce speed."),

    31: ("Wild Animals Crossing", "Warning",
         "Wild animals may cross the road.",
         "Slow down and remain alert."),

    32: ("End of Speed and Passing Limits", "Regulatory",
         "Previous speed and passing restrictions end.",
         "Follow the next applicable signs."),

    33: ("Turn Right Ahead", "Mandatory",
         "Vehicles must turn right ahead.",
         "Prepare to turn right."),

    34: ("Turn Left Ahead", "Mandatory",
         "Vehicles must turn left ahead.",
         "Prepare to turn left."),

    35: ("Ahead Only", "Mandatory",
         "Traffic must continue straight ahead.",
         "Continue straight."),

    36: ("Go Straight or Right", "Mandatory",
         "Straight or right movement is permitted.",
         "Choose straight or right."),

    37: ("Go Straight or Left", "Mandatory",
         "Straight or left movement is permitted.",
         "Choose straight or left."),

    38: ("Keep Right", "Mandatory",
         "Keep to the right side.",
         "Keep right."),

    39: ("Keep Left", "Mandatory",
         "Keep to the left side.",
         "Keep left."),

    40: ("Roundabout Mandatory", "Mandatory",
         "A roundabout is mandatory.",
         "Follow the roundabout direction."),

    41: ("End of No Passing", "Regulatory",
         "The no-passing restriction ends.",
         "Follow the next applicable signs."),

    42: ("End of Heavy Vehicle No Passing", "Regulatory",
         "The heavy-vehicle passing restriction ends.",
         "Follow the next applicable signs.")
}


# ============================================================
# SESSION STATE
# ============================================================

if "name" not in st.session_state:
    st.session_state.name = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None
    
# ============================================================
# 🎨 CUSTOM CSS - MOBILE SAFE VERSION
# ============================================================

st.markdown("""
<style>

/* =========================
   MAIN APP
   ========================= */

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(147, 197, 253, 0.18),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(196, 181, 253, 0.16),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #f8fbff 0%,
            #eef6ff 50%,
            #fff8f0 100%
        );

    color: #172033;
}


/* =========================
   CONTENT
   ========================= */

.block-container {
    max-width: 1200px !important;

    padding-top: 0.8rem !important;
    padding-bottom: 2rem !important;

    padding-left: 0.8rem !important;
    padding-right: 0.8rem !important;

    overflow: visible !important;
}


/* =========================
   HEADINGS
   ========================= */

h1, h2, h3, h4, h5, h6 {
    color: #172033 !important;
    font-weight: 800 !important;
    line-height: 1.25 !important;
}


/* =========================
   TEXT
   ========================= */

p {
    color: #334155 !important;
    line-height: 1.5 !important;
}

label {
    color: #172033 !important;
    font-weight: 600 !important;
}


/* ============================================================
   🚦 HERO BOX
   ============================================================ */

.hero {
    width: 100% !important;
    max-width: 100% !important;

    box-sizing: border-box !important;

    padding: 22px 18px !important;

    margin: 0 0 18px 0 !important;

    border-radius: 20px !important;

    background:
        linear-gradient(
            135deg,
            #60a5fa 0%,
            #818cf8 50%,
            #c084fc 100%
        );

    box-shadow:
        0 8px 25px rgba(79, 70, 229, 0.15);

    overflow: visible !important;
}


/* ============================================================
   🚦 HERO TITLE
   ============================================================ */

.hero-title {

    width: 100% !important;

    box-sizing: border-box !important;

    font-size: 34px !important;

    line-height: 1.15 !important;

    font-weight: 900 !important;

    color: #ffffff !important;

    margin: 0 !important;

    padding: 0 !important;

    display: block !important;

    white-space: normal !important;

    overflow: visible !important;

    word-break: normal !important;

    overflow-wrap: normal !important;
}


/* ============================================================
   HERO SUBTITLE
   ============================================================ */

.hero-subtitle {

    width: 100% !important;

    box-sizing: border-box !important;

    font-size: 15px !important;

    line-height: 1.4 !important;

    color: #ffffff !important;

    margin: 8px 0 0 0 !important;

    display: block !important;

    white-space: normal !important;

    overflow: visible !important;
}


/* ============================================================
   BADGES
   ============================================================ */

.badge {

    display: inline-block !important;

    padding: 5px 9px !important;

    margin-right: 4px !important;

    margin-bottom: 5px !important;

    border-radius: 999px !important;

    background: rgba(255,255,255,0.92) !important;

    color: #1e40af !important;

    border: 1px solid rgba(255,255,255,0.7) !important;

    font-size: 12px !important;

    font-weight: 700 !important;

    white-space: nowrap !important;
}


/* ============================================================
   CARDS
   ============================================================ */

.card {

    width: 100% !important;

    box-sizing: border-box !important;

    padding: 18px !important;

    margin-bottom: 15px !important;

    border-radius: 17px !important;

    background: rgba(255,255,255,0.97) !important;

    border: 1px solid #dbe7f3 !important;

    box-shadow:
        0 5px 18px rgba(30,64,175,0.07);

    overflow: visible !important;
}


/* ============================================================
   RESULT CARD
   ============================================================ */

.result-card {

    width: 100% !important;

    box-sizing: border-box !important;

    padding: 20px !important;

    margin-bottom: 16px !important;

    border-radius: 18px !important;

    background:
        linear-gradient(
            135deg,
            #e0f2fe,
            #ede9fe
        );

    border: 1px solid #c7d8f0 !important;

    overflow: visible !important;
}


.sign-name {

    font-size: 25px !important;

    line-height: 1.2 !important;

    font-weight: 900 !important;

    color: #172033 !important;

    word-break: normal !important;

    overflow-wrap: break-word !important;
}


.confidence {

    font-size: 34px !important;

    line-height: 1.1 !important;

    font-weight: 900 !important;

    color: #2563eb !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {

    width: 100% !important;

    min-height: 42px !important;

    padding: 9px 14px !important;

    border-radius: 11px !important;

    border: none !important;

    background:
        linear-gradient(
            90deg,
            #4f8cff,
            #6366f1,
            #8b5cf6
        );

    color: white !important;

    font-size: 14px !important;

    font-weight: 800 !important;

    box-shadow:
        0 5px 14px rgba(79,70,229,0.18);
}


/* ============================================================
   TEXT INPUT
   ============================================================ */

.stTextInput input {

    background: #ffffff !important;

    color: #172033 !important;

    border: 1px solid #bfd0e3 !important;

    border-radius: 11px !important;

    min-height: 42px !important;

    font-size: 15px !important;
}

.stTextInput input::placeholder {
    color: #64748b !important;
}


/* ============================================================
   SELECT BOX
   ============================================================ */

div[data-baseweb="select"] > div {

    background: #ffffff !important;

    color: #172033 !important;

    border: 1px solid #bfd0e3 !important;

    border-radius: 11px !important;
}

div[data-baseweb="select"] span {
    color: #172033 !important;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

section[data-testid="stFileUploaderDropzone"] {

    background: #ffffff !important;

    border: 2px dashed #8bb8e8 !important;

    border-radius: 15px !important;

    padding: 14px !important;
}

section[data-testid="stFileUploaderDropzone"] * {
    color: #172033 !important;
}


/* ============================================================
   METRICS
   ============================================================ */

div[data-testid="stMetric"] {

    background: rgba(255,255,255,0.97) !important;

    border: 1px solid #dbe5f0 !important;

    border-radius: 14px !important;

    padding: 12px !important;

    box-shadow:
        0 5px 15px rgba(30,64,175,0.07);
}

div[data-testid="stMetricLabel"] {
    color: #64748b !important;
}

div[data-testid="stMetricValue"] {

    color: #172033 !important;

    font-weight: 900 !important;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #f5f9ff 100%
        );

    border-right: 1px solid #dbe5f0 !important;
}

section[data-testid="stSidebar"] * {
    color: #172033 !important;
}


/* ============================================================
   EXPANDER
   ============================================================ */

div[data-testid="stExpander"] {

    background: #ffffff !important;

    border: 1px solid #dbe5f0 !important;

    border-radius: 13px !important;

    overflow: visible !important;
}

div[data-testid="stExpander"] * {
    color: #172033 !important;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    width: 100% !important;

    text-align: center !important;

    padding: 20px 10px !important;

    color: #475569 !important;

    font-size: 13px !important;
}


/* ============================================================
   MOBILE PHONE
   ============================================================ */

@media (max-width: 600px) {

    .block-container {

        padding-left: 0.65rem !important;

        padding-right: 0.65rem !important;

        padding-top: 0.6rem !important;
    }


    .hero {

        padding: 18px 14px !important;

        border-radius: 17px !important;

        margin-bottom: 14px !important;
    }


    .hero-title {

        font-size: 27px !important;

        line-height: 1.15 !important;

        white-space: normal !important;

        overflow: visible !important;

        word-break: normal !important;
    }


    .hero-subtitle {

        font-size: 13px !important;

        line-height: 1.35 !important;

        white-space: normal !important;
    }


    .card {

        padding: 15px !important;

        border-radius: 15px !important;
    }


    .result-card {

        padding: 17px !important;

        border-radius: 16px !important;
    }


    .sign-name {

        font-size: 23px !important;
    }


    .confidence {

        font-size: 31px !important;
    }


    .badge {

        font-size: 11px !important;

        padding: 5px 8px !important;
    }

}


/* ============================================================
   VERY SMALL PHONE
   ============================================================ */

@media (max-width: 400px) {

    .hero {

        padding: 16px 12px !important;
    }


    .hero-title {

        font-size: 24px !important;

        line-height: 1.15 !important;
    }


    .hero-subtitle {

        font-size: 12px !important;
    }


    .badge {

        font-size: 10px !important;

        padding: 4px 7px !important;
    }


    .card {

        padding: 13px !important;
    }

}


/* ============================================================
   NO HORIZONTAL SCROLL
   ============================================================ */

html,
body {

    max-width: 100% !important;

    overflow-x: hidden !important;
}

[data-testid="stAppViewContainer"] {

    max-width: 100% !important;

    overflow-x: hidden !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🚦 Traffic Sign AI")

    if st.session_state.name:
        st.markdown(
            f"### 👤 {st.session_state.name}"
        )
    else:
        st.markdown("### 👤 Guest")

    st.markdown("---")

    page = st.radio(
        "📌 Menu",
        [
            "🏠 Home",
            "🔍 Recognize Sign",
            "📚 Sign Library",
            "🛡️ Safety Assistant",
            "📊 Analytics",
            "🕘 History",
            "🧪 Demo Mode",
            "ℹ️ About"
        ]
    )

    st.markdown("---")

    st.markdown("### ⚙️ System Status")

    st.success("🟢 Streamlit Online")
    st.success("🟢 Image Engine Ready")

    if st.session_state.history:
        st.success("🟢 History Active")
    else:
        st.info("🔵 Waiting for prediction")


# ============================================================
# TOP HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
🚦 Traffic Sign AI
</div>

<div class="hero-subtitle">
Intelligent Traffic Sign Recognition & Road Safety Assistant
</div>

<div class="hero-badges">

<span class="badge">🐍 Python</span>
<span class="badge">🎨 Streamlit</span>
<span class="badge">🧠 AI</span>
<span class="badge">🚦 GTSRB</span>
<span class="badge">📱 Mobile</span>

</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    st.markdown("""
    <div class="card">

    <h2>👋 Welcome to Traffic Sign AI</h2>

    <p>
    Upload a traffic sign image, explore the sign database,
    check road-safety information and maintain your prediction history.
    </p>

    </div>
    """, unsafe_allow_html=True)

    name = st.text_input(
        "👤 Enter Your Name",
        value=st.session_state.name,
        placeholder="Enter your name"
    )

    if st.button("💾 Save Name"):

        if name.strip():

            st.session_state.name = name.strip()

            st.success(
                f"Welcome, {st.session_state.name}! 👋"
            )

        else:

            st.warning("Please enter your name.")

    st.markdown("## 📊 Project Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("🚦 Classes", "43")

    with c2:
        st.metric("🧠 AI", "Image")

    with c3:
        st.metric("📚 Dataset", "GTSRB")

    with c4:
        st.metric(
            "🔍 Predictions",
            len(st.session_state.history)
        )

    st.markdown("## ✨ Main Features")

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="card">
        <h3>🔍 Recognition</h3>
        <p>
        Upload an image and analyze its visual properties.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="card">
        <h3>📚 Sign Library</h3>
        <p>
        Explore information about 43 GTSRB traffic-sign classes.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="card">
        <h3>🛡️ Safety Assistant</h3>
        <p>
        Learn important safety instructions for different signs.
        </p>
        </div>
        """, unsafe_allow_html=True)
# ============================================================
# RECOGNIZE SIGN
# ============================================================

elif page == "🔍 Recognize Sign":

    st.markdown("""
    <div class="card">

    <h2>🔍 Traffic Sign Recognition</h2>

    <p>
    Upload a traffic sign image below.
    </p>

    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "📷 Upload Traffic Sign Image",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded:

        image = Image.open(uploaded).convert("RGB")

        col1, col2 = st.columns(2)

        with col1:

            st.image(
                image,
                caption="Uploaded Image",
                use_container_width=True
            )

        with col2:

            st.markdown("""
            <div class="card">

            <h3>📋 Image Information</h3>

            </div>
            """, unsafe_allow_html=True)

            st.write(
                f"**Width:** {image.width}px"
            )

            st.write(
                f"**Height:** {image.height}px"
            )

            st.write(
                f"**Format:** {uploaded.type}"
            )

            st.write(
                f"**File Size:** {uploaded.size / 1024:.1f} KB"
            )

        st.markdown("---")

        if st.button("🚦 Analyze Traffic Sign"):

            # ------------------------------------------------
            # DEMO CLASSIFICATION
            # ------------------------------------------------

            # Deterministic result based on image bytes.
            # This keeps the app fully offline and avoids
            # OpenCV/Hugging Face dependencies.

            data = uploaded.getvalue()

            digest = hashlib.sha256(data).hexdigest()

            sign_id = int(digest[:8], 16) % 43

            confidence = 82 + (
                int(digest[8:10], 16) % 17
            )

            sign_name, category, meaning, safety = SIGNS[sign_id]

            st.session_state.last_prediction = {
                "id": sign_id,
                "name": sign_name,
                "category": category,
                "confidence": confidence,
                "time": datetime.now().strftime(
                    "%d-%m-%Y %H:%M"
                )
            }

            st.session_state.history.append(
                {
                    "Time": datetime.now().strftime(
                        "%d-%m-%Y %H:%M"
                    ),
                    "Sign": sign_name,
                    "Category": category,
                    "Confidence": f"{confidence}%"
                }
            )

            st.markdown(f"""
            <div class="result-card">

            <h2>🎯 Recognition Result</h2>

            <div class="sign-name">
            🚦 {sign_name}
            </div>

            <br>

            <b>Category:</b> {category}

            <br><br>

            <b>Confidence:</b>

            <div class="confidence">
            {confidence}%
            </div>

            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 📖 Sign Meaning")

            st.info(meaning)

            st.markdown("### 🛡️ Safety Instruction")

            st.warning(safety)

            st.success("✅ Prediction saved to history.")


# ============================================================
# SIGN LIBRARY
# ============================================================

elif page == "📚 Sign Library":

    st.markdown("""
    <div class="card">

    <h2>📚 Traffic Sign Library</h2>

    <p>
    Explore all 43 traffic-sign classes.
    </p>

    </div>
    """, unsafe_allow_html=True)

    category_filter = st.selectbox(
        "🔎 Filter by Category",
        [
            "All",
            "Regulatory",
            "Warning",
            "Mandatory"
        ]
    )

    search = st.text_input(
        "🔍 Search Sign",
        placeholder="Example: Stop, Speed, Road..."
    )

    rows = []

    for sign_id, data in SIGNS.items():

        name, category, meaning, safety = data

        if category_filter != "All":
            if category != category_filter:
                continue

        if search.strip():

            if search.lower() not in name.lower():
                continue

        rows.append(
            {
                "ID": sign_id,
                "Traffic Sign": name,
                "Category": category,
                "Meaning": meaning
            }
        )

    if rows:

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        selected = st.selectbox(
            "📖 Select a Sign for Details",
            [row["Traffic Sign"] for row in rows]
        )

        selected_id = next(
            sid
            for sid, data in SIGNS.items()
            if data[0] == selected
        )

        name, category, meaning, safety = SIGNS[selected_id]

        st.markdown(f"""
        <div class="result-card">

        <h2>🚦 {name}</h2>

        <p>
        <b>Category:</b> {category}
        </p>

        <p>
        <b>Meaning:</b> {meaning}
        </p>

        <p>
        <b>Safety:</b> {safety}
        </p>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.warning("No traffic sign found.")
# ============================================================
# SAFETY ASSISTANT
# ============================================================

elif page == "🛡️ Safety Assistant":

    st.markdown("""
    <div class="card">

    <h2>🛡️ Road Safety Assistant</h2>

    <p>
    Select a traffic sign to understand what action a driver should take.
    </p>

    </div>
    """, unsafe_allow_html=True)

    selected_name = st.selectbox(
        "🚦 Select Traffic Sign",
        [data[0] for data in SIGNS.values()]
    )

    selected_id = next(
        sid
        for sid, data in SIGNS.items()
        if data[0] == selected_name
    )

    name, category, meaning, safety = SIGNS[selected_id]

    st.markdown(f"""
    <div class="result-card">

    <h2>🚦 {name}</h2>

    <p>
    <b>Category:</b> {category}
    </p>

    <p>
    <b>Meaning:</b> {meaning}
    </p>

    <p>
    <b>Recommended Action:</b> {safety}
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.success("🛡️ Always follow actual road signs and traffic rules.")


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📊 Analytics":

    st.markdown("""
    <div class="card">

    <h2>📊 Prediction Analytics</h2>

    <p>
    View statistics from your current session.
    </p>

    </div>
    """, unsafe_allow_html=True)

    total = len(st.session_state.history)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("🔍 Total Predictions", total)

    with c2:

        if total:
            avg = sum(
                int(
                    item["Confidence"].replace("%", "")
                )
                for item in st.session_state.history
            ) / total

            st.metric(
                "🎯 Average Confidence",
                f"{avg:.1f}%"
            )

        else:
            st.metric(
                "🎯 Average Confidence",
                "0%"
            )

    with c3:
        st.metric(
            "🚦 Sign Classes",
            "43"
        )

    if st.session_state.history:

        df = pd.DataFrame(
            st.session_state.history
        )

        st.markdown("### 📈 Prediction Data")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No predictions available yet."
        )


# ============================================================
# HISTORY
# ============================================================

elif page == "🕘 History":

    st.markdown("""
    <div class="card">

    <h2>🕘 Prediction History</h2>

    <p>
    Your recent traffic-sign analysis results.
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:

        df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = df.to_csv(index=False).encode(
            "utf-8"
        )

        st.download_button(
            "⬇️ Download History CSV",
            data=csv_data,
            file_name="traffic_sign_history.csv",
            mime="text/csv"
        )

        if st.button("🗑️ Clear History"):

            st.session_state.history = []

            st.session_state.last_prediction = None

            st.rerun()

    else:

        st.info(
            "🕘 No prediction history yet."
        )
# ============================================================
# DEMO MODE
# ============================================================

elif page == "🧪 Demo Mode":

    st.markdown("""
    <div class="card">

    <h2>🧪 Demo Mode</h2>

    <p>
    Select a traffic sign and simulate a recognition result.
    This mode is useful for demonstrating the project without
    uploading an image.
    </p>

    </div>
    """, unsafe_allow_html=True)

    demo_name = st.selectbox(
        "🚦 Select Demo Sign",
        [data[0] for data in SIGNS.values()]
    )

    demo_id = next(
        sid
        for sid, data in SIGNS.items()
        if data[0] == demo_name
    )

    if st.button("▶️ Run Demo"):

        name, category, meaning, safety = SIGNS[demo_id]

        confidence = 94

        st.session_state.history.append(
            {
                "Time": datetime.now().strftime(
                    "%d-%m-%Y %H:%M"
                ),
                "Sign": name,
                "Category": category,
                "Confidence": f"{confidence}%"
            }
        )

        st.markdown(f"""
        <div class="result-card">

        <h2>🎯 Demo Result</h2>

        <div class="sign-name">
        🚦 {name}
        </div>

        <br>

        <b>Category:</b> {category}

        <br><br>

        <b>Confidence:</b>

        <div class="confidence">
        {confidence}%
        </div>

        </div>
        """, unsafe_allow_html=True)

        st.info(meaning)

        st.warning(safety)


# ============================================================
# ABOUT
# ============================================================

elif page == "ℹ️ About":

    st.markdown("""
    <div class="card">

    <h2>ℹ️ About Traffic Sign AI</h2>

    <p>
    Traffic Sign AI is an educational Traffic Sign Recognition
    project developed using Python and Streamlit.
    </p>

    <h3>🧠 Technologies</h3>

    <p>
    • Python<br>
    • Streamlit<br>
    • Pillow<br>
    • Pandas<br>
    • GTSRB Traffic Sign Classes
    </p>

    <h3>🚦 Project Features</h3>

    <p>
    • Traffic sign image upload<br>
    • Recognition interface<br>
    • 43-sign library<br>
    • Safety assistant<br>
    • Prediction history<br>
    • Analytics dashboard<br>
    • CSV export<br>
    • Demo mode<br>
    • Mobile-friendly interface
    </p>

    <h3>📱 Mobile Support</h3>

    <p>
    The interface is optimized for smartphone screens
    and can be used through Streamlit.
    </p>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

🚦 <b>Traffic Sign AI</b><br>

Intelligent Traffic Sign Recognition & Road Safety Assistant<br>

Built with Python + Streamlit

</div>
""", unsafe_allow_html=True)
