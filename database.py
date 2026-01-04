from db_connections import con, cur
from register import Register
from login import Login
import uuid


# =======================
# DATABASE SETUP
# =======================
def startDB():
    # USERS table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS USERS (
        UID VARCHAR(36) PRIMARY KEY,
        EMAIL VARCHAR(100) UNIQUE,
        PASSWORD VARCHAR(255),
        NAME VARCHAR(255)
    )
    """)

    # TASKS table (linked to user)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS TASKS (
        TASKNO INT AUTO_INCREMENT PRIMARY KEY,
        UID VARCHAR(36),
        TASK TEXT,
        FOREIGN KEY (UID) REFERENCES USERS(UID) ON DELETE CASCADE
    )
    """)

    # NOTES table (linked to user)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS NOTES (
        NOTENO INT AUTO_INCREMENT PRIMARY KEY,
        UID VARCHAR(36),
        NOTES TEXT,
        FOREIGN KEY (UID) REFERENCES USERS(UID) ON DELETE CASCADE
    )
    """)

    con.commit()


# =======================
# TODO FUNCTIONS (USER-SPECIFIC)
# =======================
def addTodoDB(uid: str, todo: str):
    cur.execute("INSERT INTO TASKS (UID, TASK) VALUES (%s, %s)", (uid, todo))
    con.commit()


def allTodoDB(uid: str):
    cur.execute("SELECT TASKNO, TASK FROM TASKS WHERE UID = %s", (uid,))
    return cur.fetchall()


def removeTodoDB(todo_no, uid):
    cur.execute("DELETE FROM TASKS WHERE TASKNO = %s AND UID = %s", (todo_no, uid))
    con.commit()
    return True


# =======================
# NOTES FUNCTIONS (USER-SPECIFIC)
# =======================
def addNotesDB(uid: str, note: str):
    cur.execute("INSERT INTO NOTES (UID, NOTES) VALUES (%s, %s)", (uid, note))
    con.commit()


def allNotesDB(uid: str):
    cur.execute("SELECT NOTENO, NOTES FROM NOTES WHERE UID = %s", (uid,))
    return cur.fetchall()


def removeNotesDB(note_no: int, uid: str):
    cur.execute("DELETE FROM NOTES WHERE NOTENO = %s AND UID = %s", (note_no, uid))
    con.commit()
    return True


# =======================
# AUTH (DATABASE-BASED)
# =======================
def save_user(user) -> bool:
    """
    Save a new user into USERS table
    """
    try:
        uid = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO USERS (UID, EMAIL, PASSWORD, NAME) VALUES (%s, %s, %s, %s)",
            (uid, user.email, user.password, user.name)
        )
        con.commit()
        return True
    except Exception as e:
        print("Error saving user:", e)
        return False


def register_user(name: str, email: str, password: str) -> bool:
    try:
        user = Register(name=name, email=email, password=password)
        return save_user(user)
    except Exception as e:
        print("Registration failed:", e)
        return False


def login_user(email: str, password: str):
    """
    Returns user dict {uid, email, name} if valid, else False
    """
    try:
        user = Login(email=email, password=password)
        return user.valid_user()
    except Exception as e:
        print("Login failed:", e)
        return False
