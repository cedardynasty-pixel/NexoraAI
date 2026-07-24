import streamlit as st
from style import inject_css, hero, section_title
from auth import is_logged_in, is_admin, current_user
import db

inject_css()

if not is_logged_in() or not is_admin():
    st.warning("This page is for admins only.")
    st.stop()

hero("Admin Panel", "Manage student and admin accounts, and configure the AI Study Tools.")

tab_users, tab_settings = st.tabs(["👥 Manage Users", "⚙️ Settings"])

# ---------------- USERS TAB ----------------
with tab_users:
    section_title("All Accounts")
    users = db.get_all_users()
    me = current_user()

    for u in users:
        with st.container(border=True):
            cols = st.columns([2, 2, 1, 1, 1, 1])
            cols[0].markdown(f"**{u['username']}**" + (" 🛡️ admin" if u["is_admin"] else ""))
            cols[1].markdown(u["email"] or "—")
            cols[2].markdown(u["grade"] or "—")
            cols[3].markdown(u["created_at"][:10])

            if u["username"] == me:
                cols[4].markdown("_(you)_")
            else:
                if u["is_admin"]:
                    if cols[4].button("Remove admin", key=f"demote_{u['username']}"):
                        db.set_admin(u["username"], False)
                        st.rerun()
                else:
                    if cols[4].button("Make admin", key=f"promote_{u['username']}"):
                        db.set_admin(u["username"], True)
                        st.rerun()

                if cols[5].button("Delete", key=f"delete_{u['username']}"):
                    db.delete_user(u["username"])
                    st.rerun()

    st.divider()
    section_title("Create a New Admin Account")
    with st.form("create_admin_form"):
        new_username = st.text_input("Username")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Create Admin Account")
        if submitted:
            ok, message = db.create_user(
                new_username.strip(), new_email.strip(), new_password, "Staff", is_admin=True
            )
            if ok:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    st.divider()
    section_title("Reset a Password")
    with st.form("reset_password_form"):
        target_username = st.selectbox("Account", [u["username"] for u in users])
        new_pw = st.text_input("New password", type="password")
        reset_submitted = st.form_submit_button("Reset Password")
        if reset_submitted:
            if len(new_pw) < 6:
                st.error("Password should be at least 6 characters.")
            else:
                db.set_password(target_username, new_pw)
                st.success(f"Password reset for {target_username}.")

# ---------------- SETTINGS TAB ----------------
with tab_settings:
    section_title(
        "Gemini API Key",
        "Powers the student AI Study Tools (notes, worksheets, study plans, flashcards).",
    )
    current_key = db.get_setting("gemini_api_key") or ""
    masked = f"{'•' * max(len(current_key) - 4, 0)}{current_key[-4:]}" if current_key else "Not set"
    st.markdown(f"**Current key:** `{masked}`")

    with st.form("gemini_key_form"):
        new_key = st.text_input(
            "Gemini API key",
            type="password",
            placeholder="Paste your key from aistudio.google.com/apikey",
        )
        key_submitted = st.form_submit_button("Save Key")
        if key_submitted:
            if new_key.strip():
                db.set_setting("gemini_api_key", new_key.strip())
                st.success("Gemini API key saved.")
                st.rerun()
            else:
                st.error("Please paste a key before saving.")

    st.caption(
        "Get a free key at aistudio.google.com/apikey. The key is stored in the app's local "
        "database — on Streamlit Community Cloud this can reset if the app restarts, so you "
        "may need to re-enter it occasionally unless you move storage to a persistent database "
        "(see README)."
    )
