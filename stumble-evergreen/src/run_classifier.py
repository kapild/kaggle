import json
from dao.PageManager import PageManager
from algo.LibFMFeatures import LibFMFeatures


from dao.PageManager import PageManager 
from models.StumbleData import StumbleData
from common.CrossValidation import run_cross_validation

#
#output_header = model.get_feature_list()
#output_header_text = model.get_header_text(output_header)
#f_write.write(output_header_text + "\n")
#            
#index = 0

#for page_id in pm.get_page_id_list():
#    item = pm.get_item(page_id)
#    index+=1
#    if(index % 1000 == 0):
#        print line
#
#    line =  model.get_output_line(item)
#    
#    f_write.write(line)
#     
#f_write.close()

#print "Done creating a test features file :" + page_test_out_file



def generate_train_test(ARGS):
    train_file_name = ARGS['train_file_name']
    test_file_name = ARGS['test_file_name']


    train_pm = PageManager(train_file_name)
    test_pm = PageManager(test_file_name)

    st = StumbleData(train_pm.panda_data, test_pm.panda_data)
   
    feat_algo = LibFMFeatures(st)
    X_train, y_train, X_test = feat_algo.get_tranform_features()
    run_cross_validation(X_train, y_train, X_test)

if __name__ == '__main__':
    ARGS = {}
    ARGS['train_file_name'] = "../data/train.tsv"
    ARGS['test_file_name'] = "../data/test.tsv"

    generate_train_test(ARGS)