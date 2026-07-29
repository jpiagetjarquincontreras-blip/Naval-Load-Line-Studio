from __future__ import annotations

import json
import re
from datetime import date, datetime
from textwrap import dedent
from typing import Any

import streamlit as st


APP_NAME = "Naval Load Line Studio"
APP_VERSION = "0.3"
PROJECT_FILE_EXTENSION = ".nlls"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def apply_styles() -> None:
    st.markdown(
        dedent(
            """
            <style>
            :root {
                --navy: #071A2B;
                --steel-blue: #163A59;
                --steel-gray: #6E7B87;
                --light-gray: #F4F6F8;
                --border: #D8E0E7;
                --green: #1F8A5B;
                --yellow: #B7791F;
                --red: #C33A3A;
            }

            html,
            body,
            [class*="css"] {
                font-family: "Segoe UI", Arial, sans-serif;
            }

            .stApp {
                background: var(--light-gray);
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
                padding-top: 1.4rem;
                padding-bottom: 2.4rem;
            }

            .hero-card,
            .panel-card,
            .summary-card {
                background: #FFFFFF;
                border: 1px solid var(--border);
                box-shadow: 0 10px 28px rgba(7, 26, 43, 0.07);
            }

            .hero-card {
                border-radius: 22px;
                padding: 42px 34px 36px;
                text-align: center;
            }

            .panel-card,
            .summary-card {
                border-radius: 18px;
                padding: 24px;
            }

            .logo-symbol {
                width: 92px;
                height: 92px;
                margin: 0 auto 18px;
                border: 4px solid var(--navy);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 46px;
                color: var(--navy);
                position: relative;
                box-sizing: border-box;
            }

            .logo-symbol::before,
            .logo-symbol::after {
                content: "";
                position: absolute;
                top: 50%;
                width: 48px;
                height: 4px;
                background: var(--navy);
                transform: translateY(-50%);
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
            }

            .section-title {
                color: var(--navy);
                font-size: 21px;
                font-weight: 750;
                margin-bottom: 6px;
            }

            .section-text {
                color: var(--steel-gray);
                font-size: 14px;
                line-height: 1.6;
                margin-bottom: 16px;
            }

            .status-item {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 11px 0;
                color: #263746;
                font-size: 14px;
                border-bottom: 1px solid #EEF2F5;
            }

            .status-dot {
                width: 10px;
                height: 10px;
                min-width: 10px;
                border-radius: 50%;
                background: var(--green);
                box-shadow: 0 0 0 4px rgba(31, 138, 91, 0.12);
            }

            .ready-badge,
            .saved-badge,
            .warning-badge {
                display: inline-block;
                margin-top: 18px;
                padding: 9px 18px;
                border-radius: 999px;
                font-weight: 800;
                letter-spacing: 0.7px;
            }

            .ready-badge,
            .saved-badge {
                background: rgba(31, 138, 91, 0.12);
                color: var(--green);
            }

            .warning-badge {
                background: rgba(183, 121, 31, 0.14);
                color: var(--yellow);
            }

            .module-title {
                color: var(--navy);
                font-size: 31px;
                font-weight: 800;
                margin-bottom: 5px;
            }

            .module-subtitle {
                color: var(--steel-gray);
                font-size: 15px;
                line-height: 1.6;
            }

            .step-label {
                color: var(--steel-blue);
                font-size: 13px;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 7px;
            }

            .summary-row {
                display: flex;
                justify-content: space-between;
                gap: 20px;
                padding: 10px 0;
                border-bottom: 1px solid #EDF1F4;
                color: #263746;
                font-size: 14px;
            }

            .summary-row:last-child {
                border-bottom: none;
            }

            .summary-label {
                color: var(--steel-gray);
            }

            .summary-value {
                color: var(--navy);
                font-weight: 700;
                text-align: right;
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

            div.stButton > button,
            div.stDownloadButton > button {
                width: 100%;
                min-height: 52px;
                border-radius: 12px;
                border: 1px solid #C8D3DC;
                background: #FFFFFF;
                color: var(--navy);
                font-size: 15px;
                font-weight: 750;
                transition: all 0.18s ease;
                box-shadow: 0 4px 10px rgba(7, 26, 43, 0.04);
            }

            div.stButton > button:hover,
            div.stDownloadButton > button:hover {
                border-color: var(--steel-blue);
                color: #FFFFFF;
                background: var(--steel-blue);
                transform: translateY(-1px);
            }

            div[data-baseweb="input"] > div,
            div[data-baseweb="select"] > div,
            div[data-baseweb="textarea"] > div {
                border-radius: 10px;
            }


            .result-card {
                background: #FFFFFF;
                border: 1px solid var(--border);
                border-left: 7px solid var(--steel-blue);
                border-radius: 16px;
                padding: 24px;
                box-shadow: 0 10px 28px rgba(7, 26, 43, 0.07);
                margin-top: 16px;
            }

            .result-card.applies {
                border-left-color: var(--green);
            }

            .result-card.excluded {
                border-left-color: var(--steel-gray);
            }

            .result-card.review {
                border-left-color: var(--yellow);
            }

            .result-title {
                color: var(--navy);
                font-size: 24px;
                font-weight: 850;
                margin-bottom: 8px;
            }

            .result-reference {
                color: var(--steel-blue);
                font-size: 14px;
                font-weight: 750;
                margin-bottom: 12px;
            }

            .result-text {
                color: #34495A;
                font-size: 15px;
                line-height: 1.65;
            }

            @media (max-width: 700px) {
                .block-container {
                    padding-left: 0.8rem;
                    padding-right: 0.8rem;
                }

                .software-title {
                    font-size: 28px;
                }

                .software-subtitle {
                    font-size: 16px;
                }

                .ready-message {
                    font-size: 17px;
                }

                .hero-card {
                    padding: 32px 18px;
                }
            }
            </style>
            """
        ),
        unsafe_allow_html=True,
    )


def initialize_state() -> None:
    defaults = {
        "page": "home",
        "project_saved": False,
        "project_data": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go_to(page: str) -> None:
    st.session_state.page = page
    st.rerun()


def clean_filename(value: str) -> str:
    cleaned = re.sub(r"[^\w\-]+", "_", value.strip(), flags=re.UNICODE)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "naval_load_line_project"


def project_to_json(project: dict[str, Any]) -> str:
    return json.dumps(project, ensure_ascii=False, indent=2, default=str)


def footer() -> None:
    st.markdown(
        dedent(
            f"""
            <div class="footer-signature">
                Developed by<br>
                <strong>Jade Fernanda Jarquín Contreras</strong><br>
                {APP_NAME} · Version {APP_VERSION}
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def render_home() -> None:
    st.markdown(
        dedent(
            """
            <div class="hero-card">
                <div class="logo-symbol">⚓</div>
                <div class="software-title">NAVAL LOAD LINE STUDIO</div>
                <div class="software-subtitle">Engineering Freeboard Analysis</div>
                <div class="ready-message">
                    Ready to perform a Load Line Assessment
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.write("")
    _, center, _ = st.columns([1, 1.7, 1])

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
            dedent(
                """
                <div class="panel-card">
                    <div class="section-title">Professional Freeboard Assessment</div>
                    <div class="section-text">
                        Create, document and evaluate ship load line projects
                        using a structured engineering workflow.
                    </div>
                    <div class="status-item">
                        <span class="status-dot"></span>
                        <span>Project-based assessment workflow</span>
                    </div>
                    <div class="status-item">
                        <span class="status-dot"></span>
                        <span>Regulatory calculation architecture</span>
                    </div>
                    <div class="status-item">
                        <span class="status-dot"></span>
                        <span>Technical report preparation</span>
                    </div>
                    <div class="status-item">
                        <span class="status-dot"></span>
                        <span>Engineering traceability</span>
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    with status_col:
        st.markdown(
            dedent(
                """
                <div class="panel-card">
                    <div class="section-title">Engine Status</div>
                    <div class="section-text">
                        System modules available in this development version.
                    </div>
                    <div class="status-item">
                        <span class="status-dot"></span>
                        <span>User Interface Ready</span>
                    </div>
                    <div class="status-item">
                        <span class="status-dot"></span>
                        <span>Project Manager Ready</span>
                    </div>
                    <div class="status-item">
                        <span class="status-dot"></span>
                        <span>Convention Module Prepared</span>
                    </div>
                    <div class="status-item">
                        <span class="status-dot"></span>
                        <span>Report Architecture Prepared</span>
                    </div>
                    <div class="ready-badge">STATUS: READY</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    footer()


def render_new_project() -> None:
    back_col, title_col = st.columns([1, 5])

    with back_col:
        if st.button("← Home", use_container_width=True):
            go_to("home")

    with title_col:
        st.markdown(
            dedent(
                """
                <div class="step-label">Project workflow · Step 1</div>
                <div class="module-title">Create New Project</div>
                <div class="module-subtitle">
                    Register the project and ship identification data before
                    beginning the regulatory load line assessment.
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    st.write("")

    existing = st.session_state.project_data

    with st.form("new_project_form", clear_on_submit=False):
        st.subheader("Project Information")

        c1, c2 = st.columns(2)
        with c1:
            project_name = st.text_input(
                "Project name *",
                value=existing.get("project_name", ""),
                placeholder="Example: Load Line Assessment – MV Aurora",
            )
            engineer = st.text_input(
                "Responsible engineer *",
                value=existing.get(
                    "engineer",
                    "Jade Fernanda Jarquín Contreras",
                ),
            )
            organization = st.text_input(
                "Organization",
                value=existing.get("organization", ""),
                placeholder="University, shipyard, company or consultancy",
            )

        with c2:
            project_code = st.text_input(
                "Project code",
                value=existing.get("project_code", ""),
                placeholder="Example: NLLS-2026-001",
            )
            project_date = st.date_input(
                "Project date *",
                value=(
                    date.fromisoformat(existing["project_date"])
                    if existing.get("project_date")
                    else date.today()
                ),
            )
            unit_system = st.selectbox(
                "Unit system *",
                ["Metric (SI)", "Imperial"],
                index=0 if existing.get("unit_system", "Metric (SI)") == "Metric (SI)" else 1,
            )

        st.divider()
        st.subheader("Ship Information")

        s1, s2 = st.columns(2)
        with s1:
            ship_name = st.text_input(
                "Ship name *",
                value=existing.get("ship_name", ""),
                placeholder="Example: MV Aurora",
            )
            imo_number = st.text_input(
                "IMO number",
                value=existing.get("imo_number", ""),
                max_chars=7,
                placeholder="Seven digits",
                help="Enter only the seven numerical digits when available.",
            )
            flag = st.text_input(
                "Flag",
                value=existing.get("flag", ""),
                placeholder="Example: Mexico",
            )
            port_registry = st.text_input(
                "Port of registry",
                value=existing.get("port_registry", ""),
                placeholder="Example: Veracruz",
            )

        with s2:
            classification_society = st.selectbox(
                "Classification society",
                [
                    "Not specified",
                    "ABS",
                    "DNV",
                    "Lloyd's Register",
                    "Bureau Veritas",
                    "RINA",
                    "ClassNK",
                    "KR",
                    "CCS",
                    "Other",
                ],
                index=(
                    [
                        "Not specified",
                        "ABS",
                        "DNV",
                        "Lloyd's Register",
                        "Bureau Veritas",
                        "RINA",
                        "ClassNK",
                        "KR",
                        "CCS",
                        "Other",
                    ].index(existing.get("classification_society", "Not specified"))
                    if existing.get("classification_society", "Not specified")
                    in [
                        "Not specified",
                        "ABS",
                        "DNV",
                        "Lloyd's Register",
                        "Bureau Veritas",
                        "RINA",
                        "ClassNK",
                        "KR",
                        "CCS",
                        "Other",
                    ]
                    else 0
                ),
            )
            ship_type = st.selectbox(
                "Ship type *",
                [
                    "Select ship type",
                    "Cargo ship",
                    "Oil tanker",
                    "Chemical tanker",
                    "Gas carrier",
                    "Bulk carrier",
                    "Container ship",
                    "Passenger ship",
                    "Ro-Ro ship",
                    "Offshore support vessel",
                    "Fishing vessel",
                    "Other",
                ],
                index=(
                    [
                        "Select ship type",
                        "Cargo ship",
                        "Oil tanker",
                        "Chemical tanker",
                        "Gas carrier",
                        "Bulk carrier",
                        "Container ship",
                        "Passenger ship",
                        "Ro-Ro ship",
                        "Offshore support vessel",
                        "Fishing vessel",
                        "Other",
                    ].index(existing.get("ship_type", "Select ship type"))
                    if existing.get("ship_type", "Select ship type")
                    in [
                        "Select ship type",
                        "Cargo ship",
                        "Oil tanker",
                        "Chemical tanker",
                        "Gas carrier",
                        "Bulk carrier",
                        "Container ship",
                        "Passenger ship",
                        "Ro-Ro ship",
                        "Offshore support vessel",
                        "Fishing vessel",
                        "Other",
                    ]
                    else 0
                ),
            )
            call_sign = st.text_input(
                "Call sign",
                value=existing.get("call_sign", ""),
                placeholder="Optional",
            )
            year_built = st.number_input(
                "Year built",
                min_value=1800,
                max_value=date.today().year + 5,
                value=int(existing.get("year_built", date.today().year)),
                step=1,
            )

        notes = st.text_area(
            "Project notes",
            value=existing.get("notes", ""),
            placeholder="Optional comments, scope or document references.",
            height=110,
        )

        save_submitted = st.form_submit_button(
            "💾 Save Project",
            use_container_width=True,
        )

    if save_submitted:
        errors = []

        if not project_name.strip():
            errors.append("Project name is required.")
        if not engineer.strip():
            errors.append("Responsible engineer is required.")
        if not ship_name.strip():
            errors.append("Ship name is required.")
        if ship_type == "Select ship type":
            errors.append("Select a ship type.")
        if imo_number.strip() and not re.fullmatch(r"\d{7}", imo_number.strip()):
            errors.append("IMO number must contain exactly seven digits.")

        if errors:
            for error in errors:
                st.error(error)
        else:
            project = {
                "software": APP_NAME,
                "software_version": APP_VERSION,
                "file_format": "NLLS Project",
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "project_name": project_name.strip(),
                "project_code": project_code.strip(),
                "engineer": engineer.strip(),
                "organization": organization.strip(),
                "project_date": project_date.isoformat(),
                "unit_system": unit_system,
                "ship_name": ship_name.strip(),
                "imo_number": imo_number.strip(),
                "flag": flag.strip(),
                "port_registry": port_registry.strip(),
                "classification_society": classification_society,
                "ship_type": ship_type,
                "call_sign": call_sign.strip(),
                "year_built": int(year_built),
                "notes": notes.strip(),
                "assessment_status": "Project created",
            }

            st.session_state.project_data = project
            st.session_state.project_saved = True
            st.success("Project saved successfully in the current session.")

    if st.session_state.project_saved and st.session_state.project_data:
        render_project_summary(st.session_state.project_data)

    footer()


def render_project_summary(project: dict[str, Any]) -> None:
    st.write("")
    st.markdown(
        dedent(
            """
            <div class="step-label">Saved project</div>
            <div class="module-title">Project Summary</div>
            """
        ),
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.25, 1])

    with left:
        rows = [
            ("Project", project.get("project_name", "—")),
            ("Ship", project.get("ship_name", "—")),
            ("IMO number", project.get("imo_number") or "Not provided"),
            ("Ship type", project.get("ship_type", "—")),
            ("Flag", project.get("flag") or "Not provided"),
            (
                "Classification society",
                project.get("classification_society", "Not specified"),
            ),
            ("Responsible engineer", project.get("engineer", "—")),
            ("Unit system", project.get("unit_system", "—")),
        ]

        html_rows = "\n".join(
            f"""
            <div class="summary-row">
                <span class="summary-label">{label}</span>
                <span class="summary-value">{value}</span>
            </div>
            """
            for label, value in rows
        )

        st.markdown(
            dedent(
                f"""
                <div class="summary-card">
                    <div class="section-title">Identification</div>
                    {html_rows}
                    <div class="saved-badge">PROJECT SAVED</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    with right:
        filename = (
            clean_filename(project.get("project_name", "project"))
            + PROJECT_FILE_EXTENSION
        )
        project_json = project_to_json(project)

        st.markdown(
            dedent(
                """
                <div class="panel-card">
                    <div class="section-title">Next Actions</div>
                    <div class="section-text">
                        Download the project file for backup or continue to
                        the Convention applicability assessment.
                    </div>
                    <div class="status-item">
                        <span class="status-dot"></span>
                        <span>Identification data validated</span>
                    </div>
                    <div class="status-item">
                        <span class="status-dot"></span>
                        <span>Project structure initialized</span>
                    </div>
                    <div class="warning-badge">
                        NEXT: APPLICABILITY ASSESSMENT
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

        st.write("")
        st.download_button(
            "⬇️ Download project file (.nlls)",
            data=project_json,
            file_name=filename,
            mime="application/json",
            use_container_width=True,
        )

        if st.button(
            "Continue to Applicability Assessment →",
            use_container_width=True,
        ):
            go_to("applicability")


def render_open_project() -> None:
    _, back = st.columns([5, 1])
    with back:
        if st.button("← Home", use_container_width=True):
            go_to("home")

    st.markdown(
        dedent(
            """
            <div class="step-label">Project manager</div>
            <div class="module-title">Open Project</div>
            <div class="module-subtitle">
                Upload a Naval Load Line Studio project file previously
                downloaded with the .nlls extension.
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.write("")
    uploaded = st.file_uploader(
        "Select a project file",
        type=["nlls", "json"],
        accept_multiple_files=False,
    )

    if uploaded is not None:
        try:
            project = json.loads(uploaded.getvalue().decode("utf-8"))

            if project.get("file_format") != "NLLS Project":
                st.warning(
                    "The file is valid JSON, but it does not appear to be "
                    "a Naval Load Line Studio project."
                )
                return

            st.session_state.project_data = project
            st.session_state.project_saved = True
            st.success("Project loaded successfully.")
            render_project_summary(project)

        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            st.error(f"The selected file could not be opened: {exc}")

    footer()


def render_placeholder(
    title: str,
    description: str,
    badge: str = "MODULE IN DEVELOPMENT",
) -> None:
    _, back = st.columns([5, 1])
    with back:
        if st.button("← Home", use_container_width=True):
            go_to("home")

    st.markdown(
        dedent(
            f"""
            <div class="hero-card">
                <div class="module-title">{title}</div>
                <div class="module-subtitle">{description}</div>
                <div class="warning-badge">{badge}</div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    footer()


def evaluate_applicability(
    international_voyage: str,
    convention_flag_status: str,
    vessel_category: str,
    ship_condition: str,
    length_m: float,
    gross_tonnage: float,
    navigation_area: str,
    exemption_status: str,
) -> dict[str, Any]:
    """Preliminary applicability decision based on Articles IV, V and VI.

    This module is an engineering screening tool. Formal exemptions and final
    statutory determinations remain under the competent Administration.
    """
    reasons: list[str] = []
    references: list[str] = []

    if international_voyage == "No":
        return {
            "status": "Convention Does Not Apply",
            "status_code": "excluded",
            "reason": (
                "The Convention applies to ships engaged on international "
                "voyages. The declared operation is not an international voyage."
            ),
            "references": ["Article IV(2)"],
            "requires_authority": False,
        }

    if convention_flag_status == "No / Unknown":
        return {
            "status": "Technical Review Required",
            "status_code": "review",
            "reason": (
                "The ship's registration or flag relationship with a "
                "Contracting Government has not been confirmed. Applicability "
                "cannot be concluded automatically."
            ),
            "references": ["Article IV(1)"],
            "requires_authority": True,
        }

    category_exclusions = {
        "Warship": "Warships are excluded from the Convention.",
        "Non-commercial pleasure yacht": (
            "Pleasure yachts not engaged in trade are excluded."
        ),
        "Fishing vessel": "Fishing vessels are excluded from the Convention.",
    }

    if vessel_category in category_exclusions:
        return {
            "status": "Convention Does Not Apply",
            "status_code": "excluded",
            "reason": category_exclusions[vessel_category],
            "references": ["Article V(1)"],
            "requires_authority": False,
        }

    if ship_condition == "New ship" and length_m < 24.0:
        return {
            "status": "Convention Does Not Apply",
            "status_code": "excluded",
            "reason": (
                "A new ship with Convention length below 24 m is excluded."
            ),
            "references": ["Article V(1)(b)"],
            "requires_authority": False,
        }

    if ship_condition == "Existing ship" and gross_tonnage < 150.0:
        return {
            "status": "Convention Does Not Apply",
            "status_code": "excluded",
            "reason": (
                "An existing ship with gross tonnage below 150 is excluded."
            ),
            "references": ["Article V(1)(c)"],
            "requires_authority": False,
        }

    excluded_navigation_areas = {
        "North American Great Lakes / specified St. Lawrence area",
        "Caspian Sea",
        "Río de la Plata, Paraná and Uruguay specified area",
    }

    if navigation_area in excluded_navigation_areas:
        return {
            "status": "Convention Does Not Apply",
            "status_code": "excluded",
            "reason": (
                "The vessel is declared to operate exclusively within a "
                "navigation area expressly excepted by the Convention."
            ),
            "references": ["Article V(2)"],
            "requires_authority": False,
        }

    if exemption_status != "No exemption claimed":
        return {
            "status": "Technical Review Required",
            "status_code": "review",
            "reason": (
                "A possible exemption has been declared. Exemptions under "
                "Article VI require acceptance or determination by the "
                "Administration and, where applicable, the Governments concerned."
            ),
            "references": ["Article VI"],
            "requires_authority": True,
        }

    reasons.append(
        "The ship is declared to undertake international voyages and no "
        "automatic exception has been identified."
    )
    references.extend(["Article IV", "Article V"])

    if ship_condition == "Existing ship":
        reasons.append(
            "As an existing ship, the detailed technical requirements may be "
            "subject to the minimum provisions and conditions described in "
            "Article IV(4)."
        )
        references.append("Article IV(4)")

    return {
        "status": "Convention Applies",
        "status_code": "applies",
        "reason": " ".join(reasons),
        "references": references,
        "requires_authority": False,
    }


def render_applicability_result(result: dict[str, Any]) -> None:
    references = " · ".join(result.get("references", []))
    st.markdown(
        dedent(
            f"""
            <div class="result-card {result['status_code']}">
                <div class="result-title">{result['status']}</div>
                <div class="result-reference">Regulatory basis: {references}</div>
                <div class="result-text">{result['reason']}</div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    if result.get("requires_authority"):
        st.warning(
            "This outcome cannot be closed solely by the application. "
            "Confirmation from the competent Administration is required."
        )
    else:
        st.info(
            "This is a preliminary engineering screening. The flag "
            "Administration and applicable statutory documents remain the "
            "authoritative basis for certification."
        )


def render_applicability() -> None:
    if not st.session_state.project_data:
        st.warning("Create or open a project before continuing.")
        if st.button("Go to New Project", use_container_width=True):
            go_to("new_project")
        return

    top_left, top_right = st.columns([5, 1])
    with top_right:
        if st.button("← Home", use_container_width=True):
            go_to("home")

    project = st.session_state.project_data
    existing = project.get("applicability_assessment", {})

    st.markdown(
        dedent(
            f"""
            <div class="step-label">Project workflow · Step 2</div>
            <div class="module-title">Applicability Assessment</div>
            <div class="module-subtitle">
                Preliminary determination for <strong>{project.get('ship_name', 'the ship')}</strong>
                under Articles IV, V and VI of the International Convention
                on Load Lines, 1966, as modified by the 1988 Protocol.
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.write("")

    with st.form("applicability_form", clear_on_submit=False):
        st.subheader("Operational Scope")

        c1, c2 = st.columns(2)
        with c1:
            international_voyage = st.radio(
                "Will the ship undertake international voyages? *",
                ["Yes", "No"],
                index=0 if existing.get("international_voyage", "Yes") == "Yes" else 1,
                help=(
                    "An international voyage is a sea voyage between a country "
                    "to which the Convention applies and a port outside that country, "
                    "or conversely."
                ),
            )

            convention_flag_status = st.radio(
                "Is the ship registered in, or entitled to fly the flag of, a Contracting Government? *",
                ["Yes", "No / Unknown"],
                index=0 if existing.get("convention_flag_status", "Yes") == "Yes" else 1,
            )

        with c2:
            navigation_area_options = [
                "General international navigation",
                "North American Great Lakes / specified St. Lawrence area",
                "Caspian Sea",
                "Río de la Plata, Paraná and Uruguay specified area",
            ]
            navigation_area = st.selectbox(
                "Exclusive navigation area *",
                navigation_area_options,
                index=(
                    navigation_area_options.index(
                        existing.get(
                            "navigation_area",
                            "General international navigation",
                        )
                    )
                    if existing.get(
                        "navigation_area",
                        "General international navigation",
                    )
                    in navigation_area_options
                    else 0
                ),
            )

            exemption_options = [
                "No exemption claimed",
                "Voyages between nearby ports of two or more States",
                "Ship with novel features requiring exemption",
                "Single international voyage under special conditions",
                "Other exemption or Administration decision",
            ]
            exemption_status = st.selectbox(
                "Possible exemption under Article VI",
                exemption_options,
                index=(
                    exemption_options.index(
                        existing.get(
                            "exemption_status",
                            "No exemption claimed",
                        )
                    )
                    if existing.get(
                        "exemption_status",
                        "No exemption claimed",
                    )
                    in exemption_options
                    else 0
                ),
            )

        st.divider()
        st.subheader("Ship Status and Automatic Exceptions")

        c3, c4 = st.columns(2)
        with c3:
            vessel_category_options = [
                "Commercial ship / other ship",
                "Warship",
                "Fishing vessel",
                "Non-commercial pleasure yacht",
            ]
            vessel_category = st.selectbox(
                "Vessel category *",
                vessel_category_options,
                index=(
                    vessel_category_options.index(
                        existing.get(
                            "vessel_category",
                            "Commercial ship / other ship",
                        )
                    )
                    if existing.get(
                        "vessel_category",
                        "Commercial ship / other ship",
                    )
                    in vessel_category_options
                    else 0
                ),
            )

            ship_condition = st.radio(
                "Convention status of the ship *",
                ["New ship", "Existing ship", "Not yet determined"],
                index=(
                    ["New ship", "Existing ship", "Not yet determined"].index(
                        existing.get("ship_condition", "New ship")
                    )
                    if existing.get("ship_condition", "New ship")
                    in ["New ship", "Existing ship", "Not yet determined"]
                    else 0
                ),
                help=(
                    "The formal distinction depends on the keel-laying or "
                    "equivalent construction date relative to the Convention's "
                    "entry into force for the relevant Contracting Government."
                ),
            )

        with c4:
            length_m = st.number_input(
                "Convention length L [m] *",
                min_value=0.0,
                value=float(existing.get("length_m", 24.0)),
                step=0.1,
                format="%.2f",
                help=(
                    "Use the length L defined in Article II(8), not LOA or Lpp "
                    "unless they coincide with the Convention definition."
                ),
            )

            gross_tonnage = st.number_input(
                "Gross tonnage [GT] *",
                min_value=0.0,
                value=float(existing.get("gross_tonnage", 150.0)),
                step=1.0,
                help=(
                    "This value is used for the Article V exception applicable "
                    "to existing ships below 150 gross tons."
                ),
            )

        assessment_notes = st.text_area(
            "Assessment notes",
            value=existing.get("assessment_notes", ""),
            placeholder=(
                "Record flag Administration evidence, voyage description, "
                "exemption documents or other relevant observations."
            ),
            height=110,
        )

        submitted = st.form_submit_button(
            "Evaluate Applicability",
            use_container_width=True,
        )

    if submitted:
        if ship_condition == "Not yet determined":
            result = {
                "status": "Technical Review Required",
                "status_code": "review",
                "reason": (
                    "The ship has not yet been classified as new or existing. "
                    "This distinction is necessary to evaluate the automatic "
                    "length and tonnage exceptions and the technical regime "
                    "applicable to the ship."
                ),
                "references": ["Article II(6) and II(7)", "Article IV", "Article V"],
                "requires_authority": True,
            }
        else:
            result = evaluate_applicability(
                international_voyage=international_voyage,
                convention_flag_status=convention_flag_status,
                vessel_category=vessel_category,
                ship_condition=ship_condition,
                length_m=length_m,
                gross_tonnage=gross_tonnage,
                navigation_area=navigation_area,
                exemption_status=exemption_status,
            )

        assessment = {
            "evaluated_at": datetime.now().isoformat(timespec="seconds"),
            "international_voyage": international_voyage,
            "convention_flag_status": convention_flag_status,
            "navigation_area": navigation_area,
            "exemption_status": exemption_status,
            "vessel_category": vessel_category,
            "ship_condition": ship_condition,
            "length_m": float(length_m),
            "gross_tonnage": float(gross_tonnage),
            "assessment_notes": assessment_notes.strip(),
            "result": result,
        }

        project["applicability_assessment"] = assessment
        project["assessment_status"] = result["status"]
        project["updated_at"] = datetime.now().isoformat(timespec="seconds")
        st.session_state.project_data = project
        st.session_state.project_saved = True
        st.success("Applicability assessment saved in the current project.")

    saved_assessment = st.session_state.project_data.get(
        "applicability_assessment"
    )

    if saved_assessment:
        st.write("")
        render_applicability_result(saved_assessment["result"])

        st.write("")
        filename = (
            clean_filename(project.get("project_name", "project"))
            + PROJECT_FILE_EXTENSION
        )

        st.download_button(
            "⬇️ Download updated project (.nlls)",
            data=project_to_json(st.session_state.project_data),
            file_name=filename,
            mime="application/json",
            use_container_width=True,
        )

        if saved_assessment["result"]["status"] == "Convention Applies":
            if st.button(
                "Continue to Principal Dimensions →",
                use_container_width=True,
            ):
                st.info(
                    "The Principal Dimensions module will be incorporated "
                    "in Version 0.4."
                )

    with st.expander("Regulatory scope used by this module"):
        st.markdown(
            """
            - **Article IV:** scope of application, including ships engaged
              on international voyages.
            - **Article V:** automatic exceptions for warships, certain small
              new or existing ships, non-commercial pleasure yachts, fishing
              vessels and ships navigating exclusively in specified areas.
            - **Article VI:** exemptions that require a determination by the
              Administration and, where applicable, the Governments concerned.
            """
        )
        st.caption(
            "The module does not issue a statutory certificate or approve an "
            "exemption. It records a preliminary engineering decision."
        )

    footer()


def main() -> None:
    initialize_state()
    apply_styles()

    pages = {
        "home": render_home,
        "new_project": render_new_project,
        "open_project": render_open_project,
        "applicability": render_applicability,
        "convention": lambda: render_placeholder(
            "Load Line Convention",
            (
                "Regulatory reference, indexed rules and technical "
                "guidance will be incorporated in a later version."
            ),
        ),
        "settings": lambda: render_placeholder(
            "Settings",
            (
                "Application preferences, default units and report "
                "configuration will be incorporated in a later version."
            ),
        ),
    }

    page_function = pages.get(st.session_state.page, render_home)
    page_function()


if __name__ == "__main__":
    main()
