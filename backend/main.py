from fastapi import FastAPI
import openai
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Backend is running!"}

# ✅ Fixed OpenAI API Call
@app.post("/chat")
async def chat_with_ai(request: dict):
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": request["message"]}]
    )
    return {"reply": response.choices[0].message.content}
