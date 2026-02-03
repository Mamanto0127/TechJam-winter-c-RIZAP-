from django.shortcuts import render
import requests

def index(request):
    res = requests.get("https://ipinfo.io/json")
    data = res.json()

    return render(request, 'kenkou/index.html', {
        'response': data
    })
