import streamlit as st
import time
import streamlit as st
from google.oauth2 import id_token
from google.auth.transport import requests
#from anthropic import Anthropic
import sys
sys.path.append('../')
from auth import *

# Hardcoded user credentials (use environment variables or a more secure method in production)
USER_ID = "admin"
PASSWORD = "password" 


def login_page_google():
    st.title("Login Page")
    st.link_button("Google Login", get_login_str(), type="primary")
    st.write("button done")
    auth_code = st.query_params.get("code")
    # try:
    #     auth_code = st.experimental_get_query_params()['code']
    # except:
    #     auth_code = None
    if auth_code:
        st.write("Login Done")
        st.session_state["authenticated"] = True
        
        user_id, user_email, user_first_name, user_last_name = user_details()
        st.write("user id: ", user_id)
        type, session = store_user_info(user_id, user_email, user_first_name, user_last_name)
        st.session_state["session_id"] =session
        st.session_state["type"] = type
        st.rerun()

import streamlit as st
import requests


#FLASK_SERVER_URL = " https://yogyagit--thinkwell-fastapi-app-dev.modal.run"  # Update with your Flask server URL
#FLASK_SERVER_URL = "https://anubhavghildiyal--thinkwell-fastapi-app-dev.modal.run"
FLASK_SERVER_URL = " https://noelnebu2206--thinkwell-fastapi-app-dev.modal.run"  # Update with your Flask server URL

def store_user_info(user_id, user_email, user_first_name,user_last_name):
    data = {"firstname":user_first_name ,"lastname":user_last_name, "email": user_email, "user_id": user_id}
    # Send data to the process_input endpoint
    response = requests.post(f"{FLASK_SERVER_URL}/process_user_data", json=data)
    if response.status_code != 200:
        return f"Error: Failed to communicate with the backend. Status code: {response.status_code}"
    type =  response.json()["type"]
    session =  response.json()["type"]

    return type, session


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
    #print(data)
    # Send data to the end_session endpoint
    response = requests.post(f"{FLASK_SERVER_URL}/end_session", json=data)
    
    if response.status_code != 200:
        return f"Error: Failed to communicate with the backend. Status code: {response.status_code}"
    
    return response.json()["response"]

def response_stream(chatbot_output):
    for word in chatbot_output.split():
        yield word + " "
        time.sleep(0.05)
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
            #st.markdown(response)
            st.write_stream(response_stream(response))

            st.session_state.messages.append({"role": "assistant", "content": response})
            
    if prompt := st.chat_input("Please type in your response here"):
        with st.chat_message("user"):
            st.markdown(prompt)

        #print(list_of_dicts_to_string(st.session_state.messages))
        #response = send_input_to_backend_followup(prompt, list_of_dicts_to_string(st.session_state.messages), st.session_state["session_id"])
        response = send_input_to_backend_followup(prompt, st.session_state.messages, st.session_state["session_id"])

        with st.chat_message("assistant"):
            #st.markdown(response)
            st.write_stream(response_stream(response))
        
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

def auth_flow():
    st.write("Welcome to My App!")
    auth_code = st.query_params.get("code")
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "client_secret.json", # replace with you json credentials from your google auth app
        scopes=["https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri=redirect_uri,
    )
    if auth_code:
        flow.fetch_token(code=auth_code)
        credentials = flow.credentials
        st.write("Login Done")
        user_info_service = build(
            serviceName="oauth2",
            version="v2",
            credentials=credentials,
        )
        user_info = user_info_service.userinfo().get().execute()
        assert user_info.get("email"), "Email not found in infos"
        st.session_state["google_auth_code"] = auth_code
        st.session_state["user_info"] = user_info
    else:
        if st.button("Sign in with Google"):
            authorization_url, state = flow.authorization_url(
                access_type="offline",
                include_granted_scopes="true",
            )
            webbrowser.open_new_tab(authorization_url)

    
    
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
        login_page_google()

    #chat_interface()

if __name__ == "__main__":
    main()
