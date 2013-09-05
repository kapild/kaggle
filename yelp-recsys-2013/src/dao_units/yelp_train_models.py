import sys
import json

from sets import Set

from dao.UserManager import UserManager
from dao.BusinessManager import BusinessManager
from dao.ReviewManager import ReviewManager
from yelp_data_set import YelpData
class YelpReview():


	def __init__(self,
		review_file,
		user_file,
		business_file,
	):
		self.review_file = review_file
		self.user_file = user_file
		self.business_file = business_file
		self.run(self.user_file, self.business_file, self.review_file)

 	def run(self,user_file, business_file, review_file):
 		
 		user_manager = UserManager(user_file)
 		user_manager.pickle()
 		
 		business_manager = BusinessManager(business_file)
 		business_manager.pickle()

 		review_manager = ReviewManager(review_file)
 		review_manager.pickle()

 		yelp_train_set = YelpData(user_manager, business_manager, review_manager)

#		yelp_train_set.get_global_avg_rating_matrix()

if __name__ == '__main__':
	file_name = sys.argv[1]
	user_file_name = sys.argv[2]
	business_file_name = sys.argv[3]
	yelp_review = YelpReview(file_name, user_file_name, business_file_name)
