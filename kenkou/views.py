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

@csrf_exempt
def location_receive(request):
    if request.method == "POST":
        data = json.loads(request.body)
        distance = float(data.get("distance", 0))

        today = date.today()

        # 🔵 ログインしている場合 → DB保存
        if request.user.is_authenticated:
            walklog, _ = WalkLog.objects.get_or_create(
                user=request.user,
                date=today
            )
            walklog.total_distance = distance
            walklog.save()

        # 🔵 ログインしていない場合 → セッション保存
        request.session["today_distance"] = distance
        request.session["distance_date"] = today.isoformat()

        return JsonResponse({
            "status": "ok",
            "total_distance": distance
        })

    return JsonResponse({"status": "error"}, status=400)

def index(request):
    today = date.today()
    total_distance = 0.0   # ← 最初から数値

    if request.user.is_authenticated:
        walklog, _ = WalkLog.objects.get_or_create(
            user=request.user,
            date=today
        )
        total_distance = walklog.total_distance or 0.0
    else:
        if request.session.get("distance_date") == today.isoformat():
            total_distance = request.session.get("today_distance", 0.0)

    return render(
        request,
        "kenkou/index.html",
        {"total_distance": total_distance}
    )

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

