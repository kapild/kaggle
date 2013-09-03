import json
from common.utils import (print_debug, DEBUG_INT, INFO_INT)
from models.review import Review
import pickle
class ReviewManager:

	def __init__(self, review_file):

		# stats
		self.review_file = review_file
		self.review_item_hash = {}
		self.load_review_data(self.review_file)

	def load_review_data(self, review_file):

		review_item_hash = {}
		print_debug("Starting to read review file from:" + review_file, INFO_INT)
 		f_bus = open(review_file)

 		for line in f_bus:
 			review_line = json.loads(line)
 			review_item = Review(review_line)
 			review_item_hash[str(review_item.user_id) + "-" + str(review_item.business_id)] = review_item
 			print_debug("Reading record review_id: " + str(review_item.review_id), DEBUG_INT)
 		f_bus.close()

 		self.review_item_hash = review_item_hash

 	def total_items(self):
 		return len(self.review_item_hash.keys())

 	def get_item(self, id):
 		return self.review_item_hash[id]

 	def get_all_item_keys(self):
 		return self.review_item_hash.keys()

 	def pickle(self,):
		with open("../data/review_manager.pkl", 'w') as f:
			pickle.dump(self.data, f)
