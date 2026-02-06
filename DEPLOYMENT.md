# 🚀 Deployment Guide - SmartBid Control Tower

## Quick Deploy Options

### Option 1: Railway (Recommended - Easiest)

**Backend + Database:**

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Deploy setup"
   git push origin main
   ```

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repo
   - Railway auto-detects `Dockerfile` and `railway.json`
   - Add services: PostgreSQL, Redis
   - Set environment variables:
     ```
     DATABASE_URL (auto-filled by Railway)
     REDIS_URL (auto-filled by Railway)
     SECRET_KEY=your-secret-key-here
     SYNC_PROCESSING=true
     ```

3. **Frontend on Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repo
   - Root Directory: `frontend`
   - Framework Preset: Vite
   - Environment Variables:
     ```
     VITE_API_URL=https://your-backend.railway.app
     ```

**✅ Auto-deployment enabled! Every push to main auto-deploys.**

---

### Option 2: Render

1. **Push to GitHub**

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - "New" → "Blueprint"
   - Connect GitHub repo
   - Render reads `render.yaml` automatically
   - Click "Apply"

**✅ Auto-deployment from `render.yaml` config.**

---

### Option 3: Docker + Your Own Server

**1. Build and Push Docker Images:**
```bash
# Backend
docker build -t smartbid-backend .
docker tag smartbid-backend your-registry/smartbid-backend
docker push your-registry/smartbid-backend

# Frontend
cd frontend
docker build -t smartbid-frontend .
docker tag smartbid-frontend your-registry/smartbid-frontend
docker push your-registry/smartbid-frontend
```

**2. On Your Server:**
```bash
# Clone repo
git clone https://github.com/your-username/rfp-automation.git
cd rfp-automation

# Create .env file
cp .env.template .env
# Edit .env with production values

# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Initialize database
docker exec smartbid-backend python shared/database/init_db.py
```

**3. Setup Auto-Deploy with Webhook:**
```bash
# On server, create deploy script
nano /home/deploy/auto-deploy.sh
```

```bash
#!/bin/bash
cd /home/deploy/rfp-automation
git pull origin main
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

**4. Setup GitHub Webhook:**
- Go to GitHub repo → Settings → Webhooks
- Add webhook: `http://your-server-ip:9000/hooks/deploy`
- Install webhook listener on server

---

## GitHub Actions Auto-Deploy

**Already configured in `.github/workflows/deploy.yml`**

### Setup Secrets:

Go to GitHub repo → Settings → Secrets and variables → Actions

Add these secrets:

**For Railway/Render:**
```
BACKEND_DEPLOY_HOOK = [Your deploy hook URL from Railway/Render]
```

**For Vercel:**
```
VERCEL_TOKEN = [Your Vercel API token]
VERCEL_ORG_ID = [Your Vercel org ID]
VERCEL_PROJECT_ID = [Your Vercel project ID]
VITE_API_URL = https://your-backend.railway.app
```

### How It Works:

1. **Push code to `main` branch**
2. **GitHub Actions runs automatically:**
   - Runs tests
   - Builds Docker images
   - Triggers deployment webhook
   - Deploys frontend to Vercel
3. **Website updates in ~2-3 minutes**

---

## Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
QDRANT_HOST=localhost
QDRANT_PORT=6333
SECRET_KEY=your-secret-key-minimum-32-chars
SYNC_PROCESSING=true
LOG_LEVEL=INFO
```

### Frontend (.env)
```bash
VITE_API_URL=https://your-backend-url.railway.app
```

---

## Post-Deployment

### 1. Initialize Database:
```bash
# If using Railway/Render - connect via SSH or web shell
python shared/database/init_db.py
```

### 2. Test API:
```bash
curl https://your-backend.railway.app/health
```

### 3. Test Frontend:
```
https://your-frontend.vercel.app
```

---

## Monitoring & Logs

**Railway:**
- Dashboard → Your Project → Deployments → View Logs

**Render:**
- Dashboard → Your Service → Logs

**Vercel:**
- Dashboard → Your Project → Deployments → View Function Logs

---

## Rollback

**Railway/Render:**
- Dashboard → Deployments → Click on previous deployment → "Redeploy"

**Manual:**
```bash
git revert HEAD
git push origin main
# GitHub Actions auto-deploys previous version
```

---

## Custom Domain

**Backend (Railway):**
1. Settings → Domains → Add Custom Domain
2. Add DNS record: `api.yourdomain.com` → Railway provided URL

**Frontend (Vercel):**
1. Settings → Domains → Add Domain
2. Add DNS record: `yourdomain.com` → Vercel provided URL

---

## Troubleshooting

**Deployment fails:**
```bash
# Check logs in Railway/Render dashboard
# Or GitHub Actions logs
```

**Database connection error:**
```bash
# Verify DATABASE_URL is set correctly
# Check database service is running
```

**Changes not reflecting:**
```bash
# Check if deployment succeeded in GitHub Actions
# Hard refresh browser: Ctrl+Shift+R
# Clear Vercel cache: vercel --force
```

---

## Cost Estimate (Free Tier)

- **Railway:** $5/month (free $5 credit) = FREE for small apps
- **Vercel:** FREE (100GB bandwidth, unlimited deploys)
- **Render:** FREE (PostgreSQL + Redis + Web Service)
- **GitHub Actions:** FREE (2000 minutes/month)

**Total: $0-5/month** 🎉

---

## Need Help?

1. Check logs in deployment platform
2. Review GitHub Actions workflow runs
3. Test locally with Docker first: `docker-compose -f docker-compose.prod.yml up`
