# Deployment Guide

This guide provides instructions for deploying the Energy Tracker Django application to various production environments.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Production Deployment Options](#production-deployment-options)
- [Security Considerations](#security-considerations)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## Prerequisites

### System Requirements
- Python 3.13+
- Web server (Nginx, Apache, or similar)
- WSGI server (Gunicorn, uWSGI, or mod_wsgi)
- Database server (PostgreSQL recommended for production)
- SSL certificate for HTTPS

### Dependencies
```bash
pip install -r requirements.txt
pip install gunicorn psycopg2-binary  # For production
```

## Environment Configuration

### 1. Environment Variables

Create a `.env` file (do not commit to version control):

```bash
# Django Settings
SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/energy_tracker

# Static Files
STATIC_ROOT=/var/www/energy_tracker/static/
MEDIA_ROOT=/var/www/energy_tracker/media/

# Email Settings (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.youremail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
```

### 2. Production Settings

Create `energy_tracker/settings_production.py`:

```python
from .settings import *
import os
from decouple import config, Csv

# Security Settings
DEBUG = False
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Static Files
STATIC_ROOT = config('STATIC_ROOT', default='/var/www/energy_tracker/static/')
STATIC_URL = '/static/'

# Media Files
MEDIA_ROOT = config('MEDIA_ROOT', default='/var/www/energy_tracker/media/')
MEDIA_URL = '/media/'

# Security Headers
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/energy_tracker/django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

## Database Setup

### PostgreSQL (Recommended)

1. **Install PostgreSQL:**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   
   # CentOS/RHEL
   sudo yum install postgresql-server postgresql-contrib
   ```

2. **Create Database and User:**
   ```sql
   sudo -u postgres psql
   CREATE DATABASE energy_tracker;
   CREATE USER energy_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE energy_tracker TO energy_user;
   ALTER USER energy_user CREATEDB;
   \q
   ```

3. **Update Database Settings:**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'energy_tracker',
           'USER': 'energy_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### Migration to Production Database

```bash
# Export data from SQLite (if migrating)
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > data.json

# Run migrations on production database
python manage.py migrate

# Load data (if migrating)
python manage.py loaddata data.json
```

## Production Deployment Options

### Option 1: Traditional VPS/Server Deployment

#### 1. Gunicorn + Nginx Setup

**Install and configure Gunicorn:**
```bash
pip install gunicorn
```

**Create Gunicorn configuration (`gunicorn.conf.py`):**
```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
user = "www-data"
group = "www-data"
tmp_upload_dir = None
errorlog = "/var/log/energy_tracker/gunicorn_error.log"
accesslog = "/var/log/energy_tracker/gunicorn_access.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
```

**Create systemd service (`/etc/systemd/system/energy_tracker.service`):**
```ini
[Unit]
Description=Energy Tracker Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/energy_tracker
Environment="DJANGO_SETTINGS_MODULE=energy_tracker.settings_production"
ExecStart=/var/www/energy_tracker/env/bin/gunicorn --config gunicorn.conf.py energy_tracker.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

**Nginx configuration (`/etc/nginx/sites-available/energy_tracker`):**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/energy_tracker/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/energy_tracker/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
}
```

**Start services:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable energy_tracker
sudo systemctl start energy_tracker
sudo systemctl enable nginx
sudo systemctl restart nginx
```

### Option 2: Docker Deployment

**Create `Dockerfile`:**
```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn psycopg2-binary

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "energy_tracker.wsgi:application"]
```

**Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SETTINGS_MODULE=energy_tracker.settings_production
    volumes:
      - static_volume:/app/static
      - media_volume:/app/media
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: energy_tracker
      POSTGRES_USER: energy_user
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - static_volume:/var/www/static
      - media_volume:/var/www/media
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

**Deploy with Docker:**
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

### Option 3: Cloud Platform Deployment

#### Heroku
```bash
# Install Heroku CLI and login
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set DJANGO_SETTINGS_MODULE=energy_tracker.settings_production
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
heroku run python manage.py migrate
```

#### DigitalOcean App Platform
Create `app.yaml`:
```yaml
name: energy-tracker
services:
- name: web
  source_dir: /
  github:
    repo: yourusername/Energy-Tracker
    branch: main
  run_command: gunicorn --worker-tmp-dir /dev/shm energy_tracker.wsgi
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: DJANGO_SETTINGS_MODULE
    value: energy_tracker.settings_production
databases:
- name: energy-tracker-db
  engine: PG
  version: "13"
```

## Security Considerations

### 1. Environment Security
- Use environment variables for sensitive data
- Never commit `.env` files or secrets
- Use strong, unique passwords
- Enable two-factor authentication where possible

### 2. Django Security Settings
```python
# In production settings
DEBUG = False
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 3. Server Security
- Keep system packages updated
- Configure firewall (UFW, iptables)
- Use fail2ban for intrusion prevention
- Regular security audits
- Monitor logs for suspicious activity

### 4. Database Security
- Use strong passwords
- Limit database user permissions
- Regular backups
- Enable database logging
- Use connection encryption

## Monitoring and Maintenance

### 1. Logging Setup
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/energy_tracker/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 2. Health Check Endpoint
Add to `urls.py`:
```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'ok'})

urlpatterns = [
    path('health/', health_check, name='health_check'),
    # ... other patterns
]
```

### 3. Backup Strategy
```bash
#!/bin/bash
# Backup script
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump energy_tracker > /backups/energy_tracker_$DATE.sql
find /backups -name "energy_tracker_*.sql" -mtime +7 -delete
```

### 4. Monitoring Tools
- Use application monitoring (New Relic, Sentry)
- Set up server monitoring (Prometheus, Grafana)
- Configure alerts for downtime
- Monitor database performance

### 5. Update Process
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application
sudo systemctl restart energy_tracker
```

## Troubleshooting

### Common Issues
1. **Static files not loading**: Check `STATIC_ROOT` and `STATIC_URL` settings
2. **Database connection errors**: Verify database credentials and network connectivity
3. **Permission errors**: Check file/directory permissions for web server user
4. **SSL certificate issues**: Ensure certificates are valid and properly configured

### Debug Commands
```bash
# Check service status
sudo systemctl status energy_tracker

# View logs
sudo journalctl -u energy_tracker -f
tail -f /var/log/energy_tracker/django.log

# Test database connection
python manage.py dbshell

# Check Django configuration
python manage.py check --deploy
```

This deployment guide provides a comprehensive overview of deploying Energy Tracker in production environments. Choose the deployment option that best fits your infrastructure and requirements.