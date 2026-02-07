from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from .models import WalkLog
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from datetime import datetime
from .services.battle import calculate_damage, attack_enemy
from .services.mission import get_today_missions
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import WalkLog, Mission, MissionClear, AttackStock, UserMission
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import EnemyMaster, UserEnemy
import random


@login_required
@login_required
def battle_view(request):
    today = date.today()

    # ===== 初期化（GETでも必ず存在させる）=====
    distance_damage = 0
    mission_damage = 0
    total_damage = 0
    damage = 0

    # ===== 今日の歩行ログ =====
    walklog, _ = WalkLog.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={"steps": 0, "distance": 0}
    )

    # ===== 今戦っている敵 =====
    user_enemy = UserEnemy.objects.filter(user=request.user).first()

    if not user_enemy:
        enemy_qs = EnemyMaster.objects.all()
        if not enemy_qs.exists():
            return HttpResponse("EnemyMaster が未登録です（adminで追加してください）")

        enemy_master = random.choice(enemy_qs)

        user_enemy = UserEnemy.objects.create(
            user=request.user,
            enemy=enemy_master,
            current_hp=enemy_master.max_hp
        )

    # ===== 攻撃ストック =====
    stock, _ = AttackStock.objects.get_or_create(user=request.user)

    # ===== 攻撃処理 =====
    if request.method == "POST":
        distance_damage = int(walklog.distance // 100)
        mission_damage = stock.damage
        total_damage = distance_damage + mission_damage
        damage = total_damage

        user_enemy.current_hp -= total_damage

        # 💀 撃破した場合
        if user_enemy.current_hp <= 0:
            next_enemy = random.choice(EnemyMaster.objects.all())
            user_enemy.enemy = next_enemy
            user_enemy.current_hp = next_enemy.max_hp

        user_enemy.save()

        # 攻撃ストック消費
        stock.damage = 0
        stock.save()

    # ===== HP 割合 =====
    hp_percent = int(
        user_enemy.current_hp / user_enemy.enemy.max_hp * 100
    )

    return render(request, "kenkou/battle.html", {
        "user_enemy": user_enemy,
        "enemy": user_enemy.enemy,
        "current_hp": user_enemy.current_hp,
        "hp_percent": hp_percent,
        "damage": damage,
        "distance_damage": distance_damage,
        "stored_damage": mission_damage,
        "total_damage": total_damage,
    })


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
    missions = Mission.objects.all()[:3]     # ユーザーのクリア状態を取得
    user_missions = UserMission.objects.filter(user=request.user)
    cleared_ids = [um.mission.id for um in user_missions if um.cleared]

    context = {
        'missions': missions,
        'cleared_ids': cleared_ids,
    }
    return render(request, 'kenkou/mission.html', context)


def logs_view(request):
    return render(request, "kenkou/logs.html")


@login_required
def mission_clear(request, mission_id):
    if request.method != "POST":
        return redirect("kenkou:mission")

    mission = get_object_or_404(Mission, id=mission_id)
    today = date.today()

    # MissionClear に記録
    cleared, created = MissionClear.objects.get_or_create(
        user=request.user,
        mission=mission,
        date=today
    )

    if created:
        stock, _ = AttackStock.objects.get_or_create(user=request.user)
        stock.damage += mission.reward_damage
        stock.save()

    # 🔹 UserMission を更新
    user_mission, _ = UserMission.objects.get_or_create(
        user=request.user,
        mission=mission
    )
    user_mission.cleared = True
    user_mission.save()

    return redirect("kenkou:mission")


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ★ 作成後そのままログイン
            return redirect("kenkou:index")
    else:
        form = UserCreationForm()

    return render(request, "kenkou/signup.html", {"form": form})
