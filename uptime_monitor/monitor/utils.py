import time
import requests
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


def check_single_url(monitored_url_instance):
    """
    Checks a single MonitoredURL instance.
    Returns: (is_up, status_code, response_time, status_changed)
    """
    from .models import CheckLog

    start = time.time()
    status_code = None
    is_up = False

    try:
        response = requests.head(
            monitored_url_instance.url,
            timeout=5,
            allow_redirects=True,
        )
        status_code = response.status_code

        # Some servers don't support HEAD — retry with GET (stream only headers)
        if status_code == 405:
            response = requests.get(
                monitored_url_instance.url,
                timeout=5,
                stream=True,
            )
            # Don't download the body
            response.close()
            status_code = response.status_code

        is_up = status_code in range(200, 400)

    except requests.exceptions.Timeout:
        is_up = False
        status_code = None
    except requests.exceptions.ConnectionError:
        is_up = False
        status_code = None
    except requests.exceptions.RequestException:
        is_up = False
        status_code = None

    response_time = time.time() - start

    # Detect status change before updating
    previous_status = monitored_url_instance.current_status
    status_changed = (is_up != previous_status)

    # Create log entry
    CheckLog.objects.create(
        monitored_url=monitored_url_instance,
        status_code=status_code,
        response_time=response_time,
        is_up=is_up,
    )

    # Update the MonitoredURL record
    monitored_url_instance.last_checked = timezone.now()
    monitored_url_instance.current_status = is_up
    monitored_url_instance.current_response_time = response_time
    monitored_url_instance.save(
        update_fields=['last_checked', 'current_status', 'current_response_time']
    )

    return (is_up, status_code, response_time, status_changed)


def send_alert_email(monitored_url, new_status):
    """
    Sends an alert email to the URL owner when status changes.
    Skips if the user has no email set.
    """
    user = monitored_url.user

    if not bool(user.email):
        return  # No email configured — skip

    if new_status:
        subject = f"🟢 [{monitored_url.name}] is back UP"
        status_text = "UP ✅"
    else:
        subject = f"🔴 [{monitored_url.name}] is DOWN"
        status_text = "DOWN ❌"

    now = timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')

    body = f"""
Hello {user.username},

Your monitored URL has changed status:

  Name    : {monitored_url.name}
  URL     : {monitored_url.url}
  Status  : {status_text}
  Time    : {now}

Please log in to your UptimeChecker dashboard to review the details
and recent check logs.

-- 
UptimeChecker Monitoring Service
(This is an automated alert. Do not reply to this email.)
""".strip()

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        # Log the error but don't crash the monitoring loop
        print(f"  [EMAIL ERROR] Failed to send alert to {user.email}: {e}")
