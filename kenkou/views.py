from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json

def location_receive(request):
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