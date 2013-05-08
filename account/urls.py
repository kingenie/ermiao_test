# coding: utf-8


from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('account.views',
	url(r'^register/?', 'register'),
	url(r'^uploadavatar/?', 'upload_avatar'),
)

