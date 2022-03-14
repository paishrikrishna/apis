"""fitness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from apis.views import otp_verification, dashboard_apis, membership_data, user_data, available_dashboards, add_dashboard,todays_attendance_record, test, membership_detail
urlpatterns = [
    path('admin/', admin.site.urls),
    path('otp/',otp_verification),
    path('dashboard_apis/',dashboard_apis),
    path('membership_data/',membership_data),
    path('user_data/',user_data),
    path('available_dashboards/',available_dashboards),
    path('add_dashboard/',add_dashboard),
    path('todays_attendance_record/',todays_attendance_record),
    path('test/',test),
    path('membership_detail/',membership_detail)
]
