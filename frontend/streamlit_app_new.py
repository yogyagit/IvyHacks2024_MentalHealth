import streamlit as st
from anthropic import Anthropic  # Added missing import statement
import requests

# Use environment variables for sensitive data
import os
# USER_ID = os.getenv("USER_ID")
# PASSWORD = os.getenv("PASSWORD")

USER_ID = "admin"
PASSWORD = "password" 

def login_page():
    """Display a login page with input fields and button."""
    st.title("Login Page")
    user_id = st.text_input("User ID", value="", max_chars=50)
    password = st.text_input("Password", value="", type="password", max_chars=50)

    if st.button("Login"):
        if user_id == USER_ID and password == PASSWORD:
            st.session_state.authenticated = True
            st.session_state.session_id += 1
            st.rerun()
        else:
            st.error("Invalid credentials")

# Flask server URL should be configurable and not hardcoded
FLASK_SERVER_URL = os.getenv("FLASK_SERVER_URL", "http://127.0.0.1:5001")

def send_data_to_backend(endpoint, data):
    """Send data to the specified backend endpoint and handle errors."""
    response = requests.post(f"{FLASK_SERVER_URL}/{endpoint}", json=data)
    if response.status_code != 200:
        st.error(f"Error: Failed to reach backend. Status code: {response.status_code}")
        return None
    return response.json()["response"]

def send_input_to_backend_initial(user_prompt, transcript):
    data = {"user_prompt": user_prompt, "transcript": transcript}
    return send_data_to_backend("process_input_initial", data)

def send_input_to_backend_followup(user_prompt, transcript, session_id):
    data = {"user_prompt": user_prompt, "transcript": transcript, "session_id": session_id}
    return send_data_to_backend("process_input_followup", data)

def end_session(transcript):
    data = {"transcript": transcript}
    send_data_to_backend("end_session", data)

def chat_interface():
    """Main chat interface function."""
    st.title("Let's Talk!")
    
    messages = st.session_state.get("messages", [])
    
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if not messages:
        initial_response = send_input_to_backend_initial("", "")
        messages.append({"role": "assistant", "content": initial_response})
    
    prompt = st.chat_input("Your response:")
    
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        
        messages = list(map(lambda x: {"role": "user", "content": x}, messages))
        response = send_input_to_backend_followup(prompt, messages, st.session_state.session_id)
        
        with st.chat_message("assistant"):
            st.markdown(response)
        
        messages += [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response},
        ]

        if "Goodbye" in response:
            end_session(messages)

def logout():
    """Logout function to clear session state."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def configure_app():
    """Configure the Streamlit app."""
    st.set_page_config(
        page_title="Thinkwell-AI",
        page_icon=":brain:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .stApp { background-color: #98FF98; }
        .st-af { color: #333333; }
        .st-ag { color: #333333; }
        h1, h2, h3, h4, h5, h6, p, .stTextInput>div>div>input { color: #333333; }
        .stButton>button { color: #333333; }
        </style>
        """,
        unsafe_allow_html=True,
    )
def logout_button():
    with st.sidebar:
        if st.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def main():
    configure_app()

    # if not st.session_state.authenticated:
    #     login_page()
    # else:
    #     chat_interface()
    #     # Moved the logout function to a separate button for better UI
    #     st.sidebar.button("Logout", logout)

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if "session_id" not in st.session_state:
        st.session_state["session_id"] = 0
    
    if st.session_state["authenticated"]:
        chat_interface()
        logout_button()  # Moved the logout to the sidebar for logical placement
    else:
        login_page()

if __name__ == "__main__":
    main()
