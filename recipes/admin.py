from django.contrib import admin

# Import the class/model
from .models import Recipe

# Register your models here.
admin.site.register(Recipe)