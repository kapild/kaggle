import sys
from models.page import Page
import json
import csv

def get_label(val):
    if float(val) >= 0.5:
        return '1'
    else:
        return '0'


if __name__ == '__main__':
    libfm_predictions_file_name = sys.argv[1]
    output_file_name  = sys.argv[1] + ".submit"
    test_file_name = "../data/test.tsv"
    
    f_write = open(output_file_name, "w")
    line = ''
    print "Starting to read libFM output file from:" + libfm_predictions_file_name
    f_libfm_predicts = open(libfm_predictions_file_name)
    
    
    f_test = open(test_file_name, "r")
    test_data = csv.DictReader(f_test, delimiter="\t")
    
    import pdb
    pdb.set_trace()
    count = 0
    f_write.write("urlid,label" + "\n")
    libfm_lines = f_libfm_predicts.readlines()
    
    for row in test_data: 
        item = Page(row)
        out_str =  str(item.urlid) + "," + get_label(libfm_lines[count])
        print out_str
        f_write.write(out_str + "\n")
        count+=1
        
    f_libfm_predicts.close()
    print "...done :" + output_file_name
    
    f_write.close()



