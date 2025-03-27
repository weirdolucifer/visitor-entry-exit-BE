"""
URL configuration for visitor_entry_exit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include

from visitor_entry_exit.controllers.health_status import (
    HealthStatusCheck,
    ReadinessCheck,
    LivelinessCheck,
)

urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(
        r"health/",
        HealthStatusCheck.as_view(),
        name="health_status",
    ),
    path(r"ready/", ReadinessCheck.as_view(), name="ready_status"),
    path(r"live/", LivelinessCheck.as_view(), name="live_status"),
    path(r"accounts/", include("account.urls")),
    path(r"visitor/", include("visitor.urls")),
    path(r"passes/", include("pass.urls")),
]
