from django.contrib import admin
from dishes import models

class Dishes(admin.ModelAdmin):
    list_display = ('name','creator', 'image','recipe_url', 'other_votes', 'date_added',)
    list_filter = ('date_added',)
    ordering = ('name',)
    filter_horizontal = ('ingredients', 'boxes',)

class Ingredients(admin.ModelAdmin):
	list_display = ('name',)
    	
#class Tags(admin.ModelAdmin):
#	list_display = ('tag',)
	
#class Comments(admin.ModelAdmin):
#	list_display = ('user', 'dish', 'comment',)
	
class Boxes(admin.ModelAdmin):
	list_display = ('name', )
	
admin.site.register(models.Dishes, Dishes)
admin.site.register(models.Ingredients, Ingredients)
#admin.site.register(models.Tags, Tags)
#admin.site.register(models.Comments, Comments)
admin.site.register(models.Boxes, Boxes)