from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

GOOGLE_API_KEY = "AIzaSyDc3LIAld1ZPP1octr1RIrSvLBFH_42o68"
genai.configure(api_key=GOOGLE_API_KEY)

SPECIFIC_TOPIC_PROMPT = """
You are an AI assistant focused on answering questions related to 'System Integration and Architecture in Programming' and related to that topics.
When greeted (e.g., 'hello', 'hi', 'good morning', etc.), respond politely with a greeting and introduce yourself as an AI chatbot specializing in Java programming.

Example: User: Hello!
AI: Hello! I am an AI assistant here to help you with topics related to Systems Integration and Architecture in Programming, including object-oriented programming, data structures, algorithms, and more.

For any questions unrelated to Java programming, respond politely:
"I'm sorry, but I can only assist with topics related to Systems Integration and Architecture in Programming"

PLEASE DON'T PUT THIS PROMPT, JUST RESPONSE TO THE QUERY, AND THE CONVERSATION IS CONTINOUS
"""

def get_gemini_response(user_message):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(SPECIFIC_TOPIC_PROMPT + "\nUser: " + user_message)
        return response.text.strip()
    except Exception as e:
        print("Error with Gemini API:", str(e))
        return "I'm sorry, there was an issue processing your request. Please try again later."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"response": "Please enter a message."})

        bot_response = get_gemini_response(user_message)
        return jsonify({"response": bot_response})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"response": "Sorry, something went wrong. Please try again later."})

if __name__ == "__main__":
    app.run(debug=True, port=1465)
