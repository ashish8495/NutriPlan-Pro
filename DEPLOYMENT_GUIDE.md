# 🚀 Public Cloud Deployment Guide for NutriPlan Pro

Deploy **NutriPlan Pro** to a live public URL on the web for free so you can start sharing it with initial users, collecting feedback, and acquiring your first audience.

---

## 🌟 Method 1: Streamlit Community Cloud (Recommended & Easiest — 2 Minutes, 100% Free)

Streamlit Community Cloud is designed specifically for Streamlit apps. It provides:
- **Free permanent hosting** with a public HTTPS link (e.g. `https://nutriplan-pro.streamlit.app`).
- **Auto-deployment**: Every time you push a change to your GitHub repo, the live app updates automatically.

### Step 1: Push your project to GitHub
Open your terminal in `c:\Users\000M0E744\Desktop\Diet` and run:

```bash
# 1. Initialize git (if not already done)
git init

# 2. Add and commit all files
git add .
git commit -m "feat: public cloud deployment release"

# 3. Create main branch
git branch -M main

# 4. Link your GitHub repository (create an empty repo on github.com first)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/NutriPlan-Pro.git

# 5. Push to GitHub
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)** and click **"Continue with GitHub"**.
2. Click the blue **"New app"** button.
3. Fill in the three fields:
   - **Repository:** `YOUR_GITHUB_USERNAME/NutriPlan-Pro`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
4. Click **"Deploy!"**
5. Within 60 seconds, your application will be live at:
   ```
   https://YOUR_APP_NAME.streamlit.app
   ```
6. You can customize the URL under **Settings &rarr; General &rarr; App URL** (e.g., `https://nutriplan-pro.streamlit.app`).

---

## ⚡ Method 2: Render.com (100% Free Web Service)

Render allows you to host both the Streamlit app or the Flask version with a public URL (e.g. `https://nutriplan-pro.onrender.com`).

### Steps:
1. Sign up for free at **[render.com](https://render.com)**.
2. Click **"New +" &rarr; "Web Service"**.
3. Connect your GitHub repository (`NutriPlan-Pro`).
4. Configure the settings:
   - **Name:** `nutriplan-pro`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command (for Streamlit):**
     ```bash
     streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
     ```
     *(Or for Flask: `gunicorn app:app`)*
   - **Plan:** Select **Free**.
5. Click **"Deploy Web Service"**.

---

## 🤗 Method 3: Hugging Face Spaces (100% Free)

1. Create a free account at **[huggingface.co](https://huggingface.co)**.
2. Click **"New Space"**.
3. Set **Space SDK** to **Streamlit**.
4. Set Space name (e.g., `nutriplan-pro`).
5. Push your files or connect your GitHub repository.
6. Your app is immediately live at `https://huggingface.co/spaces/YOUR_USERNAME/nutriplan-pro`.

---

## 🔗 Method 4: Instant Temporary Public Link (Live in 10 Seconds from Local)

If you want to immediately share a live link with someone right now without uploading to GitHub first:

Using **Localtunnel** (Node.js) or **Cloudflare Tunnel**:
```bash
# If using npx (Node.js installed):
npx localtunnel --port 5000
```
This gives you an instant temporary public URL (e.g., `https://bright-nutri-plan.loca.lt`) pointing directly to your running application.

---

## 📈 Post-Deployment Checklist for Public Sharing

- [ ] **Custom Domain**: Connect your own domain (e.g., `nutriplan.fit` or `myhighproteindiet.com`) under Streamlit or Render Custom Domain settings.
- [ ] **Google Analytics / PostHog**: Add a simple tracking snippet in `templates/index.html` or Streamlit to monitor user visits and goal completions.
- [ ] **Feedback Link**: Add a small feedback form (Google Form / Tally.so) in the sidebar to collect what initial users think of their meal plans.
