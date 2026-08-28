import json
import re
from pathlib import Path

import streamlit as st
from PIL import Image, ImageOps


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

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
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
    h3 {
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
       PROJECT DESCRIPTION
       ===================================================== */

    .featured-description {
        color: #CBD5E1;

        font-size: 14px;

        line-height: 1.8;

        min-height: 105px;
    }


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

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PROFILE
# =========================================================

PROFILE = {

    "name":
        "Aditya Nugroho",

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
        "S1 Teknik Informatika",

    "university":
        "Universitas Pamulang",

    "education_period":
        "2020 – 2024",

    "gpa":
        "3.62",

    "thesis":
        """
        Implementasi Metode Regresi Linear Dan Support Vector
        Machine Untuk Prediksi Harga Penutupan XAUUSD
        Di Platform MetaTrader 4
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

    Example:
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
        for part in re.split(r"(\d+)", str(value))
    ]


def sorted_images(paths):
    """
    Sort images using natural numeric order.
    """

    return sorted(
        paths,
        key=lambda path: natural_key(path.name)
    )


def render_image_box(image_path, label=""):
    """
    Display image inside a fixed 16:9 area.

    Large images are reduced.
    Small images are NOT enlarged.
    """

    BOX_W = 1200
    BOX_H = 675

    try:

        image = Image.open(
            image_path
        ).convert("RGB")

        fitted = ImageOps.contain(
            image,
            (
                BOX_W - 40,
                BOX_H - 40
            ),
            method=Image.Resampling.LANCZOS
        )

        canvas = Image.new(
            "RGB",
            (
                BOX_W,
                BOX_H
            ),
            (
                17,
                24,
                39
            )
        )

        x = (
            BOX_W - fitted.width
        ) // 2

        y = (
            BOX_H - fitted.height
        ) // 2

        canvas.paste(
            fitted,
            (
                x,
                y
            )
        )

        st.image(
            canvas,
            use_container_width=True
        )

        if label:

            st.caption(
                label
            )

    except Exception:

        st.image(
            str(image_path),
            use_container_width=True
        )

        if label:

            st.caption(
                label
            )


# =========================================================
# GALLERY CALLBACK
# =========================================================

def open_gallery_callback(
    state_prefix
):
    """
    Safely open gallery.

    IMPORTANT:
    The state key is different from the button widget key.
    """

    st.session_state[
        f"{state_prefix}_is_open"
    ] = True

    st.session_state[
        f"{state_prefix}_index"
    ] = 0


def close_gallery_callback(
    state_prefix
):

    st.session_state[
        f"{state_prefix}_is_open"
    ] = False

    st.session_state[
        f"{state_prefix}_index"
    ] = 0


def previous_gallery_callback(
    state_prefix
):

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

def show_project_gallery(
    title,
    images,
    state_prefix="gallery"
):

    if not images:
        return

    index_key = (
        f"{state_prefix}_index"
    )

    open_key = (
        f"{state_prefix}_is_open"
    )


    # -----------------------------------------------------
    # INITIALIZE STATE
    # -----------------------------------------------------

    if index_key not in st.session_state:

        st.session_state[
            index_key
        ] = 0


    if open_key not in st.session_state:

        st.session_state[
            open_key
        ] = False


    # -----------------------------------------------------
    # GALLERY CLOSED
    # -----------------------------------------------------

    if not st.session_state[
        open_key
    ]:

        return


    # -----------------------------------------------------
    # CURRENT IMAGE
    # -----------------------------------------------------

    current = max(
        0,
        min(
            st.session_state[
                index_key
            ],
            len(images) - 1
        )
    )


    st.session_state[
        index_key
    ] = current


    # -----------------------------------------------------
    # GALLERY TITLE
    # -----------------------------------------------------

    st.markdown(
        f"### 🖼️ {title} — Gallery"
    )


    # -----------------------------------------------------
    # IMAGE
    # -----------------------------------------------------

    render_image_box(
        images[current],
        label=(
            f"Image {current + 1} "
            f"of {len(images)} · "
            f"{images[current].stem}"
        )
    )


    # -----------------------------------------------------
    # CONTROLS
    # -----------------------------------------------------

    prev_col, count_col, next_col, close_col = st.columns(
        [1, 1, 1, 1]
    )


    with prev_col:

        st.button(
            "← Previous",
            key=f"{state_prefix}_prev",
            use_container_width=True,
            disabled=current == 0,
            on_click=previous_gallery_callback,
            args=(state_prefix,)
        )


    with count_col:

        st.markdown(
            f"""
            <div style="
                text-align:center;
                padding:8px 0;
                color:#94A3B8;
                font-weight:700;
            ">
                {current + 1} / {len(images)}
            </div>
            """,
            unsafe_allow_html=True
        )


    with next_col:

        st.button(
            "Next →",
            key=f"{state_prefix}_next",
            use_container_width=True,
            disabled=current == len(images) - 1,
            on_click=next_gallery_callback,
            args=(
                state_prefix,
                len(images)
            )
        )


    with close_col:

        st.button(
            "✕ Close",
            key=f"{state_prefix}_close",
            use_container_width=True,
            on_click=close_gallery_callback,
            args=(state_prefix,)
        )


# =========================================================
# LOAD PROJECTS
# =========================================================

def load_projects():

    projects = []


    if not PROJECTS_DIR.exists():

        return projects


    folders = sorted(
        PROJECTS_DIR.iterdir(),
        key=lambda folder: natural_key(
            folder.name
        )
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

            projects.append(
                data
            )

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

def load_project_images(
    folder
):

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


    return sorted_images(
        images
    )


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

def get_featured_description(
    project
):
    """
    Short description khusus untuk
    Featured Projects pada Home.

    Description lengkap dari JSON
    tetap digunakan pada halaman Projects.
    """

    title = str(
        project.get(
            "title",
            ""
        )
    ).lower()


    # -----------------------------------------------------
    # FINANCE PERFORMANCE
    # -----------------------------------------------------

    if (
        "finance performance branch"
        in title
    ):

        return (
            "Analyzed branch financial "
            "performance using Power BI "
            "to identify disbursement trends "
            "and performance gaps across "
            "branch age groups."
        )


    # -----------------------------------------------------
    # TREASURY
    # -----------------------------------------------------

    if (
        "treasury" in title
        or "wealth management" in title
    ):

        return (
            "Developed a Python and Streamlit "
            "application for financial transaction "
            "monitoring and customer portfolio analysis."
        )


    # -----------------------------------------------------
    # XAUUSD
    # -----------------------------------------------------

    if "xauusd" in title:

        return (
            "Analyzed and predicted XAUUSD "
            "closing prices using Linear Regression "
            "and SVM with historical market data."
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


    # Ambil bagian sebelum section berikutnya
    description = description.split(
        "\n\n"
    )[0].strip()


    # Hapus markdown sederhana
    description = re.sub(
        r"\*\*(.*?)\*\*",
        r"\1",
        description
    )


    # Batasi panjang
    if len(description) > 180:

        description = (
            description[:177].rstrip()
            + "..."
        )


    return description


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


page = st.sidebar.radio(
    "MENU",
    [
        "Home",
        "Projects",
        "Experience",
        "Certificates",
        "Education",
        "Contact"
    ]
)


st.sidebar.divider()


st.sidebar.caption(
    "Data Analyst • Financial Analysis • Machine Learning"
)


# =========================================================
# HOME
# =========================================================

if page == "Home":


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
                str(profile_image),
                width=190
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
    # SKILLS
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
                # TITLE
                # -----------------------------------------

                st.subheader(
                    project.get(
                        "title",
                        "Untitled Project"
                    )
                )


                # -----------------------------------------
                # CATEGORY
                # -----------------------------------------

                if project.get(
                    "category"
                ):

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

                if project.get(
                    "demo"
                ):

                    st.link_button(
                        "🔗 Live Demo",
                        project["demo"],
                        use_container_width=True
                    )

                elif project.get(
                    "github"
                ):

                    st.link_button(
                        "💻 GitHub",
                        project["github"],
                        use_container_width=True
                    )


# =========================================================
# PROJECTS
# =========================================================

elif page == "Projects":


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

        if project.get(
            "category"
        ):

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

            if project.get(
                "demo"
            ):

                st.link_button(
                    "🔗 Live Demo",
                    project["demo"],
                    use_container_width=True
                )


        with col2:

            if project.get(
                "github"
            ):

                st.link_button(
                    "💻 GitHub",
                    project["github"],
                    use_container_width=True
                )


# =========================================================
# EXPERIENCE
# =========================================================

elif page == "Experience":


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


        for description in experience[
            "description"
        ]:

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
# CERTIFICATES
# =========================================================

elif page == "Certificates":


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
# EDUCATION
# =========================================================

elif page == "Education":


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
        "🇮🇩 Bahasa Indonesia"
    )


    st.write(
        "🇬🇧 Bahasa Inggris"
    )


# =========================================================
# CONTACT
# =========================================================

elif page == "Contact":


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
    # CV
    # =====================================================

    cv_file = (
        ASSETS_DIR / "cv.pdf"
    )


    if cv_file.exists():


        st.divider()


        st.download_button(
            "📄 Download CV",
            data=cv_file.read_bytes(),
            file_name="Aditya_Nugroho_CV.pdf",
            mime="application/pdf",
            use_container_width=True
        )


# =========================================================
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