
def index( request ):
	# TODO
	# ...

	recent_photo = Photo.objects.filter( create_date__gte = (dt.now-timedelta(days=5)) )

	cat_photo = recent_photo.filter( pet__type = 'cat' ).order_by('-like_count')
	not_cat_photo = recent_photo.filter( pet_type__not = 'cat' ).order_by('-like_count')

	min_num = min( len(cat_photo), len(not_cat_photo) )
	cat_photo = cat_photo[:min_num]
	not_cat_photo = not_cat_photo[:min_num]

	random.shuffle( cat_photo )
	random.shuffle( not_cat_photo )

	# TODO
	# ...
