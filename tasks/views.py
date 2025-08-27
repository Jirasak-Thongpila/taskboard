from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Task

def dashboard(request):
    qs = Task.objects.all().order_by('-id')
    if request.user.is_authenticated:
        qs = qs.filter(owner=request.user)
    
    # Calculate progress
    total_count = qs.count()
    completed_count = qs.filter(done=True).count()
    progress_percentage = round((completed_count / total_count * 100) if total_count > 0 else 0)
    
    context = {
        'tasks': qs,
        'total_count': total_count,
        'completed_count': completed_count,
        'progress_percentage': progress_percentage,
    }
    return render(request, "tasks/dashboard.html", context)

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        detail = request.POST.get('detail', '')
        due_date = request.POST.get('due_date') or None
        
        if title:
            Task.objects.create(
                owner=request.user,
                title=title,
                detail=detail,
                due_date=due_date
            )
            messages.success(request, 'เพิ่มงานใหม่เรียบร้อยแล้ว')
        else:
            messages.error(request, 'กรุณาระบุชื่องาน')
    
    return redirect('dashboard')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    
    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.detail = request.POST.get('detail', task.detail)
        due_date = request.POST.get('due_date')
        task.due_date = due_date if due_date else None
        task.save()
        
        messages.success(request, 'แก้ไขงานเรียบร้อยแล้ว')
    
    return redirect('dashboard')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'ลบงานเรียบร้อยแล้ว')
    
    return redirect('dashboard')

@login_required
def mark_done(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    
    if request.method == 'POST':
        task.done = True
        task.save()
        messages.success(request, f'เสร็จสิ้นงาน "{task.title}" แล้ว')
    
    return redirect('dashboard')

@login_required
def mark_undone(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    
    if request.method == 'POST':
        task.done = False
        task.save()
        messages.info(request, f'เปลี่ยนสถานะงาน "{task.title}" เป็นยังไม่เสร็จ')
    
    return redirect('dashboard')
