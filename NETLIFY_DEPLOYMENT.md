# Netlify Deployment Guide for Python Quiz App

## Important Note
**Netlify is primarily designed for static sites and serverless functions.** Since your app uses Flask/Python with PostgreSQL, you have a few options:

## Option 1: Deploy Backend to a Different Platform (Recommended)

### Best Platforms for Python + PostgreSQL:
1. **Render** (Free tier available)
2. **Railway** (Free tier available)
3. **Fly.io** (Free tier available)
4. **Heroku** (Paid)

### For Render Deployment:
1. Push your code to GitHub
2. Go to https://render.com
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (or `python app.py`)


## Option 2: Use Netlify Functions (Limited)

If you want to use Netlify, you can only host:
- **Frontend** (HTML, CSS, JS) on Netlify
- **Backend API** as Netlify Functions (serverless)

### Steps for Netlify Functions:

1. **Update your project structure**:
   ```
   /
   ├── netlify/
   │   └── functions/
   │       └── api.py
   ├── public/
   │   ├── index.html
   │   └── admin.html
   └── netlify.toml
   ```

2. **Create `netlify.toml`**:
   ```toml
   [build]
     publish = "public"
     functions = "netlify/functions"

   [[redirects]]
     from = "/api/*"
     to = "/.netlify/functions/api/:splat"
     status = 200
   ```

3. **Install Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   ```

4. **Deploy**:
   ```bash
   netlify login
   netlify init
   netlify deploy --prod
   ```

## Option 3: Frontend on Netlify + Backend Elsewhere

1. **Deploy static files** (index.html, admin.html) to Netlify
2. **Deploy Python backend** to Render/Railway/Fly.io
3. **Update frontend** to call your backend API URL

### Environment Variables on Netlify:
- Go to Site Settings → Environment Variables
- Add your database credentials (if using Netlify Functions)

## Recommended Approach

**Use Render for the full stack app:**

1. Add `gunicorn` to requirements.txt
2. Push to GitHub
3. Deploy on Render
4. Set environment variables
5. Your app will be live with a URL like: `https://yourapp.onrender.com`

## Testing Database Connection

Run this command to test your database connection:
```bash
python test_db_connection.py
```

If successful, you'll see:
- "Connection successful!"
- Current timestamp from database
- "Connection closed."
