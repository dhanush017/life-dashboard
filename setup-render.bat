@echo off
REM Render.com Deployment Setup for Life Dashboard (Windows)
REM This script prepares your repository for Render deployment

setlocal enabledelayedexpansion
set SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%

echo.
echo 🚀 Life Dashboard — Render Deployment Setup
echo =============================================
echo.

REM Step 1: Verify requirements
echo ✓ Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git not found. Please install Git
    pause
    exit /b 1
)

echo ✓ Python and Git installed
echo.

REM Step 2: Create render.yaml
echo 📝 Creating render.yaml for deployment...
(
echo services:
echo   - type: web
echo     name: lifedashboard-api
echo     env: python
echo     buildCommand: pip install -r requirements.txt
echo     startCommand: gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app
echo     plan: free
echo     envVars:
echo       - key: ENVIRONMENT
echo         value: production
echo       - key: DATABASE_URL
echo         fromDatabase:
echo           name: lifedashboard-db
echo           property: connectionString
echo       - key: GROQ_API_KEY
echo         sync: false
echo       - key: SECRET_KEY
echo         sync: false
echo       - key: CORS_ORIGINS
echo         value: ${RENDER_EXTERNAL_URL}
echo.
echo   - type: pserv
echo     name: lifedashboard-db
echo     ipAllowList: []
echo     plan: free
echo     region: oregon
) > render.yaml

echo ✓ render.yaml created
echo.

REM Step 3: Generate SECRET_KEY
echo 🔑 Generating SECRET_KEY...
for /f "delims=" %%i in ('python -c "import secrets; print(secrets.token_urlsafe(32))"') do set SECRET_KEY=%%i
echo Generated SECRET_KEY: %SECRET_KEY%
echo.

REM Step 4: Provide instructions
echo 📋 DEPLOYMENT CHECKLIST
echo =======================
echo.
echo Before deploying to Render:
echo.
echo 1. COMMIT YOUR CODE:
echo    git add .
echo    git commit -m "Prepare for Render deployment"
echo    git push origin main
echo.
echo 2. GET YOUR GROQ_API_KEY:
echo    - Go to https://console.groq.com
echo    - Create an API key
echo    - Copy it (you'll need it in step 5)
echo.
echo 3. CREATE RENDER ACCOUNT:
echo    - Go to https://render.com
echo    - Sign up with GitHub
echo    - Authorize Render to access your repositories
echo.
echo 4. DEPLOY ON RENDER:
echo    - Click 'New +' ^> 'Web Service'
echo    - Connect your GitHub repository
echo    - Render will auto-detect render.yaml
echo    - Click 'Create Web Service'
echo.
echo 5. ADD ENVIRONMENT VARIABLES:
echo    - Backend Service ^> Environment
echo    - Add: GROQ_API_KEY=^<your-key-from-step-2^>
echo    - Add: SECRET_KEY=%SECRET_KEY%
echo    - Click 'Save'
echo.
echo 6. DEPLOY STATIC FRONTEND (optional but recommended):
echo    - Click 'New +' ^> 'Static Site'
echo    - Connect same repository
echo    - Build Command: echo 'Static site'
echo    - Publish Directory: .
echo    - Click 'Create Static Site'
echo.
echo 7. UPDATE FRONTEND API URL:
echo    - In index.html, find the API_BASE line
echo    - Add to ^<head^>: ^<script^>window.API_URL = 'https://your-backend.onrender.com';^</script^>
echo    - Commit and push (static site auto-redeploys)
echo.
echo 8. TEST YOUR APP:
echo    - Visit your backend URL + /docs (e.g., https://lifedashboard-api.onrender.com/docs)
echo    - Visit your frontend URL
echo    - Create an account and test
echo.
echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Save this SECRET_KEY somewhere safe: %SECRET_KEY%
echo 2. Follow the deployment checklist above
echo 3. Your app will be live in ~5-10 minutes!
echo.
pause
