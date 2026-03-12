from django.db import models
from django.contrib.auth.models import User


class MonitoredURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monitored_urls')
    name = models.CharField(max_length=100)
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_checked = models.DateTimeField(null=True, blank=True)
    current_status = models.BooleanField(default=True)   # True=Up, False=Down
    current_response_time = models.FloatField(null=True, blank=True)

    def uptime_percentage(self, hours=24):
        """Return uptime % over last N hours. Returns None if no logs."""
        from django.utils import timezone
        import datetime
        since = timezone.now() - datetime.timedelta(hours=hours)
        logs = self.logs.filter(timestamp__gte=since)
        total = logs.count()
        if total == 0:
            return None
        up = logs.filter(is_up=True).count()
        return round((up / total) * 100, 1)

    def __str__(self):
        return f"{self.name} ({self.url})"

    class Meta:
        ordering = ['-created_at']


class CheckLog(models.Model):
    monitored_url = models.ForeignKey(MonitoredURL, on_delete=models.CASCADE, related_name='logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField(null=True, blank=True)
    response_time = models.FloatField()   # seconds
    is_up = models.BooleanField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        status = "UP" if self.is_up else "DOWN"
        return f"{self.monitored_url.name} — {status} at {self.timestamp}"
