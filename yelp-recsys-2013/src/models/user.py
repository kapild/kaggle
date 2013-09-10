# {
#   'type': 'user',
#   'user_id': (encrypted user id),
#   'name': (first name),
#   'review_count': (review count),
#   'average_stars': (floating point average, like 4.31),
#   'votes': {'useful': (count), 'funny': (count), 'cool': (count)}
# }

class User:

	def __init__(self, json):
		self.type = 'user'
		self.user_id =  self.data(json,'user_id')
		self.name =  self.data(json,'name')
		self.review_count =  self.data(json,'review_count', 1)
		self.average_stars =  self.data(json,'average_stars', 1)
		self.votes =  self.data(json,'votes')
		if( self.votes):
			self.funny  = self.votes['funny']
			self.useful  = self.votes['useful']
			self.cool  = self.votes['cool']

	def data(self, json, key, is_int=0):
		if key in json:
			return json[key]
		if(is_int == 1):
			return 0
		return None

