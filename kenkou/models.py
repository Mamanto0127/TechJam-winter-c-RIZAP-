from django.db import models
from django.contrib.auth.models import User

class WalkLog(models.Model):  #歩いた歩数を記録するデータベースを作る宣言
    user = models.ForeignKey(User, on_delete=models.CASCADE)   #どのユーザの歩数記録かを保存
    date = models.DateField()  #いつの記録なのかを保存     6500歩 → 65ダメージ　※参考
    steps = models.IntegerField()  #その日に歩いた歩数を保存
    distance = models.FloatField()   #歩いた距離を保存
    

class Enemy(models.Model):   #敵を作るための宣下
    max_hp = models.IntegerField() #敵のHPを保存
    current_hp = models.IntegerField()

class Mission(models.Model):  #ミッション一覧を保存する宣言
    title = models.CharField(max_length=100) #ミッションのタイトル
    description = models.TextField()  #ミッションの詳しい説明
    reward_damage = models.IntegerField()   #ミッションクリア時に敵へ与えるダメージ量
