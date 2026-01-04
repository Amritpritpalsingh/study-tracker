import mysql.connector as conn
from dotenv import load_dotenv
import os
load_dotenv()
con = conn.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE"),
    
)

cur = con.cursor()