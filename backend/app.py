from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_output():
    prompt = request.json.get('prompt')
    # Here you will call the function to generate output from LLM
    output = generate_output_with_llm(prompt)
    return jsonify({"output": output})

def generate_output_with_llm(prompt):
    # Placeholder for LLM logic
    return f"Generated output for: {prompt}"

if __name__ == '__main__':
    app.run(debug=True)
