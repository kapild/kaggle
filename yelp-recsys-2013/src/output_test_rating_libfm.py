import json
from models.review import Review

from dao.UserManager import UserManager
from dao.BusinessManager import BusinessManager
from algo.LibFMWithUserBusinessFeatures import LibFMWithUserBusinessFeatures

bus_train_file = "../data/yelp_training_set_business.json"
user_train_file = "../data/yelp_training_set_user.json"

review_data_file = "../data/final_test_set_review.json"
rating_out_file = "../data/rating.data.test"
bus_test_file = "../data/final_test_set_business.json"
user_test_file = "../data/final_test_set_user.json"

bus = BusinessManager(bus_train_file)
user = UserManager(user_train_file)

bus_test = BusinessManager(bus_test_file)
user_test = UserManager(user_test_file)

f_write = open(rating_out_file, "w")
line = ''

print "Starting to read the review file file from:" + review_data_file
f_bus = open(review_data_file)

model = LibFMWithUserBusinessFeatures(bus, user, bus_test, user_test)
for line in f_bus:
    review_line = json.loads(line)
    item = Review(review_line)

    line = model.get_output_line(item)
    print line
    f_write.write(line)

f_bus.close()
f_write.close()

print "Done creating a rating file :" + rating_out_file
