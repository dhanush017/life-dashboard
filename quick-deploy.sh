#!/usr/bin/env bash
# Quick Deploy Script - Copy & paste these commands

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

clear
echo -e "${BLUE}🚀 Life Dashboard - Quick Deploy Guide${NC}"
echo "========================================"
echo ""

# Step 1: Verify setup
echo -e "${YELLOW}Step 1: Verify Setup${NC}"
echo "Running pre-deployment checks..."
echo ""

if command -v git &> /dev/null; then
    echo -e "${GREEN}✓${NC} Git installed"
else
    echo -e "${YELLOW}⚠${NC} Git not found - please install it"
    exit 1
fi

if command -v python &> /dev/null; then
    python_version=$(python --version 2>&1)
    echo -e "${GREEN}✓${NC} $python_version"
else
    echo -e "${YELLOW}⚠${NC} Python not found"
    exit 1
fi

echo ""

# Step 2: Generate SECRET_KEY
echo -e "${YELLOW}Step 2: Generate SECRET_KEY${NC}"
echo "Run this command and copy the output:"
echo ""
echo -e "${BLUE}python -c \"import secrets; print(secrets.token_urlsafe(32))\"${NC}"
echo ""
read -p "Paste your generated SECRET_KEY here: " SECRET_KEY
if [ -z "$SECRET_KEY" ]; then
    echo -e "${YELLOW}⚠${NC} SECRET_KEY is empty!"
    exit 1
fi
echo -e "${GREEN}✓${NC} SECRET_KEY saved"
echo ""

# Step 3: Get GROQ_API_KEY
echo -e "${YELLOW}Step 3: Get GROQ_API_KEY${NC}"
echo "Go to https://console.groq.com and get your API key"
echo ""
read -p "Paste your GROQ_API_KEY here: " GROQ_API_KEY
if [ -z "$GROQ_API_KEY" ]; then
    echo -e "${YELLOW}⚠${NC} GROQ_API_KEY is empty!"
    exit 1
fi
echo -e "${GREEN}✓${NC} GROQ_API_KEY saved"
echo ""

# Step 4: Create .env file
echo -e "${YELLOW}Step 4: Creating .env file${NC}"
cat > .env << EOF
ENVIRONMENT=production
GROQ_API_KEY=$GROQ_API_KEY
SECRET_KEY=$SECRET_KEY
DATABASE_URL=sqlite:///./life_dashboard.db
CORS_ORIGINS=http://localhost:3000
PORT=8000
WORKERS=4
EOF

if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env file created"
else
    echo -e "${YELLOW}⚠${NC} Failed to create .env"
    exit 1
fi
echo ""

# Step 5: Install dependencies
echo -e "${YELLOW}Step 5: Installing dependencies${NC}"
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Dependencies installed"
else
    echo -e "${YELLOW}⚠${NC} Failed to install dependencies"
    exit 1
fi
echo ""

# Step 6: Test locally
echo -e "${YELLOW}Step 6: Quick local test${NC}"
echo "Starting server for 10 seconds..."
timeout 10 python start_production.py &
sleep 5

if curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Server responds correctly"
else
    echo -e "${YELLOW}⚠${NC} Server test inconclusive"
fi
echo ""

# Step 7: Initialize Git repo
echo -e "${YELLOW}Step 7: Initializing Git Repository${NC}"
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Life Dashboard - Production ready"
    echo -e "${GREEN}✓${NC} Git repository initialized"
else
    echo -e "${GREEN}✓${NC} Git repository already exists"
fi
echo ""

# Step 8: Show deployment options
echo -e "${YELLOW}Step 8: Choose Deployment Platform${NC}"
echo ""
echo "1) Railway (Recommended - Easiest)"
echo "2) Render (Free alternative)"
echo "3) DigitalOcean"
echo "4) Manual (View instructions)"
echo ""
read -p "Choose (1-4): " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}Railway Deployment:${NC}"
        echo "1. Go to https://railway.app/dashboard"
        echo "2. Click 'New Project' → 'Deploy from GitHub'"
        echo "3. Select your repository"
        echo "4. Add environment variables:"
        echo "   - ENVIRONMENT: production"
        echo "   - GROQ_API_KEY: $GROQ_API_KEY"
        echo "   - SECRET_KEY: (your generated key)"
        echo "5. Railway automatically adds PostgreSQL"
        echo "6. Click deploy!"
        echo ""
        echo "Your domain: https://your-app-name.railway.app"
        ;;
    2)
        echo ""
        echo -e "${BLUE}Render Deployment:${NC}"
        echo "1. Go to https://dashboard.render.com"
        echo "2. Click 'New +' → 'Web Service'"
        echo "3. Connect your GitHub repo"
        echo "4. Fill in:"
        echo "   - Name: life-dashboard"
        echo "   - Build: pip install -r requirements.txt"
        echo "   - Start: python start_production.py"
        echo "5. Add environment variables"
        echo "6. Click 'Create Web Service'"
        echo ""
        echo "Your domain: https://life-dashboard.onrender.com"
        ;;
    3)
        echo ""
        echo -e "${BLUE}DigitalOcean Deployment:${NC}"
        echo "1. Create account at digitalocean.com"
        echo "2. Create App Platform app"
        echo "3. Connect GitHub repository"
        echo "4. Add PostgreSQL database"
        echo "5. Set environment variables"
        echo "6. Deploy!"
        ;;
    4)
        echo ""
        echo "See DEPLOYMENT_GUIDE.md for detailed instructions"
        ;;
esac

echo ""
echo -e "${GREEN}✓${NC} Setup complete!"
echo ""
echo "📚 Documentation:"
echo "  - PRODUCTION_READY.md - Full deployment guide"
echo "  - DEPLOYMENT_GUIDE.md - Platform-specific instructions"
echo "  - .env.example - Environment variable template"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Push to GitHub: git push -u origin main"
echo "2. Go to your chosen platform"
echo "3. Connect your repo"
echo "4. Add environment variables"
echo "5. Deploy! 🚀"
echo ""
