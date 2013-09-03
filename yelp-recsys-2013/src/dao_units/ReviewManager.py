import json
from common.utils import ( print_debug, DEBUG_INT, INFO_INT)
from models.review import Review
import pickle
class ReviewManager:

	def __init__(self, review_file):

		#stats

		self.review_file = review_file

		self.load_review_data(self.review_file)


	def load_review_data(self, review_file):

		total_stars = 0
		total_reviews = 0
		review_item_hash = {}
		user_business_rating = {}
		total_business_rating_by_user = {}
		total_business_rating_by_user_count = {}
		total_user_rating_in_business = {}
		total_user_rating_in_business_count = {}
		print_debug("Starting to read review file from:" + review_file, INFO_INT)
 		f_bus = open(review_file)

 		count = 0
 		for line in f_bus:
 			review_line = json.loads(line)
 			review_item = Review(review_line)
 			review_item_hash[review_item.review_id] = review_item
 			key = self.user_business_key(review_item)
 			user_business_rating[key] = review_item
 			count+=1

 			#increment user rating
 			self.increment_hash_count(
 				total_user_rating_in_business, 
 				review_item.user_id,  
 				review_item.stars,
 			)

 			self.increment_hash_count(
 				total_user_rating_in_business_count, 
 				review_item.user_id,  
 				1,
 			)

 			#increment business rating
 			self.increment_hash_count(
 				total_business_rating_by_user,
 				review_item.business_id,
 				review_item.stars,
 			)

 			#increment business rating
 			self.increment_hash_count(
 				total_business_rating_by_user_count,
 				review_item.business_id,
 				1,
 			)

 			total_stars += review_item.stars

 			total_reviews += 1
 			print_debug("Reading record review_id: " + str(review_item.review_id), DEBUG_INT)
 		f_bus.close()

# 		print_debug("Total reviews line read: " + str(count), INFO_INT)
# 		print_debug("Total unique review item read: " + str(len(review_item_hash.keys())), INFO_INT)
# 		print_debug("Total stars: " + str(self.get_total_stars()), INFO_INT)
# 		print_debug("Avg stars rating:" + str(self.get_average_review()), INFO_INT)
 	
 		data = { 'review_item_hash' : review_item_hash, 
				'user_business_rating' : user_business_rating,
				'total_business_rating_by_user' : total_business_rating_by_user,
				'total_business_rating_by_user_count': total_business_rating_by_user_count,
				'total_user_rating_in_business' : total_user_rating_in_business,
				'total_user_rating_in_business_count' : total_user_rating_in_business_count,
				'total_reviews' : total_reviews,
				'total_stars' : total_stars
		}
 		
 		
 		self.data = { 'data' :  data}
 	

 	def increment_hash_count(self, hash_object, key, incerement_val):
 		val = 0
 		if key in hash_object:
 			val = hash_object[key]
 		hash_object[key] = val  + incerement_val


 	def total_items(self):
 		return len(self.review_item_hash.keys())

 	def get_item(self, id):
 		return self.review_item_hash[id] 		

 	def get_all_item_keys(self):
 		return self.review_item_hash.keys() 		


 	def user_business_key(self, review_item):
 		return self._get_key(review_item.user_id, review_item.business_id)

 	def _get_key(self, user_id, bussiness_id):
 		return "-".join([user_id, bussiness_id])

 	def get_total_stars(self):
 		return self.total_stars

 	def get_total_reviews(self):
 		return self.total_reviews

 	def get_average_review(self):
 		return self.get_total_stars()/float(self.get_total_reviews())

 	def get_business_total_ratings(self, business_id):
 		return self.total_business_rating_by_user[business_id]

 	def get_business_total_ratings_count(self, business_id):
 		return self.total_business_rating_by_user_count[business_id]

 	def get_user_total_ratings_count(self, user_id):
 		return self.total_user_rating_in_business_count[user_id]
 	
 	def get_business_avg_rating(self, business_id):
 		return float(self.get_business_total_ratings(business_id))/self.get_business_total_ratings_count(business_id)

 	def get_user_total_ratings(self, user_id):
 		return self.total_user_rating_in_business[user_id]

 	def get_user_avg_rating(self, user_id):
 		return float(self.get_user_total_ratings(user_id))/self.get_user_total_ratings_count(user_id)

 	def is_exist_user_business_rating(self, user_id, business_id):
 		if self._get_key(user_id, business_id) in self.user_business_rating:
 			return True
 		else:
 			return False

 	def get_user_business_rating(self,key):
 		return self.user_business_rating[key]
 	
 	def pickle(self,):
		with open("../data/review_manager.pkl", 'w') as f:
			pickle.dump(self.data, f)
 	