from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user).order_by('created_at')
    context = {
        'tasks': tasks
    }
    return render(request, 'main/home.html', context)

@login_required
def save_task(request):
    if request.method == 'POST':
        data = request.POST
        task_name = data.get('task_name')
        task_note = data.get('task_note')
        due_date = data.get('due_date')
        due_time = data.get('due_time')
        priority = data.get('priority')
        tags = data.get('tags')

        if not task_name:
            messages.error(request, "Task name is required")
            return render(request, 'main/home.html')
        
        #date and time validation
        try:
            if due_date: 
                due_date = datetime.strptime(due_date, '%Y-%m-%d').date()

            if due_time: 
                due_time = datetime.strptime(due_time, '%H:%M').time()
        except ValueError as e:
            messages.error(request,'Invalid date and time format')
            return render(request, 'main/home.html')

        #create task
        task = Task(
            user = request.user,
            title = task_name,
            description = task_note,
            due_date = due_date,
            due_time = due_time,
            priority = priority,
            tags = tags
            )
        task.save()
        messages.success(request, 'task successfully saved')
        return redirect('home')
    else:
        return render(request, 'main/home.html')




                 