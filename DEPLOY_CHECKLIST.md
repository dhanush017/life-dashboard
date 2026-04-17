# 🚀 DEPLOY NOW - Checklist

## ✅ Pre-Deployment Checklist

- [x] Code pushed to GitHub ✓
- [x] render.yaml configured ✓
- [x] README.md ready ✓
- [x] requirements.txt updated ✓
- [ ] **You have: GROQ_API_KEY** (need this!)
- [ ] **You have: SECRET_KEY** (generated below)

---

## 🔑 Step 1: Generate Your Keys

### SECRET_KEY (Copy the output):
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Save this!** You'll need it in deployment.

### GROQ_API_KEY:
1. Go to: https://console.groq.com
2. Sign up (free) or login
3. Click "API Keys" → Create Key
4. Copy the key (looks like: `gsk_...`)
5. **Save this!**

---

## 🌐 Step 2: Deploy on Render (5 minutes)

### 2.1 Create Render Account
1. Go to: https://render.com
2. Click **Sign Up**
3. Choose **GitHub**
4. Authorize Render

### 2.2 Deploy Backend
1. Click **New +** → **Web Service**
2. Select your **life-dashboard** repository
3. Settings:
   - **Name:** `lifedashboard-api`
   - **Runtime:** Python (auto-selected)
   - **Build Command:** (leave blank - render.yaml handles it)
   - **Start Command:** (leave blank - render.yaml handles it)
   - **Plan:** Free
4. Click **Create Web Service**
5. **Wait 3-5 minutes** for build to complete

### 2.3 Add Environment Variables
While backend is building:
1. Go to your service → **Environment**
2. Add **two** variables:
   - Name: `GROQ_API_KEY` → Value: `gsk_...` (your Groq key)
   - Name: `SECRET_KEY` → Value: `<your generated key from Step 1>`
3. Click **Save**
4. Backend will auto-redeploy with new variables

### 2.4 Verify Backend is Live
- When it says **Live** in dashboard ✓
- Note your URL: `https://lifedashboard-api.onrender.com`
- Test it: https://lifedashboard-api.onrender.com/docs
  - Should see Swagger API documentation

---

## 📱 Step 3: Deploy Frontend (Optional but Recommended)

### 3.1 Deploy Static Site
1. Click **New +** → **Static Site**
2. Select **same repository** (life-dashboard)
3. Settings:
   - **Name:** `lifedashboard-web`
   - **Build Command:** `echo "Static site"`
   - **Publish Directory:** `.`
4. Click **Create Static Site**
5. **Wait 1-2 minutes** for deployment

### 3.2 Update Frontend API URL
1. Open your repo on GitHub: https://github.com/dhanush017/life-dashboard
2. Click **index.html** → Edit (pencil icon)
3. Find line ~1467 (search for `API_URL`)
4. Add this code in the `<head>` section (after other meta tags):

```html
<script>
    if (window.location.hostname !== 'localhost') {
        window.API_URL = 'https://lifedashboard-api.onrender.com';
    }
</script>
```

5. Scroll to bottom → **Commit changes**
6. Message: "Update API URL for production"
7. Static site auto-redeploys (wait 1-2 min)

---

## ✅ Step 4: Test Your App!

### Backend Test
- URL: `https://lifedashboard-api.onrender.com/docs`
- Should show Swagger documentation

### Frontend Test
- URL: `https://lifedashboard-web.onrender.com`
- Should show Life Dashboard UI

### App Test
1. Create account (email/password)
2. Add data (mood, energy, etc.)
3. View history
4. Get insights (should work!)

---

## 🎉 Done! Your App is LIVE!

| Component | URL |
|-----------|-----|
| **Frontend** | https://lifedashboard-web.onrender.com |
| **Backend** | https://lifedashboard-api.onrender.com |
| **API Docs** | https://lifedashboard-api.onrender.com/docs |

---

## 📊 Cost

- Backend (Render Free): **$0/month**
- Frontend (Render Free): **$0/month**
- Database (PostgreSQL Free): **$0/month**
- **TOTAL: $0/month** 🎉

Upgrade anytime for better performance ($7+/month).

---

## 🐛 If Something Goes Wrong

### Backend won't deploy?
- Check logs: Render Dashboard → Services → Logs
- Common issue: Missing GROQ_API_KEY or SECRET_KEY
- Fix: Add to Environment variables

### Frontend shows "Cannot reach API"?
- Check you added the script to index.html
- Verify API URL is correct: `https://lifedashboard-api.onrender.com`
- Redeploy frontend: Settings → Manual Deploy

### Database error?
- Render auto-creates PostgreSQL
- If stuck, check Services → PostgreSQL is running

---

## 🚀 Next Steps

1. **Gather your keys** (GROQ_API_KEY and SECRET_KEY)
2. **Go to Render:** https://render.com
3. **Follow steps above**
4. **Share your app!** 🎉

**Estimated time: 15 minutes total**

Good luck! 🌟
