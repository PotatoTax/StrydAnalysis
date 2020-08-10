from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import Activity


def index(request):
    latest_activity_list = Activity.objects.order_by('-start_time')[:5]
    context = {
        'latest_activity_list': latest_activity_list
    }
    return render(request, 'activities/index.html', context)


def activity_page(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    context = {
        'activity': activity
    }

    return render(request, 'activities/activity.html', context)


def activity_data(request, activity_id):
    # TODO: Split series into separate panes
    # TODO: Create detail chart
    activity = get_object_or_404(Activity, pk=activity_id)

    fields = request.GET.getlist('fields[]')

    series = {}

    for f in fields:
        series[f] = []

    for r in activity.record_set.all().iterator():
        for f in fields:
            if f == 'ground_time':
                if r.__getattribute__(f) > 350:
                    series[f].append(350)
            else:
                series[f].append(r.__getattribute__(f))

    return JsonResponse({'series': series})
