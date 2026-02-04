from django.urls import path
from . import views

app_name = "kenkou"

urlpatterns = [
  path('', views.index, name='index'),
  path("location/", views.location_receive, name="location_receive"),
  path("mission/", views.mission_view, name="mission"), 
  path("battle/", views.battle_view, name="battle"),
  path("set_goal/", views.set_goal_distance, name="set_goal"),
  path("logs/", views.logs_view, name="logs")
]
