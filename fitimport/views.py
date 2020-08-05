from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from fitimport.FitParser import parse_fit
from fitimport.forms import FITUploadForm


def upload_fit(request):
    if request.method == 'POST':
        form = FITUploadForm(request.POST, request.FILES)
        if form.is_valid():
            parse_fit(request.FILES['file'])
            return HttpResponseRedirect('/activity')
    else:
        form = FITUploadForm()
    return render(request, 'fitimport/upload.html', {'form': form})
