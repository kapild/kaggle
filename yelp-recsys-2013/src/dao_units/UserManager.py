import json
from common.utils import (print_debug, DEBUG_INT, INFO_INT)
from models.user import User
import pickle

class UserManager:

	def __init__(self, user_file):

		self.user_file = user_file
		self.data = {}
		self.load_user_data(self.user_file)


	def load_user_data(self, user_file):


		user_item_hash = {}
		print_debug("Starting to read user file from:" + user_file, INFO_INT)
 		f_bus = open(user_file)

 		count = 0
 		total_rating = 0
 		for line in f_bus:
 			user_line = json.loads(line)
 			user_item = User(user_line)
 			user_item_hash[user_item.user_id] = user_item
 			count += 1
 			total_rating += user_item.average_stars
 			print_debug("Reading record user_id: " + str(user_item.user_id), DEBUG_INT)

 		all_user_avg_rating = float(total_rating) / count
 		print_debug("Total users line read: " + str(count), INFO_INT)
 		print_debug("Total unique user item read: " + str(len(user_item_hash.keys())), INFO_INT)
 		print_debug("All user avg rating: " + str(all_user_avg_rating), INFO_INT)
 		
 		data = { 'user_item_hash' : user_item_hash, 
				'all_user_avg_rating' : all_user_avg_rating
		}
 		
 		
 		self.data = { 'data' :  data}
 		# f_bus.close()

 	def get_all_user_avg_rating(self):
 		return self.all_user_avg_rating

 	def total_items(self):
 		return len(self.user_item_hash.keys())


 	def get_item(self, id):
 		return self.user_item_hash[id]

 	def get_all_item_keys(self):
 		return self.user_item_hash.keys()

 	def get_user_avg_rating(self, user_id):
 		return self.user_item_hash[user_id].average_stars

 	def pickle(self,):
		with open("../data/user_manager.pkl", 'w') as f:
			pickle.dump(self.data, f)
