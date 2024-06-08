from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Driver)
admin.site.register(Constructor)
admin.site.register(Track)
admin.site.register(TrackResult)
admin.site.register(SeasonResult)
admin.site.register(CurrentSeason)
admin.site.register(CurrentStanding)
admin.site.register(DriverProfile)
admin.site.register(TrackProfile)