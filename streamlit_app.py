import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime
import io

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
# 🎨 CUSTOM CSS - LIGHT, COLOURFUL & MOBILE FRIENDLY
# ============================================================

st.markdown("""
<style>

/* ============================================================
   MAIN APP
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(147, 197, 253, 0.22),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(196, 181, 253, 0.20),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #f8fbff 0%,
            #eef6ff 50%,
            #fff8f0 100%
        );

    color: #172033;
}


/* ============================================================
   CONTENT AREA
   ============================================================ */

.block-container {
    max-width: 1200px;
    padding-top: 1rem;
    padding-bottom: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}


/* ============================================================
   HEADINGS
   ============================================================ */

h1, h2, h3, h4, h5, h6 {
    color: #172033 !important;
    font-weight: 800 !important;
    line-height: 1.25 !important;
}


/* ============================================================
   NORMAL TEXT
   ============================================================ */

p {
    color: #334155 !important;
    line-height: 1.5 !important;
}

label {
    color: #172033 !important;
    font-weight: 600 !important;
}


/* ============================================================
   HERO SECTION
   ============================================================ */

.hero {
    width: 100%;
    box-sizing: border-box;

    padding: 24px 20px;

    border-radius: 22px;

    background:
        linear-gradient(
            135deg,
            #60a5fa 0%,
            #818cf8 50%,
            #c084fc 100%
        );

    box-shadow:
        0 10px 28px rgba(79, 70, 229, 0.16);

    margin-bottom: 18px;

    overflow: hidden;
}

.hero-title {
    font-size: 36px;
    line-height: 1.15;

    font-weight: 900;

    color: #ffffff !important;

    margin: 0 0 8px 0;
}

.hero-subtitle {
    font-size: 16px;

    line-height: 1.4;

    color: #ffffff !important;

    margin: 0;
}


/* ============================================================
   CARDS
   ============================================================ */

.card {
    width: 100%;
    box-sizing: border-box;

    padding: 20px;

    border-radius: 18px;

    background: rgba(255, 255, 255, 0.96);

    border: 1px solid #dbe7f3;

    box-shadow:
        0 6px 20px rgba(30, 64, 175, 0.07);

    margin-bottom: 16px;

    overflow: hidden;
}


/* ============================================================
   RESULT CARD
   ============================================================ */

.result-card {
    width: 100%;
    box-sizing: border-box;

    padding: 22px;

    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            #e0f2fe,
            #ede9fe
        );

    border: 1px solid #c7d8f0;

    box-shadow:
        0 8px 24px rgba(30, 64, 175, 0.08);

    margin-bottom: 18px;

    overflow: hidden;
}

.sign-name {
    font-size: 28px;

    line-height: 1.2;

    font-weight: 900;

    color: #172033 !important;

    word-wrap: break-word;
}

.confidence {
    font-size: 38px;

    line-height: 1.1;

    font-weight: 900;

    color: #2563eb !important;
}


/* ============================================================
   BADGES
   ============================================================ */

.badge {
    display: inline-block;

    padding: 6px 11px;

    border-radius: 999px;

    background: #e0ecff;

    color: #1e40af !important;

    border: 1px solid #bfd5f5;

    margin-right: 5px;

    margin-bottom: 5px;

    font-size: 13px;

    font-weight: 700;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    width: 100%;

    min-height: 44px;

    background:
        linear-gradient(
            90deg,
            #4f8cff,
            #6366f1,
            #8b5cf6
        );

    color: #ffffff !important;

    border: none;

    border-radius: 11px;

    padding: 9px 16px;

    font-size: 15px;

    font-weight: 800;

    box-shadow:
        0 5px 14px rgba(79, 70, 229, 0.18);
}

.stButton > button:hover {
    transform: translateY(-1px);

    box-shadow:
        0 8px 18px rgba(79, 70, 229, 0.23);
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

    padding: 9px 12px !important;

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

    min-height: 42px;
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

    border-radius: 16px !important;

    padding: 14px !important;
}

section[data-testid="stFileUploaderDropzone"] * {
    color: #172033 !important;
}


/* ============================================================
   METRICS
   ============================================================ */

div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.96);

    border: 1px solid #dbe5f0;

    border-radius: 15px;

    padding: 13px;

    box-shadow:
        0 5px 15px rgba(30, 64, 175, 0.07);
}

div[data-testid="stMetricLabel"] {
    color: #64748b !important;

    font-size: 13px !important;
}

div[data-testid="stMetricValue"] {
    color: #172033 !important;

    font-size: 25px !important;

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

    border-right: 1px solid #dbe5f0;
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

    overflow: hidden;
}

div[data-testid="stExpander"] * {
    color: #172033 !important;
}


/* ============================================================
   DATAFRAME
   ============================================================ */

div[data-testid="stDataFrame"] {
    background: #ffffff;

    border-radius: 12px;

    border: 1px solid #dbe5f0;

    overflow: hidden;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    width: 100%;

    text-align: center;

    padding: 20px 10px;

    color: #475569 !important;

    font-size: 13px;

    line-height: 1.4;
}


/* ============================================================
   DIVIDER
   ============================================================ */

hr {
    border-color: #dbe5f0 !important;

    margin: 12px 0 !important;
}


/* ============================================================
   MOBILE - SMALL PHONE
   ============================================================ */

@media (max-width: 600px) {

    .block-container {
        padding-left: 0.7rem;
        padding-right: 0.7rem;
        padding-top: 0.7rem;
    }

    .hero {
        padding: 20px 16px;

        border-radius: 18px;

        margin-bottom: 14px;
    }

    .hero-title {
        font-size: 28px;

        line-height: 1.15;

        word-break: normal;
    }

    .hero-subtitle {
        font-size: 14px;

        line-height: 1.35;
    }

    .card {
        padding: 16px;

        border-radius: 16px;
    }

    .result-card {
        padding: 18px;

        border-radius: 17px;
    }

    .sign-name {
        font-size: 24px;
    }

    .confidence {
        font-size: 32px;
    }

    .badge {
        font-size: 12px;

        padding: 5px 9px;
    }

    .stButton > button {
        min-height: 42px;

        font-size: 14px;
    }

}


/* ============================================================
   VERY SMALL PHONE
   ============================================================ */

@media (max-width: 400px) {

    .hero {
        padding: 17px 14px;
    }

    .hero-title {
        font-size: 21px;
    }

    .hero-subtitle {
        font-size: 13px;
    }

    .card {
        padding: 14px;
    }

    .result-card {
        padding: 15px;
    }

    .sign-name {
        font-size: 21px;
    }

    .confidence {
        font-size: 29px;
    }

}


/* ============================================================
   PREVENT HORIZONTAL OVERFLOW
   ============================================================ */

html, body {
    overflow-x: hidden !important;
}

[data-testid="stAppViewContainer"] {
    overflow-x: hidden !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================

if "name" not in st.session_state:
    st.session_state.name = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🚦 Traffic Sign AI")

    st.markdown(
        "### 👤 " +
        (st.session_state.name
         if st.session_state.name
         else "Guest")
    )

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

<br>

<span class="badge">🐍 Python</span>
<span class="badge">🎨 Streamlit</span>
<span class="badge">🧠 AI</span>
<span class="badge">🚦 GTSRB</span>
<span class="badge">📱 Mobile Friendly</span>

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
    Enter your name below and start analyzing traffic signs
    using our interactive recognition interface.
    </p>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input(
        "👤 Enter Your Name",
        value=st.session_state.name,
        placeholder="Enter your name"
    )

    if st.button("💾 Save Name", use_container_width=True):

        if name.strip():

            st.session_state.name = name.strip()

            st.success(
                f"Welcome, {st.session_state.name}! 👋"
            )

        else:

            st.warning("Please enter your name.")

    if st.session_state.name:

        st.markdown(
            f"""
            <div class="result-card">

            <h2>
            👋 Welcome, {st.session_state.name}!
            </h2>

            <p>
            Your Traffic Sign AI dashboard is ready.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-title">📊 Project Overview</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("🚦 Classes", "43")

    with c2:
        st.metric("🧠 AI", "CNN")

    with c3:
        st.metric("📚 Dataset", "GTSRB")

    with c4:
        st.metric(
            "🔍 Predictions",
            len(st.session_state.history)
        )

    st.markdown(
        '<div class="section-title">✨ Main Features</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="card">
        <h3>🔍 Recognition</h3>
        Upload a traffic-sign image and analyze it.
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="card">
        <h3>📊 Analytics</h3>
        Track predictions and confidence statistics.
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="card">
        <h3>🛡️ Safety</h3>
        Learn the meaning and recommended action for signs.
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# RECOGNIZE
# ============================================================

elif page == "🔍 Recognize Sign":

    st.markdown(
        '<div class="section-title">🔍 Recognize Traffic Sign</div>',
        unsafe_allow_html=True
    )

    uploaded = st.file_uploader(
        "📤 Upload a traffic sign image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded:

        image = Image.open(uploaded).convert("RGB")

        left, right = st.columns([1.1, 1])

        with left:

            st.markdown("### 🖼️ Image")

            st.image(
                image,
                caption=uploaded.name,
                use_container_width=True
            )

            width, height = image.size

            st.markdown("### 📐 Image Information")

            x, y, z = st.columns(3)

            with x:
                st.metric("Width", f"{width}px")

            with y:
                st.metric("Height", f"{height}px")

            with z:
                st.metric(
                    "Format",
                    uploaded.type.upper()
                )

        with right:

            # ------------------------------------------------
            # DEMO RESULT
            # ------------------------------------------------

            predicted_class = 14
            confidence = 98.7

            name, category, meaning, action = \
                SIGNS[predicted_class]

            st.markdown(
                f"""
                <div class="result-card">

                <div class="sign-name">
                🛑 {name}
                </div>

                <div class="confidence">
                {confidence}%
                </div>

                <p>Confidence</p>

                <span class="badge">
                Class {predicted_class}
                </span>

                <span class="badge">
                {category}
                </span>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(confidence / 100)

            if confidence >= 90:

                st.success(
                    "🟢 High Confidence"
                )

            elif confidence >= 70:

                st.warning(
                    "🟡 Moderate Confidence"
                )

            else:

                st.error(
                    "🔴 Low Confidence"
                )

            st.markdown("### 📚 Sign Information")

            st.write(
                f"**Meaning:** {meaning}"
            )

            st.write(
                f"**Driver Action:** {action}"
            )

            st.write(
                f"**Category:** {category}"
            )

            st.write(
                f"**GTSRB Class:** {predicted_class}"
            )

        # ----------------------------------------------------
        # TOP 5
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">🔝 Top 5 Predictions</div>',
            unsafe_allow_html=True
        )

        top5 = pd.DataFrame({
            "Rank": [1, 2, 3, 4, 5],
            "Traffic Sign": [
                "STOP",
                "No Entry",
                "Yield",
                "No Vehicles",
                "Priority Road"
            ],
            "Confidence": [
                "98.7%",
                "0.6%",
                "0.4%",
                "0.2%",
                "0.1%"
            ]
        })

        st.dataframe(
            top5,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # SAFETY
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">🛡️ Safety Recommendation</div>',
            unsafe_allow_html=True
        )

        st.info(
            f"🚦 {name}: {action}"
        )

        # ----------------------------------------------------
        # HISTORY BUTTON
        # ----------------------------------------------------

        if st.button(
            "➕ Save Prediction to History",
            use_container_width=True
        ):

            st.session_state.history.append({

                "Date & Time":
                    datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S"
                    ),

                "User":
                    st.session_state.name
                    if st.session_state.name
                    else "Guest",

                "Image":
                    uploaded.name,

                "Prediction":
                    name,

                "Class":
                    predicted_class,

                "Category":
                    category,

                "Confidence":
                    confidence
            })

            st.success(
                "✅ Prediction saved successfully!"
            )

        st.warning(
            "⚠️ Current result is a demonstration result. "
            "Connect your trained traffic-sign model before "
            "using this as a real AI prediction."
  )
      # ============================================================
# SIGN LIBRARY
# ============================================================

elif page == "📚 Sign Library":

    st.markdown(
        '<div class="section-title">📚 Traffic Sign Library</div>',
        unsafe_allow_html=True
    )

    search = st.text_input(
        "🔎 Search sign",
        placeholder="Example: stop, speed, curve..."
    )

    category = st.selectbox(
        "📂 Select Category",
        [
            "All",
            "Regulatory",
            "Warning",
            "Mandatory"
        ]
    )

    count = 0

    for class_id, data in SIGNS.items():

        sign_name, cat, meaning, action = data

        if category != "All" and cat != category:
            continue

        if search and \
           search.lower() not in sign_name.lower():
            continue

        count += 1

        with st.expander(
            f"🚦 {sign_name}"
        ):

            st.write(
                f"**Class:** {class_id}"
            )

            st.write(
                f"**Category:** {cat}"
            )

            st.write(
                f"**Meaning:** {meaning}"
            )

            st.write(
                f"**Driver Action:** {action}"
            )

    st.info(
        f"Showing {count} traffic signs."
    )

# ============================================================
# SAFETY ASSISTANT
# ============================================================

elif page == "🛡️ Safety Assistant":

    st.markdown(
        '<div class="section-title">🛡️ Road Safety Assistant</div>',
        unsafe_allow_html=True
    )

    selected = st.selectbox(
        "Select a traffic sign",
        [
            data[0]
            for data in SIGNS.values()
        ]
    )

    selected_id = next(
        class_id
        for class_id, data in SIGNS.items()
        if data[0] == selected
    )

    name, category, meaning, action = \
        SIGNS[selected_id]

    st.markdown(
        f"""
        <div class="result-card">

        <div class="sign-name">
        🚦 {name}
        </div>

        <br>

        <span class="badge">
        {category}
        </span>

        <span class="badge">
        Class {selected_id}
        </span>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📖 Meaning")

    st.write(meaning)

    st.markdown("### 🚘 Recommended Driver Action")

    st.success(action)

    st.markdown("### ⚠️ Safety Reminder")

    st.warning(
        "Always follow actual road signs, traffic signals "
        "and local traffic laws. This application is an "
        "educational/project demonstration."
    )

# ============================================================
# ANALYTICS
# ============================================================

elif page == "📊 Analytics":

    st.markdown(
        '<div class="section-title">📊 Analytics Dashboard</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.history:

        st.info(
            "No predictions available yet."
        )

    else:

        df = pd.DataFrame(
            st.session_state.history
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Total Predictions",
                len(df)
            )

        with c2:
            st.metric(
                "Average Confidence",
                f"{df['Confidence'].mean():.1f}%"
            )

        with c3:
            st.metric(
                "Highest Confidence",
                f"{df['Confidence'].max():.1f}%"
            )

        with c4:
            st.metric(
                "Lowest Confidence",
                f"{df['Confidence'].min():.1f}%"
            )

        st.markdown("### 📈 Confidence Chart")

        chart_data = df[
            ["Prediction", "Confidence"]
        ].copy()

        chart_data = chart_data.set_index(
            "Prediction"
        )

        st.bar_chart(
            chart_data
        )

        st.markdown("### 📊 Prediction Table")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Download CSV Report",
            data=csv,
            file_name="traffic_sign_report.csv",
            mime="text/csv",
            use_container_width=True
        )

# ============================================================
# HISTORY
# ============================================================

elif page == "🕘 History":

    st.markdown(
        '<div class="section-title">🕘 Prediction History</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.history:

        st.info(
            "Prediction history is empty."
        )

    else:

        df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Export History",
            csv,
            "prediction_history.csv",
            "text/csv",
            use_container_width=True
        )

        if st.button(
            "🗑️ Clear History",
            use_container_width=True
        ):

            st.session_state.history = []

            st.success(
                "History cleared."
            )

            st.rerun()

# ============================================================
# DEMO MODE
# ============================================================

elif page == "🧪 Demo Mode":

    st.markdown(
        '<div class="section-title">🧪 Demonstration Mode</div>',
        unsafe_allow_html=True
    )

    st.info(
        "This mode is useful for your college presentation "
        "when the actual model is unavailable."
    )

    demos = {
        "🛑 STOP": 14,
        "🚫 NO ENTRY": 17,
        "⚠️ GENERAL CAUTION": 18,
        "🚸 CHILDREN CROSSING": 28,
        "↪️ TURN RIGHT": 33,
        "🔵 KEEP RIGHT": 38,
        "5️⃣ SPEED LIMIT 50": 2
    }

    selected = st.selectbox(
        "Choose Demo Sign",
        list(demos.keys())
    )

    class_id = demos[selected]

    name, category, meaning, action = \
        SIGNS[class_id]

    demo_confidence = {
        14: 98.7,
        17: 97.3,
        18: 95.8,
        28: 94.5,
        33: 96.4,
        38: 97.8,
        2: 96.9
    }[class_id]

    st.markdown(
        f"""
        <div class="result-card">

        <div class="sign-name">
        🚦 {name}
        </div>

        <div class="confidence">
        {demo_confidence}%
        </div>

        <p>Demonstration Confidence</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        demo_confidence / 100
    )

    st.write(
        f"**Category:** {category}"
    )

    st.write(
        f"**Meaning:** {meaning}"
    )

    st.success(
        f"🚘 Driver Action: {action}"
    )

# ============================================================
# ABOUT
# ============================================================

elif page == "ℹ️ About":

    st.markdown(
        '<div class="section-title">ℹ️ About Project</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="card">

    <h2>🚦 Traffic Sign Recognition System</h2>

    <p>
    A computer-vision based application designed to
    classify traffic-sign images and provide useful
    road-safety information.
    </p>

    </div>
    """, unsafe_allow_html=True)

    a, b = st.columns(2)

    with a:

        st.markdown("### 🛠️ Technologies")

        st.write("🐍 Python")
        st.write("🎨 Streamlit")
        st.write("🖼️ Pillow")
        st.write("📊 Pandas")
        st.write("🧠 Deep Learning")
        st.write("🚦 GTSRB Dataset")

    with b:

        st.markdown("### 🎯 Applications")

        st.write("• Driver assistance")
        st.write("• Road safety education")
        st.write("• Intelligent transportation")
        st.write("• Traffic-sign learning")
        st.write("• Computer Vision demonstration")

    st.markdown("### 👤 Project User")

    if st.session_state.name:

        st.success(
            f"Project user: {st.session_state.name}"
        )

    else:

        st.info(
            "No name entered yet."
        )

    st.markdown("### ⚠️ Disclaimer")

    st.write(
        "This application is an educational project. "
        "It should not be used as a substitute for official "
        "traffic signs, traffic signals or professional "
        "driver-assistance systems."
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

🚦 Traffic Sign AI

<br>

Python • Streamlit • Computer Vision • GTSRB

<br><br>

BCA Project

</div>
""", unsafe_allow_html=True)
