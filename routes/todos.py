from flask import Blueprint, render_template, request, session, redirect,jsonify
from database import addTodoDB, allTodoDB, removeTodoDB

todo_bp = Blueprint("todo", __name__, url_prefix="/note&do/todo")


@todo_bp.route("/", methods=["GET"])
def todos_page():
    if "uid" not in session:
        return redirect("/note&do/auth/login")

    todos = allTodoDB(session["uid"])
    
    return render_template("todo.html", todos=todos)

@todo_bp.route("/all", methods=["GET"])
def todos_all():
    if "uid" not in session:
        return redirect("/note&do/auth/login")

    
    
    return jsonify(allTodoDB(session["uid"]))


@todo_bp.route("/add", methods=["POST"])
def add_todo():
    if "uid" not in session:
        return redirect("/note&do/auth/login")

    todo_text = request.form.get("todo")
    
    addTodoDB(session["uid"], todo_text)
    return redirect("/note&do/todo/")


@todo_bp.route("/remove/<int:task_no>",methods=["DELETE"])
def delete_todo(task_no):
    if "uid" not in session:
        return redirect("/note&do/auth/login")

    removeTodoDB(int(task_no), session["uid"])
    return redirect("/note&do/todo/")
