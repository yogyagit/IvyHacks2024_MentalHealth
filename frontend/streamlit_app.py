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
            st.session_state["session_id"] += 1
            st.rerun()
        else:
            st.error("Incorrect User ID or Password")


import streamlit as st
import requests

FLASK_SERVER_URL = "http://127.0.0.1:5001"  # Update with your Flask server URL

def send_input_to_backend_initial(user_prompt, transcript):
    data = {"user_prompt": user_prompt, "transcript": transcript}
    
    # Send data to the process_input endpoint
    response = requests.post(f"{FLASK_SERVER_URL}/process_input_initial", json=data)
    
    if response.status_code != 200:
        return f"Error: Failed to communicate with the backend. Status code: {response.status_code}"
    
    return response.json()["response"]

def send_input_to_backend_followup(user_prompt, transcript, session_id):
    data = {"user_prompt": user_prompt, "transcript": transcript, "session_id" : session_id}
    
    # Send data to the process_input endpoint
    response = requests.post(f"{FLASK_SERVER_URL}/process_input_followup", json=data)
    
    if response.status_code != 200:
        return f"Error: Failed to communicate with the backend. Status code: {response.status_code}"
    
    return response.json()["response"]

def end_session(transcript):
    data = {"transcript": transcript}
    print(data)
    # Send data to the end_session endpoint
    response = requests.post(f"{FLASK_SERVER_URL}/end_session", json=data)
    
    if response.status_code != 200:
        return f"Error: Failed to communicate with the backend. Status code: {response.status_code}"
    
    return response.json()["response"]

def chat_interface():
    st.title("Let's Talk!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if st.session_state.messages == []:
        with st.chat_message("assistant"):
            response = send_input_to_backend_initial("", "")
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    if prompt := st.chat_input("Please type in your response here"):
        with st.chat_message("user"):
            st.markdown(prompt)

        print(list_of_dicts_to_string(st.session_state.messages))
        response = send_input_to_backend_followup(prompt, list_of_dicts_to_string(st.session_state.messages), st.session_state["session_id"])

        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Check if the conversation has ended
        if "Goodbye" in response:
            end_response = end_session(list_of_dicts_to_string(st.session_state.messages))
            st.markdown(end_response)

def list_of_dicts_to_string(lst):
    return str(lst)

     
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

    if "session_id" not in st.session_state:
        st.session_state["session_id"] = 0
    
    if st.session_state["authenticated"]:
        chat_interface()
        logout_button()  # Moved the logout to the sidebar for logical placement
    else:
        login_page()

    #chat_interface()

if __name__ == "__main__":
    main()
