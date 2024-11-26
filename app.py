from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import re

app = Flask(__name__)

# Function to initialize the database and create the users table
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            Contact_Number TEXT NOT NULL,
            Gender TEXT NOT NULL,
            Email TEXT NOT NULL,
            password TEXT NOT NULL,
            Confirm_Password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to get users from the database
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# Function to add a new user
def add_user(username, Contact_Number, Gender, Email, password, Confirm_Password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, Contact_Number, Gender, Email, password, Confirm_Password) VALUES (?, ?, ?, ?, ?, ?)", 
                   (username, Contact_Number, Gender, Email, password, Confirm_Password))
    conn.commit()
    conn.close()

# Email validation function
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# Home route - displays users and handles form submission
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        Contact_Number = request.form['Contact_Number']
        Gender = request.form['Gender']
        Email = request.form['Email']
        password = request.form['password']
        Confirm_Password = request.form['Confirm_Password']

        # Check if passwords match
        if password != Confirm_Password:
            return "Passwords do not match!", 400

        # Validate email format
        if not validate_email(Email):
            return "Invalid email format!", 400

        # Add user to the database
        add_user(username, Contact_Number, Gender, Email, password, Confirm_Password)

    users = get_users()
    return render_template('registration.html', users=users)

# Route to edit a user
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        new_username = request.form['username']
        new_Contact_Number = request.form['Contact_Number']
        new_Gender = request.form['Gender']
        new_Email = request.form['Email']
        new_password = request.form['password']
        new_Confirm_Password = request.form['Confirm_Password']

        # Check if passwords match
        if new_password != new_Confirm_Password:
            return "Passwords do not match!", 400

        # Validate email format
        if not validate_email(new_Email):
            return "Invalid email format!", 400

        # Update user in the database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET username=?, Contact_Number=?, Gender=?, Email=?, password=?, Confirm_Password=? WHERE id=?", 
                       (new_username, new_Contact_Number, new_Gender, new_Email, new_password, new_Confirm_Password, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    
    # Fetch the user to prepopulate the form
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    # Render the edit form with user data
    return render_template('login.html', user=user)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Email = request.form['Email']
        password = request.form['password']

        # Check if the user exists in the database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE Email=? AND password=?", (Email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return "Login successful!"
        else:
            return "Invalid email or password!", 400

    return render_template('login.html')

if __name__ == "__main__":
    init_db()  # Ensure the database and table exist
    app.run(debug=True)
