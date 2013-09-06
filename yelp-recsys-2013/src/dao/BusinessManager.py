import json
import string
from common.utils import ( print_debug, DEBUG_INT, INFO_INT)
from models.business import Business
import pickle

class BusinessManager:

	def __init__(self, business_file):

		self.business_file = business_file
		self.business_item_hash = {}
		self.category_hash = {}

		self.count = 0		
		self.total_rating_count = 0
		self.total_review_count = 0
		
		self.load_business_data(self.business_file)
		self.max_cat, self.max_cat_count = self.store_max_cat(self.category_hash, self.business_item_hash)

	def load_business_data(self, business_file):

		business_item_hash = {}
		print_debug("Starting to read business file from:" + business_file, INFO_INT)
 		f_bus = open(business_file)

 		count = 0
 		cat_count = 0
 		total_review_count = 0
 		for line in f_bus:
 			business_line = json.loads(line)
 			business_item = Business(business_line)
 			business_item_hash[business_item.business_id] = business_item
 			cat_count = self.update_categories(business_item, self.category_hash, cat_count)
 			total_review_count+=business_item.review_count
 			count+=1
 			print_debug("Reading record business_id: " + str(business_item.business_id), DEBUG_INT)

 		self.total_review_count= total_review_count
 		self.count = count
 	 	self.business_item_hash = business_item_hash

 	def update_categories(self, business_item, category_hash, cat_count):
 		categories = business_item.categories
 		for cat in categories:
 			cat_lower = string.lower(cat)
 			if cat_lower in category_hash:
 				continue
 			else:
 				category_hash[cat_lower] = cat_count
	  			cat_count+=1
 		return cat_count

 	def store_max_cat(self, category_hash, business_item_hash):
 		
 		cat_count = {}
 		count = 0
 		total_stars = 0
 		for bus in business_item_hash:
 			count+=1
 			cats = business_item_hash[bus].categories
 			stars = business_item_hash[bus].stars
 			
 			total_stars+=stars
 			for cat in cats:
 				cat_id = self.get_cat_id(cat)
 				if cat_id in cat_count:
 					cat_count[cat_id]+=1
 				else:
 					cat_count[cat_id] =1
 		
 		max_count = None
 		max_cat = None
 		self.total_rating_count = total_stars 		
 		
 		# get the max_cat count and max cat
 		for cat_count_key  in cat_count.keys():
 			 if max_count is None or cat_count[cat_count_key] > max_count:
 			 	max_count = cat_count[cat_count_key]
 			 	max_cat = cat_count_key
 		return max_cat, max_count

 	def total_items(self):
 		return len(self.business_item_hash.keys())

 	def get_item(self, id):
 		return self.business_item_hash[id] 		 		

 	def get_norm_rating_count(self, id):
 		return float(self.get_item_rating(id))/self.total_rating_count

 	def get_norm_item_review_count(self, id):
 		return float(self.get_item_review_count(id))/self.total_review_count

 	def get_avg_norm_review_count(self):
 		return 1/float(self.count)

 	def get_avg_norm_rating_count(self):
 		return 1/float(self.count)
 	
 	def get_item_rating(self, id):
 		return self.get_item(id).stars
 		
 	def get_item_review_count(self, id):
 		return self.get_item(id).review_count

 	def get_item_is_open(self, id):
 		return self.get_item(id).open

 	def get_item_name(self, id):
 		return self.get_item(id).name
 	
 	def is_exists(self, id):
 		return id in self.business_item_hash
 	
 	def get_all_item_keys(self):
 		return self.business_item_hash.keys()

 	def get_bus_city_text(self, id):
 		city_text = string.lower(self.get_item(id).city)
 		return city_text.split(" ")[0]

 	def get_max_cat_id(self):
 		return self.max_cat


 	def get_avg_bus_stars(self):
 		return float(self.total_rating_count)/self.count

 	def get_avg_bus_review_count(self):
 		return float(self.total_review_count)/self.count
 	
 	def get_cat_id(self, cat_text):
 		cat_lower_text = string.lower(cat_text) 
 		if cat_lower_text in self.category_hash:
 			return self.category_hash[cat_lower_text]
 	 	
 	 	return self.get_max_cat_id()
 	def pickle(self,):
		with open("../data/business_manager.pkl", 'w') as f:
			pickle.dump(self.data, f)
