from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Event


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Имя пользователя"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Пароль"})
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Повторите пароль"}
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}),
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}),
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "description_long",
            "event_date",
            "participants",
            "photo_url",
        ]
        labels = {
            "name": "Название",
            "description": "Короткое описание",
            "description_long": "Длинное описание",
            "event_date": "Дата проведения конференции",
            "participants": "Участники",
            "photo_url": "Ссылка на обложку",
        }


class RoleAssignmentForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    role = forms.ChoiceField(
        choices=[("user", "User"), ("manager", "Manager"), ("admin", "Admin")]
    )
