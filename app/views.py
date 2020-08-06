from django.shortcuts import render, get_object_or_404

from .models import Activity, Record


def index(request):
    latest_activity_list = Activity.objects.order_by('-start_time')[:5]
    context = {
        'latest_activity_list': latest_activity_list
    }
    return render(request, 'activities/index.html', context)


def activity(request, activity_id, chart_id='chart_id', chart_height=500):
    activity = get_object_or_404(Activity, pk=activity_id)

    chart = {
        "render_to": chart_id,
        "type": 'line',
        "height": chart_height
    }
    title = 'Activity Data'
    xAxis = {
        "title": {"text": "Time"},
        "categories": list(range(int(activity.timer_time)))
    }
    yAxis = {
        "title": {"text": 'Power'},
        "categories": list(range(0, activity.max_power))
    }
    series = [
        {
            "name": "Power",
            "data": [r.power for r in Record.objects.filter(activity=activity)]
        }
    ]

    context = {
        'activity': activity,
        'chart_id': chart_id,
        'chart': chart,
        'series': series,
        'title': title,
        'xAxis': xAxis,
        'yAxis': yAxis
    }

    return render(request, 'activities/activity.html', context)