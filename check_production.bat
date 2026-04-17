@echo off
REM Production Readiness Verification Script for Windows

echo.
echo 🔍 Life Dashboard Production Readiness Check
echo ============================================
echo.

REM Check Python version
echo ✓ Checking Python version...
python --version
echo.

REM Check required files
echo ✓ Checking required files...
for %%F in (main.py index.html .env.example requirements.txt start_production.py) do (
    if exist "%%F" (
        echo   ✓ %%F
    ) else (
        echo   ✗ %%F ^(MISSING^)
    )
)
echo.

REM Check .env file
echo ✓ Checking .env configuration...
if not exist ".env" (
    echo   ⚠ .env file not found
    echo   cp .env.example .env
) else (
    echo   ✓ .env file exists
)
echo.

REM Final status
echo ============================================
echo ✅ Pre-deployment checklist complete!
echo.
echo Before deploying to production:
echo 1. Verify all environment variables in .env
echo 2. Test locally: python start_production.py
echo 3. Check logs for any errors
echo 4. Follow deployment guide: DEPLOYMENT_GUIDE.md
echo.
echo Deploy to Railway ^(fastest^):
echo   1. Push to GitHub
echo   2. Go to railway.app
echo   3. Connect your GitHub repo
echo   4. Add environment variables
echo   5. Railway does the rest! 🚀
echo.
pause
