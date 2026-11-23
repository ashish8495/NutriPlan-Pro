# 🥗 NutriPlan Pro

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![CI Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/)

**NutriPlan Pro** is an open-source, evidence-based nutrition calculation and meal planning engine built with **Streamlit** and **Python**. It computes personalized metabolic targets (**BMR, TDEE, Safe Deficit**) and generates 7-day **Low-Calorie, High-Protein, High-Fiber** weekly meal plans with exact portions, recipe instructions, interactive charts, and grocery checklists.

---

## 🌟 Key Features

- **⚡ Clinical Metabolic Engine**:
  - **BMR Calculation**: Mifflin-St Jeor equation (*American Journal of Clinical Nutrition*).
  - **TDEE & Physical Activity Levels**: WHO / FAO PAL activity multipliers.
  - **Controlled Caloric Deficit**: Safe 20–22% deficit designed for fat loss while preventing muscle loss.
  - **High-Protein Target**: 1.8–2.2g per kg body weight (~35% of total calories) based on ISSN consensus.
  - **Fiber & Micronutrient Support**: 30–38g daily fiber target for gut microbiome and glycemic control.
  - **BMI & Healthy Weight Classification**.
  - **Daily Hydration Recommendation** based on body mass and exercise.

- **📅 7-Day Interactive Meal Schedule**:
  - Monday to Sunday: **Breakfast, Lunch, Evening Snack, Dinner**.
  - Detailed macros (Calories, Protein, Carbs, Fiber, Fat) and cooking steps per meal.
  - **"🔄 Swap Meal"** feature to dynamically rotate recipes inside the app.

- **📊 Visual Analytics**:
  - Interactive Macronutrient ratio doughnut chart (*Plotly*).
  - Energy balance breakdown bar chart (*BMR vs TDEE vs Target*).

- **🛒 Smart Grocery Shopping List**:
  - Auto-aggregates and sums all raw ingredients across the entire 7-day schedule with interactive checklists.

- **📥 Export Capabilities**:
  - One-click **CSV Spreadsheet Export** for diet tracking.
  - Printable layout for PDF export.

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/NutriPlan-Pro.git
cd NutriPlan-Pro
```

### 2. Create a virtual environment & install requirements
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Launch the Streamlit App
```bash
streamlit run streamlit_app.py
```
The application will open automatically in your browser at `http://localhost:8501`.

---

## ☁️ Deploy to Streamlit Community Cloud (Free in 1 Click)

You can deploy this open-source application to the web for free using [Streamlit Community Cloud](https://streamlit.io/cloud):

1. **Push this repo to GitHub** (see instructions below).
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with your GitHub account.
3. Click **"New app"**.
4. Select your repository, branch (`main`), and set the main file path to:
   ```
   streamlit_app.py
   ```
5. Click **"Deploy!"** &mdash; your app will be live with a public URL in seconds!

---

## 🐙 Step-by-Step GitHub Setup Guide

To publish this project to your GitHub account:

```bash
# 1. Initialize git
git init

# 2. Stage and commit files
git add .
git commit -m "feat: initial open-source release of NutriPlan Pro"

# 3. Rename branch to main
git branch -M main

# 4. Add your GitHub remote repository
git remote add origin https://github.com/YOUR_USERNAME/NutriPlan-Pro.git

# 5. Push to GitHub
git push -u origin main
```

---

## 📂 Repository Structure

```
NutriPlan-Pro/
├── streamlit_app.py        # Streamlit web application
├── app.py                  # Flask REST API backend
├── nutrition_engine.py     # Core metabolic calculations & meal database
├── generate_sources_doc.py # Word doc generator for clinical sources
├── NutriPlan_Pro_Scientific_Sources_and_Methodology.docx
├── requirements.txt        # Dependencies (Streamlit, Plotly, Pandas, etc.)
├── LICENSE                 # MIT Open Source License
├── CONTRIBUTING.md         # Guidelines for open source contributors
├── README.md               # Project documentation
├── .streamlit/
│   └── config.toml         # Streamlit UI theme configuration
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions continuous integration test runner
├── templates/
│   └── index.html          # Standalone HTML5 web interface
├── static/                 # Static assets (CSS, JS)
└── tests/
    └── test_nutrition.py   # Automated unit tests
```

---

## 🧪 Running Unit Tests

Run the full automated test suite:
```bash
python -m unittest discover -s tests -v
```

---

## 📚 Scientific References

- **Mifflin-St Jeor Equation**: *Am J Clin Nutr* 1990; 51:241-247.
- **Protein & Exercise Stand**: *J Int Soc Sports Nutr* 2017; 14:20.
- **Physical Activity Energy Requirements**: *WHO Technical Report Series 935*.
- **Food Composition Data**: *USDA FoodData Central (FDC)*.

---

## 🤝 Contributing

Contributions are welcome! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for details on submitting pull requests and reporting issues.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.
