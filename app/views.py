from django.shortcuts import render, get_object_or_404

from .forms import ActivityDataForm
from .models import Activity, Record


def index(request):
    latest_activity_list = Activity.objects.order_by('-start_time')[:5]
    context = {
        'latest_activity_list': latest_activity_list
    }
    return render(request, 'activities/index.html', context)


def activity(request, activity_id):
    form = ActivityDataForm()
    if request.method == 'POST':
        form = ActivityDataForm(request.POST)

    activity = get_object_or_404(Activity, pk=activity_id)

    times = []
    for s in range(int(activity.timer_time)):
        t = ""
        if s >= 3600:
            t += str(s // 3600) + ":"
            if (s % 3600) // 60 < 10:
                t += "0"
        t += str((s % 3600) // 60) + ":"
        if s % 60 < 10:
            t += "0"
        t += str(s % 60 // 1)
        times.append(t)

    chart = {
        "render_to": 'chart_id',
        "type": 'line',
        "height": 500
    }
    title = 'Activity Data'
    x_axis = {
        "title": {"text": "Time (hh:mm:ss)"},
        "categories": times
    }
    y_axis = {
        "title": {"text": 'Power'},
        "categories": list(range(0, activity.max_power))
    }

    records = [r for r in Record.objects.filter(activity=activity)]
    # series = []
    #
    # for field in fields:
    #     series.append(
    #         {
    #             "name": field,
    #             "data": [r.__getattribute__(field.lower()) for r in records]
    #         }
    #     )
    series = [
        {
            "name": "Power",
            "data": [r.__getattribute__('power') for r in records]
        }
    ]

    context = {
        'activity': activity,
        'chart_id': 'chart_id',
        'chart': chart,
        'series': series,
        'title': title,
        'xAxis': x_axis,
        'yAxis': y_axis,
        'form': form
    }

    return render(request, 'activities/activity.html', context)
