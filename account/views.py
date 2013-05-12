# coding: utf-8


import json
import Image
import urllib
import urllib2
import hashlib
from string import ascii_letters, digits

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from account.models import Account, Avatar
from account.forms import AccountForm, AvatarForm


SEND_WEIBO_URL = 'https://api.weibo.com/2/statuses/update.json'
ALPHANUMERIC = digits + ascii_letters


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

	acc = Account.objects.create(
		username = username, email = email,
		password = password,
	)

	gravatar_url = get_gravatar_url( email )
	acc.avatar_url = gravatar_url
	acc.save()

	# Redirect to some place
	return HttpResponseRedirect( 'http://www.ermiao.com' )


def upload_avatar( request, user_id ):
	tpl = 'account/upload_avatar.html'

	acc = get_object_or_404( Account, id = user_id )

	if request.method != 'POST':
		return render( request, tpl, {'form': AvatarForm()} )

	form = AvatarForm( request.POST, request.FILES )
	if not form.is_valid():
		return render( request, tpl, {'form': form} )

	c_data = form.cleaned_data
	avatar = c_data['avatar']
	rotate_angle = c_data['rotate_angle']

	avatar_obj = Avatar.objects.filter( account = acc )
	if not avatar_obj:
		avatar_obj = Avatar.objects.create( account = acc,
				avatar_file_450 = avatar,
				avatar_file_160 = avatar,
				avatar_file_140 = avatar,
			)
	else:
		avatar_obj = avatar_obj[0]
		avatar_obj.avatar_file_450 = avatar
		avatar_obj.avatar_file_160 = avatar
		avatar_obj.avatar_file_140 = avatar
		avatar_obj.save()

	# Rotate avatar
	orig_img = Image.open( avatar_obj.avatar_file_450.path )
	rotated_img = orig_img.rotate( rotate_angle )

	# Save real thumbnails
	AVATAR_WIDTH_MAP = (
		( avatar_obj.avatar_file_450, 450 ),
		( avatar_obj.avatar_file_160, 160 ),
		( avatar_obj.avatar_file_140, 140 ),
	)
	for save_obj, width in AVATAR_WIDTH_MAP:
		resized_img = resize_image_to_width( rotated_img, width )
		resized_img.save( save_obj.path )


	# Send weibo
	post_dict = {
		access_token: access_token,
		status: 'XXX在鸸鹋动物园(www.ermiao.com)上传了头像',
	}
	post_data = urllib.urlencode( post_dict )
	resp = urllib2.urlopen( SEND_WEIBO_URL, post_data )
	resp = json.loads( resp.read() )

	if not resp.get('error'):
		# Save weibo url
		mid = int(resp['mid'])
		uid = resp['user']['id']
		weibo_url = 'weibo.com/%s/%s' % ( uid, base62_encode(mid) )
		avatar_obj.weibo_url = weibo_url
		avatar_obj.save()

	return render( request, tpl, {'msg': 'upload success'} )


def user_profile( request, user_id ):
	tpl = 'account/user_profile.html'

	acc = get_object_or_404( Account, id = user_id )
	is_admin = check_admin( acc )

	avatar_obj = Avatar.objects.filter( account = acc )
	avatar_url = None
	weibo_url = None
	if avatar_obj:
		avatar_obj = avatar_obj[0]
		avatar_url = avatar_obj.avatar_file_140.url
		weibo_url = avatar_obj.weibo_url

	ctx = {
		'account': acc,
		'avatar_url': avatar_url,
		'is_admin': is_admin,
		'weibo_url': weibo_url,
	}
	return render( request, tpl, ctx )


###################################
## Functions below are not views
###################################

def resize_image_to_width( image_obj, width ):
	cur_width, cur_height = image_obj.size
	if cur_width <= width:
		resized_img = image_obj.copy()
	else:
		scale = cur_width * 1.0 / width
		height = cur_height / scale
		resized_img = image_obj.resize( (int(width), int(height)), Image.ANTIALIAS )

	return resized_img


def base62_encode( num, alphabet = ALPHANUMERIC ):
	if (num == 0):
		return alphabet[0]

	arr = []
	base = len(alphabet)
	while num:
		rem = num % base
		num = num // base
		arr.append(alphabet[rem])

	arr.reverse()
	return ''.join(arr)


def get_gravatar_url( email ):
	default_url = settings.DEFAULT_AVATAR_URL 
	size = settings.AVATAR_SIZE

	hashed_email = hashlib.md5( email ).hexdigest()
	url = settings.GRAVATAR_URL + hashed_email + '?'
	url += urllib.urlencode({'d': default_url, 's': str(size)})
	return url

