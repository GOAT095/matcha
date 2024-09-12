import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

#PostgreSQL database connection details
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

#Connect to the PostgreSQL database
def connect_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

#Create the 'users' table
def create_users_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            gender VARCHAR(10),
            sexual_preferences VARCHAR(100),
            biography TEXT,
            interests TEXT[],
            profile_picture TEXT,
            pictures TEXT[]
        );
    ''')
    cur.execute('''
    INSERT INTO users (gender, sexual_preferences, biography, interests, profile_picture, pictures)
    VALUES (
        'Male', 
        'Heterosexual', 
        'A software engineer who loves hiking and photography.', 
        ARRAY['hiking', 'photography', 'coding'], 
        'profile_pic.jpg', 
        ARRAY['pic1.jpg', 'pic2.jpg', 'pic3.jpg']
    );
    ''')

    conn.commit()
    cur.close()
    conn.close()

#Route to add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    gender = data.get('gender')
    sexual_preferences = data.get('sexual_preferences')
    biography = data.get('biography')
    interests = data.get('interests')  #List of tags
    profile_picture = data.get('profile_picture')
    pictures = data.get('pictures')  #List of up to 5 pictures

    if len(pictures) > 5:
        return jsonify({"error": "You can upload up to 5 pictures"}), 400

    conn = connect_db()
    cur = conn.cursor()

    #Insert the new user into the database
    cur.execute('''
        INSERT INTO users (gender, sexual_preferences, biography, interests, profile_picture, pictures)
        VALUES (%s, %s, %s, %s, %s, %s);
    ''', (gender, sexual_preferences, biography, interests, profile_picture, pictures))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User added successfully!"}), 201

if __name__ == '__main__':
    create_users_table()  #Ensure the users table is created
    app.run(debug=True)
