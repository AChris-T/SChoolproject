# 🚀 Deployment Guide

## Quick Overview

This guide covers multiple deployment options for the Hostel Waste Analytics app. Choose the one that best fits your needs.

---

## 📋 Prerequisites

- Python 3.9+
- Git
- Docker (optional, for Docker deployments)
- GitHub account (for Streamlit Cloud)

---

## 🌐 Option 1: Streamlit Cloud (Recommended - Free & Easiest)

**Best for:** Quick deployment, team sharing, automatic updates

### Step 1: Push to GitHub

```bash
cd /path/to/waste_analytics_app
git init
git add .
git commit -m "Initial commit: Waste Analytics App"
git remote add origin https://github.com/YOUR_USERNAME/waste_analytics_app.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect with GitHub
4. Fill in:
   - **Repository:** YOUR_USERNAME/waste_analytics_app
   - **Branch:** main
   - **Main file path:** waste_app/app.py
5. Click "Deploy"

### Step 3: Configure Secrets (Optional)

1. In Streamlit Cloud, go to your app's settings
2. Add any API keys or secrets to "Secrets"
3. They'll be available in `st.secrets` in your app

**Pros:**
- ✅ Free tier available
- ✅ Automatic deployments on push
- ✅ Custom domain support
- ✅ No infrastructure to manage

**Cons:**
- ⚠️ Limited to Streamlit Cloud's resources
- ⚠️ Public by default (can be made private)

---

## 🐳 Option 2: Docker (Recommended - Production)

**Best for:** Production, self-hosted servers, full control

### Step 1: Build Docker Image

```bash
cd /path/to/waste_analytics_app
docker build -t waste-analytics:latest .
```

### Step 2: Run Locally

```bash
docker run -p 8501:8501 waste-analytics:latest
```

Visit `http://localhost:8501`

### Step 3: Deploy to Cloud

#### **AWS ECS:**
```bash
# Push to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker tag waste-analytics:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/waste-analytics:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/waste-analytics:latest
```

#### **Google Cloud Run:**
```bash
# Push to Google Container Registry
docker tag waste-analytics:latest gcr.io/YOUR_PROJECT/waste-analytics
docker push gcr.io/YOUR_PROJECT/waste-analytics

# Deploy
gcloud run deploy waste-analytics \
  --image gcr.io/YOUR_PROJECT/waste-analytics \
  --platform managed \
  --region us-central1 \
  --port 8501
```

#### **Azure Container Instances:**
```bash
# Push to Azure Container Registry
az acr login --name YOUR_REGISTRY
docker tag waste-analytics:latest YOUR_REGISTRY.azurecr.io/waste-analytics
docker push YOUR_REGISTRY.azurecr.io/waste-analytics

# Deploy
az container create \
  --resource-group myResourceGroup \
  --name waste-analytics \
  --image YOUR_REGISTRY.azurecr.io/waste-analytics \
  --ports 8501 \
  --cpu 2 --memory 1
```

#### **Docker Hub:**
```bash
docker tag waste-analytics:latest YOUR_USERNAME/waste-analytics
docker login
docker push YOUR_USERNAME/waste-analytics
```

**Pros:**
- ✅ Consistent across environments
- ✅ Easy scaling
- ✅ Full control
- ✅ Works on any cloud provider

**Cons:**
- ⚠️ Requires Docker knowledge
- ⚠️ Some infrastructure costs

---

## 🚢 Option 3: Heroku (Easy - Free tier ended, but still affordable)

**Best for:** Quick deployment, simple hosting

### Step 1: Set Up Heroku

```bash
# Install Heroku CLI
# On Windows: https://devcenter.heroku.com/articles/heroku-cli

heroku login
heroku create your-app-name
```

### Step 2: Deploy

```bash
cd /path/to/waste_analytics_app
git push heroku main
```

### Step 3: View Logs

```bash
heroku logs --tail
```

**Pros:**
- ✅ Git-based deployments
- ✅ Simple CLI
- ✅ Good documentation

**Cons:**
- ⚠️ Paid dyno hours required
- ⚠️ Slower startup times

---

## 💻 Option 4: Local Server (Linux/Windows/Mac)

**Best for:** Testing, development, internal use

### Linux (Ubuntu/Debian):

```bash
# Install Python 3.11
sudo apt-get update
sudo apt-get install python3.11 python3-pip python3-venv

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r waste_app/requirements.txt

# Run app
streamlit run waste_app/app.py
```

### Windows (PowerShell):

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r waste_app\requirements.txt

# Run app
streamlit run waste_app\app.py
```

### Mac:

```bash
# Using Homebrew
brew install python@3.11

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r waste_app/requirements.txt

# Run app
streamlit run waste_app/app.py
```

---

## 🐳 Option 5: Docker Compose (Development)

**Best for:** Local development, easy setup

```bash
cd /path/to/waste_analytics_app
docker-compose up
```

Visit `http://localhost:8501`

---

## 🔐 Environment Variables

Create a `.env` file (never commit to git):

```env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

Reference: `.env.example`

---

## 📊 Choosing Your Deployment Option

| Option | Cost | Setup | Best For |
|--------|------|-------|----------|
| **Streamlit Cloud** | Free | ⭐⭐ | Quick demos, team sharing |
| **Docker + AWS/GCP/Azure** | $5-50/month | ⭐⭐⭐ | Production, scalability |
| **Heroku** | Free-$7/month | ⭐⭐ | Small projects |
| **Local Server** | $0 | ⭐ | Development, testing |
| **Docker Compose** | $0 | ⭐⭐ | Local development |

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] App loads without errors
- [ ] File upload works (CSV/Excel)
- [ ] Data analysis charts render
- [ ] Download buttons work
- [ ] All pages navigate correctly
- [ ] Styling displays properly (dark mode)
- [ ] Regression analysis runs with sample data

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Linux/Mac: Find process on port 8501
lsof -i :8501
kill -9 <PID>

# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### ModuleNotFoundError
```bash
pip install -r requirements.txt --upgrade
```

### Streamlit Caching Issues
```bash
streamlit cache clear
streamlit run app.py
```

### Docker Build Fails
```bash
docker build --no-cache -t waste-analytics:latest .
```

---

## 📞 Support

For deployment issues:
1. Check [Streamlit Docs](https://docs.streamlit.io/deploy)
2. Check [Docker Docs](https://docs.docker.com/)
3. Review logs: `streamlit run app.py --logger.level=debug`
4. Contact course instructors (TCE 528)

---

**Last Updated:** 2025-05-20
