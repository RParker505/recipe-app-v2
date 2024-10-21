from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, TemplateView   # To display list of recipes and their details
from .models import Recipe                  # To access Recipe model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import RecipeSearchForm, AddRecipeForm    # Import form from forms.py
import pandas as pd
from .utils import get_chart    # Import from utils.py

# Create your views here.

# Define home function that takes a request as an argument and returns a rendered object using the imported render function
def home(request):
    return render(request, 'recipes/recipes_home.html')

# List view
class RecipeListView(LoginRequiredMixin, ListView):                 # Class-based view
    model = Recipe                               # Specify model
    template_name = 'recipes/recipe_list.html'   # Specify template 

# Detail View
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipe_details.html'

class RecipeSearchView(LoginRequiredMixin, View):
    form_class = RecipeSearchForm  # Define form_class as a class attribute
    template_name = 'recipes/recipe_search.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()  # Now this will work because form_class is defined
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        # Default queryset for recipes
        queryset = Recipe.objects.all()

        # Initialize to None
        chart_type = None
        chart = None

        if form.is_valid():
            recipe_name = form.cleaned_data.get("Recipe_Name")
            ingredients = form.cleaned_data.get("Ingredients")
            chart_type = form.cleaned_data.get("chart_type")

            # Filter by recipe name
            if recipe_name:
                queryset = queryset.filter(name__icontains=recipe_name)

            # Filter by ingredients
            if ingredients:
                for ingredient in ingredients:
                    queryset = queryset.filter(ingredients__icontains=ingredient)

        # Convert queryset to DataFrame with calculated difficulty
        recipe_data = []
        for recipe in queryset:
            recipe_data.append({
                'name': recipe.name,
                'cooking_time': recipe.cooking_time,
                'difficulty': recipe.calculate_difficulty(),  # Call calculate_difficulty method
            })

        recipe_df = pd.DataFrame(recipe_data)

        # Generate chart if there are results and a valid chart type is provided
        if not recipe_df.empty and chart_type:
            if chart_type == "#1":  # Bar Chart
                chart = get_chart('bar', recipe_df)
            elif chart_type == "#2":  # Pie Chart
                chart = get_chart('pie', recipe_df)
            elif chart_type == "#3":  # Line Chart
                chart = get_chart('line', recipe_df)
            else:
                chart = None  # If the chart type is invalid, set chart to None

        # Add form, DataFrame, chart, and queryset (for recipe cards) to context
        context = {
            'form': form,
            'recipe_df': recipe_df.to_html() if not recipe_df.empty else None,
            'chart': chart if chart else None,
            'recipes': queryset,  # Pass queryset for recipe cards
        }
        return render(request, self.template_name, context)

@login_required
def add_recipe_view(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to create a new Recipe
            return redirect('recipes:list')  # Redirect to the recipe list page (adjust as needed)
    else:
        form = AddRecipeForm()
    
    return render(request, 'recipes/add_recipe.html', {'form': form})

# Class-based view for About Me
class AboutMeView(LoginRequiredMixin, TemplateView):
    template_name = 'recipes/about_me.html'