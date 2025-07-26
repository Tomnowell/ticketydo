from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F, ExpressionWrapper, DurationField
from django.utils import timezone
from .models import Task, TaskSession
from .forms import TaskForm


def task_list(request):
    return render(request, 'tasks/task_list.html')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).prefetch_related('sessions')

    for task in tasks:
        task.total_duration = TaskSession.objects.filter(
            task=task,
            end_time__isnull=False
        ).annotate(
            duration=ExpressionWrapper(F('end_time') - F('start_time'), output_field=DurationField())
        ).aggregate(
            total=Sum('duration')
        )['total']

    active_sessions = {
        session.task.id: session
        for session in TaskSession.objects.filter(
            task__in=tasks,
            end_time__isnull=True
        )
    }

    context = {
        'tasks': tasks,
        'active_sessions': active_sessions
    }
    return render(request, 'tasks/task_list.html', context)

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


@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.is_completed = True
        task.save()
        return redirect('task-list')

    return redirect('task-list')  # fallback for GET

@login_required
def task_toggle(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.is_completed = not task.is_completed
        task.save()
        return redirect('task-list')

    return redirect('task-list')

@login_required
def task_start_timer(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    # Only start if no session is active
    active = TaskSession.objects.filter(task=task, end_time__isnull=True).first()
    if not active and request.method == 'POST':
        TaskSession.objects.create(task=task, start_time=timezone.now())

    return redirect('task-list')

@login_required
def task_stop_timer(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    session = TaskSession.objects.filter(task=task, end_time__isnull=True).first()
    if session and request.method == 'POST':
        session.end_time = timezone.now()
        session.save()

    return redirect('task-list')