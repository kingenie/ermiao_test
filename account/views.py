# coding: utf-8


import hashlib
import urllib

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect

from account.models import Account
from account.forms import AccountForm


def register( request ):
	tpl = 'account/register.html'

	if request.method != 'POST':
		return render( request, tpl, {'form': AccountForm()} )

	form = AccountForm( request.POST )
	if not form.is_valid():
		return render( request, tpl, {'form': form} )

	c_data = form.cleaned_data
	username = c_data['username']
	email = c_data['email']
	password = c_data['password']

	gravatar_url = get_gravatar_url( email )
	print gravatar_url
	# TODO

	Account.objects.create(
		username = username, email = email,
		password = password, avatar = avatar,
	)

	# Redirect to some place
	return HttpResponseRedirect( 'http://www.ermiao.com' )


def get_gravatar_url( email ):
	default_url = settings.DEFAULT_AVATAR_URL 
	size = settings.AVATAR_SIZE

	hashed_email = hashlib.md5( email ).hexdigest()
	url = settings.GRAVATAR_URL + hashed_email + '?'
	url += urllib.urlencode({'d': default_url, 's': str(size)})
	return url

