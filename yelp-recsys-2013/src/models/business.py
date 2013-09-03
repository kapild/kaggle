# {
#   'type': 'business',
#   'business_id': (encrypted business id),
#   'name': (business name),
#   'neighborhoods': [(hood names)],
#   'full_address': (localized address),
#   'city': (city),
#   'state': (state),
#   'latitude': latitude,
#   'longitude': longitude,
#   'stars': (star rating, rounded to half-stars),
#   'review_count': review count,
#   'categories': [(localized category names)]
#   'open': True / False (corresponds to permanently closed, not business hours),
# }

class Business:

	def __init__(self, json):
		self.type = 'business'
		self.business_id = self.data( json , 'business_id',  )
		self.name = self.data( json, 'name')
		self.neighborhoods = self.data( json, 'neighborhoods' )
		self.full_address = self.data( json,'full_address')
		self.city = self.data( json,'city')
		self.state = self.data( json,'state')
		self.latitude = self.data( json,'latitude', 1)
		self.longitude = self.data( json,'longitude', 1)
		self.stars = self.data( json,'stars', 1)
		self.review_count = self.data( json,'review_count', 1)
		self.categories = self.data( json,'categories')
		self.open = self.data( json,'open')


	def data(self, json, key, is_int=0):
		if key in json:
			return json[key]
		if(is_int == 1):
			return 0
		return None





