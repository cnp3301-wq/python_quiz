from flask import Flask, jsonify, request, send_from_directory, abort
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from pathlib import Path
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).parent
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', 'kprcascs123')

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Database configuration
DB_CONFIG = {
    'user': os.getenv("user"),
    'password': os.getenv("password"),
    'host': os.getenv("host"),
    'port': os.getenv("port"),
    'dbname': os.getenv("dbname")
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn


@app.route('/')
def index():
    # Serve the admin page (or index.html by default)
    return send_from_directory('.', 'index.html')

@app.route('/admin')
def admin():
    # Serve the admin page (or admin.html by default)
    return send_from_directory('.', 'admin.html')


@app.route('/api/results', methods=['GET'])
def api_results():
    token = request.headers.get('X-Admin-Token') or request.args.get('token')
    if token != ADMIN_TOKEN:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM results ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        attempts = [dict(r) for r in rows]
        return jsonify({'attempts': attempts})
    except Exception as e:
        return jsonify({'error': str(e), 'attempts': []}), 500
    finally:
        conn.close()


@app.route('/api/clear', methods=['POST'])
def api_clear():
    token = request.headers.get('X-Admin-Token') or request.args.get('token')
    if token != ADMIN_TOKEN:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM results')
        deleted = cur.rowcount
        conn.commit()
        return jsonify({'success': True, 'cleared': deleted})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e), 'success': False}), 500
    finally:
        conn.close()


@app.route('/api/submit', methods=['POST'])
def api_submit():
    # Accept a quiz attempt JSON and insert into the DB
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    try:
        name = data.get('name')
        rollNumber = data.get('rollNumber')
        score = int(data.get('score') or 0)
        total = int(data.get('total') or 0)
        percentage = int(data.get('percentage') or 0)
        timeSpent = int(data.get('timeSpent') or 0)
        timestamp = data.get('timestamp')
        results_json = None
        
        # Store results as JSON string if present
        import json as _json
        if 'results' in data:
            results_json = _json.dumps(data.get('results'))

        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create table if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                rollNumber VARCHAR(100),
                score INTEGER,
                total INTEGER,
                percentage INTEGER,
                timeSpent INTEGER,
                timestamp TIMESTAMP,
                results TEXT
            );
        ''')
        
        cur.execute('''
            INSERT INTO results (name, rollNumber, score, total, percentage, timeSpent, timestamp, results)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (name, rollNumber, score, total, percentage, timeSpent, timestamp, results_json))
        
        inserted_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({'success': True, 'id': inserted_id})
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
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
    # Get port from environment variable (for Render/Heroku) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Listen on 0.0.0.0 to accept external connections
    app.run(host='0.0.0.0', port=port, debug=False)
