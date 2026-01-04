from flask import Flask
from database import startDB
from extensions import socketio
from dotenv import load_dotenv
load_dotenv()
from routes.todos import todo_bp
from routes.notes import notes_bp
from routes.auth import auth_bp
from routes.chat import chat_bp
import os
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
startDB()

app.register_blueprint(todo_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)

# IMPORTANT
socketio.init_app(app)

if __name__ == "__main__":
    socketio.run(app,port=os.getenv("PORT"), debug=True)
