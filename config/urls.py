from django.urls import include, path
from portfolio import views

urlpatterns = [
    path("health/", views.health_check, name="health_check"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap"),
    path("", include("portfolio.urls")),
]
