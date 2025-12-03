from django.shortcuts import render

def manager_main(request):
    return render(request, "manager_main.html")
