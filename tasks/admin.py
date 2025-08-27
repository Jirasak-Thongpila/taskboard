from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "due_date", "done")
    list_filter = ("done", "due_date")
    search_fields = ("title", "detail")
