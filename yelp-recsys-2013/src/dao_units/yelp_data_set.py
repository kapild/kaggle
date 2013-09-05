import sys
import json

from sets import Set
from common.utils import ( print_debug, DEBUG_INT, INFO_INT)

from numpy import zeros

from dao.ReviewManager import ReviewManager
class YelpData():


	def __init__(self,
		user_manager,
		business_manager,
		review_manager,
	):
		self.user_manager = user_manager
		self.business_manager = business_manager
		self.review_manager = review_manager



	def get_global_avg_rating_matrix(self):

#		f_write  = open("../data/user_business.matrix", 'w')
	# """ returns a very basic user to business rating matrix

	# Returns a user to business rating matrix by replacing unknown ratings
	# with average user rating, average business rating 
	# """		

		dim_user = len(self.user_manager.get_all_item_keys())
		dim_bus = len(self.business_manager.get_all_item_keys())
		print "user dimension: " + str(dim_user)
		print "business dimension: " + str(dim_bus)

		# initialize the final user business matrix with zeros
#		rating_matrix = zeros((dim_user, dim_user))


		print_debug("Generating the user business avg rating matrix", INFO_INT)
		index = 0
		mod_val = 10000
		all_user_avg_rating = self.user_manager.get_all_user_avg_rating()
		all_bus_avg_rating = self.business_manager.get_all_business_avg_rating()
		index_i = 0
		output_line = ""
		for user_id in self.user_manager.get_all_item_keys():
			index_j = 0
			user_row_array = zeros((1,dim_bus))
			for business_id in self.business_manager.get_all_item_keys():
				key = "-".join([user_id, business_id])
				index+=1
#				if ( index %  mod_val == 0):
#					print(".",)

				rating  = 0 
				if self.review_manager.is_exist_user_business_rating(user_id, business_id):
					rating = self.review_manager.get_user_business_rating(key)
				else:
					rating = self.review_manager.get_business_avg_rating(business_id) +\
					all_user_avg_rating - self.user_manager.get_user_avg_rating(user_id) +\
					all_bus_avg_rating - self.business_manager.get_business_avg_rating(business_id)
#				print  str(index_i) + ":" + str(index_j) + " " + "user:business_id:" + str(user_id) + ":" + str(business_id) + "\t" + str(rating)
				output_line+=str(rating) + ","
				#user_row_array[index_i, index_j] = rating
				index_j+=1
			#rating_matrix[index_i,:] = user_row_array
			if(index_i % 100 == 0):
				print str(index_i)
			index_i+=1
			
