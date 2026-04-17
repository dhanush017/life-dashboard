# 🚀 Render Deployment — Life Dashboard (LIVE NOW!)

## ⚡ 5-MINUTE QUICK START

Your code is ready to deploy! Follow these steps:

### Step 1️⃣: Get Your SECRET_KEY (1 min)

Run this command and **save the output:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Example output: `a_very_long_random_string_here`

### Step 2️⃣: Get Your GROQ_API_KEY (2 min)

1. Go to **https://console.groq.com**
2. Sign up (free) or log in
3. Click **API Keys** in the left sidebar
4. Click **Create API Key** or copy existing key
5. **Copy the key** (looks like: `gsk_...`)

### Step 3️⃣: Create Render Account (1 min)

1. Go to **https://render.com**
2. Click **Sign Up**
3. Choose **GitHub** as sign-up method
4. Authorize Render to access your GitHub
5. **Done!** You're logged in

### Step 4️⃣: Deploy Backend (1 min)

1. In Render Dashboard, click **New +** → **Web Service**
2. Find and select your **LifeDashboard** repo
3. Configure:
   - **Name:** `lifedashboard-api`
   - **Runtime:** `Python`
   - Render will auto-detect `render.yaml` ✅
4. Click **Create Web Service**
5. **Wait 3-5 minutes** for build to complete (watch the logs)
6. When it says **Live** ✅, note your URL: `https://lifedashboard-api.onrender.com`

### Step 5️⃣: Add Environment Variables (1 min)

While waiting for backend build:

1. Go to your Web Service → **Environment**
2. Add two variables:
   - `GROQ_API_KEY` = `<paste your Groq key from Step 2>`
   - `SECRET_KEY` = `<paste your secret from Step 1>`
3. Click **Save**
4. The backend will **auto-redeploy** with new variables

### Step 6️⃣: Deploy Frontend (1 min)

1. Click **New +** → **Static Site**
2. Select your **LifeDashboard** repo (same one)
3. Configure:
   - **Name:** `lifedashboard-web`
   - **Build Command:** `echo 'Static site'`
   - **Publish Directory:** `.` (single dot)
4. Click **Create Static Site**
5. **Wait 1-2 minutes** for deployment
6. When it says **Live** ✅, note your URL: `https://lifedashboard-web.onrender.com`

### Step 7️⃣: Connect Frontend to Backend (1 min)

1. Open your repo on GitHub
2. Edit `index.html` (click the pencil icon)
3. Find line ~1465 (search for `API_BASE`)
4. Add this line in the `<head>` section (right after other `<meta>` tags):

```html
<script>
    // Production API URL
    if (window.location.hostname !== 'localhost') {
        window.API_URL = 'https://lifedashboard-api.onrender.com';
    }
</script>
```

5. Scroll down and click **Commit changes**
6. Message: `Update API URL for Render production`
7. **Auto-redeploys!** ✅ (give it 2 min)

### Step 8️⃣: Test Your Live App! 🎉

1. **Test Backend:** Go to `https://lifedashboard-api.onrender.com/docs`
   - Should see Swagger API docs
   
2. **Test Frontend:** Go to `https://lifedashboard-web.onrender.com`
   - Should see Life Dashboard UI
   
3. **Create Account:**
   - Sign up with email/password
   - Should work! ✅

4. **Add Test Data:**
   - Click "Add Data"
   - Fill in mood, energy, etc.
   - Click "Save Entry"
   - Should appear in history ✅

5. **Get Insights:**
   - Click "Get Insights"
   - Should show AI-generated analysis ✅

---

## 📊 VERIFY EVERYTHING WORKS

### Backend Health Check

```bash
curl https://lifedashboard-api.onrender.com/docs
# Should return 200 OK with HTML page
```

### Frontend Load Test

```bash
curl https://lifedashboard-web.onrender.com
# Should return 200 OK with HTML
```

---

## ⚙️ AFTER DEPLOYMENT

### Check Logs (Troubleshooting)

1. Go to Render Dashboard → Your Web Service
2. Click **Logs** tab
3. See what's happening in real-time

### Scale Up Later

When you get users:
1. Go to Settings → **Plan**
2. Upgrade from **Free** to **Starter** ($7/month)
3. Auto-scales automatically!

### Monitor Performance

1. Render Dashboard → **Metrics**
2. See CPU, memory, requests
3. Alerts for issues

### Custom Domain (Optional)

1. Go to Settings → **Custom Domain**
2. Add your domain (e.g., `lifedashboard.com`)
3. Follow DNS setup instructions
4. ~$1-3/month for domain

---

## 🐛 TROUBLESHOOTING

### "503 Service Unavailable" after deployment

**Cause:** Backend still building or crashed
- **Solution:** Wait 2-3 more minutes and refresh
- **Check:** Go to backend service → Logs

### "CORS error" when accessing from frontend

**Cause:** Backend doesn't know about frontend URL
- **Solution:** Check CORS_ORIGINS in render.yaml
- **Fix:** Update to: `CORS_ORIGINS=https://lifedashboard-web.onrender.com`

### "Database connection refused"

**Cause:** PostgreSQL not initialized yet
- **Solution:** Backend auto-creates on first connection (wait 1-2 min)
- **Check:** Go to Services → PostgreSQL → check if it's running

### "SECRET_KEY or GROQ_API_KEY not found"

**Cause:** Environment variables not added
- **Solution:** Go to Web Service → Environment
- **Add:** Both GROQ_API_KEY and SECRET_KEY

### "Build failed - missing requirements"

**Cause:** requirements.txt outdated
- **Solution:** Your render.yaml handles this automatically
- **Manual fix:** Redeploy: go to Settings → Manual Deploy

### Frontend shows "Cannot reach API"

**Cause:** API_URL not set correctly
- **Solution:** Check the script in Step 7 was added correctly
- **Debug:** Open browser console (F12) → check window.API_URL

---

## 💰 COST BREAKDOWN

| Component | Plan | Cost/Month |
|-----------|------|-----------|
| Web Service (Backend) | Free | $0 |
| PostgreSQL Database | Free | $0 |
| Static Site (Frontend) | Free | $0 |
| **TOTAL** | | **$0** 🎉 |

**Upgrade when you need:**
- **Starter Plan:** $7/month (always-on, no auto-sleep)
- **Pro Plan:** $12/month (more resources)

---

## 📱 NEXT STEPS

After your app is live:

1. **Share with friends!** Send them the frontend URL
2. **Collect feedback** on the UI/UX
3. **Monitor logs** for any issues
4. **Add features** based on user feedback
5. **Upgrade to paid** when you have consistent users

---

## 🎯 YOU'RE DONE! 🚀

Your Life Dashboard is now:
- ✅ **Live on the internet**
- ✅ **Backed by PostgreSQL database**
- ✅ **Running on Render's infrastructure**
- ✅ **Free for the first month**
- ✅ **Auto-scaling when needed**

Congratulations! 🎉

---

## 📞 SUPPORT

- **Render Docs:** https://render.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Groq API:** https://console.groq.com/docs/quickstart
- **Community:** Discord @ Render, FastAPI

---

## 📝 QUICK REFERENCE

| What | Where |
|------|-------|
| Backend URL | `https://lifedashboard-api.onrender.com` |
| Frontend URL | `https://lifedashboard-web.onrender.com` |
| API Docs | Backend URL + `/docs` |
| Logs | Render Dashboard → Services → Logs |
| Settings | Render Dashboard → Services → Settings |
| Environment Vars | Render Dashboard → Services → Environment |
| Metrics | Render Dashboard → Metrics |

**Happy deploying! 🚀✨**
