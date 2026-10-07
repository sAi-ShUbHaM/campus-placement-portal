from werkzeug.security import generate_password_hash
from database import get_db_connection

connection = get_db_connection()

name = "Placement Admin"
email = "admin@college.com"
password = "admin123"
phone = "9999999999"
role = "admin"

hashed_password = generate_password_hash(password)

connection.execute("""
    INSERT INTO users
    (name, email, password, phone, role)
    VALUES (?, ?, ?, ?, ?)
""", (
    name,
    email,
    hashed_password,
    phone,
    role
))

connection.commit()
connection.close()

print("Admin account created successfully!")