import streamlit as st
import requests

# --- Dummy credentials for login (you can replace with database check)
CREDENTIALS = {
    "aizh": "1234",
    "alice": "abcd"
}

# --- Your n8n webhook URL (replace this with your actual URL)
N8N_WEBHOOK_URL = "https://aizh.app.n8n.cloud/webhook-test/5e33cc6f-4f0c-449a-a857-e6b85e8367e8"

# --- Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- Login screen
def login_screen():
    st.title("Employee Portal - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username in CREDENTIALS and CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# --- Action item form
def action_item_form():
    st.title("Submit Meeting Action Item")
    st.write(f"Logged in as: **{st.session_state.username}**")
    st.button("Logout", on_click=logout)

    with st.form("action_form"):
        meeting_title = st.text_input("Meeting Title")
        action_item = st.text_area("Action Item")
        assigned_to = st.text_input("Assigned To")
        email = st.text_input("Email")  # <-- Added email field here
        due_date = st.date_input("Due Date")

        submit = st.form_submit_button("Submit")

        if submit:
            payload = {
                "submitted_by": st.session_state.username,
                "meeting_title": meeting_title,
                "action_item": action_item,
                "assigned_to": assigned_to,
                "email": email,  # <-- Added email to payload
                "due_date": due_date.isoformat()
            }

            try:
                response = requests.post(N8N_WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    st.success("Action item submitted successfully!")
                else:
                    st.error(f"Submission failed with status code {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- Main app logic
if st.session_state.logged_in:
    action_item_form()
else:
    login_screen()
