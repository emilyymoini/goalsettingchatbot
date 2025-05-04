import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a supportive and ambitious goal-setting coach. Help users set, refine, and achieve their goals. Always encourage them to think bigger and provide actionable advice."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Error: {str(e)}"
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
