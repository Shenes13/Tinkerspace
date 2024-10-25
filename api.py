import os
from groq import Groq

# Initialize the client using the environment variable for the API key
client = Groq(
    api_key=os.environ.get("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")
)

# Function to filter sensitive topics
def filter_sensitive_input(user_input):
    sensitive_topics = ['black', 'race', 'gender', 'ethnicity', 'religion', 'disability', 'sexuality']
    
    # Check if the input contains any sensitive words
    return not any(topic in user_input.lower() for topic in sensitive_topics)

# Function to get a roast based on user input and roast level
def get_roast(user_input, roast_level):
    if not filter_sensitive_input(user_input):
        return "I can't roast you on that topic. Let's keep it fun and respectful!"
    
    # Define roast prompts for different levels
    prompts = {
        "mild": f"Give a mild but effective roast for this statement: \"{user_input}\". Keep it playful.",
        "medium": f"Give a medium level, witty, funny and embarassing roast for this statement: \"{user_input}\". It should be humorous .",
        "high": f"Give a high-intensity, highly embarassing roast for this statement: \"{user_input}\". Go for something really witty and sarcastic."
    }
    
    # Select the appropriate prompt based on roast level
    roast_prompt = prompts.get(roast_level, prompts["mild"])  # Default to mild if level is invalid
    
    # API call to generate the roast using the gemma2-9b-it model
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": roast_prompt,
            }
        ],
        model="gemma2-9b-it",
    )
    
    # Extract and return the roast message from the API response
    return chat_completion.choices[0].message.content

# Example of how this would work in a website backend context
if __name__ == "__main__":
    user_input = input("Enter something to be roasted (e.g., 'I am fat'): ")
    roast_level = input("Enter roast level (mild, medium, high): ").lower()
    roast_response = get_roast(user_input, roast_level)
    print(f"Roast: {roast_response}")
