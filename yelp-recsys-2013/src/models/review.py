class Review:


	def __init__(self, json):
		self.user_id = self.data(json,'user_id')  
		self.review_id = self.data(json,'review_id') 
		self.text = self.data(json,'text') 
		self.stars = self.data(json,'stars', 1) 
		self.business_id = self.data(json,'business_id') 
		self.date = self.data(json,'date') 
		self.type = self.data(json,'type')
		
	def data(self, json, key, is_int=0):
		if key in json:
			return json[key]
		if(is_int == 1):
			return 0
		return None


		
