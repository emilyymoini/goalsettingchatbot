from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": "You are a goal-setting coach focused on helping users set and achieve ambitious goals. Your approach includes:\n1. Helping users set clear, measurable goals\n2. Encouraging users to think bigger and be more ambitious\n3. Providing constructive feedback on goal alignment\n4. Maintaining a supportive and motivating tone"
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Error: {str(e)}"
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
