# 🚀 COMPLETE DEPLOYMENT GUIDE

## SECTION 1: PREPARATION FILES (Done ✅)
I have already created these critical files for you:
1. `C:\Users\shiva\Desktop\krishi-net\.gitignore`
2. `C:\Users\shiva\Desktop\krishi-net\backend\Procfile`
3. `C:\Users\shiva\Desktop\krishi-net\backend\.env.example` (With generated SECRET_KEY)
4. `C:\Users\shiva\Desktop\krishi-net\railway.json`
5. `C:\Users\shiva\Desktop\krishi-net\mobile\eas.json`
6. `C:\Users\shiva\Desktop\krishi-net\mobile\app.json.prod` (Template for production)

## SECTION 2: EXACT COMMAND SEQUENCE

### 2.1. Git Initialization
Run these commands in your project root:
```bash
cd C:\Users\shiva\Desktop\krishi-net
git init
git add .
git commit -m "Initial commit for production"
```

### 2.2. GitHub Repository Creation
1. Go to: [https://github.com/new](https://github.com/new)
2. **Repository name**: `krishi-net`
3. **Description**: "AI-powered crop disease detection system"
4. **Public/Private**: Private (recommended for interview)
5. **Do NOT** initialize with README, .gitignore, or License.
6. Click **Create repository**.

**Push commands** (copy from GitHub screen, or use these):
```bash
git remote add origin https://github.com/[YOUR-USERNAME]/krishi-net.git
git branch -M main
git push -u origin main
```

### 2.3. Railway Deployment
1. Go to: [https://railway.app/new](https://railway.app/new)
2. Select **"Deploy from GitHub repo"**.
3. Select `krishi-net`.
4. Click **"Deploy Now"**.

**Database Setup**:
1. In Railway project view, click **New > Database > PostgreSQL**.
2. Wait for it to deploy.
3. Click on the PostgreSQL service > **Connect** tab.
4. Copy the **DATABASE_URL**.

**Environment Variables**:
1. Go to `krishi-net-backend` service > **Variables** tab.
2. Add these (Values provided in Section 3):
   - `SECRET_KEY`
   - `DATABASE_URL` (Paste from PostgreSQL service)
   - `CORS_ORIGINS`
   - `PORT` (Railway sets this automatically, but you can set 8000 just in case)

**Model File**:
- Since `disease_model.h5` is <100MB, it was pushed to GitHub and will be deployed automatically.

### 2.4. Mobile App Configuration
Once Railway gives you a public URL (e.g., `https://krishi-net-production.up.railway.app`):
1. Open `C:\Users\shiva\Desktop\krishi-net\mobile\app.json.prod`.
2. Replace `[YOUR-RAILWAY-URL]` with your actual Railway URL.
3. **Copy content** of `app.json.prod` and **overwrite** `mobile/app.json`.

### 2.5. Production APK Build
Run these commands:
```bash
cd C:\Users\shiva\Desktop\krishi-net\mobile
npx eas build --platform android --profile production
```
- Select "Yes" to log in.
- Select "Yes" to generate Keystore.
- Wait for build to finish (approx. 15-20 mins).

### 2.6. Install APK
1. Expo will give you a download link (or check Expo dashboard).
2. Download `.apk` to your phone.
3. Install and run!

## SECTION 3: ENVIRONMENT VARIABLES

**SECRET_KEY**:
`9f8e7d6c5b4a32109876543210abcdef1234567890abcdef1234567890abcdef`

**DATABASE_URL**:
(Get this from Railway PostgreSQL service)

**CORS_ORIGINS**:
`["*"]`

## SECTION 4: RAILWAY CONFIGURATION
(Already handled by `railway.json` and `backend/Procfile`)
- Service Name: `krishi-net-backend`
- Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Build Command: `pip install -r backend/requirements.txt`

## SECTION 5: MODEL FILE HANDLING
**Recommended: Option A (Git)**
Your model is 10.4MB. GitHub limit is 100MB.
It is safely inside `backend/models/` (or wherever you placed it) and pushed to GitHub. No extra steps needed.

## SECTION 6: MOBILE APP BUILD
(See Section 2.5)

## SECTION 7: VERIFICATION CHECKLIST
1. [ ] **Backend**: Open Railway URL `/health`. Returns `{"status": "ok"}`?
2. [ ] **Docs**: Open Railway URL `/docs`. Swagger UI loads?
3. [ ] **App**: Download APK.
4. [ ] **Login**: Create account -> Success?
5. [ ] **Scan**: Take photo of plant -> Result appears?

## SECTION 8: TROUBLESHOOTING
- **"Application Error" on Railway**: Check `Deploy Logs`. If "Module not found", check `requirements.txt`.
- **"Network Error" on App**: Did you update `app.json` with **HTTPS** Railway URL? (http won't work well on prod).
- **"Model not found"**: Ensure path in Python matches file structure on GitHub.

## SECTION 9: FINAL COPY-PASTE COMMANDS
(See `QUICK_START.txt`)

## SECTION 10: DEMO PREPARATION
**Script**:
"Good morning. This is Krishi-Net, an AI solution for farmers.
1. **Frontend**: React Native app for scanning crops.
2. **Backend**: FastAPI server processing images with TensorFlow.
3. **Demo**: I will now scan this tomato leaf..."
(Scan photo)
"As you can see, it detects 'Early Blight' with 98% confidence and suggests treatment..."

**Backup**:
If live demo fails, have a recorded video or screenshots ready in a folder `DEMO_ASSETS`.
