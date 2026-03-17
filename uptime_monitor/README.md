<<<<<<< HEAD
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
=======
<div align="center">
  <h1>🛡️ DownAlert — Professional URL Health Monitor</h1>
  <p><strong>A production-ready Django application that monitors your websites 24/7, tracks response times, and sends email alerts when status changes.</strong></p>
</div>

---

## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Architecture & How It Works](#-architecture--how-it-works)
- [Project Directory Structure](#-project-directory-structure)
- [Getting Started (Local Development)](#-getting-started-local-development)
- [Running Automated Checks](#-running-automated-checks)
- [Email Alert Configuration](#-email-alert-configuration)
- [Deployment & Production Security](#-deployment--production-security)
- [Default Admin Credentials](#-default-admin-credentials)
- [License](#-license)

---

## 🌟 About the Project

**DownAlert** is a fully-featured, Django-based uptime monitoring solution designed to provide real-time insights into the availability and performance of your critical websites and APIs. It allows multiple users to register, add URLs, and track their endpoints in complete isolation. An automated background worker routinely checks these URLs concurrently to ensure minimal delay, sending email notifications the moment an endpoint goes down or recovers.

---

## 🚀 Key Features

*   **⚡ High-Performance Concurrent Monitoring:** Utilizes Python's `ThreadPoolExecutor` to check multiple endpoints simultaneously (up to 10 concurrent workers), ensuring that health checks do not bottleneck even with hundreds of URLs.
*   **📊 Insightful Analytics & Visualization:** Interactive, real-time charts powered by **Chart.js** plot historical response times, making it easy to spot degradation or latency spikes over time.
*   **📈 Built-in Uptime Calculations:** Automatically calculates and displays accurate historical uptime percentages for both rolling 24-hour and 7-day windows.
*   **🔔 Intelligent Alerting System:** State-tracking logic ensures you only receive email alerts when a status *changes* (e.g., UP -> DOWN or DOWN -> UP), preventing inbox spam.
*   **🔐 Robust User Management:** Complete authentication system including registration, secure login, logout, and profile management.
*   **🛡️ Strict Data Isolation:** Every URL, check log, and alert is strictly bound to the authenticated user via Django's ORM, preventing data leakage across accounts.
*   **🌙 Modern Dark-Mode UI:** A beautiful, responsive interface built with Bootstrap 5, heavily customized for a distraction-free, premium dark-mode experience.

---

## 💻 Technology Stack

| Component | Technology / Library | Version |
| :--- | :--- | :--- |
| **Backend Framework** | Django | `4.2.13` |
| **HTTP Client** | Requests | `2.31.0` |
| **Form Rendering** | Django Widget Tweaks | `1.5.0` |
| **Frontend Styling** | Bootstrap 5 | N/A (CDN via Base HTML) |
| **Data Visualization** | Chart.js | N/A (CDN via Base HTML) |
| **Database** | SQLite3 (configurable to PostgreSQL) | Default |

---

## ⚙️ Architecture & How It Works

1. **User Interaction:** Users manage their URLs via a secure web dashboard.
2. **Background Automation:** A custom Django management command (`python manage.py check_urls`) is triggered per schedule (e.g., every 5 minutes) via a system scheduler (Cron/Task Scheduler).
3. **Concurrent Execution:** The management command spawns a thread pool, sending simultaneous HTTP GET requests to all `is_active` URLs using the `requests` library.
4. **Data Logging:** Timeout, status code, and response latency are recorded in the `CheckLog` database model.
5. **Event Evaluation:** The system compares the new state with the previous state (stored in `MonitoredURL.current_status`). If the state changes, an alert is dispatched using Django's email backend.
6. **Data Presentation:** The dashboard renders the latest checks and calculates uptime % dynamically from the persisted database logs.

---

## 📁 Project Directory Structure

```text
uptime_monitor/
├── manage.py                          ← Django entry point
├── requirements.txt                   ← Python dependencies
├── setup.sh                           ← Shell script for quick setup
├── start.bat                          ← Windows batch file to start dev server
├── background_checks.bat              ← Example Windows script for URL checks
├── db.sqlite3                         ← Local database (auto-generated)
├── uptime_monitor/                    ← Core Django Settings
│   ├── settings.py
│   ├── urls.py                        ← Main URL routing
│   └── wsgi.py / asgi.py
└── monitor/                           ← Main Application Directory
    ├── admin.py                       ← Admin panel configurations
    ├── forms.py                       ← Django forms (Add/Edit URL, User Update)
    ├── models.py                      ← Database schemas (MonitoredURL, CheckLog)
    ├── urls.py                        ← App-specific URL routing
    ├── utils.py                       ← Core logic: HTTP checking and Email Alerts
    ├── views.py                       ← Controllers handling web requests
    ├── management/commands/
    │   └── check_urls.py              ← Custom command for concurrent health checks
    └── templates/monitor/             ← HTML Templates
        ├── base.html                  ← Master layout
        ├── home.html                  ← Public landing page
        ├── dashboard.html             ← User dashboard listing URLs
        ├── url_detail.html            ← Chart and detailed logs for a URL
        └── ... (forms, auth pages)
>>>>>>> 9d64cfa9 (Git Repo Connection Issue - Reinit)
```

---

<<<<<<< HEAD
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

=======
## 🛠️ Getting Started (Local Development)

### Prerequisites
*   Python 3.11+
*   `pip` (Python package manager)

### Step-by-Step Setup

1. **Clone & Navigate:**
   ```bash
   cd uptime_monitor
   ```

2. **Set up Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment:**
   *   **Windows:** `venv\Scripts\activate`
   *   **macOS / Linux:** `source venv/bin/activate`

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply Database Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create an Admin User (Optional):**
   ```bash
   python manage.py createsuperuser
   # OR use the utility script (creates admin / admin123):
   # bash setup.sh
   ```

7. **Start the Development Server:**
   ```bash
   python manage.py runserver
   # OR use the batch file on Windows: .\start.bat
   ```

8. **Access the Application:**
   *   App Dashboard: `http://127.0.0.1:8000/`
   *   Admin Panel: `http://127.0.0.1:8000/admin/`

---

## 🔄 Running Automated Checks

The core engine of this project requires you to run periodic checks to update URL statuses. 

### Manual Execution & Testing
Run a normal check of all active endpoints:
```bash
python manage.py check_urls
```
Run a dry-run (prints what it *would* check without making network requests or saving to DB):
>>>>>>> 9d64cfa9 (Git Repo Connection Issue - Reinit)
```bash
python manage.py check_urls --dry-run
```

<<<<<<< HEAD
---

## ⏰ Setting Up Automated Checks

### Linux / macOS (cron)

```bash
crontab -e
```

Add this line to check every 5 minutes:

=======
### Automated Scheduling

**For Linux / macOS (Cron):**
Run `crontab -e` and add the following line to check URLs every 5 minutes:
>>>>>>> 9d64cfa9 (Git Repo Connection Issue - Reinit)
```cron
*/5 * * * * /path/to/venv/bin/python /path/to/uptime_monitor/manage.py check_urls >> /var/log/uptime_check.log 2>&1
```

<<<<<<< HEAD
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
=======
**For Windows (Task Scheduler):**
1. Open **Task Scheduler** → Create Basic Task
2. Set trigger to **Daily**, then edit the trigger to repeat **Every 5 minutes**.
3. Set the Action to **Start a program**:
   *   **Program/script**: `C:\path\to\venv\Scripts\python.exe`
   *   **Add arguments**: `C:\path\to\uptime_monitor\manage.py check_urls`
   *   **Start in**: `C:\path\to\uptime_monitor\`

---

## 📧 Email Alert Configuration

By default, the application is set to print alerts to the developer console. To enable actual SMTP email delivery, configure the following settings in `uptime_monitor/settings.py` (or load them from a `.env` file):
>>>>>>> 9d64cfa9 (Git Repo Connection Issue - Reinit)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
<<<<<<< HEAD
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

## 🗝️ Default Admin Credentials (setup.sh)

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `admin123` |
| Email | `admin@example.com` |

> ⚠️ Change these immediately in any non-local environment!
=======
EMAIL_HOST_USER = 'your.email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-secure-app-password'
DEFAULT_FROM_EMAIL = 'DownAlert <alerts@yourdomain.com>'
```

> **Requirements for User:** To receive alerts, a user MUST configure an email address in their DownAlert profile settings.

---

## 🐘 Deployment & Production Security

Before deploying to a public-facing server (e.g., AWS, Render, Heroku, DigitalOcean), follow this critical checklist:

- [ ] **Database Setup:** Switch from `db.sqlite3` to a robust database like PostgreSQL.
  ```bash
  pip install psycopg2-binary
  ```
  ```python
  # settings.py
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'downalert_db',
          'USER': 'postgres',
          'PASSWORD': 'strongpassword',
          'HOST': 'localhost',
          'PORT': '5432',
      }
  }
  ```
- [ ] **Security Keys:** Set a strong secret key by overriding `SECRET_KEY` via Environment Variables.
- [ ] **Debug Mode:** Strictly set `DEBUG = False`.
- [ ] **Allowed Hosts:** Add your final domain name or load balancer IP to `ALLOWED_HOSTS`.
- [ ] **Static Assets:** Run `python manage.py collectstatic` and serve static files using Nginx or WhiteNoise.
- [ ] **HTTPS / SSL:** Secure all traffic using Let's Encrypt / TLS certs to protect user credentials.

---

## 🗝️ Default Admin Credentials (via `setup.sh`)

If you used the initialization scripts included with this project, the default superuser credentials are:

| Field | Value |
| :--- | :--- |
| **Username** | `admin` |
| **Password** | `admin123` |
| **Email** | `admin@example.com` |

> ⚠️ **CRITICAL WARNING:** Change this password immediately after logging into any staging or production environment.
>>>>>>> 9d64cfa9 (Git Repo Connection Issue - Reinit)

---

## 📝 License

<<<<<<< HEAD
MIT — free to use and modify.
=======
This project is licensed under the **MIT License**. You are free to use, modify, distribute, and integrate this project into your own applications.
>>>>>>> 9d64cfa9 (Git Repo Connection Issue - Reinit)
