from flask import Flask, jsonify, request, send_from_directory, abort
import sqlite3
import os
from pathlib import Path
from flask_cors import CORS

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'results.db'
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', 'kprcascs123')

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    # Serve the admin page (or index.html by default)
    return send_from_directory('.', 'admin.html')


@app.route('/api/results', methods=['GET'])
def api_results():
    token = request.headers.get('X-Admin-Token') or request.args.get('token')
    if token != ADMIN_TOKEN:
        return jsonify({'error': 'Unauthorized'}), 401

    # Ensure DB exists
    if not DB_PATH.exists():
        return jsonify({'attempts': []})

    conn = get_db_connection()
    try:
        rows = conn.execute('SELECT * FROM results ORDER BY timestamp DESC').fetchall()
        attempts = [dict(r) for r in rows]
        return jsonify({'attempts': attempts})
    finally:
        conn.close()


@app.route('/api/clear', methods=['POST'])
def api_clear():
    token = request.headers.get('X-Admin-Token') or request.args.get('token')
    if token != ADMIN_TOKEN:
        return jsonify({'error': 'Unauthorized'}), 401

    if not DB_PATH.exists():
        return jsonify({'success': True, 'cleared': 0})

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM results')
        deleted = cur.rowcount
        conn.commit()
        return jsonify({'success': True, 'cleared': deleted})
    finally:
        conn.close()


@app.route('/api/submit', methods=['POST'])
def api_submit():
    # Accept a quiz attempt JSON and insert into the DB
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    # Ensure DB/table exists
    if not DB_PATH.exists():
        # Create DB and table
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                rollNumber TEXT,
                score INTEGER,
                total INTEGER,
                percentage INTEGER,
                timeSpent INTEGER,
                timestamp TEXT,
                results TEXT
            );
        ''')
        conn.commit()
        conn.close()

    try:
        name = data.get('name')
        rollNumber = data.get('rollNumber')
        score = int(data.get('score') or 0)
        total = int(data.get('total') or 0)
        percentage = int(data.get('percentage') or 0)
        timeSpent = int(data.get('timeSpent') or 0)
        timestamp = data.get('timestamp')
        results_json = None
        # store results as JSON string if present
        import json as _json
        if 'results' in data:
            results_json = _json.dumps(data.get('results'))

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO results (name, rollNumber, score, total, percentage, timeSpent, timestamp, results)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, rollNumber, score, total, percentage, timeSpent, timestamp, results_json))
        conn.commit()
        inserted_id = cur.lastrowid
        return jsonify({'success': True, 'id': inserted_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        try:
            conn.close()
        except:
            pass


@app.route('/<path:filename>')
def static_files(filename):
    # Serve static files like index.html, admin.html, etc.
    safe_path = BASE_DIR / filename
    if safe_path.exists() and safe_path.is_file():
        return send_from_directory('.', filename)
    abort(404)


if __name__ == '__main__':
    app.run(debug=True)
