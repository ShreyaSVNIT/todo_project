from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from datetime import date

# normal log out view
def logout_view(request):
    logout(request)
    return redirect('task_list')

def signup_view(request):
    # if user is alr logged in redirect immediately.
    if request.user.is_authenticated:
        return redirect('task_list')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'todo_app/signup.html', {'form': form})
    #syntax - render(Httprequest, template, variable sent to use inside the dictionnary)


@login_required
def task_list(request):
    '''
    show the task list
    '''
    # syntax - model.objects.get -> returns only 1 value what is asked or filter -> multiple entries.
    tasks = Task.objects.filter(user=request.user).order_by('completed')
    return render(request, 'todo_app/task_list.html', {'tasks': tasks, 'today': date.today()})

"""
this view handles GET and POST requests to add a new task.
GET request: Displays an empty form.

POST request: Receives form data, validates it, saves it to the database.

if reqest is not post, it shows the empty form, else it gets form data done.
"""

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False) #commit="false" lets us modify the instance before saving
            task.user = request.user #attaching current user to task
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo_app/add_task.html', {'form': form})

# allows user to update their task list by primary id , pk -> primary key
@login_required
def update_task(request, pk): 
    task = get_object_or_404(Task, pk=pk, user=request.user) #instead of get, use this to safely fetch
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task) #binds form to task instance..?? basically linking
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        # if its a GET request (first time seeing it) then comes pre filled with its existing data.
        form = TaskForm(instance=task)
    return render(request, 'todo_app/update_task.html', {'form': form})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('task_list')

@login_required
def mark_completed(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed #this line is to flip the boolean (its a toggle)
    task.save()
    return redirect('task_list')

'''
basically a crud operation goes like this:
1) Only logged in users are allowed to access (by use of decorator)
2) try to find the task in the given database by use of primary key and make sure it belongs to current user
if task not existing or belongs to someone else, 404 not found error
3) if request.method == POSt is to see if form was saved/submitted
4)    form = TaskForm(request.POST, instance=task)
create a form using the submitted data, and link it to the existing task.
5) finally show the HTML page that contains the form so user can edit and see the task.
'''
