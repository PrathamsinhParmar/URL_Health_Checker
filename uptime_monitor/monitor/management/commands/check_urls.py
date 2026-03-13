# CRON SETUP:
# Run `crontab -e` on Linux/macOS and add:
# */5 * * * * /path/to/venv/bin/python /path/to/manage.py check_urls >> /var/log/uptime_check.log 2>&1
#
# For Windows (Task Scheduler), run every 5 minutes:
# python manage.py check_urls
#
# Example Task Scheduler action:
#   Program: C:\path\to\venv\Scripts\python.exe
#   Arguments: C:\path\to\uptime_monitor\manage.py check_urls
#   Start in: C:\path\to\uptime_monitor\

import concurrent.futures
from django.core.management.base import BaseCommand
from monitor.models import MonitoredURL
from monitor.utils import check_single_url, send_alert_email


class Command(BaseCommand):
    help = 'Check all active monitored URLs and log their status.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Print what would be checked without making HTTP requests or writing to DB.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        active_urls = (
            MonitoredURL.objects
            .filter(is_active=True)
            .select_related('user')
        )

        total = active_urls.count()

        if total == 0:
            self.stdout.write(self.style.WARNING('No active URLs to check.'))
            return

        if dry_run:
            self.stdout.write(self.style.NOTICE(
                f'[DRY RUN] Would check {total} URL(s):'
            ))
            for mu in active_urls:
                self.stdout.write(f'  • {mu.name}  →  {mu.url}')
            return

        self.stdout.write(self.style.NOTICE(
            f'Checking {total} active URL(s) with up to 10 concurrent workers...\n'
        ))

        results = {}  # pk -> (mu, is_up, status_code, response_time, status_changed)

        def worker(mu):
            try:
                is_up, status_code, response_time, status_changed = check_single_url(mu)
                return (mu, is_up, status_code, response_time, status_changed)
            except Exception as exc:
                return (mu, False, None, 0.0, False, str(exc))

        count_up = 0
        count_down = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_mu = {executor.submit(worker, mu): mu for mu in active_urls}
            for future in concurrent.futures.as_completed(future_to_mu):
                result = future.result()
                mu = result[0]

                if len(result) == 6:
                    # Error tuple
                    _, is_up, status_code, response_time, status_changed, err_msg = result
                    self.stdout.write(
                        self.style.ERROR(f'[ERROR] {mu.name} — {mu.url} — {err_msg}')
                    )
                    count_down += 1
                    continue

                _, is_up, status_code, response_time, status_changed = result

                if is_up:
                    count_up += 1
                    code_str = str(status_code) if status_code else 'N/A'
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'[OK]   {mu.name} — {code_str} — {response_time:.3f}s'
                        )
                    )
                else:
                    count_down += 1
                    if status_code:
                        self.stdout.write(
                            self.style.ERROR(
                                f'[DOWN] {mu.name} — {status_code} — {response_time:.3f}s'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                f'[DOWN] {mu.name} — timeout / connection error'
                            )
                        )

                # Send alert if status changed
                if status_changed:
                    self.stdout.write(
                        self.style.WARNING(
                            f'  ↳ Status change detected! Sending alert to {mu.user.email or "(no email)"}'
                        )
                    )
                    send_alert_email(mu, is_up, status_code=status_code)

        self.stdout.write('\n' + '─' * 50)
        self.stdout.write(
            self.style.SUCCESS(
                f'Summary: {total} checked — {count_up} UP — {count_down} DOWN'
            )
        )
