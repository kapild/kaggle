import json
from models.review import Review

from dao.UserManager import UserManager
from dao.BusinessManager import BusinessManager
from algo.LibFMWithUserBusinessFeatures import LibFMWithUserBusinessFeatures

bus_train_file = "../data/yelp_training_set_business.json"
user_train_file =  "../data/yelp_training_set_user.json"
review_data_file = "../data/yelp_training_set_review.json"
rating_out_file = "../data/rating.data.train" 
bus = BusinessManager(bus_train_file)
user = UserManager(user_train_file)

f_write = open(rating_out_file, "w")
line = ''

print "Starting to read the review file file from:" + review_data_file
f_bus = open(review_data_file)

model = LibFMWithUserBusinessFeatures(bus, user, bus, user)

output_header = model.get_feature_list()
output_header_text = model.get_header_text(output_header)
f_write.write(output_header_text + "\n")
            
index = 0
for line in f_bus:
    review_line = json.loads(line)
    item = Review(review_line)
    line =  model.get_output_line(item)
    index+=1
    if(index % 1000 == 0):
        print line
    f_write.write(line)
     
f_bus.close()
f_write.close()

print "Done creating a rating file :" + rating_out_file



