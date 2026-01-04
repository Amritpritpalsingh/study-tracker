from flask import Blueprint, render_template, session,redirect
from flask_socketio import emit
from extensions import socketio
from chat_model import llm, clean_text, get_history
from langchain.messages import HumanMessage, AIMessage
chat_bp = Blueprint("chat", __name__, url_prefix="/note&do/chat")

@chat_bp.route("/")
def chat():
    if "uid" not in session:
        return redirect("/note&do/auth/login")
    return render_template("chat.html")


@socketio.on("user_message")
def handle_message(data):
 
    if "uid" not in session:
        return redirect("/note&do/auth/login")
      

    user_text = data["message"]
    history = get_history()

    history.append({"role": "user", "content": user_text})

    messages = []
    for h in history:
        if h["role"] == "user":
            messages.append(HumanMessage(h["content"]))
        elif h["role"] == "assistant":
            messages.append(AIMessage(h["content"]))

    full_response = ""

    # 🔥 STREAMING TOKENS
    for chunk in llm.stream(messages):
        token = chunk.content
        if token:
            emit("ai_token", {"token": token})
            full_response += token

    history.append({"role": "assistant", "content": clean_text(full_response)})
    session.modified = True

    emit("ai_done")