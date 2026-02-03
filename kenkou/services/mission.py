import random
from kenkou.models import Mission

def get_today_missions(count=1):
    missions = list(Mission.objects.all())
    return random.sample(missions, count)