# Python Functions Quiz - Admin Backend

This small backend provides an API for the admin dashboard to fetch and clear quiz results. It uses SQLite for storage and a simple admin token for authentication.

Files added:
- `app.py` - Flask app that serves `admin.html` and the API endpoints `/api/results` and `/api/clear`.
- `init_db.py` - Initializes `results.db` with the `results` table and inserts sample rows.
- `requirements.txt` - Python dependencies.
- `admin.html` - Updated to try fetching results from `/api/results` (uses the existing admin password in the page as the token header).

Quick start (Windows PowerShell):

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Initialize the database (creates `results.db` in the same folder):

```powershell
python init_db.py
```

4. Run the Flask app:

```powershell
$env:FLASK_ENV = 'development'; python app.py
```

5. Open `http://127.0.0.1:5000/admin.html` in your browser and login with the admin password `kprcascs123`.

Notes:
- The Flask app reads an environment variable `ADMIN_TOKEN` if you want to override the default admin token/password. If set, ensure the token matches the password used in `admin.html` or change the client code to prompt for token separately.
- For production use, secure authentication and HTTPS are required. This example is intentionally simple for demonstration purposes.

Hosting options
---------------

Docker (recommended for simple hosting):

1. Build the image and run it locally:

```powershell
Set-Location "C:\Users\Prasanth K K\Downloads\python_functions_quiz_updated (1)\python_functions_quiz_updated"
docker build -t python-quiz .
docker run -p 5000:5000 -e ADMIN_TOKEN="kprcascs123" python-quiz
```

2. Or use docker-compose:

```powershell
docker-compose up --build
```

Note about persistence: The SQLite file `results.db` is created inside the container at `/app/results.db` by default. If you want the DB to survive container restarts, mount a host volume:

```powershell
docker run -p 5000:5000 -v C:\path\to\data:/app -e ADMIN_TOKEN="kprcascs123" python-quiz
```

Heroku / Platform-as-a-Service:

- This repo includes a `Procfile` for a simple Python web process. However, Heroku's ephemeral filesystem means SQLite is not suitable for production on Heroku. Use Postgres or another managed DB and update `app.py` connection accordingly.

Quick checklist before deploying to a PaaS:
- Replace SQLite with a managed database (Postgres/MySQL) and update `get_db_connection()`.
- Secure admin authentication (do not embed password in client HTML).
- Use HTTPS and environment-secured secrets.

