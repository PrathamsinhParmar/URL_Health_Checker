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


def send_alert_email(monitored_url, new_status, status_code=None, error_msg=None):
    """
    Sends an alert email to the URL owner when status changes.
    Skips if the user has no email set.
    """
    user = monitored_url.user

    if not bool(user.email):
        return  # No email configured — skip

    now = timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')

    if new_status:
        subject = f"✅ RESOLVED: {monitored_url.name} is back UP"
        body = f"Hello {user.username},\n\nGood news! Your monitored URL is back up and responding normally.\n\n  Name    : {monitored_url.name}\n  URL     : {monitored_url.url}\n  Time    : {now}\n\nLog in to your dashboard for details.\n\n--\nDownAlert Monitoring Service"
        html_body = f"""
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #10b981; border-radius: 8px; overflow: hidden; background-color: #fff;">
  <div style="background-color: #10b981; color: #fff; padding: 20px; text-align: center;">
    <h2 style="margin: 0; font-size: 24px;">✅ RESOLVED: URL IS UP ✅</h2>
  </div>
  <div style="padding: 24px; color: #232323;">
    <p style="font-size: 16px; margin-top: 0;">Hello <strong>{user.username}</strong>,</p>
    <p style="font-size: 16px; color: #10b981; font-weight: bold;">Good news! Your URL is back online.</p>
    <p style="font-size: 16px;">We have detected that your monitored URL is now responding normally.</p>
    
    <div style="background-color: #ecfdf5; border-left: 4px solid #10b981; padding: 16px; margin: 24px 0; border-radius: 4px;">
      <p style="margin: 0 0 8px 0;"><strong>Name:</strong> {monitored_url.name}</p>
      <p style="margin: 0 0 8px 0;"><strong>URL:</strong> <a href="{monitored_url.url}" style="color: #10b981;">{monitored_url.url}</a></p>
      <p style="margin: 0 0 0 0;"><strong>Recovery Time:</strong> {now}</p>
    </div>
  </div>
  <div style="background-color: #f9fafb; padding: 16px; text-align: center; font-size: 12px; color: #6b7280; border-top: 1px solid #e5e7eb;">
    <p style="margin: 0;">DownAlert Monitoring Service</p>
  </div>
</div>
"""
    else:
        subject = f"🚨 URGENT: {monitored_url.name} Stopped Working!"
        
        error_info = "Connection Failed / Timeout"
        if error_msg:
            error_info = error_msg
        elif status_code:
            error_info = f"HTTP Status {status_code}"
            
        body = f"Hello {user.username},\n\nURGENT: Your monitored URL has stopped responding!\n\n  Name    : {monitored_url.name}\n  URL     : {monitored_url.url}\n  Status  : DOWN\n  Time    : {now}\n  Details : {error_info}\n\nPlease click here to investigate: {monitored_url.url}\n\n--\nDownAlert Monitoring Service"
        
        html_body = f"""
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #ef4444; border-radius: 8px; overflow: hidden; background-color: #fff;">
  <div style="background-color: #ef4444; color: #fff; padding: 20px; text-align: center;">
    <h2 style="margin: 0; font-size: 24px;">⚠️ CRITICAL ALERT: URL IS DOWN ⚠️</h2>
  </div>
  <div style="padding: 24px; color: #232323;">
    <p style="font-size: 16px; margin-top: 0;">Hello <strong>{user.username}</strong>,</p>
    <p style="font-size: 16px; color: #ef4444; font-weight: bold;">URGENT: This requires your immediate attention!</p>
    <p style="font-size: 16px;">We have detected that your monitored URL is no longer responding.</p>
    
    <div style="background-color: #fef2f2; border-left: 4px solid #ef4444; padding: 16px; margin: 24px 0; border-radius: 4px;">
      <p style="margin: 0 0 8px 0;"><strong>Name:</strong> {monitored_url.name}</p>
      <p style="margin: 0 0 8px 0;"><strong>URL:</strong> <a href="{monitored_url.url}" style="color: #ef4444; font-weight: bold;">{monitored_url.url}</a></p>
      <p style="margin: 0 0 8px 0;"><strong>Time of Failure:</strong> {now}</p>
      <p style="margin: 0 0 0 0;"><strong>Reason:</strong> <span style="color: #b91c1c; font-weight: bold;">{error_info}</span></p>
    </div>
    
    <p style="font-size: 16px;">Please investigate this issue immediately to minimize your downtime.</p>
    
    <div style="margin-top: 32px; text-align: center;">
      <a href="{monitored_url.url}" style="background-color: #ef4444; color: white; text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; font-size: 16px; display: inline-block;">Investigate Issue</a>
    </div>
  </div>
  <div style="background-color: #f9fafb; padding: 16px; text-align: center; font-size: 12px; color: #6b7280; border-top: 1px solid #e5e7eb;">
    <p style="margin: 0;">DownAlert Monitoring Service</p>
    <p style="margin: 4px 0 0 0;">This is an automated critical alert. Do not reply to this email.</p>
  </div>
</div>
"""

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
            html_message=html_body,
        )
    except Exception as e:
        # Log the error but don't crash the monitoring loop
        print(f"  [EMAIL ERROR] Failed to send alert to {user.email}: {e}")

