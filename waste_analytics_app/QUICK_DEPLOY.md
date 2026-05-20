# 🚀 Deployment Quick Reference

## One-Line Deployment Commands

### Streamlit Cloud (Recommended)
```bash
git push origin main
# Then go to: https://share.streamlit.io and deploy
```

### Docker (Local)
```bash
docker build -t waste-analytics . && docker run -p 8501:8501 waste-analytics
```

### Docker Compose
```bash
docker-compose up
```

### Local Python
```bash
pip install -r waste_app/requirements.txt && streamlit run waste_app/app.py
```

### Quick Start Scripts
```bash
# Linux/Mac
chmod +x start.sh && ./start.sh

# Windows
start.bat
```

---

## Cloud Provider Quick Links

| Provider | Command | Cost | Docs |
|----------|---------|------|------|
| **Streamlit Cloud** | See README | Free | [link](https://docs.streamlit.io/deploy) |
| **Google Cloud Run** | `gcloud run deploy` | $0.00002/request | [link](https://cloud.google.com/run/docs) |
| **AWS Lambda** | AWS CLI or Console | Pay per invocation | [link](https://aws.amazon.com/lambda/) |
| **Azure** | `az container create` | $0.0000014/sec | [link](https://azure.microsoft.com/services/container-instances/) |
| **Heroku** | `git push heroku main` | $5-50/month | [link](https://devcenter.heroku.com/) |

---

## Pre-Deployment Checklist

- [ ] Updated Python to 3.9+
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Tested locally: `streamlit run app.py`
- [ ] All pages load without errors
- [ ] CSV upload works
- [ ] Charts display correctly
- [ ] Dark theme appears as intended
- [ ] Created `.env` file (if needed)
- [ ] Pushed to GitHub (for Streamlit Cloud)

---

## File Reference

| File | Purpose | Location |
|------|---------|----------|
| `Dockerfile` | Docker image config | Root |
| `docker-compose.yml` | Local Docker dev | Root |
| `Procfile` | Heroku deployment | Root |
| `.streamlit/config.toml` | Streamlit settings | waste_app/.streamlit/ |
| `.env.example` | Environment template | Root |
| `DEPLOYMENT.md` | Full deployment guide | Root |
| `UPDATES.md` | Summary of changes | Root |
| `README.md` | App documentation | waste_app/ |

---

## Most Popular Deployments

### 1️⃣ Streamlit Cloud (Best for Teams)
- ✅ Free tier
- ✅ Auto-deploy on push
- ✅ Easy to share
- **Setup:** 5 min

### 2️⃣ Docker + Cloud Run (Best for Scale)
- ✅ Production-ready
- ✅ Highly scalable
- ✅ Pay-per-request
- **Setup:** 15 min

### 3️⃣ Local Server (Best for Testing)
- ✅ No cost
- ✅ Full control
- ✅ Easy debugging
- **Setup:** 2 min

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Port 8501 in use | `lsof -i :8501` then kill process |
| Docker build fails | `docker build --no-cache .` |
| Slow app startup | Use Docker cache or Streamlit Cloud |

---

For detailed instructions, see `DEPLOYMENT.md` in the root directory.

**Happy deploying! 🎉**
