from django import forms
from django.forms import ModelForm
from dishes import models
from django.contrib.auth.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple


class RecipesForm(ModelForm):
	class Meta:
		model = models.Dishes
		exclude = ('creator', 'other_votes', 'comment_count')
        boxes=forms.ModelMultipleChoiceField(queryset=models.Boxes.objects.all(),widget= FilteredSelectMultiple(("Boxes"),False,attrs={'rows':'10'}))
        ingredients=forms.ModelMultipleChoiceField(queryset=models.Ingredients.objects.all(),widget= FilteredSelectMultiple(("Ingredients"),False,attrs={'rows':'10'}))
