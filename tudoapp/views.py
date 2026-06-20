from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Todo
from .forms import Registration, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required




def login_view(request):

    form = LoginForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect("task_list")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html", {
        "form": form,
         
    })


def signup_view(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "REgistration Successfully...")
            return redirect("task_list")
        else:
            messages.error(
                request, "Registration Failed please try again later...")

    else:
        form = Registration()

    return render(request, "signup.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You Have been logged Out")
    return redirect("login_view")


@login_required
def task_list(request):
    query = request.GET.get('q', '')

    task = Todo.objects.filter(user=request.user).order_by('-created_at')

    if query:
        task = task.filter(title__icontains=query)

    return render(
        request,
        'todo.html',
        {
            'task': task,
            'query': query
        }
    )


@login_required
def task_add(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        des = request.POST.get('description', '').strip()

        if title:
            Todo.objects.create(
                user=request.user,
                title=title,
                description=des
            )
            return redirect('task_list')

        return render(request, 'todo-add.html', {
            'error': 'Title cannot be empty.'
        })

    return render(request, 'todo-add.html')


@login_required
def task_updated(request, pk):
    task = get_object_or_404(Todo, pk=pk, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        des = request.POST.get('description', '').strip()

        if title:
            task.title = title
            task.description = des
            task.save()

            return redirect('task_list')

        return render(request, 'todo-add.html', {
            'task': task,
            'error': 'Title cannot be empty.'
        })

    return render(request, 'todo-add.html', {
        'task': task
    })


@login_required
def task_deleted(request, pk):
    task = get_object_or_404(Todo, pk=pk, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'task_confirm_delete.html', {
        'task': task
    })


def task_toggle(request, pk):
    task = get_object_or_404(Todo, pk=pk, user=request.user)

    if request.method == "POST":
        task.completed = not task.completed
        task.save()

    return redirect('task_list')
