# ==========================================================
# AI FIRST AID ASSISTANT
# Version 3.0
# Developed by Gaurav Yadav
# ==========================================================


# ==========================================================
# IMPORTS
# ==========================================================

import os

import json

import time

import streamlit as st

from groq import Groq

import streamlit.components.v1 as components

from dotenv import load_dotenv

from streamlit_local_storage import LocalStorage

from google import genai

from PIL import Image

from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from reportlab.lib.styles import getSampleStyleSheet

from streamlit_geolocation import streamlit_geolocation
import requests

from translations import translations

# ==========================================================
# BROWSER LOCAL STORAGE
# ==========================================================

local_storage = LocalStorage()

MAX_PERSONAL_CONTACTS = 15


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI First Aid Assistant",
    page_icon="🩹",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# LOAD GEMINI API
# ==========================================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ==========================================================
# LANGUAGE SELECTION
# ==========================================================

language = st.sidebar.selectbox(
    "🌐 Select Language",
    list(translations.keys())
)

t = translations[language]
# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🩹 AI First Aid")

st.sidebar.caption("Powered by Google Gemini")

st.sidebar.divider()

option = st.sidebar.radio(
    "🧭 Navigation",
    [
        t["home"],
        t["chat"],
        t["help"],
        t["burns"],
        t["bleeding"],
        t["fractures"],
        t["choking"],
        t["snake"],
        t["cpr"],
        t["wellbeing"],
    ]
)

st.sidebar.divider()

st.sidebar.success("🌐 Supports 6 Languages")

st.sidebar.caption("👨‍💻 Developed by Gaurav Yadav")


# ==========================================================
# PAGE COLORS
# ==========================================================

page_colors = {

    t["home"]: ("#3B82F6", "#60A5FA"),

    t["chat"]: ("#0F766E", "#14B8A6"),

    t["burns"]: ("#F59E0B", "#FBBF24"),

    t["bleeding"]: ("#DC2626", "#F87171"),

    t["fractures"]: ("#475569", "#94A3B8"),

    t["choking"]: ("#9333EA", "#C084FC"),
"🏠 " +
    t["snake"]: ("#16A34A", "#4ADE80"),

    t["cpr"]: ("#EC4899", "#F472B6"),

    t["wellbeing"]: ("#631CB9", "#506AEC"),
}

color1, color2 = page_colors.get(
    option,
    ("#2563EB", "#38BDF8")
)

# ==========================================================
# CSS
# ==========================================================

st.markdown(
    """
<style>

/* ==========================================================
   GLOBAL THEME AND TEXT VISIBILITY
========================================================== */

.stApp {
    background: #F8FAFC !important;
    color: #1E293B !important;
}

/* Main page text */
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li,
.stApp [data-testid="stMarkdownContainer"] h1,
.stApp [data-testid="stMarkdownContainer"] h2,
.stApp [data-testid="stMarkdownContainer"] h3,
.stApp [data-testid="stMarkdownContainer"] h4 {
    color: #1E293B;
}

/* Labels and captions */
.stApp label,
.stApp [data-testid="stCaptionContainer"],
.stApp .stText,
.stApp small {
    color: #334155;
}

/* ==========================================================
   HIDE STREAMLIT
========================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* ==========================================================
   SIDEBAR
========================================================== */

section[data-testid="stSidebar"] {
    background: #F1F5F9 !important;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
    color: #1E293B;
}

/* ==========================================================
   BUTTONS
========================================================== */

.stButton > button {
    width: 100%;
    border: none;
    border-radius: 14px;
    padding: 12px;
    background: #2563EB !important;
    color: #FFFFFF !important;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background: #1D4ED8 !important;
    color: #FFFFFF !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(37,99,235,.25);
}

/* ==========================================================
   INPUTS AND TEXT AREA
========================================================== */

input,
textarea {
    color: #1E293B !important;
    background: #FFFFFF !important;
    border-radius: 12px !important;
}

input::placeholder,
textarea::placeholder {
    color: #64748B !important;
    opacity: 1;
}

[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label {
    color: #1E293B !important;
}

/* ==========================================================
   SELECT BOXES
========================================================== */

[data-testid="stSelectbox"] label {
    color: #1E293B !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: #FFFFFF !important;
    color: #1E293B !important;
}

/* ==========================================================
   RADIO BUTTONS AND CHECKBOXES
========================================================== */

[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label {
    color: #1E293B !important;
}

/* ==========================================================
   SIDEBAR NAVIGATION BUTTONS
========================================================== */

div[data-testid="stRadio"] [role="radiogroup"] {
    gap: 8px;
}

div[data-testid="stRadio"] label {
    background: #FFFFFF !important;
    color: #1E293B !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    padding: 8px 14px !important;
    margin-bottom: 5px !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    font-size: 16px !important;
}

div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] label span {
    color: #1E293B !important;
}

div[data-testid="stRadio"] label:hover {
    background: #EFF6FF !important;
    border-color: #93C5FD !important;
    transform: translateX(4px);
}

div[data-testid="stRadio"] label:has(input[type="radio"]:checked) {
    background: #2563EB !important;
    color: #FFFFFF !important;
    border-color: #2563EB !important;
    font-weight: 600 !important;
    box-shadow: 0 8px 18px rgba(37,99,235,.25);
}

div[data-testid="stRadio"] label:has(input[type="radio"]:checked) p,
div[data-testid="stRadio"] label:has(input[type="radio"]:checked) span {
    color: #FFFFFF !important;
}

/* ==========================================================
   FILE UPLOADER
========================================================== */

[data-testid="stFileUploader"] {
    border-radius: 14px;
    border: 2px dashed #CBD5E1;
    padding: 15px;
    background: #FFFFFF !important;
}

[data-testid="stFileUploader"] * {
    color: #1E293B;
}

/* ==========================================================
   METRICS
========================================================== */

[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border-radius: 16px;
    padding: 14px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 4px 12px rgba(0,0,0,.08);
    color: #1E293B !important;
}

/* ==========================================================
   DOWNLOAD BUTTON
========================================================== */

[data-testid="stDownloadButton"] button {
    border-radius: 14px;
    color: #FFFFFF !important;
}

/* ==========================================================
   ALERTS
========================================================== */

[data-testid="stSuccess"],
[data-testid="stWarning"],
[data-testid="stError"],
[data-testid="stInfo"] {
    border-radius: 14px;
}

/* ==========================================================
   LINK BUTTON
========================================================== */

[data-testid="stLinkButton"] a {
    border-radius: 12px !important;
    background: #DC2626 !important;
    color: #FFFFFF !important;
    font-weight: 600;
}

[data-testid="stLinkButton"] a:hover {
    background: #B91C1C !important;
    color: #FFFFFF !important;
}

/* ==========================================================
   IMAGES
========================================================== */

img {
    border-radius: 14px;
}

/* ==========================================================
   ANIMATION
========================================================== */

.block-container {
    animation: fade .35s ease;
}

@keyframes fade {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ==========================================================
   MOBILE RESPONSIVENESS
========================================================== */

@media (max-width: 768px) {

    .block-container {
        padding: 1rem 1rem 3rem 1rem !important;
    }

    .stApp {
        color: #1E293B !important;
    }

    .stButton > button {
        width: 100%;
        min-height: 44px;
        font-size: 15px;
    }

    h1 {
        font-size: 1.8rem !important;
    }

    h2 {
        font-size: 1.5rem !important;
    }

    h3 {
        font-size: 1.25rem !important;
    }

    p, li, label {
        font-size: 15px;
    }

    [data-testid="stMetric"] {
        padding: 10px;
    }
}

</style>
""",
    unsafe_allow_html=True
)






# ==========================================================
# HEADER
# ==========================================================

if option == t["home"]:   

    # LARGE HEADER - HOME PAGE
    st.html(
        f"""
        <div style="
            background:linear-gradient(135deg,{color1},{color2});
            padding:35px;
            border-radius:22px;
            color:white;
            text-align:center;
            margin-bottom:25px;
            box-shadow:0 10px 25px rgba(0,0,0,.15);
        ">

            <h1 style="margin-bottom:10px;font-size:42px;color:white;">
                🩹 AI First Aid Assistant
            </h1>

            <p style="font-size:18px;margin-bottom:20px;color:white;">
                Instant AI-powered First Aid Guidance using Google Gemini
            </p>

            <hr style="
                border:1px solid rgba(255,255,255,.25);
                width:80%;
                margin:auto;
                margin-bottom:20px;
            ">

            <div style="
                display:flex;
                justify-content:center;
                gap:30px;
                flex-wrap:wrap;
                font-size:15px;
                font-weight:600;
            ">
                <span>🌐 6 Languages</span>
                <span>📷 Image Analysis</span>
                <span>📄 PDF Reports</span>
                <span>🤖 Gemini AI</span>
                <span>🚑 Emergency Guides</span>
                            </div>
            
                        <div style="
                margin-top:22px;
                padding-top:14px;
                border-top:1px solid rgba(255,255,255,.25);
                font-size:13px;
                line-height:1.6;
                color:white;
            ">
                ⚠️ For educational purposes only. Always contact emergency medical services during serious emergencies.
            </div>

        </div>
        """
    )
    
    # FIND NEARBY HOSPITAL BUTTON
    st.link_button(
        "🏥 Find Nearby Hospitals",
        "https://www.google.com/maps/search/hospitals+near+me"
    )

else:

    # COMPACT HEADER - ALL OTHER PAGES
    st.html(
        f"""
        <div style="
            background:linear-gradient(135deg,{color1},{color2});
            padding:12px 20px;
            border-radius:14px;
            color:white;
            text-align:center;
            margin-bottom:15px;
            box-shadow:0 4px 12px rgba(0,0,0,.10);
        ">

            <h2 style="
                margin:0;
                padding:0;
                font-size:24px;
                color:white;
            ">
                🩹 AI First Aid Assistant
            </h2>

        </div>
        """
    )

# ==========================================================
# DEVELOPER BRANDING
# ==========================================================

st.html("""
<div style="
    display:flex;
    justify-content:flex-end;
    margin:0 5px 15px 0;
">
    <div style="
        text-align:right;
        padding:8px 14px;
        border-radius:12px;
        background:#F1F5F9;
        border:1px solid #E2E8F0;
    ">
        <div style="
            font-size:14px;
            font-weight:700;
            color:#1E293B;
        ">
            🩹 AI First Aid Assistant
            <span style="
                font-size:10px;
                color:#64748B;
                font-weight:500;
            ">v3.0</span>
        </div>

        <div style="
            font-size:11px;
            color:#64748B;
            margin-top:3px;
        ">
            Developed by Gaurav Yadav
        </div>

        <div style="
            font-size:10px;
            color:#94A3B8;
        ">
            B.Sc. Computer Science
        </div>
    </div>
</div>
""")




# ==========================================================
# HELPER FUNCTIONS
# ==========================================================


def generate_ai_response(contents):

    try:

        # IMAGE INPUT: Use Gemini
        if isinstance(contents, list):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents
            )

            return response.text

        # TEXT INPUT: Use Groq
        else:

            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "user",
                        "content": contents
                    }
                ],
                temperature=0.3,
                max_completion_tokens=1024
            )

            return response.choices[0].message.content

    except Exception as e:

        provider = "Gemini" if isinstance(contents, list) else "Groq"

        print(f"{provider} API Error: {type(e).__name__}: {e}")

        if provider == "Gemini":
            st.warning(
                "Image analysis is temporarily unavailable. Please try again later."
            )
        else:
            st.error(
                "Sorry, the AI couldn't generate a response. Please try again."
            )

        return None
    
def scroll_to_latest_chat():
    st.components.v1.html(
        """
        <script>
        function updateChatPosition() {
            const doc = window.parent.document;
            const win = window.parent;

            // 1. Bring the AI Chat section to the top
            const anchor = doc.getElementById("ai-chat-anchor");

            if (anchor) {
                const top =
                    anchor.getBoundingClientRect().top + win.scrollY;

                win.scrollTo({
                    top: top,
                    behavior: "smooth"
                });
            }

            // 2. Scroll the conversation to its latest message
            const messages = doc.querySelectorAll(
                '[data-testid="stChatMessage"]'
            );

            if (messages.length > 0) {
                const latestMessage = messages[messages.length - 1];

                let parent = latestMessage.parentElement;

                while (parent && parent !== doc.body) {
                    const style = win.getComputedStyle(parent);

                    if (
                        (style.overflowY === "auto" ||
                         style.overflowY === "scroll") &&
                        parent.scrollHeight > parent.clientHeight
                    ) {
                        parent.scrollTo({
                            top: parent.scrollHeight,
                            behavior: "smooth"
                        });
                        break;
                    }

                    parent = parent.parentElement;
                }
            }
        }

        setTimeout(updateChatPosition, 300);
        setTimeout(updateChatPosition, 800);
        setTimeout(updateChatPosition, 1300);
        </script>
        """,
        height=0,
    )


# ==========================================================
# PDF REPORT
# ==========================================================

def create_pdf(title, content):

    pdf_file = "First_Aid_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b><font size='20'>AI FIRST AID ASSISTANT</font></b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Date:</b> {datetime.now().strftime('%d %B %Y %I:%M %p')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            f"<b>Report:</b> {title}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 18))

    story.append(
        Paragraph(
            "<b>First Aid Guidance</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            content.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Disclaimer</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "This report was generated using Google Gemini AI. "
            "It is intended for educational purposes only and "
            "should not replace professional medical advice.",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Developed By:</b> Gaurav Yadav",
            styles["Italic"]
        )
    )

    doc.build(story)

    return pdf_file



# ==========================================================
# QUICK FIRST AID
# ==========================================================

def show_first_aid(topic):

    st.subheader(f"🩹 {topic}")

    st.info(
        f"Click the button below to receive AI-generated first aid guidance for **{topic}**."
    )

    if st.button(
        f"Get First Aid for {topic}",
        key=topic,
        use_container_width=True
    ):

        prompt = f"""
You are an expert AI First Aid Assistant designed for users in India.

CRITICAL INSTRUCTION:
The user has specifically selected this emergency category:

"{topic}"

You MUST provide first-aid guidance ONLY for this exact category.

Do not replace it with minor cuts, general injuries, or any other
medical condition.

CATEGORY-SPECIFIC RULES:
- Burns: Explain burn first aid, cooling the burn under cool
  running water for 20 minutes, and appropriate protection.
- Bleeding: Explain direct pressure, wound protection and
  emergency help for severe bleeding.
- Fractures: Explain immobilisation, avoiding movement and
  emergency assistance.
- Choking: Explain appropriate choking first aid based on
  whether the person is an adult, child or infant.
- Snake Bite: Explain keeping the person still, immobilising
  the affected limb, urgent hospital care and what NOT to do.
- Cardiopulmonary Resuscitation (CPR): Explain checking
  responsiveness and normal breathing, calling emergency
  services, and starting CPR/AED steps where appropriate.

IMPORTANT LOCATION RULES:
- Assume the user is in India unless explicitly told otherwise.
- India's main emergency number is 112.
- Ambulance: 108.
- Never recommend 911 unless the user explicitly states
  they are in the USA.
- Never invent emergency numbers.

Reply ONLY in {t["reply_language"]}.

Use this exact structure:

🩺 Injury

📊 Severity

🩹 First Aid
• Step 1
• Step 2
• Step 3

❌ Do NOT
• Point 1
• Point 2

🏥 Visit Hospital If
• Point 1
• Point 2

Keep the answer under 180 words.

Use medically appropriate, evidence-based first-aid guidance.
Do not diagnose diseases.
If the situation is life-threatening, prioritise emergency services.
"""

        with st.spinner("Generating First Aid..."):

            answer = generate_ai_response(prompt)

        if answer:

            st.markdown(
                f"""
                <div style="
                    background:#F8FAFF;
                    padding:22px;
                    border-radius:16px;
                    border-left:6px solid #2563EB;
                    box-shadow:0 6px 18px rgba(0,0,0,.10);
                    margin-bottom:20px;
                ">

                <h3 style="color:#2563EB;">
                    🩺 AI First Aid Guidance
                </h3>

                <div style="
                    font-size:16px;
                    line-height:1.8;
                    white-space:pre-wrap;
                    color:#333333;
                ">
                {answer.replace(chr(10), "<br>")}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption(
                "⚠️ AI-generated guidance. Always seek professional medical assistance during emergencies."
            )

            pdf = create_pdf(
                topic,
                answer
            )

            with open(pdf, "rb") as file:

                st.download_button(
                    "⬇ Download First Aid Report",
                    data=file,
                    file_name="First_Aid_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )


# ==========================================================
# HOME PAGE
# ==========================================================


if option == t["home"]:
    


    # ======================================================
    # LOAD PERSONAL CONTACTS FOR SOS
    # ======================================================

    SOS_CONTACTS_KEY = "ai_first_aid_personal_contacts"

    sos_stored_data = local_storage.getItem(SOS_CONTACTS_KEY)

    try:
        if isinstance(sos_stored_data, str):
            sos_contacts = json.loads(sos_stored_data)
        elif isinstance(sos_stored_data, list):
            sos_contacts = sos_stored_data
        else:
            sos_contacts = []

        if not isinstance(sos_contacts, list):
            sos_contacts = []

    except (json.JSONDecodeError, TypeError):
        sos_contacts = []

    sos_contacts = [
        contact for contact in sos_contacts
        if isinstance(contact, dict)
        and contact.get("name")
        and contact.get("phone")
    ]

    # ======================================================
    # SOS DISTRESS SIGNAL
    # ======================================================


    components.html(
        """
        <div id="sos-container">

            <style>
                #sos-container {
                    font-family: Arial, sans-serif;
                    padding: 12px 0 18px;
                    text-align: center;
                }

                #action-row {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 12px;
                align-items: start;
                justify-items: center;
                width: 100%;
                }

                .action-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: flex-start;
                width: 100%;
                min-width: 0;
                align-self: start;
                }

                .action-button {
                width: 100%;
                max-width: 110px;
                aspect-ratio: 1 / 1;
                border-radius: 50%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 5px;
                color: white;
                font-weight: bold;
                cursor: pointer;
                border: 4px solid rgba(255,255,255,.65);
                box-shadow: 0 5px 16px rgba(0,0,0,.15);
                padding: 5px;
                text-align: center;
                font-family: Arial, sans-serif;
                margin: 0;
                }

                #hospital-button {
                    background: #2563EB;
                    font-size: 12px;
                }

                #sos-button {
                    background: #DC2626;
                    border: 5px solid #FECACA;
                    font-size: 25px;
                    touch-action: none;
                    user-select: none;
                }

                #location-button {
                    background: #16A34A;
                    font-size: 12px;
                }

                .action-button:active {
                    transform: scale(.95);
                }

                #sos-button:disabled {
                    opacity: .7;
                    cursor: not-allowed;
                }

                .action-icon {
                    font-size: 25px;
                }
                .action-description {
                    font-size: 9px;
                    font-weight: 500;
                    line-height: 1.2;
                    max-width: 85px;
                }

                #sos-status {
                    margin-top: 14px;
                    font-size: 13px;
                    color: #64748B;
                    text-align: center;
                    line-height: 1.5;
                }

                #location-result {
                    display: none;
                    margin-top: 8px;
                    font-size: 13px;
                    color: #2563EB;
                    text-decoration: underline;
                }

                #sos-cancel,
                #sos-share {
                    display: none;
                    margin-top: 12px;
                    padding: 11px 20px;
                    border-radius: 9px;
                    font-weight: bold;
                    cursor: pointer;
                }

                #sos-cancel {
                    border: 1px solid #DC2626;
                    background: white;
                    color: #DC2626;
                }

                #sos-share {
                    border: none;
                    background: #16A34A;
                    color: white;
                }
                #location-result {
                display: none;
                width: 100%;
                margin-top: 10px;
                padding: 8px 5px;
                text-align: center;
                box-sizing: border-box;
                overflow-wrap: anywhere;
            }

            #place-name {
                font-size: 12px;
                font-weight: 700;
                line-height: 1.5;
                color: #1E293B;
            }

            #gps-coordinates {
                font-size: 10px;
                line-height: 1.7;
                color: #475569;
                margin-top: 5px;
            }

            #open-map {
                display: inline-block;
                margin-top: 8px;
                font-size: 11px;
                font-weight: 700;
                color: #2563EB;
                text-decoration: underline;
                cursor: pointer;
            }
            </style>

            <div id="action-row">

                <!-- HOSPITAL BUTTON -->
                <div class="action-item">
                    <button
                        id="hospital-button"
                        class="action-button"
                        type="button"
                    >
                        <span class="action-icon">🏥</span>
                        <span>HOSPITAL</span>
                        <span class="action-description">
                            Find nearby hospitals
                        </span>
                    </button>
                </div>

                <!-- SOS BUTTON -->
                <div class="action-item">
                    <button
                        id="sos-button"
                        class="action-button"
                        type="button"
                    >
                        <span class="action-icon">🆘</span>
                        <span>SOS</span>
                    </button>

                    <div id="sos-status">
                        Press and hold SOS for 3 seconds
                    </div>

                    <button id="sos-cancel" type="button">
                        Cancel SOS
                    </button>

                    <button id="sos-share" type="button">
                        Share SOS Alert on WhatsApp
                    </button>
                </div>

                <!-- LOCATION BUTTON -->
                <div class="action-item">
                    <button
                        id="location-button"
                        class="action-button"
                        type="button"
                    >
                        <span class="action-icon">📍</span>
                        <span>LOCATION</span>
                        <span class="action-description">
                            Get your current location
                        </span>
                    </button>

                    <div id="location-result">
                        <div id="place-name"></div>
                        <div id="gps-coordinates"></div>

                        <a
                            id="open-map"
                            href="#"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            Open Map
                        </a>
                    </div>
                </div>

            </div>

            <script>
                const button = document.getElementById("sos-button");
                const hospitalButton = document.getElementById("hospital-button");
                const locationButton = document.getElementById("location-button");
                const status = document.getElementById("sos-status");
                const cancelButton = document.getElementById("sos-cancel");
                const shareButton = document.getElementById("sos-share");
                const locationResult = document.getElementById("location-result");

                let holdTimer = null;
                let countdownTimer = null;
                let countdown = 5;
                let activationStarted = false;
                let mapsLink = "";

                hospitalButton.addEventListener("click", function() {
                    window.open(
                        "https://www.google.com/maps/search/?api=1&query=hospitals+near+me",
                        "_blank"
                    );
                });

                function getLocation(forSOS = false) {
                    status.textContent = "Getting your location...";
                    locationResult.style.display = "none";

                    if (!navigator.geolocation) {
                        status.textContent =
                            "Location is not supported by this browser.";

                        if (forSOS) {
                            shareButton.style.display = "block";
                        }

                        return;
                    }

                    navigator.geolocation.getCurrentPosition(
                    async function(position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    mapsLink =
                        "https://www.google.com/maps?q=" +
                        latitude + "," + longitude;

                    if (forSOS) {
                        status.textContent =
                            "Location ready. You can now share your SOS alert.";

                        shareButton.style.display = "block";

                    } else {
                        status.textContent =
                            "Your location has been retrieved.";

                        const placeName =
                            document.getElementById("place-name");

                        const coordinates =
                            document.getElementById("gps-coordinates");

                        const openMap =
                            document.getElementById("open-map");

                        locationResult.style.display = "block";

                        coordinates.textContent =
                            "Latitude: " + latitude.toFixed(6) +
                            "° | Longitude: " + longitude.toFixed(6) + "°";

                        openMap.href = mapsLink;

                        placeName.textContent = "Finding nearby place...";

                        try {
                            const response = await fetch(
                                "https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=" +
                                latitude + "&lon=" + longitude
                            );

                            if (!response.ok) {
                                throw new Error("Location lookup failed");
                            }

                            const data = await response.json();

                            placeName.textContent =
                                data.name ||
                                data.address?.suburb ||
                                data.address?.neighbourhood ||
                                data.address?.city_district ||
                                data.address?.city ||
                                data.display_name ||
                                "Nearby place name unavailable";

                        } catch (error) {
                            placeName.textContent =
                                "Place name unavailable. GPS coordinates are available above.";
                        }
                    }

                    cancelButton.style.display = "none";
                },

                        function(error) {
                            mapsLink = "";

                            status.textContent =
                                "Location unavailable. Please allow location permission.";

                            if (forSOS) {
                                shareButton.style.display = "block";
                            }
                        },

                        {
                            enableHighAccuracy: true,
                            timeout: 15000,
                            maximumAge: 0
                        }
                    );
                }

                locationButton.addEventListener("click", function() {
                    getLocation(false);
                });

                function resetSOS() {
                    clearTimeout(holdTimer);
                    clearInterval(countdownTimer);

                    activationStarted = false;
                    button.disabled = false;
                    cancelButton.style.display = "none";
                    shareButton.style.display = "none";

                    status.textContent =
                        "SOS cancelled. Press and hold for 3 seconds.";
                }

                function startCountdown() {
                    activationStarted = true;
                    button.disabled = true;
                    cancelButton.style.display = "block";

                    countdown = 5;

                    status.textContent =
                        "SOS activating in " + countdown +
                        " seconds. Cancel if accidental.";

                    countdownTimer = setInterval(function() {
                        countdown--;

                        if (countdown > 0) {
                            status.textContent =
                                "SOS activating in " + countdown +
                                " seconds. Cancel if accidental.";
                        } else {
                            clearInterval(countdownTimer);
                            cancelButton.style.display = "none";
                            getLocation(true);
                        }
                    }, 1000);
                }

                function startHold(event) {
                    if (activationStarted || button.disabled) {
                        return;
                    }

                    event.preventDefault();

                    try {
                        button.setPointerCapture(event.pointerId);
                    } catch (error) {
                        // Continue if pointer capture is unavailable.
                    }

                    status.textContent = "Keep holding SOS...";

                    holdTimer = setTimeout(function() {
                        startCountdown();
                    }, 3000);
                }

                function stopHold() {
                    if (!activationStarted) {
                        clearTimeout(holdTimer);
                        status.textContent =
                            "Press and hold SOS for 3 seconds.";
                    }
                }

                button.addEventListener("pointerdown", startHold);
                button.addEventListener("pointerup", stopHold);
                button.addEventListener("pointercancel", stopHold);

                cancelButton.addEventListener("click", function() {
                    resetSOS();
                });

                shareButton.addEventListener("click", function() {
                    let message =
                        "SOS! I need help. Please contact me immediately.";

                    if (mapsLink) {
                        message += "\\nMy current location: " + mapsLink;
                    } else {
                        message += "\\nMy location could not be retrieved.";
                    }

                    const whatsappURL =
                        "https://wa.me/?text=" + encodeURIComponent(message);

                    window.open(whatsappURL, "_blank");
                });
            </script>

        </div>
        """,
        height=330,
        scrolling=False
    )




    st.divider()
    # ======================================================
    # DASHBOARD
    # ======================================================

    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🌐 Languages", "6")

    with col2:
        st.metric("🩹 First Aid Topics", "7")

    with col3:
        st.metric("🤖 AI Model", "Gemini 2.5 Flash")

    st.divider()

    # ======================================================
    # FEATURES
    # ======================================================

    st.subheader("✨ Key Features")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown("### 💬 AI Assistant")
            st.write(
                "Ask first-aid questions and receive AI-powered guidance."
            )

            st.markdown("---")

            st.markdown("### 📷 Image Analysis")
            st.write(
                "Upload injury images for AI-based first-aid suggestions."
            )

            st.markdown("---")

            st.markdown("### 📄 PDF Reports")
            st.write(
                "Download professional first-aid reports."
            )

    with col2:

        with st.container(border=True):

            st.markdown("### 🌍 Multilingual")
            st.write(
                "Supports six languages for better accessibility."
            )

            st.markdown("---")

            st.markdown("### ❤️ CPR & Emergency")
            st.write(
                "Quick emergency guidance for common situations."
            )

            st.markdown("---")

            st.markdown("### 🩹 Common Injuries")
            st.write(
                "Burns, Bleeding, Fractures, Choking and Snake Bites."
            )

    st.divider()

    # ======================================================
    # HOW TO USE
    # ======================================================

    st.subheader("📖 How to Use")

    st.markdown(
        """
1. 🌐 Select your preferred language.

2. 💬 Open **AI Assistant**.

3. ✍️ Describe the injury or emergency.

4. 📷 Upload an injury image (Optional).

5. ➤ Click **Get First Aid**.

6. 📄 Download the PDF report if required.
"""
    )

    st.divider()

    # ======================================================
    # EMERGENCY CONTACTS
    # ======================================================

    st.subheader("📞 Emergency Contacts (India)")

    col1, col2 = st.columns(2)

    with col1:

        st.error(
            """
🚑 **Ambulance:** 108

🚓 **Police:** 112

🔥 **Fire Brigade:** 101
"""
        )

    with col2:

        st.warning(
            """
👩 **Women Helpline:** 181

👶 **Child Helpline:** 1098

🧠 **Mental Health:** 14416
"""
        )

    st.divider()

    

# ==========================================================
# AI ASSISTANT
# ==========================================================


elif option == t["chat"]:

    st.html("""
    <div style="
        border:1px solid #CBD5E1;
        border-radius:12px;
        padding:9px 13px;
        margin-bottom:10px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        gap:10px;
    ">
        <div>
            <div style="font-size:16px;font-weight:700;color:#1E293B;">
                💬 AI First Aid Assistant
            </div>
            <div style="font-size:11px;color:#64748B;">
                Ask questions or upload an injury image.
            </div>
        </div>

        <div style="
            font-size:12px;
            font-weight:600;
            color:#2563EB;
            white-space:nowrap;
        ">
            💬 Conversation
        </div>
    </div>
    """)

    # ======================================================
    # CHAT SESSION SETUP
    # ======================================================

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    if "chat_started_at" not in st.session_state:
        st.session_state.chat_started_at = None

    if "chat_upload_version" not in st.session_state:
        st.session_state.chat_upload_version = 0

    if "confirm_clear_chat" not in st.session_state:
        st.session_state.confirm_clear_chat = False

    # Maximum number of USER + AI exchanges kept in memory
    MAX_EXCHANGES = 20

    # ======================================================
    # AUTOMATIC 15-MINUTE EXPIRY
    # ======================================================

    if st.session_state.chat_started_at is not None:

        elapsed_time = (
            datetime.now() - st.session_state.chat_started_at
        ).total_seconds()

        if elapsed_time >= 900:

            st.session_state.chat_messages = []

            st.session_state.chat_started_at = None

            st.session_state.chat_upload_version += 1

            st.session_state.confirm_clear_chat = False

            st.info(
                "⏱️ Your previous chat expired after 15 minutes. "
                "A new conversation has been started."
            )

    
    # ======================================================
    # CHAT HEADER
    # ======================================================

    col1, col2 = st.columns([4, 1])

    with col1:
        st.caption("Your conversation")

    with col2:
        clear_chat = st.button(
            "🗑 Clear",
            use_container_width=True,
            disabled=not st.session_state.chat_messages
        )

    if clear_chat:
        st.session_state.confirm_clear_chat = True


    # ======================================================
    # CLEAR CHAT CONFIRMATION
    # ======================================================

    if st.session_state.confirm_clear_chat:

        st.warning(
            "⚠️ Are you sure you want to delete this conversation?"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "✅ Yes, Delete",
                use_container_width=True
            ):

                st.session_state.chat_messages = []

                st.session_state.chat_started_at = None

                st.session_state.chat_upload_version += 1

                st.session_state.confirm_clear_chat = False

                st.rerun()

        with col2:

            if st.button(
                "❌ Cancel",
                use_container_width=True
            ):

                st.session_state.confirm_clear_chat = False

                st.rerun()

    # ======================================================
    # SCROLLABLE CHAT WINDOW
    # ======================================================
    st.markdown(
    '<div id="ai-chat-anchor"></div>',
    unsafe_allow_html=True
    )
    st.html("""
    <style>
    div.st-key-chat_window {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 14px;
        padding: 12px;
    }
    </style>
    """)
    chat_box = st.container(
    height=300,
    border=False,
    key="chat_window"
    )

    with chat_box:

        if not st.session_state.chat_messages:

            st.markdown(
                """
                Hello! How can I help you today?    
                """
            )

        else:

            for message in st.session_state.chat_messages:

                if message["role"] == "user":

                    with st.chat_message("user"):

                        st.write(message["content"])

                        if message.get("image"):

                            st.image(
                                message["image"],
                                caption="Uploaded Injury Image",
                                width=160
                            )

                else:

                    with st.chat_message("assistant"):

                        st.markdown(message["content"])
    scroll_to_latest_chat()

    submission = st.chat_input(
        "Describe your injury or attach an image...",
        accept_file=True,
        file_type=["jpg", "jpeg", "png"],
        max_upload_size=10
    )

    if submission:

        question = submission["text"].strip()

        uploaded_files = submission["files"]

        image = None

        if uploaded_files:

            image = Image.open(uploaded_files[0])

        if not question and image is None:

            st.warning(
                "Please enter a question or upload an image."
            )

            st.stop()


        # ======================================================
        # PROCESS MESSAGE
        # ======================================================

        if question or image is not None:

            # --------------------------------------------------
            # START CHAT TIMER
            # --------------------------------------------------

            if st.session_state.chat_started_at is None:

                st.session_state.chat_started_at = datetime.now()

            # --------------------------------------------------
            # SAVE USER MESSAGE
            # --------------------------------------------------

            user_message = {
                "role": "user",
                "content": question
            }

            if image is not None:

                user_message["image"] = image

            st.session_state.chat_messages.append(
                user_message
            )

        # --------------------------------------------------
        # ROLLING CHAT WINDOW
        # --------------------------------------------------
        #
        # Each exchange contains:
        #
        # User question
        # AI answer
        #
        # Therefore:
        #
        # 20 exchanges = 40 messages
        #
        # When exchange 21 is completed,
        # the oldest exchange is removed.
        # --------------------------------------------------

        if len(st.session_state.chat_messages) > (
            MAX_EXCHANGES * 2
        ):

            st.session_state.chat_messages = (
                st.session_state.chat_messages[-(
                    MAX_EXCHANGES * 2
                ):]
            )

        # --------------------------------------------------
        # BUILD PREVIOUS CONVERSATION
        # --------------------------------------------------

        conversation_context = ""

        for message in st.session_state.chat_messages[:-1]:

            role = message["role"]

            content = message["content"]

            if role == "user":

                conversation_context += (
                    f"\nUser: {content}\n"
                )

            else:

                conversation_context += (
                    f"\nAssistant: {content}\n"
                )

        # --------------------------------------------------
        # INDIA SAFETY PROMPT
        # --------------------------------------------------

        prompt = f"""
You are an expert AI First Aid Assistant designed for users in India.

IMPORTANT LOCATION RULES:

- Assume the user is in India unless the user explicitly states another country.
- Never recommend emergency numbers from the USA or another country unless the user explicitly states that they are in that country.
- For users in India, use 112 for general emergencies.
- Ambulance: 108.
- Fire Brigade: 101.
- Women Helpline: 181.
- Child Helpline: 1098.
- Disaster Management: 1078.
- Never invent emergency numbers.

IMPORTANT MEDICAL SAFETY RULES:

- Give clear and practical first-aid guidance.
- Give step-by-step instructions when appropriate.
- Clearly mention what NOT to do.
- Mention when professional medical care is needed.
- Never diagnose diseases.
- Do not pretend to be a doctor.
- If the situation appears life-threatening, tell the user to seek emergency medical help immediately.
- Keep the response concise and easy to understand.

Reply ONLY in {t["reply_language"]}.

Previous Conversation:

{conversation_context}

Current User Question:

{question if question else "The user submitted an injury image without a written question."}
"""

        # ==================================================
        # GENERATE RESPONSE
        # ==================================================

        with st.spinner("🤖 Thinking..."):

            if image is not None:

                image_prompt = f"""
{prompt}

The user has also uploaded an image.

Analyze the image only for visible signs relevant to first aid.

Do not claim certainty from an image.

If an injury is visible, explain appropriate first-aid steps.

Never diagnose a medical condition.
"""

                answer = generate_ai_response(
                    [image_prompt, image]
                )

            else:

                answer = generate_ai_response(
                    prompt
                )

        # ==================================================
        # SAVE AI RESPONSE
        # ==================================================

        if answer:

            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            # --------------------------------------------------
            # ROLLING WINDOW AFTER AI RESPONSE
            # --------------------------------------------------

            if len(st.session_state.chat_messages) > (
                MAX_EXCHANGES * 2
            ):

                st.session_state.chat_messages = (
                    st.session_state.chat_messages[-(
                        MAX_EXCHANGES * 2
                    ):]
                )

            # --------------------------------------------------
            # CLEAR UPLOADED IMAGE AFTER SENDING
            # --------------------------------------------------

            st.session_state.chat_upload_version += 1

            # ==================================================
            # PDF REPORT
            # ==================================================

            pdf = create_pdf(
                "AI First Aid Report",
                answer
            )

            with open(pdf, "rb") as file:

                st.download_button(
                    "⬇ Download First Aid Report",
                    data=file,
                    file_name="First_Aid_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            st.rerun()

        else:

            # Remove user message if AI failed

            st.session_state.chat_messages.pop()

            st.error(
                "⚠️ Unable to generate a response. "
                "Please try again."
            )
# ==========================================================
# QUICK FIRST AID PAGES
# ==========================================================

elif option == t["burns"]:

    show_first_aid("Burns")


elif option == t["bleeding"]:

    show_first_aid("Bleeding")


elif option == t["fractures"]:

    show_first_aid("Fractures")


elif option == t["choking"]:

    show_first_aid("Choking")


elif option == t["snake"]:

    show_first_aid("Snake Bite")


elif option == t["cpr"]:

    show_first_aid("Cardiopulmonary Resuscitation (CPR)")

elif option == t["help"]:

    st.title("🚨 Emergency Contacts")

    st.caption(
        "Tap any button below to open your phone's dialer."
    )

    st.divider()

    emergency_numbers = [

        ("🚑 Ambulance", "108"),
        ("🚓 Police", "112"),
        ("🔥 Fire Brigade", "101"),
        ("👩 Women Helpline", "181"),
        ("👶 Child Helpline", "1098"),
        ("🧠 Mental Health", "14416"),
        ("🚨 Disaster Management", "1078"),

    ]

    
    # ==========================================================
    # EMERGENCY CONTACTS - TWO COLUMN LAYOUT
    # ==========================================================

    general_col, personal_col = st.columns([1, 1], gap="medium")

    # ----------------------------------------------------------
    # LEFT: GENERAL EMERGENCY CONTACTS
    # ----------------------------------------------------------

    with general_col:

        st.subheader("🚨 General Emergency")

        for name, number in emergency_numbers:

            with st.container(border=True):

                st.markdown(f"**{name}**")
                st.caption(f"Emergency Number: {number}")

                st.link_button(
                    "📞 Call",
                    f"tel:{number}",
                    use_container_width=True
                )

    # ----------------------------------------------------------
    # RIGHT: PERSONAL EMERGENCY CONTACTS
    # ----------------------------------------------------------

    with personal_col:

        CONTACTS_KEY = "ai_first_aid_personal_contacts"

        header_col, button_col = st.columns([3, 1])

        with header_col:
            st.subheader("👥 Personal Contacts")

        with button_col:
            add_clicked = st.button(
                "＋ Add",
                key="open_add_contact",
                use_container_width=True
            )

        # Load browser contacts
        stored_data = local_storage.getItem(CONTACTS_KEY)

        if stored_data:
            try:
                contacts = (
                    json.loads(stored_data)
                    if isinstance(stored_data, str)
                    else stored_data
                )

                if not isinstance(contacts, list):
                    contacts = []

            except (json.JSONDecodeError, TypeError):
                contacts = []
                st.error("Unable to read saved contacts.")
        else:
            contacts = []

        st.session_state.personal_contacts = contacts

        st.caption(
            f"{len(contacts)} / {MAX_PERSONAL_CONTACTS} saved"
        )

        if add_clicked:
            st.session_state.show_add_contact_form = True

        if "show_add_contact_form" not in st.session_state:
            st.session_state.show_add_contact_form = False

        # ADD CONTACT FORM
        if st.session_state.show_add_contact_form:

            with st.form("add_personal_contact"):

                contact_name = st.text_input(
                    "Name",
                    max_chars=60,
                    placeholder="Contact name"
                )

                contact_phone = st.text_input(
                    "Phone Number",
                    max_chars=15,
                    placeholder="Phone number"
                )

                save_col, cancel_col = st.columns(2)

                with save_col:
                    submitted = st.form_submit_button(
                        "Save",
                        use_container_width=True
                    )

                with cancel_col:
                    cancelled = st.form_submit_button(
                        "Cancel",
                        use_container_width=True
                    )

                if cancelled:
                    st.session_state.show_add_contact_form = False
                    st.rerun()

                if submitted:

                    clean_name = contact_name.strip()
                    clean_phone = contact_phone.strip()

                    if not clean_name:
                        st.error("Enter a contact name.")

                    elif not clean_phone.isdigit() or not (
                        10 <= len(clean_phone) <= 15
                    ):
                        st.error("Enter a valid phone number.")

                    elif len(contacts) >= MAX_PERSONAL_CONTACTS:
                        st.error("Maximum 15 contacts allowed.")

                    elif any(
                        c.get("phone") == clean_phone
                        for c in contacts
                    ):
                        st.error("This number already exists.")

                    else:
                        contacts.append({
                            "name": clean_name,
                            "phone": clean_phone
                        })

                        local_storage.setItem(
                            CONTACTS_KEY,
                            json.dumps(contacts, ensure_ascii=False)
                        )

                        st.session_state.show_add_contact_form = False

                        time.sleep(1.5)
                        st.success("Contact saved!")
                        st.rerun()

        # DISPLAY CONTACTS
        if contacts:

            for index, contact in enumerate(contacts):

                with st.container(border=True):

                    st.markdown(f"**👤 {contact['name']}**")
                    st.caption(f"📞 {contact['phone']}")
                    st.link_button(
                        "📞 Call",
                        f"tel:{contact['phone']}",
                        use_container_width=True
                    )

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_contact_{index}",
                        use_container_width=True
                    ):

                        contacts.pop(index)

                        local_storage.setItem(
                            CONTACTS_KEY,
                            json.dumps(contacts, ensure_ascii=False)
                        )

                        time.sleep(1.5)
                        st.rerun()

        else:
            st.info("No personal contacts saved yet.")



    # ==========================================================
    # GET LOCATION
    # ==========================================================

    st.divider()

    st.subheader("📍 Your Location")

    location = streamlit_geolocation()

    if isinstance(location, dict) and location.get("latitude") is not None:

        latitude = location["latitude"]
        longitude = location["longitude"]

        try:

            response = requests.get(
                "https://nominatim.openstreetmap.org/reverse",
                params={
                    "lat": latitude,
                    "lon": longitude,
                    "format": "json",
                    "addressdetails": 1
                },
                headers={
                    "User-Agent": "AI First Aid Assistant"
                },
                timeout=10
            )

            if response.status_code == 200:

                data = response.json()

                address = data.get(
                    "display_name",
                    "Address not found"
                )

                address_info = data.get("address", {})

                area = (
                    address_info.get("suburb")
                    or address_info.get("neighbourhood")
                    or address_info.get("city")
                    or address_info.get("town")
                    or address_info.get("village")
                    or "Not Available"
                )

                maps_url = (
                    f"https://www.google.com/maps?q="
                    f"{latitude},{longitude}"
                )

                with st.container(border=True):

                    st.success("✅ Location Retrieved")

                    st.markdown("#### 📍 Current Location")

                    st.write(f"**🏠 Address:** {address}")

                    st.write(f"**📌 Area:** {area}")

                    st.write(
                        f"**🌍 Coordinates:** "
                        f"{latitude:.6f}, {longitude:.6f}"
                    )

                    st.link_button(
                        "🗺 Open in Google Maps",
                        maps_url,
                        use_container_width=True
                    )

            else:

                st.error("Unable to fetch address.")

        except Exception as e:

            st.error(f"Error: {e}")

    else:

        st.info("📍 Click 'Get My Location' and allow location permission.")

elif option == t["wellbeing"]:

    st.title("💙 Wellbeing")

    st.caption(
        "Taking care of yourself also means taking care of "
        "your emotional wellbeing."
    )

    st.info(
        "🌿 Feeling stressed, overwhelmed, anxious, or simply "
        "having a difficult day is something many people experience."
    )

    st.markdown("### 🫂 You can try")

    st.write("• Take a few slow, deep breaths.")
    st.write("• Talk to someone you trust.")
    st.write("• Take a short break and get some fresh air.")
    st.write("• Try to get enough sleep and stay hydrated.")

    st.markdown("### 💙 Remember")

    st.write(
        "Asking for support is a sign of taking care of yourself, "
        "not a sign of weakness."
    )

    st.caption(
        "If you feel that you may be in immediate danger, "
        "use the Help section for emergency contacts."
    )


# ==========================================================
# UNKNOWN PAGE (Safety)
# ==========================================================

else:

    st.warning("⚠️ Page not found.")


# ==========================================================
# FOOTER
# ==========================================================

st.html("""
<div style="
    margin-top:12px;
    padding:10px 12px;
    background:#F8FAFC;
    border:1px solid #E2E8F0;
    border-radius:10px;
">

    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        flex-wrap:wrap;
        gap:5px;
        font-size:11px;
        color:#64748B;
    ">
        <span>
            🩹 <b>AI First Aid Assistant</b> · v3.0
        </span>

        <span>
            👨‍💻 Gaurav Yadav · SYCS
        </span>
    </div>

    <div style="
        text-align:center;
        font-size:10px;
        color:#64748B;
        margin-top:5px;
    ">
        🤖 Powered by Google Gemini 2.5 Flash
    </div>

    <div style="
        margin-top:8px;
        padding-top:7px;
        border-top:1px solid #E2E8F0;
        font-size:10px;
        color:#64748B;
        line-height:1.5;
        text-align:center;
    ">
        ⚠️ For educational purposes only. Not a substitute for professional
        medical advice, diagnosis or treatment. Contact emergency services
        immediately in life-threatening situations.
    </div>

    <div style="
        text-align:center;
        font-size:9px;
        color:#94A3B8;
        margin-top:5px;
    ">
        © 2026 AI First Aid Assistant
    </div>

</div>
""")
