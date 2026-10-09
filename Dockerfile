# ==============================================================================
# Thathvamasi Corporate Web Platform - Root Production Dockerfile
# Stage 1: Build static assets using Node.js Alpine
# Stage 2: Serve optimized assets with hardened Nginx Alpine
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build Environment
# ------------------------------------------------------------------------------
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependency files first for layer caching
COPY package*.json ./
COPY frontend/package*.json ./frontend/

# Install dependencies using workspaces
RUN npm install

# Copy application source tree
COPY . .

# Build arguments for Dokploy environment variables
ARG VITE_API_ENDPOINT
ARG VITE_SITE_URL
ARG VITE_GA_TRACKING_ID
ARG VITE_WHATSAPP_NUMBER

ENV VITE_API_ENDPOINT=$VITE_API_ENDPOINT
ENV VITE_SITE_URL=$VITE_SITE_URL
ENV VITE_GA_TRACKING_ID=$VITE_GA_TRACKING_ID
ENV VITE_WHATSAPP_NUMBER=$VITE_WHATSAPP_NUMBER

# Build production bundle
ENV NODE_ENV=production
RUN npm run build:prod

# ------------------------------------------------------------------------------
# Stage 2: Production Web Server
# ------------------------------------------------------------------------------
FROM nginx:alpine

# Remove default static site
RUN rm -rf /usr/share/nginx/html/*

# Copy built distribution files from builder
COPY --from=builder /app/frontend/dist /usr/share/nginx/html

# Copy production nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Health check to ensure web server is responding
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://127.0.0.1/ || exit 1

# Launch Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
