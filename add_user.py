import bcrypt
import re
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['user_auth_db']
users_collection = db['users']

# Regular expression for password strength
# At least 8 characters, at least one uppercase letter, one lowercase letter, one digit, and one special character
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

# Hashing function
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

# Function to validate password strength
def is_password_strong(password):
    return bool(re.match(PASSWORD_REGEX, password))

# Function to add a user with password strength validation
def add_user(username, password):
    while not is_password_strong(password):
        print("Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
        password = input("Enter password: ")

    
    hashed_password = hash_password(password)
    user_data = {"username": username, "password": hashed_password}
    users_collection.insert_one(user_data)
    print(f"User '{username}' added successfully with hashed password.")

if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    add_user(username, password)
