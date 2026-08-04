"""
style.py — shared CSS for the Nova Learn Streamlit app.

The original site's css/js/images folders were not included in the upload,
so this recreates a clean, modern edtech look natively for Streamlit
rather than porting nonexistent files.
"""

import streamlit as st

NOVA_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

:root {
    --nova-primary: #6C5CE7;
    --nova-primary-dark: #4834d4;
    --nova-accent: #00cec9;
    --nova-bg-soft: #f5f4ff;
}

/* Hero banner */
.nova-hero {
    background: linear-gradient(135deg, var(--nova-primary) 0%, var(--nova-primary-dark) 100%);
    color: white;
    padding: 3rem 2.5rem;
    border-radius: 20px;
    margin-bottom: 2rem;
}
.nova-hero h1 {
    color: white;
    font-size: 2.3rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
}
.nova-hero p {
    color: #e8e6ff;
    font-size: 1.05rem;
    max-width: 700px;
}

/* Generic content card */
.nova-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 2px 12px rgba(108, 92, 231, 0.10);
    border: 1px solid #eee6ff;
    height: 100%;
    margin-bottom: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
}
.nova-card:hover,
.nova-card:focus-within {
    transform: translateY(-6px);
    box-shadow: 0 12px 28px rgba(108, 92, 231, 0.25);
    border-color: var(--nova-primary);
}
.nova-card:active {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(108, 92, 231, 0.30);
}
.nova-card h3 {
    color: var(--nova-primary-dark) !important;
    margin-top: 0;
}
.nova-card p,
.nova-card li,
.nova-card ul,
.nova-card ol {
    color: #333333 !important;
}

/* Stat boxes */
.nova-stat {
    text-align: center;
    background: var(--nova-bg-soft);
    border-radius: 14px;
    padding: 1.2rem 0.5rem;
    margin-bottom: 1rem;
}
.nova-stat h2 {
    color: var(--nova-primary) !important;
    font-size: 1.9rem;
    margin-bottom: 0.2rem;
}
.nova-stat p {
    color: #555555 !important;
    margin: 0;
}

/* Pricing card */
.nova-plan {
    background: white;
    border-radius: 18px;
    padding: 1.6rem;
    text-align: center;
    border: 2px solid #eee6ff;
    height: 100%;
}
.nova-plan.popular {
    border-color: var(--nova-primary);
    box-shadow: 0 4px 20px rgba(108, 92, 231, 0.25);
}
.nova-plan .tag {
    background: var(--nova-primary);
    color: white !important;
    font-size: 0.75rem;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 0.5rem;
}
.nova-plan h1 {
    color: var(--nova-primary-dark) !important;
    font-size: 2rem;
    margin: 0.3rem 0;
}
.nova-plan h3 {
    color: #1a1a1a !important;
}
.nova-plan ul,
.nova-plan li {
    color: #333333 !important;
}

/* Section title */
.nova-section-title h2 {
    font-weight: 700;
    margin-bottom: 0.2rem;
    color: var(--nova-primary-dark) !important;
}
.nova-section-title p {
    color: #666666 !important;
}

/* Buttons: recolor Streamlit's default button to match brand */
div.stButton > button {
    background: var(--nova-primary);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
}
div.stButton > button:hover {
    background: var(--nova-primary-dark);
    color: white;
}

/* Sidebar branding */
[data-testid="stSidebarNav"] ul {
    padding-top: 0.5rem;
}
</style>
"""


def inject_css():
    st.markdown(NOVA_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="nova-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="nova-section-title">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card(title: str, body: str):
    st.markdown(
        f"""
        <div class="nova-card">
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat(number: str, label: str):
    st.markdown(
        f"""
        <div class="nova-stat">
            <h2>{number}</h2>
            <p>{label}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
