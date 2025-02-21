import json
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 Allow all origins for debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API keys securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CAT_API_KEY = os.getenv("CAT_API_KEY")

# Pydantic model for chat requests
class ChatRequest(BaseModel):
    message: str

def get_breed_id(breed_name: str):
    breed_name = breed_name.lower()
    response = requests.get(
        "https://api.thecatapi.com/v1/breeds",
        headers={"x-api-key": CAT_API_KEY}
    )
    if response.status_code == 200:
        breeds = response.json()
        for breed in breeds:
            if breed_name in breed["name"].lower():
                return breed["id"]
    return None

# Route to handle chat with OpenAI and CatAPI Function Calling
@app.post("/chat")
async def chat_with_ai(request: ChatRequest):
    try:
        openai.api_key = OPENAI_API_KEY
        print(f"Received message: {request.message}")
        
        # Define the function for fetching cat images with optional breed and quantity
        cat_api_function = {
            "name": "get_cat_image",
            "description": "Fetches random cat images from TheCatAPI with optional breed and quantity",
            "parameters": {
                "type": "object",
                "properties": {
                    "breed": {
                        "type": "string",
                        "description": "Optional breed of the cat, e.g., 'siamese', 'persian'",
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Number of cat images to fetch",
                        "default": 1,
                        "minimum": 1,
                        "maximum": 10,
                    },
                },
                "required": [],
            },
        }

        # Generate a chat completion with function calling
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": request.message}],
            functions=[cat_api_function],
            function_call="auto"
        )
        
        # Extract chatbot reply and potential function call
        message = response.choices[0].message

        image_urls = []

        # 🛠️ Safely check if function_call exists
        if hasattr(message, "function_call") and message.function_call:
            if message.function_call.name == "get_cat_image":
                print("OpenAI model requested cat images...")
                
                # Extract function parameters (breed and quantity)
                function_args = json.loads(message.function_call.arguments)
                breed = function_args.get("breed", "")
                quantity = int(function_args.get("quantity", 1))
                
                # Prepare the CatAPI request
                cat_api_url = f"https://api.thecatapi.com/v1/images/search?limit={quantity}"
                if breed:
                    breed_id = get_breed_id(breed)
                    if breed_id:
                        cat_api_url += f"&breed_ids={breed_id}"
                
                cat_response = requests.get(
                    cat_api_url,
                    headers={"x-api-key": CAT_API_KEY}
                )
                
                if cat_response.status_code == 200:
                    image_urls = [img["url"] for img in cat_response.json()]
        
        # ✅ Return both text response and image URLs
        return {"reply": message.content, "image_urls": image_urls}
    
    except Exception as e:
        print(f"Error in chat_with_ai: {str(e)}")
        return {"error": f"Failed to get response from OpenAI: {str(e)}"}

# ✅ Route to get a random cat image from CatAPI
@app.get("/cat")
async def get_cat_image():
    try:
        cat_response = requests.get(
            "https://api.thecatapi.com/v1/images/search",
            headers={"x-api-key": CAT_API_KEY}
        )
        if cat_response.status_code == 200:
            return {"image_url": cat_response.json()[0]["url"]}
    except Exception as e:
        print(f"Error in get_cat_image: {str(e)}")
    return {"error": "Request to CatAPI failed."}


