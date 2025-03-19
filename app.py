import os
from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

# Use environment variables for database credentials
db_config = {
    "host": os.getenv("DB_HOST", "mysql"),
    "user": os.getenv("DB_USER", "myuser"),
    "password": os.getenv("DB_PASSWORD", "mypassword"),
    "database": os.getenv("DB_NAME", "mydatabase")
}

# Function to get database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Create table if it doesn't exist
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Call the function to create the table if it doesn't exist
create_table()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        # Insert user data into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cursor.close()
        conn.close()

    # Fetch all users from the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("form.html", users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)