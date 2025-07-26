from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

def task_list(request):
    return render(request, 'tasks/task_list.html')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task-list')
        # ❗ If invalid, re-render form with errors:
        return render(request, 'tasks/task_form.html', {'form': form})
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

from django.shortcuts import get_object_or_404

@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.is_completed = True
        task.save()
        return redirect('task-list')

    return redirect('task-list')  # fallback for GET