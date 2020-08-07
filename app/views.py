from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .forms import ActivityDataForm
from .models import Activity


def index(request):
    latest_activity_list = Activity.objects.order_by('-start_time')[:5]
    context = {
        'latest_activity_list': latest_activity_list
    }
    return render(request, 'activities/index.html', context)


def activity_page(request, activity_id):
    form = ActivityDataForm()

    if request.method == 'GET':
        form = ActivityDataForm(request.GET)

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

    context = {
        'activity': activity,
        'chart_id': 'chart_id',
        'chart': {
            "render_to": 'chart_id',
            "type": 'line',
            "height": 500
        },
        'title': 'Activity Data',
        'xAxis': {
            "title": {"text": "Time (hh:mm:ss)"},
            "categories": times,
            "crosshairs": 'true'
        },
        'tooltip': {'shared': 'true'},
        'form': form
    }

    return render(request, 'activities/activity.html', context)


def activity_data(request, activity_id):
    # TODO: Split series into separate panes
    activity = get_object_or_404(Activity, pk=activity_id)

    fields = request.GET.getlist('fields[]')

    series = {}

    for f in fields:
        series[f] = []
        if f == 'ground_time':
            for r in activity.record_set.all():
                if r.__getattribute__(f) > 350:
                    series[f].append(350)
                else:
                    series[f].append(r.__getattribute__(f))
        else:
            for r in activity.record_set.all():
                series[f].append(r.__getattribute__(f))

    data = {
        'series': series
    }

    return JsonResponse(data)
