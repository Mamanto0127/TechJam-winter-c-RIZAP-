from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from .models import WalkLog, Enemy
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from datetime import datetime
from .services.battle import calculate_damage, attack_enemy
from .services.mission import get_today_missions
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from datetime import datetime


@csrf_exempt
def location_receive(request):
    if request.method == "POST":
        data = json.loads(request.body)

        lat = data["latitude"]
        lon = data["longitude"]
        time = datetime.fromtimestamp(data["timestamp"] / 1000)

        print(lat, lon, time)

        return JsonResponse({"status": "ok"})

def index(request):
    return render(request, 'kenkou/index.html')

def mission_view(request):
    missions = get_today_missions(count=3)
    return render(request, "kenkou/mission.html", {"missions": missions})

def battle_view(request):
    today = date.today()
    walklog = WalkLog.objects.get(user=request.user, date=today)
    enemy = Enemy.objects.first()

    damage = calculate_damage(walklog.steps)
    attack_enemy(enemy, damage)

    return render(request, "kenkou/battle.html", {"damage": damage, "enemy": enemy})

@csrf_exempt
def location_receive(request):
    if request.method == "POST":
        data = json.loads(request.body)

        lat = data["latitude"]
        lon = data["longitude"]
        time = datetime.fromtimestamp(data["timestamp"] / 1000)

        print(lat, lon, time)

        return JsonResponse({"status": "ok"})
