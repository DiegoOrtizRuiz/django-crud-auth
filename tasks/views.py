from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Tasks
from django.utils import timezone
# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    else:

        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username =request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': 'Username already exists'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm(),
            'error': 'Passwords did not match'
        })

      
def tasks(request):
    tasks = Tasks.objects.filter(user = request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', 
                  {
        'tasks': tasks
    })

def signuot (request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
        
def createTask (request):
    
    if request.method =='GET' :
        return render(request, 'create_task.html', {
            'form': TaskForm()
        })
    else:
        form = TaskForm(request.POST)
        print(request.POST)
        try:
            new_task = form.save(commit = False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm(),
                'error': 'Bad data passed in. Try again.'
            })
            
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Tasks, pk=task_id)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        task = get_object_or_404(Tasks, pk=task_id)
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Bad info'
            })
            
def completeTask(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')