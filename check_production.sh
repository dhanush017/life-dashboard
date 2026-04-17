#!/usr/bin/env bash
# Production Readiness Verification Script

echo "🔍 Life Dashboard Production Readiness Check"
echo "=============================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python --version 2>&1)
echo "  $python_version"
echo ""

# Check required files
echo "✓ Checking required files..."
required_files=("main.py" "index.html" ".env.example" "requirements.txt" "start_production.py")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (MISSING)"
    fi
done
echo ""

# Check .env file
echo "✓ Checking .env configuration..."
if [ ! -f ".env" ]; then
    echo "  ⚠ .env file not found (copy from .env.example)"
    echo "  cp .env.example .env"
else
    echo "  ✓ .env file exists"
fi
echo ""

# Check environment variables
echo "✓ Checking critical environment variables..."
if [ -f ".env" ]; then
    if grep -q "your-groq-api-key-here" .env; then
        echo "  ✗ GROQ_API_KEY not set (still has default value)"
    else
        echo "  ✓ GROQ_API_KEY configured"
    fi
    
    if grep -q "your-super-secret-key-change-this" .env; then
        echo "  ✗ SECRET_KEY not set (still has default value)"
    else
        echo "  ✓ SECRET_KEY configured"
    fi
fi
echo ""

# Check for debug code
echo "✓ Checking for debug code..."
debug_files=("main.py" "ai_insights.py" "index.html")
debug_count=0

for file in "${debug_files[@]}"; do
    if grep -q "console.log\|console.error\|print(" "$file" 2>/dev/null; then
        echo "  ⚠ Found potential debug code in $file"
        ((debug_count++))
    fi
done

if [ $debug_count -eq 0 ]; then
    echo "  ✓ No obvious debug code found"
fi
echo ""

# Check requirements
echo "✓ Checking dependencies..."
if pip freeze 2>/dev/null | grep -q "fastapi"; then
    echo "  ✓ Dependencies appear to be installed"
else
    echo "  ⚠ Dependencies may not be installed"
    echo "  Run: pip install -r requirements.txt"
fi
echo ""

# Final status
echo "=============================================="
echo "✅ Pre-deployment checklist complete!"
echo ""
echo "Before deploying to production:"
echo "1. Verify all environment variables in .env"
echo "2. Test locally: python start_production.py"
echo "3. Check logs for any errors"
echo "4. Follow deployment guide: DEPLOYMENT_GUIDE.md"
echo ""
echo "Deploy to Railway (fastest):"
echo "  1. Push to GitHub"
echo "  2. Go to railway.app"
echo "  3. Connect your GitHub repo"
echo "  4. Add environment variables"
echo "  5. Railway does the rest! 🚀"
echo ""
