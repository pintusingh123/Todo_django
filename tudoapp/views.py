from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Todo


def task_list(request):
    query = request.GET.get('q', '')

    task = Todo.objects.all().order_by('-created_at')

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


def task_add(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        des = request.POST.get('description', '').strip()

        if title:
            Todo.objects.create(
                title=title,
                description=des
            )
            return redirect('task_list')

        return render(request, 'todo-add.html', {
            'error': 'Title cannot be empty.'
        })

    return render(request, 'todo-add.html')


def task_updated(request, pk):
    task = get_object_or_404(Todo, pk=pk)

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


def task_deleted(request, pk):
    task = get_object_or_404(Todo, pk=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'task_confirm_delete.html', {
        'task': task
    })


def task_toggle(request, pk):
    task = get_object_or_404(Todo, pk=pk)

    if request.method == "POST":
        task.completed = not task.completed
        task.save()

    return redirect('task_list')
