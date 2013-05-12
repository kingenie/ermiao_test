# coding: utf-8


from django.db import models
from django.conf import settings


AVATAR_DIR = 'user_avatar/%Y/%m/%d'


class Account( models.Model ):
	username = models.CharField( verbose_name = u'称号', max_length = 100, unique = True )
	email = models.EmailField( verbose_name = u'电子邮箱', max_length = 254, unique = True )
	password = models.CharField( verbose_name = u'密码', max_length = 100 )
	#avatar = models.URLField( verbose_name = u'头像', default = settings.DEFAULT_AVATAR_URL )

	created_time = models.DateTimeField( verbose_name = u'创建时间', auto_now_add = True )

	def clean_email( self ):
		email = self.cleaned_data['email']
		email = email.strip().lower()
		return email


class Avatar( models.Model ):
	account = models.ForeignKey( Account, unique = True )
	avatar_file_450 = models.ImageField( upload_to = AVATAR_DIR )
	avatar_file_160 = models.ImageField( upload_to = AVATAR_DIR )
	avatar_file_140 = models.ImageField( upload_to = AVATAR_DIR )
	weibo_url = models.URLField( null = True, blank = True )

