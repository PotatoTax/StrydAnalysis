from django.shortcuts import render, get_object_or_404

from .forms import ActivityDataForm
from .models import Activity, Record

previous_activity_data = {
    'power': True,
    'speed': False,
    'heart_rate': False,
    'cadence': False,
    'ground_time': False,
    'air_power': False,
    'form_power': False
}


def index(request):
    latest_activity_list = Activity.objects.order_by('-start_time')[:5]
    context = {
        'latest_activity_list': latest_activity_list
    }
    return render(request, 'activities/index.html', context)


def activity(request, activity_id):
    global previous_activity_data

    form = ActivityDataForm()
    if request.method == 'GET':
        form = ActivityDataForm(request.GET, initial=previous_activity_data)
        previous_activity_data = form.data

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

    records = [r for r in Record.objects.filter(activity=activity)]
    series = []

    for field in reversed([k for k in form.data.keys()]):
        if field in ['power', 'speed', 'heart_rate', 'cadence', 'form_power', 'air_power']:
            series.append(
                {
                    "name": field,
                    "data": [r.__getattribute__(field) for r in records]
                }
            )
        if field == 'ground_time':
            series.append(
                {
                    "name": field,
                    "data": [r.__getattribute__(field) if r.__getattribute__(field) < 400 else 400 for r in records]
                }
            )

    context = {
        'activity': activity,
        'chart_id': 'chart_id',
        'chart': {
            "render_to": 'chart_id',
            "type": 'line',
            "height": 500
        },
        'series': series,
        'title': 'Activity Data',
        'xAxis': {
            "title": {"text": "Time (hh:mm:ss)"},
            "categories": times,
            "crosshairs": 'true'
        },
        'yAxis': {
            "title": {"text": 'Power'},
            "categories": list(range(0, activity.max_power))
        },
        'tooltip': {'shared': 'true'},
        'form': form
    }

    return render(request, 'activities/activity.html', context)
