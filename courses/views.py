from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import RegisterForm, ApplicationForm
from .models import Application


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    error = None
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            if user.username == 'Admin26':
                return redirect('admin_panel')
            return redirect('dashboard')
        else:
            error = "Неправильный логин или пароль. Пожалуйста, проверьте данные."
    return render(request, 'login.html', {'error': error})


@login_required
def create_application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'create_application.html', {'form': form})


@login_required
def dashboard_view(request):
    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        try:
            app = Application.objects.get(id=app_id, user=request.user)
            if app.status != 'new' and not app.feedback:
                app.feedback = request.POST.get('feedback_text')
                app.save()
        except Application.DoesNotExist:
            pass
        return redirect('dashboard')

    apps = Application.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'apps': apps})


@login_required
def admin_panel_view(request):
    if request.user.username != 'Admin26':
        return redirect('dashboard')

    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        new_status = request.POST.get('status')
        try:
            app = Application.objects.get(id=app_id)
            app.status = new_status
            app.save()
            messages.success(request, f"Статус заявки #{app.id} успешно обновлен.")
        except Application.DoesNotExist:
            messages.error(request, "Заявка не найдена.")
        return redirect('admin_panel')

    sort_by = request.GET.get('sort', '-created_at')
    status_filter = request.GET.get('status_filter', '')
    search_query = request.GET.get('search', '')

    apps_list = Application.objects.select_related('user').all().order_by(sort_by)

    if status_filter:
        apps_list = apps_list.filter(status=status_filter)
    if search_query:
        apps_list = apps_list.filter(user__fio__icontains=search_query)

    paginator = Paginator(apps_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_panel.html', {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
        'sort_by': sort_by,
        'status_choices': Application.STATUS_CHOICES
    })


def logout_view(request):
    logout(request)
    return redirect('login')