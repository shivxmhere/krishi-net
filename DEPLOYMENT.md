# ☁️ Deployment Guide: Krishi-Net API

This guide details how to deploy the Krishi-Net API to production environments.

## 🐋 Docker Deployment (Recommended)
Docker ensures the ML dependencies (TensorFlow) are consistent across environments.

### 1. Build Image
```bash
docker build -t krishi-net-api .
```

### 2. Run Container
```bash
docker run -p 8000:8000 --env-file .env krishi-net-api
```

---

## 🚀 Cloud Providers

### Railway / Render
1. Connect your GitHub repository.
2. Add Environment Variables (from your `.env`).
3. Set the Build Command: `pip install -r requirements.txt`
4. Set the Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Manual VPS (Ubuntu/Debian)
1. Install Python 3.11 and PostgreSQL.
2. Clone repository and install requirements.
3. Use **Gunicorn** with **Uvicorn workers**:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```
4. Use **Systemd** or **PM2** for process management.

---

## 🔒 Post-Deployment Checklist
- [ ] Change `SECRET_KEY` to a cryptographically strong string.
- [ ] Ensure `Debug=False` in production.
- [ ] Configure `CORS_ORIGINS` to point ONLY to your frontend URL.
- [ ] Set up SSL/TLS (HTTPS) via Nginx or Cloudflare.
- [ ] Monitor logs at `/var/log/syslog` or your cloud logger.

## 📊 Health Monitoring
The API provides an enhanced health check at:
`GET /health`

It returns status codes for the Database and ML Model availability.
