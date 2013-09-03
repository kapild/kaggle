from dao.UserManager import UserManager
from dao.BusinessManager import BusinessManager
from dao.ReviewManager import ReviewManager
from yelp_data_set import YelpData

import json
from models.review import Review


bus = BusinessManager("../data/yelp_training_set_business.json")
user = UserManager("../data/yelp_training_set_user.json")
review_data_file = "../data/yelp_training_set_review.json"

f_bus = open(review_data_file)

user_id = set()
for line in f_bus:
    review_line = json.loads(line)
    item = Review(review_line)
    user_id.add(item.user_id)

print len(user_id)     
f_bus.close()

#test_rev = ReviewManager("../data/yelp_test_set_review.json")
#test_rev = ReviewManager("../data/yelp_test_set_review.json")
#test_bus = BusinessManager("../data/yelp_test_set_business.json")
#test_user = UserManager("../data/yelp_test_set_user.json")
#
#count = 0
#count_pos = 0
#count_neg= 0
#
#count_user = 0
#count_bus = 0
#for rev in test_rev.get_all_item_keys():
#    item = test_rev.get_item(rev)
#    count+=1
#    if  bus.is_exists(item.business_id) and user.is_exists(item.user_id):
#        count_pos+=1 
#    if  bus.is_exists(item.business_id):
#        count_bus+=1 
#    if  user.is_exists(item.user_id):
#        count_user+=1 
#    if  not bus.is_exists(item.business_id) and not user.is_exists(item.user_id):
#        count_neg+=1 
#
#print str(float(count_pos)/count)
#print str(float(count_user)/count)
#print str(float(count_bus)/count)
#print str(float(count_neg)/count)