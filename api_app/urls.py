from django.urls import path
import api_app.views as api_views
urlpatterns = [
    path("", api_views.home),
]