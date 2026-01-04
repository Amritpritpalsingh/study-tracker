
from pydantic import Field,BaseModel,EmailStr,field_validator
from typing import Literal
import hashlib
import re
import json
from db_connections import cur
class Login(BaseModel):
    email : EmailStr = Field(description="Email")
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
        description="Passwoard must contain 1 uppercase, 1 lowercase, 1 digit, 1 special char"
    )
    @field_validator('password')
    def password_validator(cls, v):
        # Regex using lookaheads manually in Python
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])', v):
            raise ValueError('Password must contain at least 1 uppercase, 1 lowercase, 1 digit, 1 special character')
        hashed_password = hashlib.sha256(v.encode()).hexdigest()
        return hashed_password
    def valid_user(self):
        """
        Check if email exists in DB and password matches.
        Returns user dict if valid, else False.
        """
        try:
            cur.execute(
                """
                SELECT UID, EMAIL, NAME
                FROM USERS
                WHERE EMAIL = %s AND PASSWORD = %s
                """,
                (self.email, self.password)
            )

            user = cur.fetchone()

            if user:
                return {
                    "uid": user[0],
                    "email": user[1],
                    "name": user[2]
                }

            return False

        except Exception as e:
            print("Login error:", e)
            return False

        
        