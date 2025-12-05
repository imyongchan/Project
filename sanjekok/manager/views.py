from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def login(request):

    return render(request, "manager_login.html")

def main(request):
    
    return render(request, 'manager_main.html')

def dash(request):
    return render(request, 'manager_dash.html')
