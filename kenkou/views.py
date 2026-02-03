from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from datetime import date
from .models import WalkLog, Enemy
from .services.battle import calculate_damage, attack_enemy
from .services.mission import get_today_missions

def location_receive(request):  #位置情報
    if request.method == "POST":
        data = json.loads(request.body)

        lat = data.get("latitude")
        lon = data.get("longitude")
        time = data.get("timestamp")

        print("受信した現在地:", lat, lon, time)

        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "ng"}, status=400)

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

    return render(request, "kenkou/battle.html", {"damege": damage, "enemy": enemy})
