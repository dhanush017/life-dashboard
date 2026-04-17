#!/bin/bash
# Render.com Deployment Setup for Life Dashboard
# This script prepares your repository for Render deployment

set -e

echo "🚀 Life Dashboard — Render Deployment Setup"
echo "=============================================="
echo ""

# Step 1: Verify requirements
echo "✓ Checking prerequisites..."
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git"
    exit 1
fi

echo "✓ Python and Git installed"
echo ""

# Step 2: Create render.yaml for Render Native deployment
echo "📝 Creating render.yaml for deployment..."
cat > render.yaml << 'EOF'
services:
  - type: web
    name: lifedashboard-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app
    plan: free
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: lifedashboard-db
          property: connectionString
      - key: GROQ_API_KEY
        sync: false
      - key: SECRET_KEY
        sync: false
      - key: CORS_ORIGINS
        value: ${RENDER_EXTERNAL_URL}

  - type: pserv
    name: lifedashboard-db
    ipAllowList: []
    plan: free
    region: oregon
EOF

echo "✓ render.yaml created"
echo ""

# Step 3: Generate SECRET_KEY if needed
echo "🔑 Generating SECRET_KEY..."
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
echo "Generated SECRET_KEY: $SECRET_KEY"
echo ""

# Step 4: Provide instructions
echo "📋 DEPLOYMENT CHECKLIST"
echo "======================="
echo ""
echo "Before deploying to Render:"
echo ""
echo "1. COMMIT YOUR CODE:"
echo "   git add ."
echo "   git commit -m 'Prepare for Render deployment'"
echo "   git push origin main"
echo ""
echo "2. GET YOUR GROQ_API_KEY:"
echo "   - Go to https://console.groq.com"
echo "   - Create an API key"
echo "   - Copy it (you'll need it in step 5)"
echo ""
echo "3. CREATE RENDER ACCOUNT:"
echo "   - Go to https://render.com"
echo "   - Sign up with GitHub"
echo "   - Authorize Render to access your repositories"
echo ""
echo "4. DEPLOY ON RENDER:"
echo "   - Click 'New +' → 'Web Service'"
echo "   - Connect your GitHub repository"
echo "   - Render will auto-detect render.yaml"
echo "   - Click 'Create Web Service'"
echo ""
echo "5. ADD ENVIRONMENT VARIABLES:"
echo "   - Backend Service → Environment"
echo "   - Add: GROQ_API_KEY=<your-key-from-step-2>"
echo "   - Add: SECRET_KEY=$SECRET_KEY"
echo "   - Click 'Save'"
echo ""
echo "6. DEPLOY STATIC FRONTEND (optional but recommended):"
echo "   - Click 'New +' → 'Static Site'"
echo "   - Connect same repository"
echo "   - Build Command: echo 'Static site'"
echo "   - Publish Directory: ."
echo "   - Click 'Create Static Site'"
echo ""
echo "7. UPDATE FRONTEND API URL:"
echo "   - In index.html, find the API_BASE line"
echo "   - Add to <head>: <script>window.API_URL = 'https://your-backend.onrender.com';</script>"
echo "   - Commit and push (static site auto-redeploys)"
echo ""
echo "8. TEST YOUR APP:"
echo "   - Visit your backend URL + /docs (e.g., https://lifedashboard-api.onrender.com/docs)"
echo "   - Visit your frontend URL"
echo "   - Create an account and test"
echo ""
echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Save this SECRET_KEY somewhere safe: $SECRET_KEY"
echo "2. Follow the deployment checklist above"
echo "3. Your app will be live in ~5-10 minutes!"
echo ""
