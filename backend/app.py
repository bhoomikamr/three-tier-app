import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import redis

app = Flask(__name__)
CORS(app) # Crucial for production routing to avoid cross-origin blocks

# Read Environment Variables injected by Kubernetes/Docker-compose
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'postgres')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)

# Auto-initialize database table if it doesn't exist
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            status VARCHAR(50) DEFAULT 'Pending'
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

try:
    init_db()
    r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
except Exception as e:
    print(f"Initialization waiting for infrastructure components... {e}")

@app.route('/api/v1/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM tasks ORDER BY id DESC;')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tasks)

@app.route('/api/v1/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    
    # 1. Persist initial task state to relational DB
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('INSERT INTO tasks (title, status) VALUES (%s, %s) RETURNING *;', (title, 'Pending'))
    new_task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    # 2. Decouple architecture: Push message to Redis broker for the worker service
    try:
        r.lpush('task_queue', json.dumps(new_task))
    except Exception as e:
        print(f"Failed to queue task asynchronously: {e}")

    return jsonify(new_task), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)