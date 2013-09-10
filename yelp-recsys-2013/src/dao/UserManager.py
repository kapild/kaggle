import json
from common.utils import (print_debug, DEBUG_INT, INFO_INT)
from models.user import User
import pickle

class UserManager:

	def __init__(self, user_file):

		self.user_file = user_file
		self.user_item_hash = {}
		self.count = 0
		self.total_rating_count = 0
		self.total_review_count = 0
		self.total_funny = 0
		self.total_cool = 0
		self.total_useful = 0
		self.load_user_data(self.user_file)


	def load_user_data(self, user_file):


		user_item_hash = {}
		print_debug("Starting to read user file from:" + user_file, INFO_INT)
 		f_bus = open(user_file)

 		count = 0
 		total_stars = 0
 		total_review = 0
 		for line in f_bus:
 			user_line = json.loads(line)
 			user_item = User(user_line)
 			user_item_hash[user_item.user_id] = user_item
 			stars = user_item.average_stars
 			total_stars+=stars
 			total_review+= user_item.review_count
 			if user_item.votes:
				self.total_funny += user_item.funny
				self.total_cool += user_item.cool
				self.total_useful += user_item.useful

 			count+=1
 			print_debug("Reading record user_id: " + str(user_item.user_id), DEBUG_INT)

 		self.user_item_hash = user_item_hash
 		self.total_review_count = total_review
 		self.count = count
 		self.total_rating_count = total_stars
 		f_bus.close()

 	def get_item(self, id):
 		return self.user_item_hash[id] 		 		

 	def get_all_item_keys(self):
 		return self.user_item_hash.keys()

 	def is_exists(self, id):
 		return id in self.user_item_hash

 	def get_avg_user_stars(self):
 		return float(self.total_rating_count)/self.count

 	def get_avg_user_review_count(self):
 		return float(self.total_review_count)/self.count

 	def get_user_stars(self, id):
 		return self.get_item(id).average_stars

 	def get_user_review_count(self, id):
 		return self.get_item(id).review_count

 	def get_user_funny(self, id):
 		return self.get_item(id).funny

 	def get_user_cool(self, id):
 		return self.get_item(id).cool
 	
 	def get_user_useful(self, id):
 		return self.get_item(id).useful

 	def get_avg_user_funny(self):
 	 	return float(self.total_funny)/self.count
 	
 	def get_avg_user_cool(self):
 	 	return float(self.total_cool)/self.count
 	
 	def get_avg_user_useful(self):
 		return float(self.total_useful)/self.count
		
 	def pickle(self,):
		with open("../data/user_manager.pkl", 'w') as f:
			pickle.dump(self.data, f)
