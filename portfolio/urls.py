from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("work/", views.work, name="work"),
    path("skills/", views.skills, name="skills"),
    path("contact/", views.contact, name="contact"),
]
