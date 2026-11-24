from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", lambda request: HttpResponse("QuickPoll is running")),  # remove later
    # path("api/", include("polls.urls")),   # Ravinder
    # path("", include("web.urls")),         # Rishi
]
