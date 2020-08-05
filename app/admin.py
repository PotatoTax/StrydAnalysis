from django.contrib import admin

# Register your models here.
from app.models import Activity, Lap, Record

admin.site.register(Activity)
admin.site.register(Lap)
admin.site.register(Record)
