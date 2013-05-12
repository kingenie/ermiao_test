# coding: utf-8


from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('account.views',
	url(r'^register/?', 'register'),
	url(r'^uploadavatar/(?P<user_id>\d+)/?', 'upload_avatar'),
	url(r'^u/(?P<user_id>\d+)/?', 'user_profile'),
)

