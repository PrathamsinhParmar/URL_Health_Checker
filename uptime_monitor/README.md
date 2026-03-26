# DownAlert — URL Health Monitor

A production-ready **Django** application that monitors your websites 24/7, tracks response times, and sends email alerts when status changes.

---

## 🚀 Features

- ✅ Monitor unlimited URLs per user
- 📊 Response time charts (Chart.js)
- 📈 Uptime percentage (24h & 7-day windows)
- 🔔 Email alerts on status change (up/down)
- ⚡ Concurrent checks via `ThreadPoolExecutor`
- 🔐 User authentication (register/login/logout)
- 🛡️ Complete data isolation per user
- 🌙 Beautiful dark-mode UI (Bootstrap 5)

---

## 📁 Project Structure

```
uptime_monitor/
├── manage.py
├── requirements.txt
├── setup.sh
├── db.sqlite3             ← created after migrate
├── uptime_monitor/        ← Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── monitor/               ← main app
    ├── models.py
    ├── views.py
    ├── forms.py
    ├── utils.py
    ├── admin.py
    ├── urls.py
    ├── management/commands/check_urls.py
    └── templates/monitor/
        ├── base.html
        ├── home.html
        ├── dashboard.html
        ├── url_form.html
        ├── url_confirm_delete.html
        ├── url_detail.html
        └── register.html
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11+
- pip

### Step-by-step

```bash
# 1. Navigate to the project folder
cd uptime_monitor

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run database migrations
python manage.py migrate

# 6. Create a superuser (for admin panel)
python manage.py createsuperuser
# OR use the setup script (creates admin/admin123):
# bash setup.sh

# 7. Start the development server
python manage.py runserver
```

Open your browser at: **http://127.0.0.1:8000/**

Admin panel: **http://127.0.0.1:8000/admin/**

---

## 🔍 Running URL Checks

Run a manual check of all active URLs:

```bash
python manage.py check_urls
```

Dry run (no HTTP requests, no DB writes):

```bash
python manage.py check_urls --dry-run
```

---

## ⏰ Setting Up Automated Checks

### Linux / macOS (cron)

```bash
crontab -e
```

Add this line to check every 5 minutes:

```cron
*/5 * * * * /path/to/venv/bin/python /path/to/uptime_monitor/manage.py check_urls >> /var/log/uptime_check.log 2>&1
```

### Windows (Task Scheduler)

1. Open **Task Scheduler** → Create Basic Task
2. Set trigger: **Every 5 minutes**
3. Action → **Start a program**:
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `C:\path\to\uptime_monitor\manage.py check_urls`
   - Start in: `C:\path\to\uptime_monitor\`

---

## 📧 Email Alerts

Currently configured to print emails to the console (development mode).

To enable real email delivery, update `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'monitor@yourdomain.com'
```

> **Note:** Users must have an email address set in their profile to receive alerts.

---

## 🐘 Switching to PostgreSQL (Production)

1. Install psycopg2:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `DATABASES` in `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'downalert',
           'USER': 'youruser',
           'PASSWORD': 'yourpassword',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

---

## 🔐 Production Security Checklist

- [ ] Set a strong `SECRET_KEY` (use environment variable)
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure SMTP email backend
- [ ] Set up HTTPS (Let's Encrypt / Nginx)
- [ ] Run `python manage.py collectstatic`

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| Django | 4.2.13 | Web framework |
| requests | 2.31.0 | HTTP checking |
| django-widget-tweaks | 1.5.0 | Form rendering |

---

## 📝 License

MIT — free to use and modify.
