import sys
from models.review import Review
import json


if __name__ == '__main__':
    input_file_name = sys.argv[1]
    output_file_name  = sys.argv[1] + ".submit"
    review_data_file = "../data/final_test_set_review.json"
    
    f_write = open(output_file_name, "w")
    line = ''
    print "Starting to read libFM output file from:" + input_file_name
    f_bus = open(input_file_name)
    f_review = open(review_data_file)
    
    count = 0
    f_write.write("review_id,stars" + "\n")
    review_lines = f_review.readlines()
    for line in f_bus:
        review_line = json.loads(review_lines[count])
        count+=1
        item = Review(review_line)
        print str(item.review_id) + "," + str(line)
        f_write.write(str(item.review_id) + "," + str(line))
    f_bus.close()
    print "...done :" + output_file_name
    
    f_write.close()



