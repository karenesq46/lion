"""
URL configuration for crud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from crud import settings
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('home/', views.home, name = 'home'),
    path('signin/', views.signin, name='signin'),
    path('close/', views.close, name='close'),
    path('signup/', views.signup, name='signup'),

    path ('profile/', views.home, name='home'),
    path('<int:profile_id>/edit_profile', views.edit_profile, name = 'edit_profile'),
    path('<int:profile_id>/trash', views.trash_profile, name = 'trash_profile'),
   
    path('tasks/', views.tasks, name='tasks'),
    path('<int:task_id>/edit_task', views.edit_task, name = 'edit_task'),

    path('history/', views.list, name = 'history'),
    path('bitacora/', views.bitacora, name = 'bitacora'),

    path('export/excel/tasks', views.report, name='report'),
    path('export/excel/profiles', views.report, name='report-general')
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
