# Thathvamasi Corporate Web Platform - Production Deployment Guide

This guide details instructions for deploying the Thathvamasi client-side corporate web platform into production.

---

## 🏗️ Architecture Overview

The frontend is built with **Vite 8** using a high-performance Multi-Page Application (MPA) architecture serving **36 static HTML entrypoints**, modular CSS, and client-side JavaScript with dynamic backend API integration.

### Core Production Files Prepared:
- **`Dockerfile`**: Production multi-stage Alpine build with hardened Nginx.
- **`nginx.conf`**: Gzip compression, immutable asset caching, security headers, clean URLs, and `/api/` reverse proxy.
- **`docker-compose.yml`**: One-command containerized production deployment.
- **`vercel.json`**: Vercel configuration with clean URLs and security headers.
- **`netlify.toml`**: Netlify configuration with redirects and asset caching.
- **`public/_redirects` & `public/_headers`**: Cloudflare Pages / Netlify static host directives.
- **`public/sitemap.xml`**: Exhaustive XML sitemap for SEO discovery across all practices.
- **`public/site.webmanifest`**: Progressive web application manifest.
- **`404.html`**: Branded error page matching THC corporate aesthetic.
- **`.github/workflows/frontend-production.yml`**: Automated CI/CD pipeline.

---

## 🚀 Deployment Options

### Option 1: Docker Container Deployment (Recommended for VPS / Cloud VMs)

#### 1. Build and Run Container Directly:
```bash
cd frontend
docker build -t thathvamasi-frontend:latest .
docker run -d --name thathvamasi-frontend -p 80:80 --restart unless-stopped thathvamasi-frontend:latest
```

#### 2. Run Using Docker Compose:
```bash
cd frontend
docker compose up -d --build
```

The container automatically:
- Compiles the static distribution via Node 20.
- Serves the bundle via Nginx Alpine with gzip and security headers.
- Proxies `/api/*` to the backend upstream service.
- Performs automated health checks on `http://localhost/`.

---

### Option 2: Traditional Nginx on Linux VPS (Ubuntu / Debian)

#### 1. Build the Static Bundle:
```bash
cd frontend
npm ci
npm run build:prod
```
The optimized production bundle will be generated in `frontend/dist/`.

#### 2. Copy Files to Web Root:
```bash
sudo mkdir -p /var/www/thathvamasi/html
sudo cp -r dist/* /var/www/thathvamasi/html/
sudo chown -R www-data:www-data /var/www/thathvamasi/html
```

#### 3. Configure Nginx Site:
Copy `frontend/nginx.conf` to `/etc/nginx/sites-available/thathvamasi.conf`, adjusting `root` to `/var/www/thathvamasi/html`, then:
```bash
sudo ln -s /etc/nginx/sites-available/thathvamasi.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 4. Enable Free SSL via Certbot:
```bash
sudo certbot --nginx -d thathvamasi.com -d www.thathvamasi.com
```

---

### Option 3: Jamstack / Cloud Static Hosting

#### Vercel:
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Root Directory:** `frontend`
- Configuration is automatically loaded from [`vercel.json`](file:///home/mrishank/thathvamasi/frontend/vercel.json).

#### Netlify:
- **Build Command:** `npm run build`
- **Publish Directory:** `frontend/dist`
- Configuration is automatically loaded from [`netlify.toml`](file:///home/mrishank/thathvamasi/frontend/netlify.toml).

#### Cloudflare Pages:
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Root Directory:** `frontend`
- Caching and routing rules are automatically loaded from `public/_headers` and `public/_redirects`.

---

### Option 4: AWS S3 + CloudFront CDN

#### 1. Build Artifacts:
```bash
cd frontend
npm ci
npm run build:prod
```

#### 2. Sync to AWS S3:
```bash
aws s3 sync dist/ s3://thathvamasi-production-frontend/ --delete
```

#### 3. Invalidate CloudFront Edge Cache:
```bash
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

---

## 🔑 Environment Variables Reference

| Variable | Description | Production Example |
| :--- | :--- | :--- |
| `VITE_SITE_URL` | Canonical URL of the platform | `https://thathvamasi.com` |
| `VITE_API_ENDPOINT` | Base URL for FastAPI backend endpoints | `https://api.thathvamasi.com/api` (or `/api` if proxied) |
| `VITE_GA_TRACKING_ID` | Google Analytics 4 Measurement ID | `G-THC2026PROD` |
| `VITE_WHATSAPP_NUMBER`| Corporate WhatsApp contact number | `919442218900` |

---

## 🧪 Post-Deployment Verification Checklist

- [ ] Homepage loads with HTTP 200 at `https://thathvamasi.com/`
- [ ] Practice URLs resolve cleanly (e.g. `/services/executive-search.html`, `/business/company-registration.html`, `/industries/auto-ev.html`)
- [ ] 404 page renders for invalid routes (e.g. `/unknown-page`)
- [ ] `https://thathvamasi.com/sitemap.xml` returns valid XML
- [ ] `https://thathvamasi.com/robots.txt` is accessible
- [ ] `https://thathvamasi.com/site.webmanifest` returns valid JSON
- [ ] Candidate intake and requisition forms transmit successfully to API or gracefully fallback to local cache
- [ ] Gzip compression is active (verify `Content-Encoding: gzip` in response headers)
- [ ] Security headers (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`) are present
