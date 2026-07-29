import streamlit as st


st.set_page_config(
    page_title="Naval Load Line Studio",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --navy: #071A2B;
            --steel-blue: #163A59;
            --steel-gray: #6E7B87;
            --light-gray: #F4F6F8;
            --border: #D8E0E7;
            --green: #1F8A5B;
        }

        .stApp {
            background: #F4F6F8;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .hero-card {
            background: white;
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 42px 34px 36px 34px;
            text-align: center;
            box-shadow: 0 12px 32px rgba(7, 26, 43, 0.08);
        }

        .logo-symbol {
            width: 92px;
            height: 92px;
            margin: 0 auto 18px auto;
            border: 4px solid var(--navy);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 46px;
            color: var(--navy);
            position: relative;
        }

        .logo-symbol::before,
        .logo-symbol::after {
            content: "";
            position: absolute;
            top: 50%;
            width: 48px;
            height: 4px;
            background: var(--navy);
        }

        .logo-symbol::before {
            right: 74px;
        }

        .logo-symbol::after {
            left: 74px;
        }

        .software-title {
            color: var(--navy);
            font-size: 38px;
            font-weight: 800;
            letter-spacing: 1.2px;
            margin-bottom: 4px;
        }

        .software-subtitle {
            color: var(--steel-gray);
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 22px;
        }

        .ready-message {
            color: var(--steel-blue);
            font-size: 20px;
            font-weight: 700;
            margin-top: 12px;
            margin-bottom: 28px;
        }

        .section-title {
            color: var(--navy);
            font-size: 21px;
            font-weight: 750;
            margin-bottom: 4px;
        }

        .section-text {
            color: var(--steel-gray);
            font-size: 14px;
            margin-bottom: 16px;
        }

        .status-card {
            background: white;
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 24px;
            box-shadow: 0 8px 22px rgba(7, 26, 43, 0.06);
            min-height: 100%;
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 9px 0;
            color: #263746;
            font-size: 14px;
            border-bottom: 1px solid #EEF2F5;
        }

        .status-item:last-child {
            border-bottom: none;
        }

        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 0 4px rgba(31, 138, 91, 0.12);
        }

        .ready-badge {
            display: inline-block;
            margin-top: 18px;
            padding: 9px 18px;
            border-radius: 999px;
            background: rgba(31, 138, 91, 0.12);
            color: var(--green);
            font-weight: 800;
            letter-spacing: 0.8px;
        }

        .footer-signature {
            text-align: center;
            color: var(--steel-gray);
            font-size: 13px;
            margin-top: 32px;
            line-height: 1.7;
        }

        .footer-signature strong {
            color: var(--navy);
            font-size: 14px;
        }

        div.stButton > button {
            width: 100%;
            min-height: 58px;
            border-radius: 12px;
            border: 1px solid #C8D3DC;
            background: white;
            color: var(--navy);
            font-size: 16px;
            font-weight: 750;
            transition: all 0.18s ease;
            box-shadow: 0 4px 10px rgba(7, 26, 43, 0.04);
        }

        div.stButton > button:hover {
            border-color: var(--steel-blue);
            color: white;
            background: var(--steel-blue);
            transform: translateY(-1px);
            box-shadow: 0 8px 18px rgba(7, 26, 43, 0.12);
        }

        div.stButton > button:focus {
            box-shadow: 0 0 0 3px rgba(22, 58, 89, 0.18);
        }

        @media (max-width: 700px) {
            .software-title {
                font-size: 29px;
            }

            .hero-card {
                padding: 32px 18px;
            }

            .logo-symbol::before,
            .logo-symbol::after {
                width: 28px;
            }

            .logo-symbol::before {
                right: 80px;
            }

            .logo-symbol::after {
                left: 80px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_state() -> None:
    if "page" not in st.session_state:
        st.session_state.page = "home"


def go_to(page: str) -> None:
    st.session_state.page = page
    st.rerun()


def render_home() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <div class="logo-symbol">⚓</div>
            <div class="software-title">NAVAL LOAD LINE STUDIO</div>
            <div class="software-subtitle">Engineering Freeboard Analysis</div>
            <div class="ready-message">
                Ready to perform a Load Line Assessment
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    left, center, right = st.columns([1, 1.7, 1])

    with center:
        if st.button("⚓  New Project", use_container_width=True):
            go_to("new_project")

        if st.button("📂  Open Project", use_container_width=True):
            go_to("open_project")

        if st.button("📘  Load Line Convention", use_container_width=True):
            go_to("convention")

        if st.button("⚙️  Settings", use_container_width=True):
            go_to("settings")

    st.write("")

    info_col, status_col = st.columns([1.35, 1])

    with info_col:
        st.markdown(
            """
            <div class="status-card">
                <div class="section-title">Professional Freeboard Assessment</div>
                <div class="section-text">
                    Create, document and evaluate ship load line projects
                    using a structured engineering workflow.
                </div>

                <div class="status-item">
                    <span class="status-dot"></span>
                    Project-based assessment workflow
                </div>

                <div class="status-item">
                    <span class="status-dot"></span>
                    Regulatory calculation architecture
                </div>

                <div class="status-item">
                    <span class="status-dot"></span>
                    Technical report preparation
                </div>

                <div class="status-item">
                    <span class="status-dot"></span>
                    Engineering traceability
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with status_col:
        st.markdown(
            """
            <div class="status-card">
                <div class="section-title">Engine Status</div>
                <div class="section-text">
                    System modules available in this development version.
                </div>

                <div class="status-item">
                    <span class="status-dot"></span>
                    User Interface Ready
                </div>

                <div class="status-item">
                    <span class="status-dot"></span>
                    Project Manager Ready
                </div>

                <div class="status-item">
                    <span class="status-dot"></span>
                    Convention Module Prepared
                </div>

                <div class="status-item">
                    <span class="status-dot"></span>
                    Report Architecture Prepared
                </div>

                <div class="ready-badge">STATUS: READY</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="footer-signature">
            Developed by<br>
            <strong>Jade Fernanda Jarquín Contreras</strong><br>
            Naval Load Line Studio · Version 0.1
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_placeholder(
    title: str,
    description: str,
) -> None:
    top_left, top_right = st.columns([5, 1])

    with top_right:
        if st.button("← Home", use_container_width=True):
            go_to("home")

    st.markdown(
        f"""
        <div class="hero-card">
            <div class="software-title">{title}</div>
            <div class="software-subtitle">{description}</div>
            <div class="ready-badge">MODULE IN DEVELOPMENT</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    initialize_state()
    apply_styles()

    pages = {
        "home": render_home,
        "new_project": lambda: render_placeholder(
            "New Project",
            "Creation and identification of a new load line assessment project.",
        ),
        "open_project": lambda: render_placeholder(
            "Open Project",
            "Open and continue a previously saved engineering assessment.",
        ),
        "convention": lambda: render_placeholder(
            "Load Line Convention",
            "Regulatory reference and technical guidance module.",
        ),
        "settings": lambda: render_placeholder(
            "Settings",
            "Application preferences, units and report configuration.",
        ),
    }

    page_function = pages.get(st.session_state.page, render_home)
    page_function()


if __name__ == "__main__":
    main()
