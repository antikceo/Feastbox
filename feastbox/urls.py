from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dishes import views
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
   	url(r'^$', 'views.home', name='home'),
    url(r'^logout/$', views.logout_view),
    url(r'^login/$', views.login_view),
    url(r'^accounts/', include('registration.urls')),
    url(r'^social/', include('socialregistration.urls',
                             namespace = 'socialregistration')),
   	url(r'^dish/(\w+)/$', 'views.dish', name='dish'),
   	url(r'^upvote/(\w+)/$', 'views.upvote', name='upvote'),
   	url(r'^browse/$', 'views.browse', name='browse'),
   	url(r'^how-it-works/$', 'views.how_it_works', name='how_it_works'),
   	url(r'^site-rules/$', 'views.site_rules', name='site_rules'),
	url(r'^filter_home/(\w+)/(\w+)/$', 'views.filter_home', name='filter_home'),
   	#url(r'^feastbox/', include('feastbox.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
   	url(r'^admin/', include(admin.site.urls)),
   	url(r'^ckeditor/', include('ckeditor.urls')),
   	url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
   	(r'^search/', include('haystack.urls')),
   	url(r'', include('social_auth.urls')),

    url(r'^post-recipe/$', views.post_recipe),
    url(r'^profile/(\w+)/$', 'views.profile', name='profile'),
)

urlpatterns += staticfiles_urlpatterns()