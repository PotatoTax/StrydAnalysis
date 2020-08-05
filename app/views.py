from django.shortcuts import render, get_object_or_404

from .models import Activity


def index(request):
    latest_activity_list = Activity.objects.order_by('-start_time')[:5]
    context = {
        'latest_activity_list': latest_activity_list
    }
    return render(request, 'activities/index.html', context)


def activity(request, activity_id: int):
    activity = get_object_or_404(Activity, pk=activity_id)
    return render(request, 'activities/activity.html', {'activity': activity})
