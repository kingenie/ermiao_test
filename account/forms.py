# coding: utf-8


from django import forms


class AccountForm( forms.Form ):
	username = forms.CharField( label = u'称号' )
	email = forms.EmailField( label = u'邮箱' )
	password = forms.CharField( label = u'密码', min_length = 6, widget = forms.PasswordInput )
	repeated_password = forms.CharField( label = u'确认密码', min_length = 6, widget = forms.PasswordInput )

	def clean( self ):
		c_data = self.cleaned_data
		pw = c_data.get('password')
		rp_pw = c_data.get('repeated_password')

		if pw and rp_pw and (pw != rp_pw):
			raise forms.ValidationError(u'密码不匹配')

		return c_data


class AvatarForm( forms.Form ):
	rotate_angle = forms.IntegerField( label = u'旋转角度' )
	avatar = forms.FileField( label = u'头像' )

