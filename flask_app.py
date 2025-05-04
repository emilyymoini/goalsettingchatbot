import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import anthropic

load_dotenv()

# Initialize Anthropic client
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"response": "Please enter a message."})
    try:
        response = anthropic_client.completions.create(
    model="claude-2",
    max_tokens_to_sample=1000,
    temperature=0.7,
    prompt=f"""System: You are a goal-setting coach focused on helping users set and achieve ambitious goals.\\nYour approach includes:\\n1. Helping users set clear, measurable goals\\n2. Encouraging users to think bigger and be more ambitious\\n3. Providing constructive feedback on goal alignment\\n4. Maintaining a supportive and motivating tone\\n\\nHuman: {user_message}\\n\\nAssistant:"""
)
        reply = response.completion
    except Exception as e:
        reply = f"Error: {str(e)}"
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
