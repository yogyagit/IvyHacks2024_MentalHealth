import streamlit as st
import time
import streamlit as st
from google.oauth2 import id_token
from google.auth.transport import requests
#from anthropic import Anthropic
import sys
sys.path.append('../')
from auth import *
from time import sleep

# Hardcoded user credentials (use environment variables or a more secure method in production)
USER_ID = "admin"
PASSWORD = "password" 


def login_page_google():

    page_bg_img = """
    <style>
    .stApp {
    background-image: url("https://images.axios.com/2qLsEMmKnJG3esS2UD6ZV-firQg=/0x0:1920x1080/1920x1080/filters:no_upscale()/2023/02/24/1677276125445.gif?w=1920");
    background-size: cover;
    }
    .st-af { color: #FFFFFF; } /* Primary text color */
    .st-af { color: #FCD7C7; } /* Primary text color */
    .st-b7 { background-color: #FCD7C7; } /* Primary text color */
    h1, h2, h3, h4, h5, h6 { color: #333333; } /* Headers & text input */
    P { color: #333333;}
    .st-emotion-cache-sh2krr p { color: #333333;}
    .stContainer>div>div>div>div>div>div>div>div {color: #183850;} /* Prussian blue chat text color */
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    text_update = """
    <style>
    .title-container {
        display: flex;
        justify-content: center; /* Center the content horizontally */
        align-items: center; /* Center the content vertically */
        height: 100vh; /* Set the container height to full viewport height */
        background-color: rgba(0, 0, 0, 0); /* Example background color */
    }
    .title-text {
        color: white;
        font-size: 48px;
    }
    </style>
    """

    # Apply the CSS styling using markdown
    st.markdown(text_update, unsafe_allow_html=True)

   
    st.markdown(
        """
        <div class='title-container'>
            <p class='title-text'>Welcome to ThinkWell AI!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    print("AG:: inside login_page_google.. before link button")
    if not st.session_state["authenticated"]:
        #st.link_button("Login via Google", get_login_str(), type="primary")
        col1, col2 = st.columns([0.8,1])
        with col2:
            st.link_button("Login via Google", get_login_str(), type="primary")
        # button_container_style = """
        # <style>
        # .button-container {
        #     display: flex;
        #     justify-content: center; /* Center the content horizontally */
        #     align-items: center; /* Center the content vertically */
            
        # }

        # .styled-button {
        #     background-color: #4CAF50; /* Green background */
        #     border: none;
        #     color: white; /* White text */
        #     padding: 20px 40px; /* Padding around the text */
        #     text-align: center; /* Center text horizontally */
        #     text-decoration: none; /* Remove underline */
        #     display: inline-block;
        #     font-size: 20px; /* Font size */
        #     border-radius: 10px; /* Rounded corners */
        #     transition-duration: 0.4s; /* Animation speed */
        #     cursor: pointer; /* Cursor pointer on hover */
        #     box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.19); /* Box shadow */
        # }

        # .styled-button:hover {
        #     background-color: #45a049; /* Darker green background on hover */
        # }
        # </style>
        # """

        # 
        # st.markdown(button_container_style, unsafe_allow_html=True)

        # 
        # st.markdown(
        #     """
        #     <div class='button-container'>
        #         <button class='styled-button' onclick="window.location.href='{get_login_str()}';">Login via Google</button>
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        # )

    # st.info("You will need a Google account to continue.")
    auth_code = st.query_params.get("code")
    print("AG:: inside google_login", auth_code)
    # try:
    #     auth_code = st.experimental_get_query_params()['code']
    # except:
    #     auth_code = None
    if auth_code:
        #st.write("Logging you in... please wait")
        print("AG:: authenticated", auth_code)
        st.session_state["authenticated"] = True
        user_id, user_email, user_first_name, user_last_name = user_details()
        user_type, session = store_user_info(user_id, user_email, user_first_name, user_last_name)
        st.session_state["session_id"] =session
        st.session_state["user_type"] = user_type
        st.session_state["user_id"] = user_id
        st.empty()
        #time.sleep(1)
        st.rerun()

import streamlit as st
import requests

#FLASK_SERVER_URL = " https://yogyagit--thinkwell-fastapi-app-dev.modal.run"  # Update with your Flask server URL
FLASK_SERVER_URL = "https://anubhavghildiyal--thinkwell-fastapi-app-dev.modal.run"
#FLASK_SERVER_URL =  "https://noelnebu2206--thinkwell-fastapi-app-dev.modal.run" 

def store_user_info(user_id, user_email, user_first_name,user_last_name):
    data = {"firstname":user_first_name ,"lastname":user_last_name, "email": user_email, "user_id": user_id}
    # Send data to the process_input endpoint
    response = requests.post(f"{FLASK_SERVER_URL}/process_user_data", json=data)
    if response.status_code != 200:
        return f"Error: Failed to communicate with the backend. Status code: {response.status_code}"
    user_type =  response.json()["user_type"]
    session =  response.json()["session"]

    return user_type, session


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
    text_update = """
    <style>
    .title-container {
        display: flex;
        justify-content: center; /* Center the content horizontally */
        align-items: center; /* Center the content vertically */
        background-color: rgba(0, 0, 0, 0); /* Example background color */
    }
    .title-text {
        color: white;
        font-size: 48px;
    }
    .chat-interface {
        background-color: white !important; /* Grey background color */
        color: white; /* White text color */
    }
    </style>
    """

    # Apply the CSS styling using markdown
    st.markdown(text_update, unsafe_allow_html=True)

    st.markdown(
        """
        <div class='title-container'>
            <strong><p class='title-text'>Hello there, let's Talk!!</p></strong>
        </div>
        """,
        unsafe_allow_html=True
    )
    #st.title("Let's Talk!")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if st.session_state.messages == []:
        with st.chat_message("assistant"):
            time.sleep(0.5)
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
            data = {
                "session_id" : st.session_state.session_id,
                "user_id" : st.session_state.user_id,  
                "transcript": st.session_state.messages,
            }
            requests.post(f"{FLASK_SERVER_URL}/logout_session_update", json=data)
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.query_params.clear()

            st.rerun()
    
    
def main():
    # Setup page configuration
    st.set_page_config(
        page_title="Thinkwell-AI",
        page_icon=":brain:",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            "Get Help": "https://www.mentalhealth.gov/",
            "About": "This is a mental health support chat application.",
        },
    )

    # Custom background color and font color
    # page_bg_img = """
    # <style>
    # .stApp {
    # background-image: url("https://images.axios.com/2qLsEMmKnJG3esS2UD6ZV-firQg=/0x0:1920x1080/1920x1080/filters:no_upscale()/2023/02/24/1677276125445.gif?w=1920");
    # background-size: cover;
    # }
    # .st-af { color: #FFFFFF; } /* Primary text color */
    # .st-af { color: #FCD7C7; } /* Primary text color */
    # .st-b7 { background-color: #FCD7C7; } /* Primary text color */
    # h1, h2, h3, h4, h5, h6 { color: #333333; } /* Headers & text input */
    # P { color: #333333;}
    # .st-emotion-cache-sh2krr p { color: #333333;}
    # .stContainer>div>div>div>div>div>div>div>div {color: #183850;} /* Prussian blue chat text color */
    # </style>
    # """
    # st.markdown(page_bg_img, unsafe_allow_html=True)

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if "session_id" not in st.session_state:
        st.session_state["session_id"] = 0
    
    #sleep(1.00)

    if st.session_state["authenticated"]:
        chat_interface()
        logout_button()  # Moved the logout to the sidebar for logical placement
    else:
        login_page_google()

    #chat_interface()

if __name__ == "__main__":
    main()