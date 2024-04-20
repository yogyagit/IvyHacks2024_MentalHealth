from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from modal_image import image, stub, volume
from modal import asgi_app, Image, Stub, method, enter, Secret
from atlas import AtlasClient
from rag import RagChain
from chatbot import CohereChatbot
from therapy import TherapyContext


web_app = FastAPI()
mongoDbClient =  AtlasClient()  

llm = CohereChatbot()
print('Noel: llm chatbot init done')
rag_chain = RagChain()
print('Noel: llm init done')
therapy_context = TherapyContext()
print('Noel: context init done')

@web_app.post("/process_user_data")
async def process_user_data(request: Request):
    data = await request.json()

    firstname = data.get("firstname")
    lastname = data.get("lastname")
    email = data.get("email")
    user_id = data.get("user_id")
    session_id = mongoDbClient.insert_user_data.remote(database_name = 'ThinkWell_AI', collection_name = 'user_data',user_id = user_id, firstname = firstname, lastname = lastname, email_id = email)
    if session_id > 1:
        return {"user_type": "Returing User", "session": session_id}
    else:
        return {"user_type": "New User", "session": 1}

@web_app.post("/process_input_initial")
async def process_input_route_initial(request: Request):
    intro_message = """
    Hello, I'm Thinkwell, your AI therapist dedicated to assisting you through Cognitive Behavioral Therapy (CBT). CBT is a form of psychotherapy that helps you manage your problems by changing the way you think and behave. It's typically used to treat anxiety, depression, and other conditions by learning practical self-help strategies.

    Today, I'm here to help you explore your thoughts, identify patterns, and provide support as you learn more about CBT and how it can be applied to improve your daily life. To get started, could you please introduce yourself and share why you have decided to seek therapy? What specific issues would you like to address or what goals are you aiming to achieve through our sessions together?

    Remember, this conversation is a safe space, and everything you share will be kept confidential. Let's start this journey together towards a better understanding of your thoughts and feelings.
    """
    return {"response": intro_message}

@web_app.post("/process_input_followup")
async def process_input_route_followup(request: Request):
    data = await request.json()
    user_prompt = data["user_prompt"]
    #chat_history = data.get("chat_history", [])
    chat_history = data.get("transcript", [])
    #print("AG: transcript", chat_history)
    #print("AG: transcript", type(chat_history))
    
    for message in chat_history:
        if message["role"] == "assistant":
            message["role"] = "CHATBOT"
        if message["role"] == "user":
            message["role"] = "USER"
        try:
            message["message"] = message.pop("content")
        except KeyError:
            # Handle the case where "content" key does not exist
            print("Exception: 'content' key does not exist in message")
    
    print("AG: message", type(message))
    session_id = data["session_id"]
    print(type)
    # Continuing a session
    if session_id >= 1: # YS For testing purposes. Original : session_id == 1 (04/17: 6:55 PM)
        print("Fetching context and generating response using RagChain and CohereChatbot.")
        # Custom prompt that instructs the llm what to do with the fetched context
        custom_prompt = therapy_context.get_prompt.remote()
        # Use RagChain to fetch context and generate response with the custom prompt
        #print(f"chat_history: {chat_history}")
        #print(f"user_prompt: {user_prompt}")
        #print(f"session_id: {session_id}")
        #llm = CohereChatbot.remote()
        #llm1 = CohereChatbot()
        #rag_chain2 = RagChain.remote()
        #response = rag_chain2.invoke.remote(question=user_prompt, prompt=custom_prompt, llm=llm1, chat_history=chat_history)
        #full_prompt = rag_chain.invoke.remote(question=user_prompt, prompt=custom_prompt)
        #full_prompt = custom_prompt
        full_prompt = custom_prompt.format(question=user_prompt)
        print("full_prompt is",full_prompt)
        print("\n")
        print("chat_history is",chat_history)
        response = llm.chat.remote(message=full_prompt, chat_history=chat_history)
        
        print("Response received from RagChain and CohereChatbot.")
        return {"response": response}
        
    else:
        return {"response": "Session ID not supported or invalid."}
    """
    else:
        response = continue_followup_session(
        user_prompt, transcript, session_results, previous_transcripts
        )
    
    # Send the response back to the frontend
    """

# Define the continue_session_1 function and any other required functions

@web_app.post("/end_session")
async def end_session_route(request: Request):
    data = await request.json()
    transcript = data.get("transcript", [])
    session_id = data.get("session_id")
    user_id = data.get("user_id")

    # Check if transcript and session ID are provided
    if not transcript or session_id is None:
        return {"response": "Missing necessary data (transcript or session ID)."}

    # Use the custom prompt to instruct the LLM to summarize the session and plan next steps
    if session_id == 1:
        custom_prompt = (
            "As an AI therapist named Thinkwell, you have been conducting a session using Cognitive Behavioral Therapy (CBT). "
            "Based on the attached transcript, summarize the key points discussed during the session and suggest a plan for the next sessions. "
            "Ensure to include techniques that might help the patient and any follow-up actions they should consider. "
            "Transcript: '{}'".format(transcript)
        )
        # Generate the concluding statements using CohereChatbot
        response = await llm.chat.remote(message=custom_prompt, chat_history=transcript)
    else:
        return {"response": "Invalid or unsupported session ID."}

    transcript.append({"role": "assistant", "content": response})

    mongoDbClient.insert_documents.remote(database_name = 'ThinkWell_AI', collection_name = 'user_session_transcripts', session_id = session_id, user_id = user_id, session_transcript = transcript)
    
    return {"response": response}

@web_app.post("/logout_session_update")
async def logout_session_update(request: Request):
    data = await request.json()
    transcript = data.get("transcript", [])
    session_id = data.get("session_id")
    user_id = data.get("user_id")
    mongoDbClient.insert_documents.remote(database_name = 'ThinkWell_AI', collection_name = 'user_session_transcripts', session_id = session_id, user_id = user_id, session_transcript = transcript)

@stub.function(image=image, volumes={"/data": volume}, secrets=[Secret.from_name("thinkwell-key")],)
@asgi_app()
def fastapi_app():
    print('Noel: starting fastapi app...')
    return web_app