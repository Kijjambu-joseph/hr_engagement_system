"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import redirect
from my_app.views import branch_hr_dashboard, employee_dashboard, genmanagerdash
from my_app.admin_site import hr_admin_site
from users import views as users_views



def redirect_method_prefixed_api_path(request, subpath):
    """Normalize malformed URLs like 'GET /api/...' to '/api/...'."""
    return redirect(f"/api/{subpath}", permanent=False)


urlpatterns = [
    path('', users_views.login_page, name='home'),
    path('admin/', hr_admin_site.urls),
    path('login/', users_views.login_page, name='login'),
    path('branchhrmanager/', branch_hr_dashboard, name='branch_hr_manager'),
    path('employeedash/', employee_dashboard, name='employee_dashboard'),
    path('genmanagerdash/', genmanagerdash, name='genmanagerdash'),
    path('api/auth/', include('users.urls')),
    path('api/', include('my_app.urls')),
    path('GET /api/<path:subpath>/', redirect_method_prefixed_api_path),
    path('GET /api/<path:subpath>', redirect_method_prefixed_api_path),
]



