"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.main, name="main"),
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("contacts/", views.contacts, name="contacts"),
    path("feedback", views.feedback_view, name="feedback"),
    path("gallery", views.gallery, name="gallery"),
    path("events_list", views.events_list, name="events_list"),
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),
    path(
        "events/<int:event_id>/register/", views.event_register, name="event_register"
    ),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path(
        "registrations/cancel/<int:event_id>/",
        views.cancel_registration,
        name="cancel_registration",
    ),
    path("admin-panel/", views.admin_panel, name="admin_panel"),
    path("admin-panel/create-event/", views.create_event, name="create_event"),
    path("admin-panel/assign-role/", views.assign_role, name="assign_role"),
    path("admin-panel/edit-event/<int:event_id>/", views.edit_event, name="edit_event"),
    path("manager/registrations/", views.manager_event_list, name="manager_event_list"),
    path(
        "manager/registrations/<int:event_id>/",
        views.view_event_registrations,
        name="view_event_registrations",
    ),
    path(
        "update-feedback-status/<int:feedback_id>/",
        views.update_feedback_status,
        name="update_feedback_status",
    ),
]
