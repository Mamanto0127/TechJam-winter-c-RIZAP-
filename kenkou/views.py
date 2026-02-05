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
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

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
            walklog.distance = distance
            walklog.save()

        # 🔵 ログインしていない場合 → セッション保存
        request.session["today_distance"] = distance
        request.session["distance_date"] = today.isoformat()

        return JsonResponse({
            "status": "ok",
            "total_distance": distance
        })

    return JsonResponse({"status": "error"}, status=400)

def set_goal_distance(request):
    if request.method == "POST":
        data = json.loads(request.body)
        goal = int(data.get("goal", 0))

        if goal <= 0:
            return JsonResponse({"status": "error"}, status=400)

        request.session["goal_distance"] = goal
        request.session["goal_date"] = date.today().isoformat()

        return JsonResponse({"status": "ok", "goal": goal})

    return JsonResponse({"status": "error"}, status=400)

def index(request):
    today = date.today()
    total_distance = 0.0

    # 🔵 目標距離（デフォルト1000m）
    goal_distance = 1000

    # ===== ログイン時 =====
    if request.user.is_authenticated:
        walklog, _ = WalkLog.objects.get_or_create(
            user=request.user,
            date=today
        )
        total_distance = walklog.distance or 0.0

    # ===== セッションから goal 読み出し（共通）=====
    if request.session.get("goal_date") == today.isoformat():
        goal_distance = request.session.get("goal_distance", 1000)

    # ===== 未ログイン時の距離 =====
    if request.session.get("distance_date") == today.isoformat():
        total_distance = request.session.get("today_distance", total_distance)

    return render(
        request,
        "kenkou/index.html",
        {
            "total_distance": total_distance,
            "goal_distance": goal_distance,  # ← ★これが重要
        }
    )

def mission_view(request):
    missions = get_today_missions(count=3)
    return render(request, "kenkou/mission.html", {"missions": missions})

@login_required
def battle_view(request):
    today = date.today()

    if not request.user.is_authenticated:
        return redirect("login")
    
    #ユーザのログ取得
    walklog, created = WalkLog.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={"steps": 0, "distance": 0}
    )    

    #敵
    enemy, created = Enemy.objects.get_or_create(
        id=1, 
        defaults={"max_hp": 100, "current_hp": 100}
    )

    damage = 0
    if request.method == "POST":
        distance_damage = int (walklog.distance / 100)   #100メートルにつき1ダメージ

        mission_damage = request.session.get("mission_damage", 0) #ミッションクリアでダメージ

        damage = distance_damage + mission_damage

        enemy.current_hp = max(enemy.current_hp - damage, 0) #攻撃
        enemy.save()

        request.session["mission_damage"] = 0

    hp_percent = int(enemy.current_hp / enemy.max_hp * 100)

    return render(request, "kenkou/battle.html", {
        "damage": damage, 
        "enemy": enemy, 
        "hp_percent": hp_percent})

def logs_view(request):
    return render(request, "kenkou/logs.html")