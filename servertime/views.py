from django.shortcuts import render

def server_time(request):
    return render(request, 'servertime/servertime.html')

def server_timezone(request):
    return render(request, 'servertime/servertimezone.html')

def server_date(request):
    return render(request, 'servertime/serverdate.html')

