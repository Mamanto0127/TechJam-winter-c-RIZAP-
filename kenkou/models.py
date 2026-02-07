from django.db import models
from django.contrib.auth.models import User


class WalkLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    steps = models.IntegerField(default=0)
    distance = models.FloatField(default=0.0)

    class Meta:
        unique_together = ("user", "date")


class Mission(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    reward_damage = models.IntegerField()
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserMission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    cleared = models.BooleanField(default=False)


class AttackStock(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    damage = models.IntegerField(default=0)


class MissionClear(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ("user", "mission", "date")

    def __str__(self):
        return f"{self.user.username} - {self.mission.title} ({self.date})"


# ===== 敵マスター =====
class EnemyMaster(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    max_hp = models.IntegerField()
    image = models.ImageField(upload_to='enemies/')

    def __str__(self):
        return f"Lv.{self.level} {self.name}"


# ===== ユーザーごとの敵 =====
class UserEnemy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enemy = models.ForeignKey(EnemyMaster, on_delete=models.CASCADE)
    current_hp = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} vs {self.enemy.name}"
