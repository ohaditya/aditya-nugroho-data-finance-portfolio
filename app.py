import base64
import html as htmlmod
import json
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageOps

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Aditya Nugroho | Data & Finance Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PATH
# =========================================================

BASE_DIR = Path(__file__).parent

ASSETS_DIR = BASE_DIR / "assets"
PROJECTS_DIR = BASE_DIR / "projects"
CERTIFICATES_DIR = BASE_DIR / "certificates"


# =========================================================
# COLOR THEME
# =========================================================

PRIMARY = "#0F172A"
SECONDARY = "#0F766E"
ACCENT = "#14B8A6"
LIGHT_BG = "#F8FAFC"
CARD_BG = "#FFFFFF"
TEXT = "#1E293B"
MUTED = "#64748B"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background-color: #0B1120;
        color: #E2E8F0;
    }

    /*
       FIX:
       Memberikan ruang di bagian atas agar konten
       tidak tertutup oleh header / toolbar Streamlit.
    */

    .stAppViewContainer .main .block-container {
        max-width: 1180px;
        padding-top: 5.5rem !important;
        padding-bottom: 4rem !important;
    }


    /* =====================================================
       STREAMLIT HEADER
       ===================================================== */

    header[data-testid="stHeader"] {
        background-color: #0B1120;
        z-index: 999;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background-color: #070D1A;
        border-right: 1px solid #1E293B;
    }

    section[data-testid="stSidebar"] * {
        color: #E2E8F0;
    }


    /* =====================================================
       TEXT
       ===================================================== */

    h1,
    h2,
    h3,
    h4 {
        color: #F8FAFC !important;
    }

    p {
        color: #CBD5E1;
    }


    /* =====================================================
       HERO
       ===================================================== */

    .hero-box {
        background:
            linear-gradient(
                135deg,
                #111827 0%,
                #0F3D3E 100%
            );

        padding: 45px;
        border-radius: 25px;

        border: 1px solid #1E4545;

        box-shadow:
            0 20px 50px rgba(0, 0, 0, 0.35);

        margin-bottom: 30px;
    }


    /* =====================================================
       LABEL
       ===================================================== */

    .small-label {
        color: #2DD4BF;

        font-size: 13px;
        font-weight: 700;

        letter-spacing: 2px;
        text-transform: uppercase;

        margin-bottom: 10px;

        display: block;
    }


    /* =====================================================
       CARD
       ===================================================== */

    .card {
        background-color: #111827;

        border: 1px solid #1E293B;

        border-radius: 18px;

        padding: 22px;

        margin-bottom: 18px;

        box-shadow:
            0 10px 25px rgba(0, 0, 0, 0.20);
    }


    /* =====================================================
       SKILL
       ===================================================== */

    .skill {
        display: inline-block;

        background-color: #123B3B;

        color: #5EEAD4;

        padding: 8px 13px;

        margin: 4px;

        border-radius: 999px;

        border: 1px solid #1F5F5C;

        font-size: 13px;

        font-weight: 600;
    }


    /* =====================================================
       PROJECT IMAGE BOX
       ===================================================== */

    .project-image-box {
        width: 100%;

        height: 230px;

        min-height: 230px;

        background: #111827;

        border: 1px solid #263449;

        border-radius: 16px;

        display: flex;

        align-items: center;

        justify-content: center;

        overflow: hidden;

        margin-bottom: 8px;
    }


    /* =====================================================
       FEATURED PROJECT DESCRIPTION
       ===================================================== */

    .featured-description {
        color: #CBD5E1;

        font-size: 14px;

        line-height: 1.7;

        min-height: 75px;

        margin-bottom: 10px;
    }


    /* =====================================================
       PROJECT META
       ===================================================== */

    .project-meta {
        color: #64748B;

        font-size: 13px;

        margin-bottom: 8px;
    }


    /* =====================================================
       BUTTON
       ===================================================== */

    .stButton > button {
        border-radius: 10px !important;

        font-weight: 600 !important;

        border: 1px solid #334155 !important;
    }

    .stLinkButton > a {
        border-radius: 10px !important;

        font-weight: 600 !important;
    }


    /* =====================================================
       METRIC
       ===================================================== */

    [data-testid="stMetric"] {
        background: #111827;

        border: 1px solid #1E293B;

        padding: 15px;

        border-radius: 14px;
    }

    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #F8FAFC !important;
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {
        border-color: #1E293B !important;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {
        text-align: center;

        color: #64748B;

        padding-top: 30px;

        margin-top: 50px;

        border-top: 1px solid #1E293B;
    }


    /* =====================================================
       ONE-PAGE NAVIGATION
       ===================================================== */
    html {
        scroll-behavior: smooth;
        scroll-padding-top: 90px;
    }
    .section-anchor {
        scroll-margin-top: 90px;
        height: 1px;
    }
    section[data-testid="stSidebar"] {
        position: sticky;
        top: 0;
        height: 100vh;
    }
    .sidebar-menu-title {
        color: #2DD4BF;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .sidebar-nav {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .sidebar-nav a {
        display: block;
        padding: 10px 12px;
        border-radius: 10px;
        color: #CBD5E1 !important;
        text-decoration: none !important;
        border: 1px solid transparent;
        transition: all .18s ease;
        font-weight: 600;
    }
    .sidebar-nav a:hover,
    .sidebar-nav a:focus {
        color: #5EEAD4 !important;
        background: #102A2A;
        border-color: #1F5F5C;
        outline: none;
    }
    @media (max-width: 768px) {
        .stAppViewContainer .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 4.5rem !important;
        }
        section[data-testid="stSidebar"] {
            height: auto;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PROFILE
# =========================================================

PROFILE = {
    "name": "Aditya Nugroho",

    "headline":
        "Data Analyst | Financial Analysis | Machine Learning",

    "location":
        "Depok, Indonesia",

    "birth":
        "17 November 2000",

    "about":
        """
        Informatics Engineering graduate with a GPA of 3.62 and
        professional experience in Finance, Data Analysis, and
        Financial Market Analysis.

        Experienced in Python, SQL, Pandas, Data Cleaning,
        Exploratory Data Analysis (EDA), Data Visualization,
        Machine Learning, and Risk Analysis to process data and
        generate insights that support decision-making.

        Experienced in analyzing 71 financial instruments and
        handling high-volume financial transactions exceeding
        IDR 15 billion per day, with transaction monitoring
        exceeding IDR 25 billion per day.
        """,

    "education":
        "Bachelor of Informatics Engineering",

    "university":
        "Universitas Pamulang",

    "education_period":
        "2020 – 2024",

    "gpa":
        "3.62",

    "thesis":
        """
        Implementation of Linear Regression and Support Vector Machine
        Methods for XAUUSD Closing Price Prediction
        on the MetaTrader 4 Platform
        """,

    "whatsapp":
        "6282298373159",

    "email":
        "adityakantata@gmail.com",

    "linkedin":
        "https://www.linkedin.com/in/adityaforex",

    "github":
        "https://github.com/ohaditya"
}


# =========================================================
# TECHNICAL SKILLS
# =========================================================

SKILLS = [
    "Python",
    "Pandas",
    "SQL",
    "Data Cleaning",
    "EDA",
    "Data Visualization",
    "Machine Learning",
    "Linear Regression",
    "Logistic Regression",
    "Support Vector Machine",
    "Feature Engineering",
    "Model Evaluation",
    "Financial Analysis",
    "Risk Analysis",
    "Cash Reconciliation",
    "Financial Transaction Monitoring",
    "Microsoft Excel",
    "Power BI",
    "RapidMiner",
    "TradingView",
    "MetaTrader 4 & 5"
]


# =========================================================
# PERSONAL SKILLS
# =========================================================

PERSONAL_SKILLS = [
    "Analytical Thinking",
    "Attention to Detail",
    "Problem Solving",
    "Accuracy & Accountability",
    "Teamwork & Collaboration"
]


# =========================================================
# EXPERIENCE
# =========================================================

EXPERIENCE = [

    {
        "role":
            "Foreign Exchange Specialist",

        "company":
            "PT. Yukinvest Finansial Partner",

        "location":
            "Jakarta",

        "period":
            "January 2025 – January 2026",

        "description":
            [
                "Analyzed 71 financial instruments covering Forex, precious metals, global index futures, crude oil, and US stocks to support trading decisions and client risk management.",

                "Prepared market reports and delivered market insights to clients on a regular basis.",

                "Provided education and seminars covering trading strategies, risk management, and financial products to 80 clients."
            ]
    },

    {
        "role":
            "Technical Analyst",

        "company":
            "PT. IDS Kapital Berjangka",

        "location":
            "Jakarta",

        "period":
            "January 2020 – February 2021",

        "description":
            [
                "Monitored and analyzed 50 foreign currency instruments using technical analysis to support risk assessment and decision-making.",

                "Prepared market analysis reports and recommendations regarding price movements.",

                "Conducted Forex education and seminars for 20 clients."
            ]
    },

    {
        "role":
            "ATM Cassette Restocking",

        "company":
            "PT. Swadharma Sarana Informatika",

        "location":
            "Jakarta",

        "period":
            "February 2019 – November 2019",

        "description":
            [
                "Restocked cash for more than 40 ATMs every day according to company operational standards.",

                "Performed cash sorting, counting, and transaction data entry involving cash exceeding IDR 15 billion per day.",

                "Recorded and monitored cash inflows and outflows at the vault with total transaction values exceeding IDR 25 billion per day.",

                "Performed reconciliation between physical cash and system records to ensure transaction accuracy."
            ]
    }

]


# =========================================================
# IMAGE / GALLERY HELPERS
# =========================================================

def natural_key(value):
    """
    Natural sorting.

    image1
    image2
    image3
    image10

    instead of:

    image1
    image10
    image2
    image3
    """

    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(
            r"(\d+)",
            str(value)
        )
    ]


def sorted_images(paths):
    """
    Sort images using natural numeric order.
    """

    return sorted(
        paths,
        key=lambda path: natural_key(path.name)
    )


def render_zoomable_image(image, label="", height=500):
    """Display an image as a thumbnail; click opens a popup viewer with zoom/pan."""
    try:
        if isinstance(image, (str, Path)):
            pil_image = Image.open(image).convert("RGB")
        else:
            pil_image = image.convert("RGB")

        from io import BytesIO
        buffer = BytesIO()
        pil_image.save(buffer, format="JPEG", quality=92)
        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
        safe_label = htmlmod.escape(str(label))
        frame_height = max(220, int(height))
        uid = "imgviewer_" + re.sub(r"[^a-zA-Z0-9_]", "_", str(id(pil_image)))

        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<style>
* {{ box-sizing:border-box; }}
html,body {{ margin:0; padding:0; width:100%; height:100%; overflow:hidden; background:transparent; font-family:Arial,sans-serif; }}
.thumb {{ position:relative; width:100%; height:{frame_height}px; border:1px solid #263449; border-radius:16px; background:#111827; overflow:hidden; cursor:zoom-in; }}
.thumb img {{ width:100%; height:100%; object-fit:contain; display:block; user-select:none; -webkit-user-drag:none; }}
.thumb .open {{ position:absolute; right:12px; bottom:12px; padding:8px 12px; border-radius:9px; background:rgba(15,23,42,.9); color:#f8fafc; border:1px solid #475569; font-size:12px; font-weight:700; }}
.modal {{ display:none; position:absolute; inset:0; z-index:20; background:rgba(2,6,23,.96); }}
.modal.open {{ display:block; }}
.viewer {{ position:absolute; inset:42px 12px 42px; overflow:hidden; touch-action:none; display:flex; align-items:center; justify-content:center; }}
.viewer img {{ max-width:100%; max-height:100%; object-fit:contain; transform-origin:center; will-change:transform; user-select:none; -webkit-user-drag:none; cursor:zoom-in; }}
.top {{ position:absolute; top:8px; left:10px; right:10px; z-index:30; display:flex; align-items:center; justify-content:space-between; color:#e2e8f0; }}
.title {{ font-size:12px; font-weight:700; max-width:75%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.close {{ width:38px; height:38px; border:1px solid #475569; border-radius:10px; background:#0f172a; color:white; font-size:20px; cursor:pointer; }}
.controls {{ position:absolute; left:50%; bottom:7px; transform:translateX(-50%); z-index:30; display:flex; gap:6px; }}
.controls button {{ min-width:40px; height:38px; border:1px solid #475569; border-radius:9px; background:#0f172a; color:#fff; font-size:17px; font-weight:700; cursor:pointer; }}
.hint {{ position:absolute; left:12px; bottom:12px; color:#94a3b8; font-size:10px; z-index:30; }}
</style>
</head>
<body>
<div class="thumb" id="{uid}_thumb" role="button" tabindex="0" aria-label="Open {safe_label}">
  <img src="data:image/jpeg;base64,{encoded}" alt="{safe_label}">
  <span class="open">🔍 Click to view</span>
</div>
<div class="modal" id="{uid}_modal" aria-label="Image viewer">
  <div class="top"><div class="title">{safe_label}</div><button class="close" id="{uid}_close" type="button">×</button></div>
  <div class="viewer" id="{uid}_viewer"><img id="{uid}_image" src="data:image/jpeg;base64,{encoded}" alt="{safe_label}"></div>
  <div class="hint">🖱️ Wheel / double-click · 🤏 Pinch · Drag when zoomed</div>
  <div class="controls">
    <button id="{uid}_minus" type="button">−</button>
    <button id="{uid}_reset" type="button">⟳</button>
    <button id="{uid}_plus" type="button">+</button>
  </div>
</div>
<script>
(function() {{
 const thumb=document.getElementById('{uid}_thumb'), modal=document.getElementById('{uid}_modal'), close=document.getElementById('{uid}_close');
 const viewer=document.getElementById('{uid}_viewer'), img=document.getElementById('{uid}_image');
 const minus=document.getElementById('{uid}_minus'), plus=document.getElementById('{uid}_plus'), reset=document.getElementById('{uid}_reset');
 let scale=1,tx=0,ty=0,drag=false,sx=0,sy=0,stx=0,sty=0,pinchStart=0,pinchScale=1;
 const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
 function apply() {{ img.style.transform=`translate3d(${{tx}}px,${{ty}}px,0) scale(${{scale}})`; img.style.cursor=scale>1?'grab':'zoom-in'; }}
 function setScale(next,cx,cy) {{ const old=scale; scale=clamp(next,1,5); if(scale===1) {{tx=0;ty=0;}} else if(cx!==undefined) {{const r=scale/old;tx=cx-r*(cx-tx);ty=cy-r*(cy-ty);}} apply(); }}
 function open() {{ modal.classList.add('open'); resetZoom(); }}
 function resetZoom() {{ scale=1;tx=0;ty=0;apply(); }}
 thumb.addEventListener('click',open); thumb.addEventListener('keydown',e=>{{if(e.key==='Enter'||e.key===' '){{e.preventDefault();open();}}}});
 close.addEventListener('click',()=>modal.classList.remove('open')); modal.addEventListener('click',e=>{{if(e.target===modal)modal.classList.remove('open');}});
 plus.addEventListener('click',()=>setScale(scale+.25)); minus.addEventListener('click',()=>setScale(scale-.25)); reset.addEventListener('click',resetZoom);
 viewer.addEventListener('wheel',e=>{{e.preventDefault();const r=viewer.getBoundingClientRect();setScale(scale*(e.deltaY<0?1.18:.85),e.clientX-r.left-r.width/2,e.clientY-r.top-r.height/2);}},{{passive:false}});
 viewer.addEventListener('dblclick',e=>{{const r=viewer.getBoundingClientRect();setScale(scale>1?1:2,e.clientX-r.left-r.width/2,e.clientY-r.top-r.height/2);}});
 viewer.addEventListener('pointerdown',e=>{{if(e.pointerType==='mouse'&&scale<=1)return;drag=true;sx=e.clientX;sy=e.clientY;stx=tx;sty=ty;if(e.pointerType==='mouse')viewer.setPointerCapture(e.pointerId);}});
 viewer.addEventListener('pointermove',e=>{{if(!drag||scale<=1)return;tx=stx+e.clientX-sx;ty=sty+e.clientY-sy;apply();}});
 viewer.addEventListener('pointerup',()=>drag=false); viewer.addEventListener('pointercancel',()=>drag=false);
 function dist(a,b){{return Math.hypot(a.clientX-b.clientX,a.clientY-b.clientY);}}
 viewer.addEventListener('touchstart',e=>{{if(e.touches.length===2){{e.preventDefault();pinchStart=dist(e.touches[0],e.touches[1]);pinchScale=scale;}}}},{{passive:false}});
 viewer.addEventListener('touchmove',e=>{{if(e.touches.length===2){{e.preventDefault();setScale(pinchScale*dist(e.touches[0],e.touches[1])/Math.max(pinchStart,1));}}}},{{passive:false}});
 viewer.addEventListener('touchend',()=>pinchStart=0);
 apply();
}})();
</script>
</body>
</html>
"""
        components.html(html, height=frame_height + 8, scrolling=False)
    except Exception as error:
        st.error(f"Unable to display image viewer: {error}")


def render_image_box(image_path, label="", height=500):
    """Display a thumbnail that opens the image in the zoomable popup."""
    try:
        image = Image.open(image_path).convert("RGB")
        BOX_W, BOX_H = 1200, 675
        fitted = ImageOps.contain(image, (BOX_W - 40, BOX_H - 40), method=Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (BOX_W, BOX_H), (17, 24, 39))
        x = (BOX_W - fitted.width) // 2
        y = (BOX_H - fitted.height) // 2
        canvas.paste(fitted, (x, y))
        render_zoomable_image(canvas, label=label, height=height)
    except Exception as error:
        st.error(f"Unable to display image: {error}")


# =========================================================
# GALLERY CALLBACKS
# =========================================================


# =========================================================

def open_gallery_callback(state_prefix):

    st.session_state[
        f"{state_prefix}_is_open"
    ] = True

    st.session_state[
        f"{state_prefix}_index"
    ] = 0


def close_gallery_callback(state_prefix):

    st.session_state[
        f"{state_prefix}_is_open"
    ] = False

    st.session_state[
        f"{state_prefix}_index"
    ] = 0


def previous_gallery_callback(state_prefix):

    current = st.session_state.get(
        f"{state_prefix}_index",
        0
    )

    st.session_state[
        f"{state_prefix}_index"
    ] = max(
        0,
        current - 1
    )


def next_gallery_callback(
    state_prefix,
    total_images
):

    current = st.session_state.get(
        f"{state_prefix}_index",
        0
    )

    st.session_state[
        f"{state_prefix}_index"
    ] = min(
        total_images - 1,
        current + 1
    )


# =========================================================
# SHOW PROJECT GALLERY
# =========================================================

def show_project_gallery(title, images, state_prefix="gallery"):
    """Inline gallery: swipe/drag directly on the image, plus zoom and arrows."""
    if not images:
        return
    try:
        from io import BytesIO
        slides=[]
        for image_path in images:
            im=Image.open(image_path).convert("RGB")
            buf=BytesIO(); im.save(buf,format="JPEG",quality=92)
            slides.append({"src":"data:image/jpeg;base64,"+base64.b64encode(buf.getvalue()).decode("ascii"),"name":image_path.stem})
        payload=json.dumps(slides).replace("</","<\\/")
        uid="gallery_"+re.sub(r"[^a-zA-Z0-9_]","_",state_prefix)
        gallery_html=f"""
<div id="{uid}" class="g-wrap">
<style>
#{uid} *{{box-sizing:border-box}} #{uid} .g-frame{{position:relative;height:520px;background:#111827;border:1px solid #263449;border-radius:16px;overflow:hidden;touch-action:pan-y}}
#{uid} .g-stage{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;overflow:hidden;touch-action:none}}
#{uid} img{{max-width:100%;max-height:100%;object-fit:contain;user-select:none;-webkit-user-drag:none;will-change:transform;cursor:grab}}
#{uid} .arrow{{position:absolute;top:50%;transform:translateY(-50%);z-index:4;width:44px;height:54px;border:1px solid #475569;border-radius:12px;background:rgba(15,23,42,.9);color:#fff;font-size:28px;cursor:pointer}}
#{uid} .prev{{left:10px}} #{uid} .next{{right:10px}} #{uid} .bar{{position:absolute;left:10px;right:10px;bottom:10px;z-index:4;display:flex;align-items:center;justify-content:center;gap:7px;color:#cbd5e1;font-size:12px}}
#{uid} .bar span{{background:rgba(15,23,42,.9);padding:7px 10px;border-radius:9px;border:1px solid #334155}}
#{uid} .bar button{{height:34px;min-width:38px;border:1px solid #475569;border-radius:8px;background:#0f172a;color:#fff;font-weight:700;cursor:pointer}}
@media(max-width:768px){{#{uid} .g-frame{{height:430px}}}}
</style>
<div class="g-frame" aria-label="{htmlmod.escape(str(title))} gallery">
 <button class="arrow prev" id="{uid}_prev" type="button">‹</button>
 <div class="g-stage" id="{uid}_stage"><img id="{uid}_img" alt="Gallery image"></div>
 <button class="arrow next" id="{uid}_next" type="button">›</button>
 <div class="bar"><button id="{uid}_minus" type="button">−</button><button id="{uid}_reset" type="button">⟳</button><button id="{uid}_plus" type="button">+</button><span id="{uid}_count"></span></div>
</div>
<script>
(function(){{
 const root=document.getElementById('{uid}'),stage=document.getElementById('{uid}_stage'),img=document.getElementById('{uid}_img'),count=document.getElementById('{uid}_count');
 const prev=document.getElementById('{uid}_prev'),next=document.getElementById('{uid}_next'),minus=document.getElementById('{uid}_minus'),plus=document.getElementById('{uid}_plus'),reset=document.getElementById('{uid}_reset');
 const slides={payload}; let i=0,scale=1,tx=0,ty=0,drag=false,sx=0,sy=0,stx=0,sty=0,touchX=0,pinchStart=0,pinchScale=1;
 const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
 function apply(){{img.style.transform=`translate3d(${{tx}}px,${{ty}}px,0) scale(${{scale}})`;img.style.cursor=scale>1?'grab':'grab';count.textContent=`${{i+1}} / ${{slides.length}} · ${{slides[i].name}}`;}}
 function resetZoom(){{scale=1;tx=0;ty=0;apply();}}
 function show(n){{i=(n+slides.length)%slides.length;img.src=slides[i].src;img.alt=slides[i].name;resetZoom();}}
 prev.addEventListener('click',()=>show(i-1)); next.addEventListener('click',()=>show(i+1));
 plus.addEventListener('click',()=>{{scale=clamp(scale+.25,1,5);apply();}});minus.addEventListener('click',()=>{{scale=clamp(scale-.25,1,5);if(scale===1){{tx=0;ty=0}}apply();}});reset.addEventListener('click',resetZoom);
 stage.addEventListener('wheel',e=>{{e.preventDefault();scale=clamp(scale*(e.deltaY<0?1.18:.85),1,5);if(scale===1){{tx=0;ty=0}}apply();}},{{passive:false}});
 stage.addEventListener('dblclick',()=>{{scale=scale>1?1:2;if(scale===1){{tx=0;ty=0}}apply();}});
 stage.addEventListener('pointerdown',e=>{{drag=true;sx=e.clientX;sy=e.clientY;stx=tx;sty=ty;touchX=e.clientX;if(e.pointerType==='mouse')stage.setPointerCapture(e.pointerId);}});
 stage.addEventListener('pointermove',e=>{{if(!drag)return;if(scale>1){{tx=stx+e.clientX-sx;ty=sty+e.clientY-sy;apply();}}}});
 stage.addEventListener('pointerup',e=>{{const dx=e.clientX-touchX;drag=false;if(scale===1&&Math.abs(dx)>55)show(i+(dx<0?1:-1));}}); stage.addEventListener('pointercancel',()=>drag=false);
 function dist(a,b){{return Math.hypot(a.clientX-b.clientX,a.clientY-b.clientY);}}
 stage.addEventListener('touchstart',e=>{{if(e.touches.length===1)touchX=e.touches[0].clientX;if(e.touches.length===2){{e.preventDefault();pinchStart=dist(e.touches[0],e.touches[1]);pinchScale=scale;}}}},{{passive:false}});
 stage.addEventListener('touchmove',e=>{{if(e.touches.length===2){{e.preventDefault();scale=clamp(pinchScale*dist(e.touches[0],e.touches[1])/Math.max(pinchStart,1),1,5);apply();}}}},{{passive:false}});
 stage.addEventListener('touchend',e=>{{if(e.changedTouches.length===1&&scale===1){{const dx=e.changedTouches[0].clientX-touchX;if(Math.abs(dx)>55)show(i+(dx<0?1:-1));}}pinchStart=0;}});
 show(0);
}})();
</script>
</div>
"""
        components.html(gallery_html,height=540,scrolling=False)
    except Exception as error:
        st.error(f"Unable to display gallery: {error}")


# =========================================================
# LOAD PROJECTS
# =========================================================


def load_projects():

    projects = []

    if not PROJECTS_DIR.exists():
        return projects


    folders = sorted(
        PROJECTS_DIR.iterdir(),
        key=lambda folder:
            natural_key(folder.name)
    )


    for folder in folders:

        if not folder.is_dir():
            continue


        project_file = (
            folder / "project.json"
        )


        if not project_file.exists():
            continue


        try:

            data = json.loads(
                project_file.read_text(
                    encoding="utf-8"
                )
            )

            data["_folder"] = folder

            projects.append(data)


        except json.JSONDecodeError as error:

            st.warning(
                f"Project JSON error: "
                f"{project_file.name} — {error}"
            )


        except Exception:

            continue


    return projects


# =========================================================
# LOAD PROJECT IMAGES
# =========================================================

def load_project_images(folder):

    image_folder = (
        folder / "images"
    )


    if not image_folder.exists():
        return []


    extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    }


    images = [

        image

        for image in image_folder.iterdir()

        if (
            image.is_file()
            and image.suffix.lower()
            in extensions
        )
    ]


    return sorted_images(images)


# =========================================================
# LOAD CERTIFICATES
# =========================================================

def load_certificates():

    if not CERTIFICATES_DIR.exists():
        return []


    extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    }


    certificates = [

        certificate

        for certificate in CERTIFICATES_DIR.iterdir()

        if (
            certificate.is_file()
            and certificate.suffix.lower()
            in extensions
        )
    ]


    return sorted(
        certificates,
        key=lambda certificate:
            natural_key(
                certificate.name
            )
    )


# =========================================================
# FEATURED PROJECT DESCRIPTION
# =========================================================

def get_featured_description(project):

    title = str(
        project.get(
            "title",
            ""
        )
    ).lower()


    # -----------------------------------------------------
    # FINANCE PERFORMANCE
    # -----------------------------------------------------

    if "finance performance branch" in title:

        return (
            "Power BI analysis of branch "
            "financial performance and "
            "disbursement trends."
        )


    # -----------------------------------------------------
    # TREASURY
    # -----------------------------------------------------

    if (
        "treasury" in title
        or "wealth management" in title
    ):

        return (
            "Python and Streamlit application "
            "for transaction monitoring and "
            "portfolio analysis."
        )


    # -----------------------------------------------------
    # XAUUSD
    # -----------------------------------------------------

    if "xauusd" in title:

        return (
            "Machine learning analysis for "
            "XAUUSD closing price prediction "
            "using Linear Regression and SVM."
        )


    # -----------------------------------------------------
    # FALLBACK
    # -----------------------------------------------------

    description = str(
        project.get(
            "description",
            ""
        )
    )


    description = description.split(
        "\n\n"
    )[0].strip()


    # Remove common markdown formatting
    description = re.sub(
        r"[*_`#]",
        "",
        description
    )


    # Limit length
    if len(description) > 150:

        description = (
            description[:147].rstrip()
            + "..."
        )


    return description


# =========================================================
# PDF DOCUMENT HELPERS
# =========================================================

def render_pdf_preview(pdf_path, height=800):
    """
    Render a local PDF as images inside Streamlit.

    This avoids embedding the PDF with a data: URL in an iframe.
    Chrome can block that approach with:
    "This page has been blocked by Chrome."

    PyMuPDF renders each PDF page directly, so the preview does not depend
    on the browser's built-in PDF viewer.
    """

    if fitz is None:
        st.error(
            "PDF preview requires PyMuPDF. "
            "Add `PyMuPDF` to requirements.txt and redeploy the app."
        )
        return

    try:
        pdf_document = fitz.open(str(pdf_path))

        if pdf_document.page_count == 0:
            st.warning("This PDF is empty.")
            pdf_document.close()
            return

        preview_width = 1180
        max_preview_height = max(int(height), 500)

        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)

            rect = page.rect
            scale = min(
                preview_width / max(rect.width, 1),
                max_preview_height / max(rect.height, 1),
                1.75
            )

            pixmap = page.get_pixmap(
                matrix=fitz.Matrix(scale, scale),
                alpha=False
            )

            page_image = Image.frombytes(
                "RGB",
                [pixmap.width, pixmap.height],
                pixmap.samples
            )

            page_image = ImageOps.expand(
                page_image,
                border=1,
                fill=(30, 41, 59)
            )

            render_zoomable_image(
                page_image,
                label=f"Page {page_number + 1} of {pdf_document.page_count}",
                height=min(max_preview_height, 900)
            )

        pdf_document.close()

    except Exception as error:
        st.error(
            f"Unable to preview PDF: {error}"
        )


def document_card(document, preview_height=800):
    """
    Display document information, inline PDF preview,
    and download button.
    """

    path = document["path"]

    st.divider()

    st.header(
        f"{document['icon']} {document['title']}"
    )

    st.caption(
        document["description"]
    )

    if not path.exists():

        st.warning(
            f"File not found. Add it to: "
            f"assets/{path.name}"
        )

        return

    st.markdown(
        "#### PDF Preview"
    )

    render_pdf_preview(
        path,
        height=preview_height
    )

    st.download_button(
        f"⬇️ Download {document['title']}",
        data=path.read_bytes(),
        file_name=document["file_name"],
        mime="application/pdf",
        use_container_width=True,
        key=f"download_{path.stem}"
    )


# =========================================================
# SIDEBAR
# =========================================================


st.sidebar.markdown(
    "## Aditya Nugroho"
)

st.sidebar.caption(
    "Data & Finance Portfolio"
)

st.sidebar.divider()


st.sidebar.markdown(
    '<div class="sidebar-menu-title">MENU</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <nav class="sidebar-nav" aria-label="Portfolio navigation">
        <a href="#home">🏠 Home</a>
        <a href="#projects">📁 Projects</a>
        <a href="#experience">💼 Experience</a>
        <a href="#certificates">🏆 Certificates</a>
        <a href="#documents">📄 Documents</a>
        <a href="#education">🎓 Education</a>
        <a href="#contact">📬 Contact</a>
    </nav>
    """,
    unsafe_allow_html=True
)


st.markdown('<div id="home" class="section-anchor"></div>', unsafe_allow_html=True)
# HOME
# =========================================================


# =====================================================
# PROFILE
# =====================================================

profile_image = (
    ASSETS_DIR / "profile.jpg"
)


col1, col2 = st.columns(
    [1, 3.5],
    vertical_alignment="center"
)


with col1:

    if profile_image.exists():

        st.image(
            profile_image,
            width=210,
            output_format="JPEG"
        )

    else:

        st.markdown(
            "## 👤"
        )

        st.caption(
            "Add your photo:"
        )

        st.code(
            "assets/profile.jpg"
        )


with col2:

    st.markdown(
        """
        <div class="small-label">
            DATA • FINANCE • MACHINE LEARNING
        </div>
        """,
        unsafe_allow_html=True
    )


    st.title(
        PROFILE["name"]
    )


    st.subheader(
        PROFILE["headline"]
    )


    st.write(
        PROFILE["about"]
    )


# =====================================================
# QUICK INFO
# =====================================================

st.divider()


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Financial Instruments",
        "71"
    )


with col2:

    st.metric(
        "ATM Daily",
        "40+"
    )


with col3:

    st.metric(
        "Daily Transaction",
        "> IDR 25B"
    )


with col4:

    st.metric(
        "GPA",
        "3.62"
    )


# =====================================================
# ABOUT
# =====================================================

st.divider()


st.header(
    "About Me"
)


st.write(
    PROFILE["about"]
)


# =====================================================
# TECHNICAL SKILLS
# =====================================================

st.header(
    "Technical Skills"
)


skill_html = ""


for skill in SKILLS:

    skill_html += (
        f'<span class="skill">'
        f'{skill}'
        f'</span>'
    )


st.markdown(
    skill_html,
    unsafe_allow_html=True
)


# =====================================================
# FEATURED PROJECTS
# =====================================================

st.divider()


st.header(
    "Featured Projects"
)


project_list = load_projects()


if not project_list:

    st.info(
        "No projects found."
    )


else:

    columns = st.columns(
        min(
            3,
            len(project_list)
        )
    )


    for project_index, (
        column,
        project
    ) in enumerate(
        zip(
            columns,
            project_list[:3]
        ),
        start=1
    ):


        with column:

            # -----------------------------------------
            # TITLE
            # -----------------------------------------

            st.subheader(
                project.get(
                    "title",
                    "Untitled Project"
                )
            )

            # -----------------------------------------
            # IMAGES
            # -----------------------------------------

            images = load_project_images(
                project["_folder"]
            )


            if images:

                render_image_box(
                    images[0],
                    label=f"Project {project_index}"
                )


                gallery_state = (
                    f"home_gallery_{project_index}"
                )


                st.button(
                    "🔍 Open Gallery",

                    key=(
                        f"{gallery_state}"
                        f"_open_button"
                    ),

                    use_container_width=True,

                    on_click=open_gallery_callback,

                    args=(gallery_state,)
                )


                show_project_gallery(
                    project.get(
                        "title",
                        "Untitled Project"
                    ),

                    images,

                    state_prefix=gallery_state
                )


            else:

                st.markdown(
                    """
                    <div class="project-image-box">
                        <span style="color:#64748B;">
                            No project image
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # -----------------------------------------
            # CATEGORY
            # -----------------------------------------

            if project.get("category"):

                st.markdown(
                    f"""
                    <div class="project-meta">
                        {project["category"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # -----------------------------------------
            # SHORT DESCRIPTION
            # -----------------------------------------

            st.markdown(
                f"""
                <div class="featured-description">
                    {get_featured_description(project)}
                </div>
                """,
                unsafe_allow_html=True
            )


            # -----------------------------------------
            # LINKS
            # -----------------------------------------

            if project.get("demo"):

                st.link_button(
                    "🔗 Live Demo",
                    project["demo"],
                    use_container_width=True
                )

            elif project.get("github"):

                st.link_button(
                    "💻 GitHub",
                    project["github"],
                    use_container_width=True
                )


# =========================================================

st.markdown('<div id="projects" class="section-anchor"></div>', unsafe_allow_html=True)
# PROJECTS
# =========================================================


st.title(
    "Projects"
)


st.caption(
    "Selected projects in finance, data analysis, and machine learning."
)


project_list = load_projects()


if not project_list:

    st.info(
        "No projects found."
    )


for project in project_list:

    st.divider()


    # =================================================
    # TITLE
    # =================================================

    st.header(
        project.get(
            "title",
            "Untitled Project"
        )
    )


    # =================================================
    # CATEGORY
    # =================================================

    if project.get("category"):

        st.caption(
            project["category"]
        )


    # =================================================
    # FULL DESCRIPTION
    # =================================================

    st.write(
        project.get(
            "description",
            ""
        )
    )


    # =================================================
    # IMAGES
    # =================================================

    images = load_project_images(
        project["_folder"]
    )


    if images:

        render_image_box(
            images[0],
            label=(
                f"Image 1 of "
                f"{len(images)}"
            )
        )


        gallery_key = (
            "project_gallery_"
            + re.sub(
                r"[^a-zA-Z0-9_]",
                "_",
                str(
                    project.get(
                        "title",
                        "project"
                    )
                )
            )
        )


        st.button(
            f"🔍 Open Gallery · {len(images)} Images",

            key=(
                f"{gallery_key}"
                f"_open_button"
            ),

            use_container_width=True,

            on_click=open_gallery_callback,

            args=(gallery_key,)
        )


        show_project_gallery(
            project.get(
                "title",
                "Untitled Project"
            ),

            images,

            state_prefix=gallery_key
        )


    # =================================================
    # LINKS
    # =================================================

    col1, col2 = st.columns(2)


    with col1:

        if project.get("demo"):

            st.link_button(
                "🔗 Live Demo",
                project["demo"],
                use_container_width=True
            )


    with col2:

        if project.get("github"):

            st.link_button(
                "💻 GitHub",
                project["github"],
                use_container_width=True
            )


# =========================================================

st.markdown('<div id="experience" class="section-anchor"></div>', unsafe_allow_html=True)
# EXPERIENCE
# =========================================================


st.title(
    "Professional Experience"
)


for experience in EXPERIENCE:

    st.divider()


    st.header(
        experience["role"]
    )


    st.subheader(
        experience["company"]
    )


    st.caption(
        f'{experience["location"]} · '
        f'{experience["period"]}'
    )


    for description in experience["description"]:

        st.markdown(
            f"- {description}"
        )


st.divider()


st.header(
    "Personal Skills"
)


personal_html = ""


for skill in PERSONAL_SKILLS:

    personal_html += (
        f'<span class="skill">'
        f'{skill}'
        f'</span>'
    )


st.markdown(
    personal_html,
    unsafe_allow_html=True
)


# =========================================================

st.markdown('<div id="certificates" class="section-anchor"></div>', unsafe_allow_html=True)
# CERTIFICATES
# =========================================================


st.title(
    "Certificates"
)


st.caption(
    "Professional certificates and learning achievements."
)


certificates = load_certificates()


if not certificates:

    st.info(
        "Add certificate images to the certificates folder."
    )


else:

    columns = st.columns(3)


    for index, certificate in enumerate(
        certificates
    ):

        with columns[
            index % 3
        ]:

            render_image_box(
                certificate,

                label=(
                    certificate.stem
                    .replace(
                        "_",
                        " "
                    )
                    .title()
                )
            )



# =========================================================

st.markdown('<div id="documents" class="section-anchor"></div>', unsafe_allow_html=True)
# DOCUMENTS
# =========================================================


st.title(
    "Documents"
)

st.caption(
    "Professional and academic documents in PDF format."
)

documents = [
    {
        "title": "Curriculum Vitae",
        "icon": "📄",
        "description":
            "Professional experience, education, "
            "and technical skills.",
        "path": ASSETS_DIR / "cv.pdf",
        "file_name": "Aditya_Nugroho_CV.pdf"
    },
    {
        "title": "Bachelor's Degree Certificate",
        "icon": "🎓",
        "description":
            "Bachelor's degree certificate from "
            "Universitas Pamulang.",
        "path": ASSETS_DIR / "ijazah.pdf",
        "file_name": "Aditya_Nugroho_Degree_Certificate.pdf"
    },
    {
        "title": "Academic Transcript",
        "icon": "📊",
        "description":
            "Official academic transcript "
            "and course grades.",
        "path": ASSETS_DIR / "transkrip_nilai.pdf",
        "file_name":
            "Aditya_Nugroho_Academic_Transcript.pdf"
    }
]

st.info(
    " PDF documents are available for preview and download. "
)

for document in documents:

    document_card(
        document,
        preview_height=800
    )

# =========================================================

st.markdown('<div id="education" class="section-anchor"></div>', unsafe_allow_html=True)
# EDUCATION
# =========================================================


st.title(
    "Education"
)


st.divider()


st.header(
    PROFILE["university"]
)


st.subheader(
    PROFILE["education"]
)


st.write(
    f"📅 {PROFILE['education_period']}"
)


st.write(
    f"🎓 GPA: **{PROFILE['gpa']}**"
)


st.divider()


st.header(
    "Thesis"
)


st.write(
    PROFILE["thesis"]
)


st.divider()


st.header(
    "Languages"
)


st.write(
    "🇮🇩 Indonesian"
)


st.write(
    "🇬🇧 English"
)


# =========================================================

st.markdown('<div id="contact" class="section-anchor"></div>', unsafe_allow_html=True)
# CONTACT
# =========================================================


st.title(
    "Let's Connect"
)


st.write(
    """
    Interested in my background, projects, or potential
    collaboration? Feel free to reach out.
    """
)


st.divider()


col1, col2 = st.columns(2)


# =====================================================
# CONTACT
# =====================================================

with col1:

    st.subheader(
        "Contact"
    )


    st.link_button(
        "💬 WhatsApp",

        f"https://wa.me/{PROFILE['whatsapp']}",

        use_container_width=True
    )


    st.link_button(
        "✉️ Email",

        f"mailto:{PROFILE['email']}",

        use_container_width=True
    )


# =====================================================
# PROFESSIONAL
# =====================================================

with col2:

    st.subheader(
        "Professional"
    )


    st.link_button(
        "💼 LinkedIn",

        PROFILE["linkedin"],

        use_container_width=True
    )


    st.link_button(
        "💻 GitHub",

        PROFILE["github"],

        use_container_width=True
    )


# =====================================================

# FOOTER

# =========================================================

st.markdown(
    """
    <div class="footer">
        Aditya Nugroho ·
        Data Analyst ·
        Financial Analysis ·
        Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)
