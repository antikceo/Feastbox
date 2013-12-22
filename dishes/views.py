from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from dishes import models
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from haystack.forms import SearchForm
from django.core import serializers
from itertools import chain
from django.template import loader, Context
import json
from dishes import forms

@csrf_exempt
def home(request, template='frontend/home.html', page_template='frontend/scroll.html'):
	dishes = models.Dishes.objects.order_by('-date_added')
	boxes = models.Boxes.objects.order_by('name')
	
	if not request.user.is_authenticated():	
		#html = render_to_string('frontend/scroll.html', {'dishes': dishes}, context_instance=RequestContext(request))

		if request.is_ajax():
			template = page_template
			
		return render_to_response(template, {'dishes': dishes, 'page_template': page_template, 'boxes':boxes,}, context_instance=RequestContext(request))
		
	else:
		this_user = request.user.id
		username = request.user.username
		return_list = []
	
		for dish in dishes:
			return_list.append((dish, models.Upvotes.objects.filter(user=this_user, dish=dish)))

		#html = render_to_string('frontend/scroll.html', {'dishes': return_list}, context_instance=RequestContext(request))  

		if request.is_ajax():
			template = page_template
        
		return render_to_response(template, {'dishes': return_list, 'page_template': page_template, 'boxes':boxes, 'username':username,}, context_instance=RequestContext(request))

#trending dishes
def trending(dishes):
	response_dict = dishes.order_by('upvotes')
	popular_links = Link.objects.select_related()
	popular_links = popular_links.extra(
    	select = {'popularity': '(karma_total - 1) / POW((TIMESTAMPDIFF(HOUR, links.created, NOW()) + 2), 1.5)',},
    	order_by = ['-popularity',]
	)
	return response_dict

#recently added dishes
def recent(dishes):
	response_dict = dishes.order_by('-date_added')
	return response_dict
	
#most upvoted dishes
def most_upvoted(dishes):
	response_dict = dishes.order_by('-other_votes')
	return response_dict
	
#filters dishes by selcted criteria
def filter_by(filter):
	this_box = models.Boxes.objects.get(name=filter)
	response_dict =  models.Dishes.objects.filter(boxes=this_box)
	return response_dict

#all the filters and sorts on the home page	
@csrf_exempt
def filter_home(request, filterby, sortby):

	if filterby=="All":
		filtered_dishes = models.Dishes.objects.all()
	else:
		filtered_dishes = filter_by(filterby)
	
	if sortby == "TrendingNow":
		response_dict = trending(filtered_dishes)
	elif sortby == "RecentlyAdded":
		response_dict = recent(filtered_dishes)
	elif sortby == "AllTimeMostUpvoted":
		response_dict = most_upvoted(filtered_dishes)
	else:
		#not a valid option, default to trending
		response_dict = trending(filtered_dishes)
	
	if request.user.is_authenticated():
		dishes = []	
		for dish in response_dict:
			dishes.append((dish, models.Upvotes.objects.filter(user=request.user, dish=dish)))
		html = render_to_string('frontend/scroll.html', {'dishes': dishes}, context_instance=RequestContext(request))
	else:
		html = render_to_string('frontend/scroll.html', {'dishes': response_dict}, context_instance=RequestContext(request))
	return HttpResponse(html, content_type='application/html')
		 	
#dish page
def dish(request, id):
	this_dish = models.Dishes.objects.get(id=id)
	votes = models.Dishes.objects.get(id=id)
	dishes = models.Dishes.objects.all()
	if request.user.is_authenticated():
		like = models.Upvotes.objects.filter(user=request.user, dish=this_dish)
		return render_to_response('frontend/dish.html', {'this_dish': this_dish, 'dishes': dishes, 'liked': like,}, context_instance=RequestContext(request))
	else:
		return render_to_response('frontend/dish.html', {'this_dish': this_dish, 'dishes': dishes,}, context_instance=RequestContext(request))

	
#dish page
def browse(request):
	dishes = models.Dishes.objects.all()
	return render_to_response('frontend/browse.html', {'dishes': dishes})
	
#will eventually add parameter for user
@csrf_exempt
def upvote(request,id):
	this_user = request.user
	#user_upvotes = models.Upvotes.objects.filter(user=this_user)
	this_dish = models.Dishes.objects.get(id=id)
	
	response_dict = {}
	
	try:
		user_upvoted = models.Upvotes.objects.get(dish=this_dish, user=this_user)
	except:
		user_upvoted = None
		
	if user_upvoted:
		this_dish.other_votes -= 1
		remove_dish = user_upvoted.delete()
		this_dish.save()
	else:
		this_dish.other_votes += 1
		add_dish = models.Upvotes(dish=this_dish, user=this_user)
		add_dish.save()
		this_dish.save()
	
	response_dict.update({'vote_count' : this_dish.other_votes })
	return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
		

def login_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	else:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
        	# Correct password, and the user is marked "active"
			auth.login(request, user)
            # Redirect to a success page.
			return HttpResponseRedirect("/")
		else:
    		# Show an error page
			return HttpResponseRedirect("/accounts/login")

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def post_recipe(request):
	errors = []
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	else:
		is_logged = True
    	username = request.user.username
        if request.method == 'POST':
            user_this =  request.user
            user = models.Dishes(creator=user_this)
            form = forms.RecipesForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                cmodel = form.save()
                cmodel.save()
                url  = '/'
                return HttpResponseRedirect(url)
            else:
                errors.append('Please fill out all fields in the form!')
        else:
            form = forms.RecipesForm()
        return render_to_response('frontend/post-recipe.html', {'is_logged': is_logged, 'username': username, 'form': form, 'errors': errors}, context_instance = RequestContext(request))


def profile(request, username):
	#if not request.user.is_authenticated():
	#	return HttpResponseRedirect("/login")
	#else:
	that_user = auth.models.User.objects.get(username=username)
	#user upvotes
	upvotes = models.Upvotes.objects.filter(user=that_user).order_by('-date_added')
	#user posts
	posts = models.Dishes.objects.filter(creator=that_user).order_by('-date_added')
		
		
	return render_to_response('frontend/profile.html', { 'username': username, 'posts': posts, 'upvotes':upvotes}, context_instance = RequestContext(request))
		 
def how_it_works(request):
	return render_to_response('frontend/howitworks.html', {} ,context_instance = RequestContext(request))

def site_rules(request):	
	return render_to_response('frontend/site-rules.html', {} ,context_instance = RequestContext(request))