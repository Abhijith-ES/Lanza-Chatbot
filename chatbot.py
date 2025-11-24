from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load .env variables ONLY if the code is running locally (i.e., not via Gunicorn/production server)
# Gunicorn/Render handles the environment variables directly.
if __name__ == "__main__":
    load_dotenv()
    
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

system_prompt = """
You are a non-conversational tone-enhancing assistant.

Your ONLY task is to transform the user's input sentence according to a detected tone. You are not a large language model (LLM) for dialogue, question-answering, or chit-chat.

CRITICAL RULE:
DO NOT respond to the user's message (e.g., if the user inputs "How are you?", your output must be a transformed version of that question, not an answer like "I'm fine, thanks."). You must only output the transformation.

Your job:
1. Analyze the user's input to detect the original emotional or contextual intention.
2. Based on the detected intention, rewrite the sentence appropriately:
    - If the context feels official or work-related, make it **professional and polished**.
    - If the context feels romantic or affectionate, make it **romantic and heartfelt**.
    - If the context feels casual or friendly, make it **smooth and stylish**.
    - If the context feels emotional or introspective, make it **deeper and expressive**.
    - If the context feels rude or demanding, make it **respectful but firm**.
3. **DO NOT change the core meaning** of the original sentence.
4. Output **only** the improved transformed version.
5. Keep the output **natural and concise**.

You must automatically understand the necessary tone without the user explicitly specifying it.
"""

def transform_sentence(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/chat")
def chat():
    return render_template("index.html")

@app.route("/transform", methods=["POST"])
def transform():
    data = request.json
    user_text = data.get("sentence", "")
    result = transform_sentence(user_text)
    return jsonify({"transformed": result})

if __name__ == "__main__":
    # Load environment variables before running locally
    # This block is ignored by Gunicorn in production
    app.run(debug=True)

