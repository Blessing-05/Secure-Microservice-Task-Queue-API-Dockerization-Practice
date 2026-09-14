import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = "tasks.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT DEFAULT 'pending'
            )
        ''')
    conn.close()

init_db()

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "online",
        "service": "Secure Task Queue API",
        "endpoints": {
            "tasks": "/tasks (GET, POST)"
        }
    }), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, status FROM tasks")
        tasks = [{"id": row[0], "title": row[1], "status": row[2]} for row in cursor.fetchall()]
    return jsonify({"count": len(tasks), "tasks": tasks}), 200

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Missing 'title' field"}), 400

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (?)", (data['title'],))
        conn.commit()
        task_id = cursor.lastrowid

    return jsonify({"message": "Task created", "task_id": task_id}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)