import os
from flask import Flask, render_template, request, redirect, url_for
from groq import Groq

# Initialize the Flask application
app = Flask(__name__, template_folder='template')

# Initialize the client using the environment variable for the API key
client = Groq(
    api_key=os.environ.get("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")
)

# Function to filter sensitive topics
def filter_sensitive_input(user_input):
    sensitive_topics = ['black', 'race', 'gender', 'ethnicity', 'religion', 'disability', 'sexuality']
    return not any(topic in user_input.lower() for topic in sensitive_topics)

# Function to get a roast based on user input and roast level
def get_roast(user_input, roast_level):
    if not filter_sensitive_input(user_input):
        return "I can't roast you on that topic. Let's keep it fun and respectful!"

    prompts = {
        "mild": f"Give a mild but effective roast for this statement: \"{user_input}\". Keep it playful.",
        "medium": f"Give a medium level, witty, funny and embarrassing roast for this statement: \"{user_input}\".",
        "high": f"Give a high-intensity, highly embarrassing roast for this statement: \"{user_input}\"."
    }
    
    roast_prompt = prompts.get(roast_level, prompts["mild"])
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": roast_prompt}],
        model="gemma2-9b-it",
    )
    
    return chat_completion.choices[0].message.content

# Route for the main roast selection page (index.html)
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

# Route for the personalization form (index2.html)
@app.route("/personalize", methods=["POST"])
def personalize():
    name = request.form.get("name")
    traits = request.form.get("traits")
    hobbies = request.form.get("hobbies")
    
    # Generate a roast based on name, traits, and hobbies
    roast_response = get_roast(f"{name} is {traits} and likes {hobbies}", "mild")
    return redirect(url_for('show_roast', roast=roast_response))

# Route for handling roast levels and rendering index2.html
@app.route("/roast/<level>", methods=["GET"])
def select_roast(level):
    return render_template("index2.html", roast_level=level)

# Route to display the roast result
@app.route("/roast/result")
def show_roast():
    roast = request.args.get('roast')  # Get the roast from the query parameter
    return render_template("index3.html", roast=roast)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
