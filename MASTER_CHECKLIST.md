# MASTER DEPLOYMENT CHECKLIST

## Phase 1: Preparation (Already Done)
- [x] Create `.gitignore`
- [x] Create `backend/Procfile`
- [x] Create `railway.json`
- [x] Create `backend/.env.example`
- [x] Create `mobile/eas.json`
- [x] Create `mobile/app.json.prod` template

## Phase 2: Git & Repo
- [ ] Initialize git repo locally
- [ ] Create GitHub repo (private)
- [ ] Push code to GitHub

## Phase 3: Railway Backend
- [ ] Create Railway project from GitHub repo
- [ ] Deploy PostgreSQL database service
- [ ] Add Environment Variables (`SECRET_KEY`, `DATABASE_URL`, `CORS_ORIGINS`)
- [ ] Verify deployment success
- [ ] Copy public Railway URL (e.g. `https://xxx.up.railway.app`)

## Phase 4: Mobile App Production
- [ ] Update `mobile/app.json` with Railway URL
- [ ] Install EAS CLI (if not installed): `npm install -g eas-cli`
- [ ] Login to Expo: `eas login`
- [ ] Run build command: `npx eas build --platform android --profile production`
- [ ] Download APK file

## Phase 5: Verification & Demo
- [ ] Install APK on phone
- [ ] Test Registration
- [ ] Test Login
- [ ] Test Camera Scan & Prediction
- [ ] Verify Backend Logs in Railway
- [ ] Prepare Demo Script
