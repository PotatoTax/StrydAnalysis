from django.shortcuts import render, get_object_or_404

from .models import Activity, Record


def index(request):
    latest_activity_list = Activity.objects.order_by('-start_time')[:5]
    context = {
        'latest_activity_list': latest_activity_list
    }
    return render(request, 'activities/index.html', context)


def activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    chart = {
        "render_to": 'chart_id',
        "type": 'line',
        "height": 500
    }
    title = 'Activity Data'
    x_axis = {
        "title": {"text": "Time"},
        "categories": list(range(int(activity.timer_time)))
    }
    y_axis = {
        "title": {"text": 'Power'},
        "categories": list(range(0, activity.max_power))
    }
    series = [
        {
            "name": "Power",
            "data": [r.__getattribute__('power') for r in Record.objects.filter(activity=activity)]
        }
    ]

    context = {
        'activity': activity,
        'chart_id': 'chart_id',
        'chart': chart,
        'series': series,
        'title': title,
        'xAxis': x_axis,
        'yAxis': y_axis
    }

    return render(request, 'activities/activity.html', context)
