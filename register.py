from pydantic import Field,BaseModel,EmailStr,field_validator
from typing import Literal
import hashlib
import re
import json
DATA_FILE = "data.json"
class Register(BaseModel):
    name :str = Field(default='')
    email:EmailStr = Field(description="Email of user")
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
        description="Password must contain 1 uppercase, 1 lowercase, 1 digit, 1 special char"
    )
    @field_validator('password')
    def password_validator(cls, v):
        # Regex using lookaheads manually in Python
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])', v):
            raise ValueError('Password must contain at least 1 uppercase, 1 lowercase, 1 digit, 1 special character')
        hashed_password = hashlib.sha256(v.encode()).hexdigest()
        return hashed_password

# --- Save to JSON ---
def save_user(user, filename=DATA_FILE) -> bool:
    """
    Saves the user to JSON file.
    Returns True if saved successfully, False otherwise.
    """
    try:
        # Load existing data
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    try:
        # Convert Pydantic model to dict
        data.append(user.model_dump())  # hashed password included

        # Save back to file
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        return True  # Successfully saved
    except Exception as e:
        print("Error saving user:", e)
        return False  # Something went wrong




     
    
    
        