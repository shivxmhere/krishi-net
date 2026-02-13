# 🛠️ Krishi-Net: Local Development Shakeout Guide

Before you deploy to Railway, use this guide to ensure your local environment is 100% functional.

---

## 1. Service Map (Default Ports)
- **Backend API**: `http://localhost:8080`
- **ML Service**: `http://localhost:8000`
- **Mobile (Metro)**: `http://localhost:8081`

---

## 2. Launch Sequence (Open 3 Terminals)

### Terminal 1: ML Service (Python)
```powershell
cd ml_service
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```
*Verify: Visit `http://localhost:8000/docs`*

### Terminal 2: Backend API (Node.js)
```powershell
cd backend
npm install
npx prisma generate
npm run dev
```
*Verify: Visit `http://localhost:8080/health`*

### Terminal 3: Mobile (Expo)
```powershell
cd mobile
npm install
npx expo start
```

---

## 3. Automated Health Check Script
I have created a script called `check_local.ps1` in the root folder. You can run it to verify if your services are visible.

**To run it**:
```powershell
.\check_local.ps1
```

---

## 4. Pre-Deployment Checklist
1. [ ] **Database**: Is your local Postgres running and `DATABASE_URL` set in `backend/.env`?
2. [ ] **ML Link**: Does the Backend console show "Connected to ML Service"?
3. [ ] **Mobile**: Is the `EXPO_PUBLIC_API_URL` in `mobile/.env` set to `http://YOUR_LOCAL_IP:8080`? (Note: `localhost` doesn't work on physical phones, use your IP).
4. [ ] **Permissions**: Did you run `npx prisma generate` after any schema changes?
