import sqlite3
import secrets
import string
import os
from cryptography.fernet import Fernet


## Encryption key
def load_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
    return key


encryption_key = load_key()
cipher_suite = Fernet(encryption_key)


## Database connection
conn = sqlite3.connect('password_manager.db')
cursor = conn.cursor()

##Create password table
cursor.execute('''
CREATE TABLE IF NOT EXISTS passwords(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)               
               ''')

conn.commit()

##Create users tabele
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)               
               ''')

conn.commit()



def register_user():
    """Register a new user with encrypted password"""
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    cursor.execute("INSERT INTO users (username, password) VALUES (?,?)",
                   (username, encrypted_password))
    conn.commit()
    print("User registration successful")
    
    


def login():
    """User login and password verification"""
    global username
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    
    
    if user:
        stored_password = user[2]
        decrypted_password = cipher_suite.decrypt(stored_password.encode()).decode()
        if password == decrypted_password:
            print("Login successful")
            return True
    print("Login failed.Please try again.")
    return False





def generate_strong_password(length= 12):
    """generate a strong password including letters, digits, and special characters"""
    characters = string.ascii_letters + string.digits + string.punctuation
    strong_password = ''.join(secrets.choice(characters) for _ in range(length))   
    return strong_password



 

def change_password():
    """Change current user's account password"""
    if not login():
        return
    new_password = input("Enter your password: (or leave blank to generate strong password)")
    if not new_password:
        new_password = generate_strong_password()
        print(f"Your new password is {new_password}")
    encrypted_password = cipher_suite.encrypt(new_password.encode()).decode()
    cursor.execute("UPDATE users SET password=? WHERE username=?",(encrypted_password, username))
    conn.commit()
    print("Your password has changed successfully")
    
    
    
    

def add_password():
    """Add a new password for a website/service"""
    if not login():
        return
    website = input("website or service: ")
    username = input("Enter your username: ")
    print("Do you want to generate a strong password for this service?(y/n): ")
    generate_option = input()
    if generate_option.lower() == "y":
        password = generate_strong_password()
        print(f"Your password is {password}")
    else:
        password = input("Enter your password: ")
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    cursor.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
                   (website, username, encrypted_password))
    conn.commit()
    print("password added successfully")
    
    
    
    
def view_password():
    """View all saved passwords with decryption"""
    if not login():
        return
    cursor.execute("SELECT * FROM passwords")
    passwords = cursor.fetchall()
    if not passwords:
        print("No passwords saved yet.")
        return
    for password in passwords:
        website = password[1]
        acc_username = password[2]
        encrypted_password = password[3]
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
        print(f"ID: {password[0]}, Website: {website}, Username: {acc_username}, Password: {decrypted_password}")
        
        
        
        
        
def delete_password():
    """Delete a password by its ID"""
    if not login():
        return
    password_id = input("Enter the password ID to delete: ")
    cursor.execute("DELETE FROM passwords WHERE id=?", (password_id, ))
    conn.commit()
    print("Password deleted!")
    
    
# ----------------- Main Menu -----------------
while True:
    print("\n=== Password Manager ===")
    print("\t1. Register")
    print("\t2. Change password")
    print("\t3. Add password")
    print("\t4. View password")
    print("\t5. Delete password")
    print("\t6. Exit")
    
    choice = input("Select an option: ")
    if choice == "1":
        register_user()
    elif choice == "2":
        change_password()
    elif choice == "3":
        add_password()
    elif choice == "4":
        view_password()
    elif choice == "5":
        delete_password()
    elif choice == "6":
        break
    else:
        print("Invalid choice")
        

conn.close()