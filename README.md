### ThinkWell AI: Mental Health Support Application

ThinkWell AI is an advanced mental health support application designed to offer therapeutic assistance through Cognitive Behavioral Therapy (CBT) techniques. The application leverages a FastAPI backend integrated with various machine learning models and services to provide real-time, personalized mental health support. Users can interact with the Thinkwell AI chatbot via a friendly web interface powered by Streamlit, which allows for an engaging conversational experience.

#### Features:
- **Personalized Therapy Sessions:** Each user receives therapy sessions tailored to their needs, facilitated by an AI therapist named "Thinkwell."
- **Real-time Interaction:** Utilizing the Cohere Chatbot and RagChain models, the application can process and respond to user inputs dynamically, simulating a natural conversation flow.
- **Session Management:** Users can start, continue, and end sessions, with all interactions securely logged for continuity of care.
- **User Authentication:** Secure Google OAuth for user authentication ensures that only authorized users can access their sessions.
- **Responsive Design:** The application is designed to be responsive and accessible from various devices, ensuring a seamless user experience.

#### Technologies Used:
- **FastAPI:** Used for building the robust API that handles all backend logic, including user data processing and session management.
- **Streamlit:** Provides the frontend interface for user interaction with the AI chatbot.
- **MongoDB Atlas:** Utilized for secure storage of user sessions and transcripts, ensuring data persistence and security.
- **Cohere Chatbot:** Powers the AI-driven responses, offering a conversational model that handles user queries in real-time.
- **RagChain:** Integrates multiple data sources for comprehensive context management during user interactions.
- **Modal:** Used to serverlesly host the FastAPI server. 

#### How to Run the Application:
1. **Setup Environment:**
   - Ensure Python 3.8 or newer is installed.
   - Install required packages from the provided `requirements.txt` file using the command:
     pip install -r requirements.txt
2. **API Keys and Authentication:**
   - Set up Google OAuth credentials and MongoDB Atlas for database management.
   - Ensure all secret keys and API endpoints are configured correctly in the application settings.

3. **Starting the Server:**
   - Run the FastAPI server with the command:
     ```bash
     modal serve modal_back.py
     ```
   - Open another terminal and start the Streamlit frontend:
     ```bash
     streamlit run streamlit_app.py
     ````

4. **Using the Application:**
   - Navigate to the specified localhost address in a web browser to interact with the ThinkWell AI chatbot.
   - Log in using a Google account to start a session.

#### Security and Privacy:
- All user data is handled with strict confidentiality. Authentication is managed through secure protocols, and user transcripts are stored securely in MongoDB Atlas with restricted access.
