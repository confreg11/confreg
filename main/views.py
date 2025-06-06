from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.db import connection
from .models import Event, UserProfile, Registration, Feedback
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    EventForm,
    RoleAssignmentForm,
    UserUpdateForm,
)
from django.contrib import messages
from django.utils import translation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.


def main(request):
    return render(request, "main.html")


def about(request):
    return render(request, "about.html")


def faq(request):
    return render(request, "faq.html")


def contacts(request):
    return render(request, "contacts.html")


def gallery(request):
    return render(request, "gallery.html")


@csrf_protect
def feedback_view(request):
    success = False

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        description = request.POST.get("description", "").strip()

        if name and phone and description:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO feedback (name, phone, description, status)
                    VALUES (%s, %s, %s, 'в ожидании')
                """,
                    [name, phone, description],
                )
            success = True

    return render(request, "feedback.html", {"success": success})


def events_list(request):
    translation.activate("ru")
    events = Event.objects.order_by("event_date")
    return render(request, "events_list.html", {"events": events})


def event_detail(request, event_id):
    translation.activate("ru")
    event = get_object_or_404(Event, pk=event_id)
    participants_list = event.participants.split(",") if event.participants else []
    participants_list = [p.strip() for p in participants_list]
    context = {
        "event": event,
        "participants_list": participants_list,
    }
    return render(request, "event_detail.html", context)


def register(request):
    translation.activate("ru")
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)

            # UserProfile.objects.create(user=user)

            messages.success(request, "Регистрация прошла успешно. Добро пожаловать.")
            return redirect("events_list")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("main")
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = UserLoginForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("main")


@login_required
def profile_view(request):
    translation.activate("ru")
    user = request.user
    show_form = request.GET.get("edit") == "1"

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserUpdateForm(instance=user)

    name_placeholder = "Заполните данные для регистрации в конференциях"
    first_name = user.first_name or name_placeholder
    last_name = user.last_name or name_placeholder

    registrations = Registration.objects.filter(user=user).select_related("event")
    registered_events = [reg.event for reg in registrations]

    context = {
        "form": form,
        "first_name": first_name,
        "last_name": last_name,
        "show_form": show_form,
        "registered_events": registered_events,
    }
    return render(request, "profile.html", context)


@login_required(login_url="/register/")
def event_register(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        first_name = request.POST.get("first_name").strip()
        last_name = request.POST.get("last_name").strip()

        user = request.user
        if first_name and first_name != user.first_name:
            user.first_name = first_name
        if last_name and last_name != user.last_name:
            user.last_name = last_name
        user.save()

        registration, created = Registration.objects.get_or_create(
            user=user, event=event
        )
        if created:
            messages.success(request, "Вы успешно зарегистрировались на мероприятие!")
        else:
            messages.info(request, "Вы уже зарегистрированы на это мероприятие.")

        return redirect("event_detail", event_id=event.id)

    return redirect("event_detail", event_id=event.id)


@login_required
def cancel_registration(request, event_id):
    user = request.user
    registration = Registration.objects.filter(user=user, event_id=event_id).first()

    if registration:
        registration.delete()
        messages.success(request, "Регистрация на мероприятие успешно отменена.")
    else:
        messages.warning(request, "Регистрация не найдена или уже отменена.")

    return redirect("profile")


@login_required
def admin_panel(request):
    translation.activate("ru")

    if request.user.userprofile.role != "admin":
        return redirect("profile")

    events = Event.objects.all()
    users = UserProfile.objects.exclude(user=request.user)

    return render(
        request,
        "admin_panel.html",
        {
            "events": events,
            "users": users,
        },
    )


@login_required
def create_event(request):
    translation.activate("ru")
    if request.user.userprofile.role != "admin":
        return redirect("profile")

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Мероприятие успешно создано.")
            return redirect("admin_panel")
    else:
        form = EventForm()

    return render(request, "create_event.html", {"form": form})


@login_required
def assign_role(request):
    if request.user.userprofile.role != "admin":
        return redirect("profile")

    if request.method == "POST":
        username = request.POST.get("username")
        new_role = request.POST.get("role")

        if not username or not new_role:
            messages.error(request, "Пожалуйста, заполните все поля.")
            return redirect("assign_role")

        try:
            user = User.objects.get(username=username)
            profile = user.userprofile
            profile.role = new_role
            profile.save()
            messages.success(request, f"Роль пользователя {username} успешно изменена.")
            return redirect("admin_panel")
        except User.DoesNotExist:
            messages.error(request, "Пользователь с таким именем не найден.")
            return redirect("assign_role")

    return render(request, "assign_role.html")


@login_required
def edit_event(request, event_id):
    if request.user.userprofile.role != "admin":
        return redirect("profile")

    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("admin_panel")
    else:
        form = EventForm(instance=event)

    return render(request, "edit_event.html", {"form": form, "event": event})


@login_required
def manager_event_list(request):
    translation.activate("ru")
    if request.user.userprofile.role != "manager":
        return redirect("profile")

    events = Event.objects.all()
    pending_feedback = Feedback.objects.filter(status="в ожидании")

    return render(
        request,
        "manager_event_list.html",
        {
            "events": events,
            "pending_feedback": pending_feedback,
        },
    )


@login_required
def view_event_registrations(request, event_id):
    translation.activate("ru")
    if request.user.userprofile.role != "manager":
        return redirect("profile")

    event = get_object_or_404(Event, id=event_id)
    registrations = Registration.objects.filter(event=event).select_related("user")

    if request.method == "POST":
        registration_id = request.POST.get("registration_id")
        Registration.objects.filter(id=registration_id).delete()
        return redirect("view_event_registrations", event_id=event.id)

    return render(
        request,
        "event_registrations.html",
        {"event": event, "registrations": registrations},
    )


@require_POST
@login_required
def update_feedback_status(request, feedback_id):
    if request.user.userprofile.role != "manager":
        return redirect("profile")

    feedback = get_object_or_404(Feedback, pk=feedback_id)
    new_status = request.POST.get("status")

    if new_status in ["в ожидании", "рассмотрено"]:
        feedback.status = new_status
        feedback.save()
        messages.success(request, "Статус обновлен успешно.")
    else:
        messages.error(request, "Недопустимый статус.")

    return redirect("manager_event_list")
