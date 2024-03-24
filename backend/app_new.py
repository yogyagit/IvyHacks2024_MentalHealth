from flask import Flask, request, jsonify
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

def read_text_files(folder_path):
    text = ''
    for filename in os.listdir(folder_path):
        if filename.endswith('.rtf'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                text += file.read()
    return text

def generate_response_from_input(user_input):
    # Path to the folder containing RTF files
    folder_path = "data"

    # Read RTF files in the folder and append their contents to a string
    folder_text = read_text_files(folder_path)

    chat = ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229")

    system = "Follow instructions given and be a helpful therapist {CBT_docs}."
    human = user_input
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    response = prompt | chat
    
    return response

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = generate_response_from_input(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
