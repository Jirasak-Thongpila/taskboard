from django.shortcuts import render
from .models import Task

def dashboard(request):
    qs = Task.objects.all()
    if request.user.is_authenticated:
        qs = qs.filter(owner=request.user)
    return render(request, "tasks/dashboard.html", {"tasks": qs})
