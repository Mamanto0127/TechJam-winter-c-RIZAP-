from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "kenkou"

urlpatterns = [
  path('', views.index, name='index'),
  path("location/", views.location_receive, name="location_receive"),
  path("mission/", views.mission_view, name="mission"), 
  path("mission/clear/<int:mission_id>/", views.mission_clear, name="mission_clear"),
  path("battle/", views.battle_view, name="battle"),
  path("set_goal/", views.set_goal_distance, name="set_goal"),
  path("logs/", views.logs_view, name="logs"),
  path("logout/", auth_views.LogoutView.as_view(), name="logout"),
  path("mission/clear/<int:mission_id>/", views.mission_clear, name="mission_clear"),
  path("signup/", views.signup_view, name="signup"),
]