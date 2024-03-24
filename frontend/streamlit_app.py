import streamlit as st
from anthropic import Anthropic

# Hardcoded user credentials (use environment variables or a more secure method in production)
USER_ID = "admin"
PASSWORD = "password"

def login_page():
    st.title("Login Page")
    user_id = st.text_input("User ID", value="", max_chars=50)
    password = st.text_input("Password", value="", type="password", max_chars=50)

    if st.button("Login"):
        if user_id == USER_ID and password == PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect User ID or Password")


import streamlit as st
import requests

# Flask server URL
FLASK_SERVER_URL = "http://127.0.0.1:5001/chat"                   
# Update with your Flask server URL

def chat_interface():
    st.title("Thinkwell-AI")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.container():
            st.write(message["role"] + ": " + message["content"])

    prompt = st.text_input("Enter your message:")
    if st.button("Send"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = send_to_flask_server(prompt)
        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})

def send_to_flask_server(message):
    try:
        # Send user input to Flask server
        response = requests.post(FLASK_SERVER_URL, json={"prompt": message})
        if response.status_code == 200:
           print("Recieved") 
           return response.json()  # Assuming Flask server sends back a JSON response with key "response"
        else:
            return "Error: Unable to connect to Flask server."
    except Exception as e:
        return f"Error: {str(e)}"

     
def logout_button():
    with st.sidebar:
        if st.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def main():
    # Setup page configuration
    st.set_page_config(
        page_title="Thinkwell-AI",
        page_icon=":brain:",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://www.mentalhealth.gov/",
            "About": "This is a mental health support chat application.",
        },
    )

    # Custom background color and font color
    st.markdown(
        """
        <style>
        .stApp { background-color: #98FF98; } /* Mint green background */
        /* Font color for different elements */
        .st-af { color: #333333; } /* Primary text color */
        .st-ag { color: #333333; } /* Secondary text color, adjust as needed */
        /* You might need to inspect the page and target specific elements based on their class for more precision */
        h1, h2, h3, h4, h5, h6, p, .stTextInput>div>div>input { color: #333333; } /* Headers & text input */
        .stButton>button { color: #333333; } /* Button text */
        </style>
        """,
        unsafe_allow_html=True,
    )

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        chat_interface()
        logout_button()  # Moved the logout to the sidebar for logical placement
    else:
        login_page()


if __name__ == "__main__":
    main()
