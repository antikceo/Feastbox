from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.shortcuts import render

#categories for ingredients for sorting
class Ingredients(models.Model):
	name = models.CharField(max_length=50, unique=True)
	
	def __unicode__(self):
		return u'%s' % (self.name)

class BoxesManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)
        
#boxes with different types of food
class Boxes(models.Model):

	objects = BoxesManager()
	name = models.CharField(max_length=50, unique=True)
	#dishes = models.ManyToManyField(Dishes, blank=True, null=True)
	#image = models.ImageField(upload_to='Group-Photo', blank=True, null=True)
	#subscribers = models.ManyToManyField(User, related_name='subscriptions', blank=True, null=True)
	
	def __unicode__(self):
		return u'%s' % (self.name)
		
#dishes table
class Dishes(models.Model):
	name = models.CharField(max_length=40, unique=True)
	ingredients = models.ManyToManyField(Ingredients)
 	boxes = models.ManyToManyField(Boxes)
	creator = models.ForeignKey(User)
	image = models.ImageField(upload_to='Dish-Photo')
	recipe_url = models.URLField()
	other_votes = models.IntegerField(blank=True, null=True, default=0)
	date_added = models.DateTimeField(auto_now_add=True)
 	comment_count = models.IntegerField(blank=True, null=True, default=0)

	def natural_key(self):
		return (self.name)
 	#boxes = models.ManyToManyField(Boxes)
	#likes = models.ManyToMany(Likes)
 	
	def __unicode__(self):
		return u'%s' % (self.name)	

	class Meta:
		#trending = self.other_votes
		ordering = ["-other_votes"]
		
#user comments for a particular dish
class Comments(models.Model):
	user = models.ForeignKey(User)
	dish = models.ForeignKey(Dishes)
	comment = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)
	


#upvotes
class Upvotes(models.Model):
	dish = models.ForeignKey(Dishes)
	user = models.ForeignKey(User)
	date_added = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ["-date_added"]