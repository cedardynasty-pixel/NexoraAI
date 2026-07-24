"""
app.py — Nexora Streamlit app entry point.

Run with:  streamlit run app.py
"""

import streamlit as st
import db
from auth import is_logged_in, current_user

st.set_page_config(page_title="Nexora | Learn Without Limits", page_icon="🎓", layout="wide")

db.init_db()

# Create a first admin account if none exists yet. Override the defaults via
# Streamlit secrets (Settings -> Secrets) with ADMIN_USERNAME / ADMIN_EMAIL / ADMIN_PASSWORD.
db.seed_default_admin(
    username=st.secrets.get("ADMIN_USERNAME", "admin"),
    email=st.secrets.get("ADMIN_EMAIL", "admin@nexora.local"),
    password=st.secrets.get("ADMIN_PASSWORD", "changeme123"),
)

# ---- Sidebar branding ----
with st.sidebar:
    st.markdown("## 🎓 NEXORA")
    if is_logged_in():
        st.caption(f"Logged in as **{current_user()}**")
    else:
        st.caption("Learn Without Limits")

# ---- Build navigation (Dashboard/AI Tools/Admin shown based on login + role) ----
home_page = st.Page("views/home.py", title="Home", icon="🏠", default=True)
courses_page = st.Page("views/courses.py", title="Courses", icon="📚")
about_page = st.Page("views/about.py", title="About", icon="ℹ️")

explore_pages = [home_page, courses_page, about_page]

if is_logged_in():
    dashboard_page = st.Page("views/dashboard.py", title="Dashboard", icon="📊")
    ai_tools_page = st.Page("views/ai_tools.py", title="AI Study Tools", icon="🤖")
    account_pages = [dashboard_page, ai_tools_page]

    if is_admin():
        admin_page = st.Page("views/admin.py", title="Admin Panel", icon="🛡️")
        account_pages.append(admin_page)
else:
    login_page = st.Page("views/login.py", title="Login", icon="🔑")
    signup_page = st.Page("views/signup.py", title="Sign Up", icon="✍️")
    account_pages = [login_page, signup_page]

pg = st.navigation(
    {
        "Explore": explore_pages,
        "Account": account_pages,
    }
)
pg.run()
