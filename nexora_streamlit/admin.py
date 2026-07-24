import streamlit as st
from style import inject_css, hero, section_title
from auth import is_logged_in, is_admin, current_user
import db
import pdf_utils
 
inject_css()
 
if not is_logged_in() or not is_admin():
    st.warning("This page is for admins only.")
    st.stop()
 
hero("Admin Panel", "Manage student and admin accounts, the book library, and AI settings.")
 
tab_users, tab_books, tab_settings = st.tabs(["👥 Manage Users", "📖 Book Library", "⚙️ Settings"])
 
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
 
# ---------------- BOOK LIBRARY TAB ----------------
with tab_books:
    section_title(
        "Book Library",
        "Upload textbook PDFs so the student AI Study Tools can generate notes, worksheets, "
        "study plans and flashcards grounded in the actual book content.",
    )
 
    with st.form("upload_book_form"):
        book_title = st.text_input("Book title", placeholder="e.g. Grade 9 Science Textbook")
        uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
        upload_submitted = st.form_submit_button("Ingest Book")
 
        if upload_submitted:
            if not book_title.strip():
                st.error("Please give the book a title.")
            elif uploaded_pdf is None:
                st.error("Please choose a PDF file.")
            else:
                with st.spinner("Extracting text from the PDF... this can take a moment for large books."):
                    try:
                        text = pdf_utils.extract_text_from_pdf(uploaded_pdf)
                        if not text.strip():
                            st.error(
                                "No extractable text was found in that PDF — it may be a scanned "
                                "image without OCR, which this tool can't read."
                            )
                        else:
                            db.add_book(book_title.strip(), uploaded_pdf.name, text, current_user())
                            st.success(f"'{book_title.strip()}' ingested successfully ({len(text):,} characters).")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Couldn't process that PDF: {e}")
 
    st.divider()
    section_title("Ingested Books")
    books = db.get_all_books()
    if not books:
        st.info("No books uploaded yet.")
    else:
        for b in books:
            with st.container(border=True):
                cols = st.columns([3, 2, 2, 1])
                cols[0].markdown(f"**{b['title']}**")
                cols[1].markdown(f"{b['content_len']:,} characters")
                cols[2].markdown(f"Uploaded {b['uploaded_at'][:10]} by {b['uploaded_by'] or '—'}")
                if cols[3].button("Delete", key=f"delete_book_{b['id']}"):
                    db.delete_book(b["id"])
                    st.rerun()
 
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
