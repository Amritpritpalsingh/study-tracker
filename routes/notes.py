from flask import Blueprint, render_template, request, jsonify,session,redirect
from database import addNotesDB, allNotesDB, removeNotesDB

notes_bp = Blueprint("notes", __name__)

@notes_bp.route("/note&do/notepad")
def notepad():
    if "uid" not in session:
        return redirect("/note&do/auth/login")
    
    return render_template("notepad.html")

@notes_bp.route("/note&do/notes")
def notes_page():
    if "uid" not in session:
        return redirect("/note&do/auth/login")
    return render_template("notes.html")

@notes_bp.route("/note&do/note/add", methods=["POST"])
def add_note():
    if "uid" not in session:
        return redirect("/note&do/auth/login")
    note = request.form["note"]
    addNotesDB(session["uid"],note)
    return jsonify({"success": True})

@notes_bp.route("/note&do/notes/all")
def get_notes():
    if "uid" not in session:
        return redirect("/note&do/auth/login")
    return jsonify(allNotesDB(session["uid"]))

@notes_bp.route("/note&do/note/remove/<int:noteN>", methods=["DELETE"])
def remove_note(noteN):
    if "uid" not in session:
        return redirect("/note&do/auth/login")
    return jsonify(removeNotesDB(noteN,session["uid"]))
