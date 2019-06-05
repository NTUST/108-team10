from django.shortcuts import render
from datetime import datetime
import socket


def adminHandle(request):
    time = datetime.now()
    hostName = socket.gethostname()
    IPv4 = socket.gethostbyname(hostName)
    Data = {
        'VisteTime': time,
        'HostName': hostName,
        'IPv4': IPv4,
    }
    return render(request, 'AdminIndex.html', Data)
# Create your views here.
