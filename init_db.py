import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'results.db'

schema = '''
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
'''

sample_data = [
    ('Alice Johnson', 'R001', 12, 15, 80, 120000, '2025-10-01T10:00:00', '[]'),
    ('Bob Smith', 'R002', 14, 15, 93, 90000, '2025-10-02T11:30:00', '[]'),
    ('Charlie Brown', 'R003', 9, 15, 60, 150000, '2025-10-03T09:15:00', '[]'),
]

if __name__ == '__main__':
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(schema)
    cur.executemany('INSERT INTO results (name, rollNumber, score, total, percentage, timeSpent, timestamp, results) VALUES (?, ?, ?, ?, ?, ?, ?, ?);', sample_data)
    conn.commit()
    conn.close()
    print(f'Initialized database at {DB_PATH.absolute()} with {len(sample_data)} sample rows.')
