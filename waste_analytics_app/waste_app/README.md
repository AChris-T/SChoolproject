# ♻️ Hostel Waste Analytics & Prediction System
### TCE 528 — Waste Management Engineering · University of Ibadan

---

## 🚀 Quick Start (Local Development)

### 1. Install dependencies
```bash
cd waste_app
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```
The app will open automatically at `http://localhost:8501`

---

## 🌐 Deploy to Streamlit Cloud (Recommended)

### Option 1: Streamlit Cloud (Easiest - Free)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Deploy waste analytics app"
   git push origin main
   ```

2. **Deploy:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Select:
     - **Repository:** your-repo/waste_analytics_app
     - **Branch:** main
     - **Main file path:** waste_app/app.py
   - Click "Deploy"

3. **Your app is live!** Share the URL with your team

---

### Option 2: Docker Deployment

1. **Create `Dockerfile` in `waste_app/` directory:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   ENTRYPOINT ["streamlit", "run"]
   CMD ["app.py"]
   ```

2. **Build and run:**
   ```bash
   docker build -t waste-analytics .
   docker run -p 8501:8501 waste-analytics
   ```

3. **Deploy to services:**
   - **AWS ECS**, **Google Cloud Run**, **Azure Container Instances**
   - Push image to Docker Hub, then deploy from container

---

### Option 3: Heroku Deployment

1. **Create `Procfile` in root directory:**
   ```
   web: cd waste_app && streamlit run app.py
   ```

2. **Create `setup.sh` in `waste_app/`:**
   ```bash
   #!/bin/bash
   mkdir -p ~/.streamlit
   echo "[server]" > ~/.streamlit/config.toml
   echo "headless = true" >> ~/.streamlit/config.toml
   ```

3. **Deploy:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

---

## 📂 App Pages

| Page | What it does |
|---|---|
| 🏠 Overview | System intro, status summary, quick-start guide |
| 📊 Audit Analysis | Charts, composition, daily trends, per-capita table |
| 📋 Survey & Regression | MLR model, coefficients, p-values, awareness charts |
| 🔮 Predictor | Student profile predictor + hall-level forecast |
| 📥 Data Entry | Type records manually OR download blank templates |

---

## 📋 CSV Column Formats

### Audit Data (`audit_data.csv`)
| Column | Type | Description |
|---|---|---|
| `hall` | text | e.g. Awo, Tedder, Independence |
| `floor_block` | text | e.g. Floor 1, Block C |
| `date` | date | YYYY-MM-DD |
| `day_number` | int | 1–7 |
| `biodegradable_kg` | float | kg of food/organic waste |
| `non_biodegradable_kg` | float | kg of plastics/packaging |
| `recyclable_kg` | float | kg of recyclables |
| `hazardous_kg` | float | kg of hazardous items |
| `population` | int | Number of students on that floor/block |

### Survey Data (`survey_data.csv`)
| Column | Type | Coding |
|---|---|---|
| `respondent_id` | int | 1, 2, 3… |
| `hall` | text | Hall name |
| `level` | int | 100, 200, 300, 400, 500 |
| `meals_per_day` | int | 1, 2, or 3 |
| `packaged_food_frequency` | int | 0=Never, 1=Occasionally, 2=Often |
| `disposal_frequency_per_week` | int | 1–7 |
| `recycling_awareness` | int | 1–5 scale |
| `visitor_effect` | int | 0=No, 1=Yes |
| `separation_behaviour` | int | 0=Never … 4=Always |
| `waste_scale` | int | 1=Small, 2=Medium, 3=Large |

---

## 💡 Tips
- Enable **"Use built-in sample data"** in the sidebar to explore all features instantly
- Upload your own CSV/Excel files to replace the sample data
- Use the **Data Entry** page to type records one by one and download them as CSV or Excel
- Manually entered records are **merged** with uploaded data automatically
- The regression model needs **at least 8 complete survey rows** to run

---

## 🔬 Regression Model

The app fits a **Multiple Linear Regression (OLS)** using `statsmodels`:

```
Ŷ (waste scale) = β₀ + β₁·meals + β₂·packaged_food + β₃·disposal_freq
                     + β₄·awareness + β₅·visitor_effect + β₆·separation
```

The coefficient table shows β, standard error, t-statistic, and p-value for each predictor.
Rows highlighted in green are statistically significant (p < 0.05).

---

## 📦 Dependencies
- `streamlit` — web app framework
- `pandas` / `numpy` — data processing
- `plotly` — interactive charts
- `statsmodels` — OLS regression with full statistical output
- `scikit-learn` — supporting ML utilities
- `openpyxl` — Excel read/write
- `scipy` — statistical functions

---

## 🔧 Configuration

The app uses `.streamlit/config.toml` for Streamlit configuration:
- **Theme:** Dark mode with green accent (#48bb78)
- **Server mode:** Headless (suitable for cloud deployment)
- **Max upload size:** 200 MB

---

## 📧 Support
For issues or questions, contact the TCE 528 course instructors or submit an issue to the repository.
