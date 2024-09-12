from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message from the POST request
    user_message = request.json.get("message")

    # Define a strong system message to restrict the AI to cultural and heritage topics
    system_message = {
        "role": "system",
        "content": "You are an expert in global cultural and heritage topics. You provide information exclusively about the traditions, customs, history, architecture, arts, languages, and cultural practices of different societies and civilizations. You are not allowed to answer questions outside this domain. If a user asks about anything unrelated to culture or heritage, politely inform them that you can only provide information about cultural and heritage topics and invite them to ask a relevant question."
    }

    try:
        # Send the system message and user message to OpenAI's API and receive the response
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                system_message,
                {"role": "user", "content": user_message}
            ]
        )

        # Extract the message from the response
        response_message = completion.choices[0].message["content"]

        # Return the response message as JSON
        return jsonify({"response": response_message})

    except openai.OpenAIError as e:
        # Handle OpenAI-specific errors
        return jsonify({"error": f"OpenAI error: {str(e)}"})
    
    except Exception as e:
        # Handle any other errors
        return jsonify({"error": f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
