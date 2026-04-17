# 🚀 Vercel Deployment Guide — Life Dashboard

## ⚠️ Important: Vercel Limitations & Hybrid Approach

**Vercel is primarily for static sites and Node.js serverless functions.** For FastAPI Python backends, there are limitations:

### ❌ Why Pure Vercel Isn't Ideal:
1. **Stateless functions** — 15-60 second timeout (your database queries may exceed this)
2. **No persistent storage** — Database files lost between deploys
3. **Cold starts** — Every request spins up a new Python process (slow first request)
4. **Limited memory** — 1024MB per function (SQLAlchemy + Pandas may struggle)
5. **Cost** — Expensive for long-running database operations

### ✅ Recommended: Vercel Frontend + External Backend

**Best approach: Deploy frontend on Vercel, backend elsewhere**

| Component | Platform | Why |
|-----------|----------|-----|
| Frontend (index.html) | **Vercel** ⭐ | Fast CDN, instant deploys, free tier |
| Backend API (FastAPI) | **Railway/Render** ⭐ | Python-optimized, persistent DB, affordable |
| Database | **PostgreSQL** (included) | Handles from Railway/Render |

---

## Option A: Frontend-Only Vercel + Backend on Railway (RECOMMENDED)

### Frontend Setup on Vercel:

**1. Create `vercel-frontend.json`:**
```json
{
  "version": 2,
  "buildCommand": "echo 'Static site'",
  "outputDirectory": ".",
  "env": {
    "VITE_API_URL": "@api_url"
  },
  "routes": [
    {
      "src": "/(.*)",
      "dest": "index.html"
    }
  ]
}
```

**2. Update `index.html` API endpoint:**

In your `index.html`, update the API endpoint to use environment variable:

```javascript
// Before (hardcoded):
const API_URL = 'http://localhost:8000';

// After (environment-based):
const API_URL = process.env.VITE_API_URL || 'http://localhost:8000';
```

**3. Deploy Frontend:**
```bash
npm install -g vercel
vercel --prod
```

**4. In Vercel Dashboard:**
- Add environment variable: `VITE_API_URL=https://your-railway-backend.up.railway.app`
- Redeploy

### Backend Setup on Railway:

Keep using Railway for the FastAPI backend (as per PRODUCTION_READY.md).

**Cost comparison:**
- Vercel Frontend: **Free tier** ($0)
- Railway Backend: **$5-10/month** (includes PostgreSQL)
- **Total: ~$5-10/month** ✨

---

## Option B: Vercel Serverless FastAPI (Advanced)

If you want FastAPI on Vercel's serverless runtime:

### Requirements:
1. Lightweight code (minimal dependencies)
2. Database must be external (Vercel Postgres or Supabase)
3. Accept 15-30 second timeouts
4. Higher latency due to cold starts

### Setup:

**1. Install Vercel CLI:**
```bash
npm install -g vercel
```

**2. Create `api/main.py`:**
```python
# Move FastAPI app to api/main.py with ASGI handler
from main import app

# Vercel expects this
async def handler(request):
    return app
```

**3. Use provided `vercel.json`**

**4. Use Vercel Postgres or Supabase:**
```bash
# Costs $15/month minimum for Supabase
vercel env add DATABASE_URL  # Enter PostgreSQL connection string
```

**5. Deploy:**
```bash
vercel --prod
```

### Cost for Option B:
- Vercel Functions: **$20/month** (invocations + compute)
- Supabase Database: **$15/month**
- **Total: ~$35/month** ❌ (expensive + slow)

---

## 🎯 RECOMMENDATION

**Use Option A (Vercel Frontend + Railway Backend)**

### Why?
✅ **Free frontend hosting** (Vercel)  
✅ **Fast, reliable API** (Railway)  
✅ **Cheap** (~$5-10/month total)  
✅ **Best performance** (no serverless cold starts)  
✅ **Easy to maintain** (separate frontend/backend)  

### Deployment Steps:

**Step 1: Deploy Backend to Railway (from PRODUCTION_READY.md)**
```bash
# Push code to GitHub
git add .
git commit -m "Vercel + Railway deployment ready"
git push origin main

# Go to railway.app → New Project → Deploy from GitHub
# Note the Railway backend URL (e.g., https://your-app.up.railway.app)
```

**Step 2: Update Frontend for Vercel**

In `index.html`, update API_URL:
```javascript
const API_URL = process.env.VITE_API_URL || 'http://localhost:8000';
```

Or simpler, use the Vercel environment variable in a config:
```javascript
// In index.html, add this before other scripts:
<script>
  window.API_URL = process.env.VITE_API_URL || 'http://localhost:8000';
</script>

// Then replace all fetch('http://localhost:8000/...')
// with fetch(window.API_URL + '/...')
```

**Step 3: Deploy Frontend to Vercel**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy (from project directory)
vercel --prod
```

**Step 4: Configure Environment Variable**
```bash
# In Vercel Dashboard → Settings → Environment Variables
# Add: VITE_API_URL = https://your-railway-backend.up.railway.app
```

---

## Cost Comparison: All Options

| Option | Vercel | Backend | Database | Monthly Cost | Performance |
|--------|--------|---------|----------|--------------|-------------|
| **A (Recommended)** | Frontend | Railway | Included | ~$5-10 | ⭐⭐⭐⭐⭐ Excellent |
| **B (Pure Vercel)** | Functions | - | Supabase | ~$35+ | ⭐⭐ Slow (cold starts) |
| **Railway Only** | ❌ | Railway | Included | ~$5-10 | ⭐⭐⭐⭐⭐ Excellent |
| **Render Only** | ❌ | Render | Included | ~$7-15 | ⭐⭐⭐⭐⭐ Excellent |

---

## Troubleshooting

### "CORS error when calling backend from Vercel"
- Solution: Update `CORS_ORIGINS` in Railway to include your Vercel domain
- Example: `CORS_ORIGINS=https://your-app.vercel.app`

### "Environment variables not loading"
- Solution: In Vercel Dashboard, ensure env vars are added and redeploy

### "API calls timing out"
- Solution: Use Railway backend (serverless cold starts are the issue)

### "Database connection errors"
- Solution: Check DATABASE_URL is correct in Railway/Vercel environment

---

## Quick Start: Vercel Frontend + Railway Backend

```bash
# 1. Prepare code
git add .
git commit -m "Production ready for Vercel + Railway"
git push origin main

# 2. Deploy backend to Railway (follow PRODUCTION_READY.md)
# Save the Railway URL

# 3. Update API URL in index.html
# (Replace localhost:8000 with Railway URL)

# 4. Deploy frontend to Vercel
npm install -g vercel
vercel --prod

# 5. Add environment variable in Vercel Dashboard
# VITE_API_URL = https://your-railway-backend.up.railway.app

# Done! 🚀
```

---

## When to Use Each Platform

| Use Case | Recommendation |
|----------|-----------------|
| **Static site only** | Vercel + Netlify |
| **FastAPI + Database** | Railway or Render |
| **Hybrid (best)** | Vercel (frontend) + Railway (backend) |
| **Enterprise** | AWS / GCP / Azure |
| **Lowest cost** | Railway or Render ($5-10/mo) |

**Choose: Vercel Frontend + Railway Backend** ✅

