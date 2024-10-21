"""
URL configuration for recipe_project project.

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
from django.urls import path

# Include package allows you to use the include () function that will link the urls.py file in the app to the main urls.py file (this one)
from django.urls import include

# Settings allows you to access the MEDIA_URL and MEDIA_ROOT variables
from django.conf import settings

# Static provides access to the Django helper function static(), which allows you to create URLs from local folder name
from django.conf.urls.static import static

# Import view that is set up in the root views.py file
from .views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),  # URL pattern for admin site
    path('', include('recipes.urls')),  # Include recipe app URLs as the root
    path('login/', login_view, name='login'),  # Login view
    path('logout/', logout_view, name='logout'),  # Logout view
]

# Extend the urlpatters param to include the media info
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)