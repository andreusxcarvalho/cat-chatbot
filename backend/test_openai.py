import openai
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with the new API format
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Make a request using the updated OpenAI API syntax
response = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Say hello to a cat lover!"}]
)

# Output the response
print(response.choices[0].message.content)
