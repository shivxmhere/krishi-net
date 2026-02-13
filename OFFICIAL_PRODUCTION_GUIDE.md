# 🚀 Krishi-Net: Official Production Deployment Guide

This guide provides a step-by-step, from-scratch roadmap to deploy the entire Krishi-Net ecosystem (Backend, ML Microservice, PostgreSQL, and Mobile App) for public use.

---

## 📋 Phase 1: Local Tooling & Account Setup
Ensure you have the following installed and accounts created:
1. **GitHub**: [Create an account](https://github.com)
2. **Railway**: [Create an account](https://railway.app)
3. **Expo/EAS**: [Create an account](https://expo.dev)
4. **Git**: Installed locally.
5. **Node.js & npm**: Installed locally.

---

## 🛠️ Phase 2: Git Initialization
Deploying to Railway is easiest via GitHub. Run these in the root `krishi-net` folder:

```bash
git init
git add .
git commit -m "feat: production ready audit complete"
```

1. Create a **Private** repository on GitHub named `krishi-net`.
2. Link and push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/krishi-net.git
git branch -M main
git push -u origin main
```

---

## ☁️ Phase 3: Railway Infrastructure Provisioning
1. Login to **Railway.app**.
2. Click **New Project** > **Deploy from GitHub repo**.
3. Select your `krishi-net` repository.
4. **IMPORTANT**: Railway will detect the root. We need to define two services and a database.

### 3.1 Provisioning the Postgres Database
1. In your project dashboard, click **+ New** > **Database** > **Add PostgreSQL**.
2. Once deployed, click on the **PostgreSQL** service > **Variables** tab.
3. Copy the `DATABASE_URL`. You will need this for the Backend.

---

## 🔑 Phase 4: Environment Variables (The Key Step)
You need to configure variables for BOTH services.

### 4.1 ML Service (Microservice)
1. Go to the service running your `ml_service` code.
2. In the **Variables** tab, ensure no specific variables are required (unless you added custom ones). 
3. Note down the **Public Networking URL** Railway generates for this service (e.g., `https://ml-service-production.up.railway.app`).

### 4.2 Backend API (Node.js)
1. Go to the service running your `backend` code.
2. Add these variables:
   - `NODE_ENV`: `production`
   - `PORT`: `8080` (Railway injects this, but keep it explicit if needed)
   - `DATABASE_URL`: (Paste from Step 3.1)
   - `JWT_SECRET`: (Generate a long random string: at least 32 chars)
   - `ML_SERVICE_URL`: (Paste the URL from Step 4.1)
   - `ALLOWED_ORIGINS`: `*` (Or your eventual web domain)

---

## 📦 Phase 5: Build & Start Configuration
The project already contains `Procfile` and `railway.json`. Railway should automatically detect these:

- **Backend**: Uses `npm start` (defined in `backend/package.json`).
- **ML Service**: Uses `uvicorn main:app --host 0.0.0.0 --port $PORT`.

---

## 📱 Phase 6: Mobile App Configuration
Before building the APK, point the app to your real backend.

1. Locate `mobile/src/services/apiClient.ts`.
2. Ensure `API_URL` uses the **Backend Railway URL** (not the ML URL).
   - Alternatively, set `EXPO_PUBLIC_API_URL` in your `.env` or EAS Secrets:
   `EXPO_PUBLIC_API_URL=https://backend-production.up.railway.app`

---

## 🏗️ Phase 7: EAS Production Build (Android APK)
From the `mobile/` directory:

1. **Install EAS CLI**: `npm install -g eas-cli`
2. **Login**: `eas login`
3. **Configure**: `eas build:configure`
4. **Build APK**:
   ```bash
   eas build -p android --profile preview
   ```
   *Note: Using the `preview` profile generates an installable `.apk` file instead of an `.aab` for the store.*

---

## ✅ Phase 8: Final Verification
1. **Health Check**: Visit `https://YOUR_BACKEND_URL/health`. It should return `{"status": "ok"}`.
2. **ML Link**: Ensure the backend shows no errors in logs when communicating with the ML service.
3. **App Test**: Install the APK, register a new user, and perform a crop scan.

---

### 🆘 Troubleshooting
- **Database Connection Error**: Ensure the backend's `DATABASE_URL` matches the PostgreSQL service exactly.
- **Model Loading Error**: Ensure `disease_model.h5` is located within the `ml_service/model/` folder in your GitHub repo.
- **CORS Error**: Double-check `ALLOWED_ORIGINS` in Railway variables.
