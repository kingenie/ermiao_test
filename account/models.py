# coding: utf-8


from django.db import models
from django.conf import settings


class Account( models.Model ):
	username = models.CharField( verbose_name = u'称号', max_length = 100, unique = True )
	email = models.EmailField( verbose_name = u'电子邮箱', max_length = 254, unique = True )
	password = models.CharField( verbose_name = u'密码', max_length = 100 )
	avatar = models.URLField( verbose_name = u'头像', default = settings.DEFAULT_AVATAR_URL )

	created_time = models.DateTimeField( verbose_name = u'创建时间', auto_now_add = True )

	def clean_email( self ):
		email = self.cleaned_data['email']
		email = email.strip().lower()
		return email
