from django import forms
from .models import Recipe   # Access Recipe model

# Set chart choices
CHART_CHOICES = (
    ("#1", "Bar Chart"),
    ("#2", "Pie Chart"),
    ("#3", "Line Chart"),
)

# Define form to allow users to search by recipe name, ingredient and optional chart
class RecipeSearchForm(forms.Form):
    Recipe_Name = forms.CharField(
        required=False,
        max_length=100,
        label="Recipe Name",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter a Recipe Name"}
        ),
    )

    # Dynamically populate the Ingredients choices
    def get_ingredients_choices():
        all_ingredients = set()
        recipes = Recipe.objects.all()
        for recipe in recipes:
            ingredients_list = recipe.ingredients.split(',')
            all_ingredients.update([ingredient.strip() for ingredient in ingredients_list])

        return [(ingredient, ingredient) for ingredient in sorted(all_ingredients)]

    Ingredients = forms.MultipleChoiceField(
        required=False,
        choices=get_ingredients_choices(),
        label="Ingredients",
        widget=forms.SelectMultiple(),
    )

    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,
        widget=forms.Select(),
        required=False,
        label="Chart Type",
    )

    # Validate that user has selected as least a name or ingredient
    def clean(self):
        cleaned_data = super().clean()
        recipe_name = cleaned_data.get("Recipe_Name")
        ingredients = cleaned_data.get("Ingredients")

        if not recipe_name and not ingredients:
            raise forms.ValidationError("Please enter a recipe name or select ingredients.")
        return cleaned_data

class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe  # Specify the model to associate with the form
        fields = ['name', 'cooking_time', 'ingredients', 'pic']  # Specify the fields to be included in the form

        # Customize the form field widgets
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Recipe Name'
            }),
            'cooking_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cooking Time (in minutes)'
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Ingredients separated by commas',
                'rows': 4,
            }),
            'pic': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            })
        }

        # Customize labels if needed
        labels = {
            'name': 'Recipe Name',
            'cooking_time': 'Cooking Time',
            'ingredients': 'Ingredients (comma-separated)',
            'pic': 'Recipe Image',
        }

    # Add any custom validation logic here if needed
    def clean_ingredients(self):
        ingredients = self.cleaned_data.get('ingredients')
        if len(ingredients.split(',')) > 10:
            raise forms.ValidationError('Please limit to 10 ingredients.')
        return ingredients