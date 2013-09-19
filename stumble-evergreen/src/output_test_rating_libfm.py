import json
from dao.PageManager import PageManager
from algo.LibFMFeatures import LibFMFeatures

page_test_file = "../data/test.tsv"
page_test_out_file = "../data/test.feat"

print "Starting to read the page file file from:" + page_test_file



pm = PageManager(page_test_file)

f_write = open(page_test_out_file, "w")
line = ''

print "Starting to read the test file file from:" + page_test_file

model = LibFMFeatures(pm, pm)

output_header = model.get_feature_list()
output_header_text = model.get_header_text(output_header)
f_write.write(output_header_text + "\n")
            
index = 0

for page_id in pm.get_page_id_list():
    item = pm.get_item(page_id)
    index+=1
    if(index % 1000 == 0):
        print line

    line =  model.get_output_line(item)
    
    f_write.write(line)
     
f_write.close()

print "Done creating a test features file :" + page_test_out_file

