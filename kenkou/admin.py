from django.contrib import admin
from .models import Mission
from django.contrib import admin
from .models import WalkLog, EnemyMaster

admin.site.register(EnemyMaster)
admin.site.register(Mission)
admin.site.register(WalkLog)