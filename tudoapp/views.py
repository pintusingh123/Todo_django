from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Todo
from .forms import Registration, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import PasswordResetToken

from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import secrets
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def login_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")

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
            messages.success(request, "Login Successful 🎉")
            return redirect("task_list")
           
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login_view")

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
    messages.success(request, "Logged out successfully.... ")
    return redirect("login_view")


@login_required
def task_list(request):
    query = request.GET.get('q', '')

    # Active tasks
    tasks = Todo.objects.filter(
        user=request.user,
        is_deleted=False
    ).order_by('-created_at')

    # Deleted tasks count (TRASH BADGE + DASHBOARD CARD)
    deleted_count = Todo.objects.filter(
        user=request.user,
        is_deleted=True
    ).count()

    # Optional: total stats (future use)
    total_tasks = Todo.objects.filter(user=request.user).count()

    if query:
        tasks = tasks.filter(title__icontains=query)

    return render(request, 'todo.html', {
        'task': tasks,
        'query': query,
        'deleted_count': deleted_count,
        'total_tasks': total_tasks
    })

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
    task = get_object_or_404(
        Todo,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        task.is_deleted = True
        task.deleted_at = timezone.now()

        task.save()   # ⭐ Ye line missing thi

        messages.success(request, "Task moved to Trash successfully.")

        return redirect("task_list")

    return render(
        request,
        "task_confirm_delete.html",
        {
            "task": task
        }
    )
 

@login_required
def trash_view(request):
    tasks = Todo.objects.filter(
        user=request.user,
        is_deleted=True
    ).order_by('-deleted_at')

    # optional: remaining days add karne ke liye
    for task in tasks:
        if task.deleted_at:
            days_passed = (timezone.now() - task.deleted_at).days
            task.remaining_days = max(0, 15 - days_passed)
        else:
            task.remaining_days = 15

    return render(request, "trash_view.html", {"tasks": tasks})

@login_required
def restore_task(request, pk):
    task = get_object_or_404(
        Todo,
        pk=pk,
        user=request.user,
        is_deleted=True
    )

    task.is_deleted = False
    task.deleted_at = None
    task.save()

    messages.success(request, "Task restored successfully")

    return redirect("trash_view")

@login_required
def delete_forever(request, pk):
    task = get_object_or_404(
        Todo,
        pk=pk,
        user=request.user,
        is_deleted=True
    )

    task.delete()

    messages.success(request, "Task permanently deleted")

    return redirect("trash_view")

def task_toggle(request, pk):
    task = get_object_or_404(Todo, pk=pk, user=request.user)

    if request.method == "POST":
        task.completed = not task.completed
        task.save()

    return redirect('task_list')


def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip()

        # Security:
        # Email exists ho ya nahi, same message return karenge.

        try:
            user = User.objects.get(email=email)

            # Purane unused tokens delete
            PasswordResetToken.objects.filter(
                user=user,
                is_used=False
            ).delete()

            # Secure Random Token
            token = secrets.token_urlsafe(32)

            PasswordResetToken.objects.create(
                user=user,
                token=token
            )

            reset_link = request.build_absolute_uri(
                reverse(
                    "reset_password",
                    kwargs={"token": token}
                )
            )

            subject = "Reset Your TaskFlow Password"

            message = f"""
Hi {user.username},

We received a request to reset your password.

Click the link below:

{reset_link}

This link will expire in 15 minutes.

If you didn't request this, you can ignore this email.

Thanks,
TaskFlow Team
"""

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )

        except User.DoesNotExist:
            pass

        messages.success(
            request,
            "If an account exists with this email, a password reset link has been sent."
        )

        return redirect("login_view")

    return render(request, "forget_password.html")


# -------------------------------
# Reset Password
# -------------------------------
def reset_password(request, token):

    token_obj = get_object_or_404(
        PasswordResetToken,
        token=token
    )

    # Token already used
    if token_obj.is_used:
        messages.error(
            request, "This password reset link has already been used.")
        return redirect("login_view")

    # Token expired
    if token_obj.is_expired():
        token_obj.delete()

        messages.error(
            request,
            "Password reset link has expired."
        )

        return redirect("forgot_password")

    if request.method == "POST":

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:

            messages.error(request, "Passwords do not match.")

            return render(
                request,
                "reset_password.html",
                {
                    "token": token
                }
            )

        try:

            validate_password(password1)

        except ValidationError as e:

            for error in e.messages:
                messages.error(request, error)

            return render(
                request,
                "reset_password.html",
                {
                    "token": token
                }
            )

        user = token_obj.user

        user.set_password(password1)

        user.save()

        token_obj.is_used = True

        token_obj.save()

        messages.success(
            request,
            "Password updated successfully. Please login."
        )

        return redirect("login_view")

    return render(
        request,
        "reset_password.html",
        {
            "token": token
        }
    )
