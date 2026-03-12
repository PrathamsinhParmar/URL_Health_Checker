import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import MonitoredURL, CheckLog
from .forms import MonitoredURLForm


def home(request):
    """Landing page — redirect authenticated users to dashboard."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'monitor/home.html')


@login_required
def dashboard(request):
    """Main dashboard listing all monitored URLs for the current user."""
    monitored_urls = (
        MonitoredURL.objects
        .filter(user=request.user)
        .prefetch_related('logs')
    )

    url_data = []
    active_count = 0
    for mu in monitored_urls:
        uptime_pct = mu.uptime_percentage(hours=24)
        url_data.append((mu, uptime_pct))
        if mu.is_active and mu.current_status:
            active_count += 1

    context = {
        'monitored_urls': url_data,
        'active_count': active_count,
    }
    return render(request, 'monitor/dashboard.html', context)


@login_required
def add_url(request):
    """Add a new URL to monitor."""
    if request.method == 'POST':
        form = MonitoredURLForm(request.POST)
        if form.is_valid():
            monitored_url = form.save(commit=False)
            monitored_url.user = request.user
            monitored_url.save()
            messages.success(request, f'✅ "{monitored_url.name}" has been added to monitoring.')
            return redirect('dashboard')
    else:
        form = MonitoredURLForm()

    context = {
        'form': form,
        'form_title': 'Add URL',
        'submit_label': 'Start Monitoring',
    }
    return render(request, 'monitor/url_form.html', context)


@login_required
def edit_url(request, pk):
    """Edit an existing monitored URL (owner-only)."""
    monitored_url = get_object_or_404(MonitoredURL, pk=pk, user=request.user)

    if request.method == 'POST':
        form = MonitoredURLForm(request.POST, instance=monitored_url)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ "{monitored_url.name}" has been updated.')
            return redirect('dashboard')
    else:
        form = MonitoredURLForm(instance=monitored_url)

    context = {
        'form': form,
        'form_title': 'Edit URL',
        'submit_label': 'Save Changes',
        'monitored_url': monitored_url,
    }
    return render(request, 'monitor/url_form.html', context)


@login_required
def delete_url(request, pk):
    """Delete a monitored URL with confirmation (owner-only)."""
    monitored_url = get_object_or_404(MonitoredURL, pk=pk, user=request.user)

    if request.method == 'POST':
        name = monitored_url.name
        monitored_url.delete()
        messages.success(request, f'🗑️ "{name}" has been removed from monitoring.')
        return redirect('dashboard')

    context = {
        'monitored_url': monitored_url,
    }
    return render(request, 'monitor/url_confirm_delete.html', context)


@login_required
def url_detail(request, pk):
    """Detailed view: stats, chart, and recent check logs."""
    monitored_url = get_object_or_404(MonitoredURL, pk=pk, user=request.user)
    logs = monitored_url.logs.all()[:100]

    uptime_24h = monitored_url.uptime_percentage(hours=24)
    uptime_7d = monitored_url.uptime_percentage(hours=168)

    # Build chart data from the last 50 logs (oldest first for Chart.js)
    chart_logs = list(monitored_url.logs.all()[:50])
    chart_logs.reverse()

    chart_data = [
        {
            'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'response_time': round(log.response_time * 1000, 1),  # ms
        }
        for log in chart_logs
    ]

    context = {
        'monitored_url': monitored_url,
        'logs': logs,
        'uptime_24h': uptime_24h,
        'uptime_7d': uptime_7d,
        'chart_data_json': json.dumps(chart_data),
        'has_logs': len(chart_logs) > 0,
    }
    return render(request, 'monitor/url_detail.html', context)


def register(request):
    """User registration — auto-login on success."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'🎉 Welcome, {user.username}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'monitor/register.html', context)
