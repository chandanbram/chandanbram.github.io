from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gradio_client import Client

app = FastAPI()

# Allow CORS from your frontend (adjust origin accordingly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing use "*", for production, use your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Client("chandubram/chandan-private-chatbot")  # Your HF space

class ChatRequest(BaseModel):
    message: str
    system_message: str = "You are Chandan-Bot, a formal and professional assistant. Answer ONLY based on the provided data and never generate information outside of it. If the information is not available, say: 'I'm sorry, but I do not have that information.' Always speak in the first person."
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.95

@app.post("/api/predict")
async def predict(chat_request: ChatRequest):
    response = client.predict(
        message=chat_request.message,
        system_message=chat_request.system_message,
        max_tokens=chat_request.max_tokens,
        temperature=chat_request.temperature,
        top_p=chat_request.top_p,
        api_name="/chat",
    )
    return {"response": response}
