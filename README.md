# 🐱 Cat Chatbot 🤖  

A simple, interactive chatbot that uses **OpenAI's GPT-4** and **TheCatAPI** to generate responses and fetch cat images based on user queries. Built with **FastAPI (Python)** for the backend and **HTML, CSS, JavaScript** for the frontend.

## 🚀 Features  
- **Chat with AI** – Ask any question and get an AI-generated response.  
- **Fetch Cat Images** – Request cat images by breed or quantity.  
- **Streaming Responses** – AI responses are streamed in real-time.  
- **User-Friendly UI** – Simple and modern chat interface.  

## 🛠️ Tech Stack  
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** FastAPI (Python), OpenAI API, TheCatAPI  
- **Deployment:** GitHub  

## 🔧 Installation  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/andreusxcarvalho/cat-chatbot.git
cd cat-chatbot

2️⃣ Backend Setup (FastAPI)
Ensure you have Python installed, then install dependencies and run the backend:
pip install -r requirements.txt  # Install dependencies
uvicorn main:app --reload  # Run the backend

3️⃣ Frontend Setup
Serve the frontend using a simple HTTP server:
cd frontend-js
python3 -m http.server 4000

cat-chatbot/
│── backend/                  # FastAPI Backend
│   ├── main.py               # API logic (GPT-4 & TheCatAPI)
│   ├── requirements.txt      # Python dependencies
│   ├── .env                  # API keys (not included)
│── frontend-js/               # Frontend (HTML, CSS, JS)
│   ├── index.html            # Main chat UI
│   ├── styles.css            # Styling
│   ├── script.js             # Chatbot logic
│── README.md                 # Project documentation

🐛 Known Issues
Ensure the backend is running before accessing the frontend.
API keys must be set up in a .env file for OpenAI and TheCatAPI.

