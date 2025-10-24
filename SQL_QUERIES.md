# PostgreSQL Database Queries for Python Quiz App

## Database Connection Info
- **Host**: aws-1-ap-south-1.pooler.supabase.com
- **Port**: 5432
- **Database**: postgres
- **User**: postgres.hynenkjakgmlgibaorpx
- **Pool Mode**: session

## Table Structure

### Results Table
```sql
CREATE TABLE IF NOT EXISTS results (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    rollNumber VARCHAR(100),
    score INTEGER,
    total INTEGER,
    percentage INTEGER,
    timeSpent INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    results TEXT
);
```

## Useful SQL Queries

### 1. View All Quiz Results
```sql
SELECT * FROM results 
ORDER BY timestamp DESC;
```

### 2. Get Results by Roll Number
```sql
SELECT * FROM results 
WHERE rollNumber = 'R001' 
ORDER BY timestamp DESC;
```

### 3. Get Latest Attempt for Each Student
```sql
SELECT DISTINCT ON (rollNumber) 
    id, name, rollNumber, score, total, percentage, timeSpent, timestamp
FROM results 
ORDER BY rollNumber, timestamp DESC;
```

### 4. Calculate Average Score
```sql
SELECT 
    AVG(percentage) AS average_percentage,
    AVG(score) AS average_score
FROM results;
```

### 5. Get Top Performers
```sql
SELECT name, rollNumber, score, percentage, timestamp
FROM results 
ORDER BY score DESC, percentage DESC 
LIMIT 10;
```

### 6. Count Total Attempts
```sql
SELECT COUNT(*) AS total_attempts FROM results;
```

### 7. Count Unique Students
```sql
SELECT COUNT(DISTINCT rollNumber) AS unique_students FROM results;
```

### 8. Get Performance Statistics by Student
```sql
SELECT 
    rollNumber,
    name,
    COUNT(*) AS attempts,
    AVG(score) AS avg_score,
    MAX(score) AS best_score,
    MIN(score) AS worst_score,
    AVG(percentage) AS avg_percentage
FROM results
GROUP BY rollNumber, name
ORDER BY avg_percentage DESC;
```

### 9. Get Results by Date Range
```sql
SELECT * FROM results 
WHERE timestamp BETWEEN '2025-10-01' AND '2025-10-31'
ORDER BY timestamp DESC;
```

### 10. Get Students Who Scored Above 80%
```sql
SELECT name, rollNumber, score, percentage, timestamp
FROM results 
WHERE percentage >= 80
ORDER BY percentage DESC;
```

### 11. Get Students Who Failed (Below 60%)
```sql
SELECT name, rollNumber, score, percentage, timestamp
FROM results 
WHERE percentage < 60
ORDER BY percentage ASC;
```

### 12. Get Average Time Spent on Quiz
```sql
SELECT 
    AVG(timeSpent) AS avg_time_ms,
    AVG(timeSpent) / 1000 AS avg_time_seconds,
    AVG(timeSpent) / 60000 AS avg_time_minutes
FROM results;
```

### 13. Get Recent Quiz Attempts (Last 7 Days)
```sql
SELECT * FROM results 
WHERE timestamp >= NOW() - INTERVAL '7 days'
ORDER BY timestamp DESC;
```

### 14. Get Performance Trend for a Student
```sql
SELECT 
    timestamp::date AS date,
    score,
    percentage,
    timeSpent
FROM results 
WHERE rollNumber = 'R001'
ORDER BY timestamp ASC;
```

### 15. Delete Results Older Than 30 Days
```sql
DELETE FROM results 
WHERE timestamp < NOW() - INTERVAL '30 days';
```

### 16. Update Student Name
```sql
UPDATE results 
SET name = 'New Name'
WHERE rollNumber = 'R001';
```

### 17. Get Score Distribution
```sql
SELECT 
    CASE 
        WHEN percentage >= 90 THEN 'A+ (90-100%)'
        WHEN percentage >= 80 THEN 'A (80-89%)'
        WHEN percentage >= 70 THEN 'B (70-79%)'
        WHEN percentage >= 60 THEN 'C (60-69%)'
        ELSE 'F (Below 60%)'
    END AS grade,
    COUNT(*) AS student_count
FROM results
GROUP BY grade
ORDER BY MIN(percentage) DESC;
```

### 18. Get Today's Quiz Attempts
```sql
SELECT * FROM results 
WHERE DATE(timestamp) = CURRENT_DATE
ORDER BY timestamp DESC;
```

### 19. Get Students with Multiple Attempts
```sql
SELECT 
    rollNumber,
    name,
    COUNT(*) AS attempt_count
FROM results
GROUP BY rollNumber, name
HAVING COUNT(*) > 1
ORDER BY attempt_count DESC;
```

### 20. Export Data as CSV (in psql)
```sql
\copy (SELECT * FROM results ORDER BY timestamp DESC) TO 'quiz_results.csv' WITH CSV HEADER;
```

## Indexes for Better Performance

### Create Indexes
```sql
-- Index on rollNumber for faster student lookups
CREATE INDEX IF NOT EXISTS idx_rollNumber ON results(rollNumber);

-- Index on timestamp for faster date-based queries
CREATE INDEX IF NOT EXISTS idx_timestamp ON results(timestamp DESC);

-- Index on percentage for performance filtering
CREATE INDEX IF NOT EXISTS idx_percentage ON results(percentage);
```

### Drop Indexes (if needed)
```sql
DROP INDEX IF EXISTS idx_rollNumber;
DROP INDEX IF EXISTS idx_timestamp;
DROP INDEX IF EXISTS idx_percentage;
```

## Backup and Restore

### Backup Database (Command Line)
```bash
pg_dump -h aws-1-ap-south-1.pooler.supabase.com -p 5432 -U postgres.hynenkjakgmlgibaorpx -d postgres -t results > quiz_backup.sql
```

### Restore Database (Command Line)
```bash
psql -h aws-1-ap-south-1.pooler.supabase.com -p 5432 -U postgres.hynenkjakgmlgibaorpx -d postgres < quiz_backup.sql
```

## Maintenance Queries

### Check Table Size
```sql
SELECT 
    pg_size_pretty(pg_total_relation_size('results')) AS total_size,
    pg_size_pretty(pg_relation_size('results')) AS table_size,
    pg_size_pretty(pg_indexes_size('results')) AS indexes_size;
```

### Check Row Count
```sql
SELECT COUNT(*) FROM results;
```

### Vacuum and Analyze (for performance)
```sql
VACUUM ANALYZE results;
```

## Security

### Create Read-Only User (if needed)
```sql
CREATE USER readonly_user WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE postgres TO readonly_user;
GRANT SELECT ON results TO readonly_user;
```

### Revoke Permissions
```sql
REVOKE SELECT ON results FROM readonly_user;
```

## Quick Reference - Python Connection

```python
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

connection = psycopg2.connect(
    user=os.getenv("user"),
    password=os.getenv("password"),
    host=os.getenv("host"),
    port=os.getenv("port"),
    dbname=os.getenv("dbname")
)

cursor = connection.cursor()
cursor.execute("SELECT * FROM results LIMIT 10;")
results = cursor.fetchall()

for row in results:
    print(row)

cursor.close()
connection.close()
```
