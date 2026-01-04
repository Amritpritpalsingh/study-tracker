from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.messages import HumanMessage, AIMessage
from flask import session
import os

load_dotenv()

MODEL_NAME = "openai/gpt-oss-120b"

llm = ChatGroq(
    model=MODEL_NAME,
    api_key=os.environ["GROQ_API_KEY"],
    streaming=True,   # 🔥 REQUIRED
)

SYSTEM_PROMPT = "You are an AI assistant that helps students. Your name is Arooj."

def clean_text(text: str) -> str:
    return text.replace("**", "").strip()

def get_history():
    if "chat_history" not in session:
        session["chat_history"] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    return session["chat_history"]
