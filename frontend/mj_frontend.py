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

# def login_page():
#     st.title("Login Page")
#     user_id = st.text_input("User ID", value="", max_chars=50)
#     password = st.text_input("Password", value="", type="password", max_chars=50)

#     if st.button("Login"):
#         if user_id == USER_ID and password == PASSWORD:
#             st.session_state["authenticated"] = True
#             st.session_state["session_id"] += 1
#             st.rerun()
#         else:
#             st.error("Incorrect User ID or Password")


def login_page_google():
    st.title("Welcome to ThinkWell!")
    #st.write(get_login_str(), unsafe_allow_html=True)
    # st.write(f'''<h1>
    # Please login using<a target="_self"
    # href="{get_login_str()}">here</a></h1>''',
    #      unsafe_allow_html=True)
    st.link_button("Login via google", get_login_str(), type="primary")
    st.info("You need your google ID to continue.")
    #st.markdown(custom_css,unsafe_allow_html=True)
    auth_code = st.query_params.get("code")
    if auth_code:
        st.write("Login Done")
        st.session_state["authenticated"] = True
        st.session_state["session_id"] += 1
        st.rerun()

import streamlit as st
import requests

FLASK_SERVER_URL = " https://noelnebu2206--thinkwell-fastapi-app-dev.modal.run"  # Update with your Flask server URL

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
            # #st.rerun()
            st.query_params = {"logged_out": True}
            # st.session_state.clear()
            # st.write("Thank you for using ThinkWell! I hope I was able to help.")
            # if st.button("Login again"):
            #     st.session_state["authenticated"] = False
            # st.write("Thank you for using ThinkWell! I hope I was able to help.")
            # st.session_state.clear()
            # st.query_params = {"logged_out": True}
            

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
    # Custom CSS styling
    # background_gif_url="test.jpeg"
    # custom_css = f"""
    # <style>
    # body {{
    #     background-image: url('{background_gif_url}');
    #     background-size: cover;
    #     background-position: center;
    #     background-attachment: fixed;
    # }}
    # </style>
    # """

   
    
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
    st.markdown(
        """
        <style>
        body {{
            background-image: url('{background_gif_url}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
         </style>
        """,
        unsafe_allow_html=True,
    )
    # Apply custom CSS
    # st.markdown(custom_css, unsafe_allow_html=True)
    # import streamlit as st

    # css = """
    # <style>
    # body {
    #     background-color: lightblue;
    # }
    # </style>
    # """

    # st.markdown(css, unsafe_allow_html=True)


    # Check if user is authenticated
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if "session_id" not in st.session_state:
        st.session_state["session_id"] = 0
    
    if st.session_state["authenticated"]:
        chat_interface()
        logout_button() 
    else:
        login_page_google()

    # if st.query_params.get('logged_out'):
    #     st.session_state.clear()
    #     st.write("Thank you for using ThinkWell! I hope I was able to help.")
    #     if st.button("Login again"):
    #         st.session_state["authenticated"] = False
    #         st.session_state.clear()
    # else:
    #     if st.button("Logout"):
    #         st.experimental_set_query_params(logged_out=True)

if __name__ == "__main__":
    main()