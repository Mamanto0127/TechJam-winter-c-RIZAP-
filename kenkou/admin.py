from django.contrib import admin
from .models import Mission
from .models import Enemy, WalkLog

admin.site.register(Mission)
admin.site.register(Enemy)
admin.site.register(WalkLog)