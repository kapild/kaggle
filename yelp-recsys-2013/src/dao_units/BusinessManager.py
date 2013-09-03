import json
from common.utils import ( print_debug, DEBUG_INT, INFO_INT)
from models.business import Business
import pickle

class BusinessManager:

	def __init__(self, business_file):

		self.business_file = business_file
		self.data = {}
		self.load_business_data(self.business_file)

	def load_business_data(self, business_file):

		business_item_hash = {}
		print_debug("Starting to read business file from:" + business_file, INFO_INT)
 		f_bus = open(business_file)

 		count = 0
 		rating = 0
 		for line in f_bus:
 			business_line = json.loads(line)
 			business_item = Business(business_line)
 			business_item_hash[business_item.business_id] = business_item
 			count+=1
 			rating+=business_item.stars
 			print_debug("Reading record business_id: " + str(business_item.business_id), DEBUG_INT)

 		all_bus_avg_rating = float(rating)/count
 		print_debug("Total business line  read: " + str(count), INFO_INT)
 		print_debug("Total unique business item read: " + str(len(business_item_hash.keys())), INFO_INT)
 		print_debug("All business avg rating: " + str(all_bus_avg_rating), INFO_INT)
	
 		data = { 'business_item_hash' : business_item_hash, 
				'all_bus_avg_rating' : all_bus_avg_rating
		}
 		
 		
 		self.data = { 'data' :  data}
	

 	def total_items(self):
 		return len(self.business_item_hash.keys())

 	def get_item(self, id):
 		return self.business_item_hash[id] 		 		

 	def get_all_item_keys(self):
 		return self.business_item_hash.keys()

 	def get_business_avg_rating(self, business_id):
 		return self.business_item_hash[business_id].stars

 	def get_all_business_avg_rating(self):
		return self.all_bus_avg_rating

 	def pickle(self,):
		with open("../data/business_manager.pkl", 'w') as f:
			pickle.dump(self.data, f)
