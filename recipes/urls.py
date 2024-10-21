from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, RecipeSearchView, add_recipe_view, AboutMeView

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('recipes/', RecipeListView.as_view(), name='list'),  # List view for recipes
    path('recipes/<pk>', RecipeDetailView.as_view(), name='detail'),  # Detail view
    path('search/', RecipeSearchView.as_view(), name='recipe_search'),  # Search view
    path('add/', add_recipe_view, name='add_recipe'),  # Add recipe URL
    path('about/', AboutMeView.as_view(), name='about_me'),
]