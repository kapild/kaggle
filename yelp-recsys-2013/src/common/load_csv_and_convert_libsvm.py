import sys
import json
import csv
import numpy as np
from sklearn.datasets.svmlight_format import dump_svmlight_file
from sklearn.feature_extraction import DictVectorizer, FeatureHasher
from sklearn.preprocessing  import normalize
from sklearn import cross_validation, linear_model, pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer

cat_headers = set()
cat_headers.add('user_id')
cat_headers.add('business_id')
cat_headers.add('business_cat1')
cat_headers.add('business_cat2')
cat_headers.add('business_cat3')
cat_headers.add('bus_is_open')
cat_headers.add('city_text')


float_headers = set()
float_headers.add('bus_avg_stars')
float_headers.add('user_avg_starts')
float_headers.add('user_avg_review')
float_headers.add('bus_avg_review')
float_headers.add('user_cool')
float_headers.add('user_funny')
float_headers.add('user_useful')

#float_headers.add('business_cat_num')

float_header_list = None
text_headers = set()
text_headers.add('bus_name')

rating_header = 'rating'

delete_headers = set()
delete_headers.add('rating')

vectorizer = CountVectorizer()
transformer = TfidfTransformer()

#tdidf_transformer= TfidfVectorizer()
#categorizer = vectorizer

categorizer = pipeline.Pipeline(
    [('vectorizer', vectorizer), ('transformer', transformer),]
)

#categorizer = pipeline.Pipeline(
#    [('tfid', tdidf_transformer)]
#)

category_rows = []
numeric_rows = []
text_rows = []
rating_rows  = []

def load_file(file_name):

    global float_header_list


    print 'Openning CSV file'
    con = open(file_name, "r")
    data = csv.DictReader(con)
    
    print 'Iterating over rows'
    count = 0
    
    
    for row in data:
        local_float_header_list  = [] 
        
        if ( count % 100000 == 0):
            print count
        count+=1    
        
        cat_row = {}
        num_row = []
        text_row = {}
        for header in row.keys():
            if header in cat_headers:
                cat_row[header] = row[header]
            elif header in float_headers:
                num_row.append(float(row[header]))
                if float_header_list is None:
                    local_float_header_list.append(header)
            elif header in text_headers:
                text_row[header] = row[header]
        category_rows.append(cat_row)
        numeric_rows.append(num_row)
        text_rows.append(text_row)
        rating_rows.append(float(row[rating_header]))
        if float_header_list is None:
            float_header_list = local_float_header_list[:]

def norm_float_headers(data):

    final_norm = normalize(data, axis=0)
    return final_norm
    
#dump_group_names(vec.get_feature_names(), feature_name_bus_name, 'bus_name', output_train_libsvm_file + '.grp', y_shape, )
    
def dump_group_names(cat_feature_list, text_feature_list, text_feat_name,  numeric_feature_list, grp_out_file, y_shape, ):

    print 'dumping group names to'  + str(grp_out_file)    
    f_write = open(grp_out_file, "w")
    f_write_explain = open(grp_out_file + ".explain", "w")
    f_write_grpby = open(grp_out_file + ".explain.grpby", "w")
    
    grp_features = set()
    count= -1
    
    index = 0
    for feat in cat_feature_list:
        tokens = feat.split('=')
        if(len(tokens) >= 2):
            feat_id = tokens[0]
        else:
            feat_id = feat
        if not feat_id in grp_features:
            count+=1
            grp_features.add(feat_id)
            f_write_grpby.write("start_index=" + str(index) + "\t"  + " group=" + str(feat_id) + "\n")            
        f_write.write(str(count) + "\n")
        f_write_explain.write("index=" + str(index) + "\t" + "grp=" + str(count) + "\t"+ "feat_name=" + feat_id + "\t" + "feat=" + feat + "\n")
        index+=1
    

    for i in range(len(numeric_feature_list)):
        count+=1
        f_write.write(str(count) + "\n")
        f_write_explain.write("index=" + str(index) + "\t" + "grp=" + str(count) + "\t"+ "feat_name=" + numeric_feature_list[i] + "\t" + "feat=numeric"  + "\n")
        f_write_grpby.write("start_index=" + str(index) + "\t"  + " group=" + str(numeric_feature_list[i]) + "\n")            
        index+=1
    
    count+=1
    assert y_shape == len(text_feature_list)
    f_write_grpby.write("start_index=" + str(index) + "\t"  + " group=" + str(text_feat_name) + "\n")            
    for i in range(y_shape):
        f_write.write(str(count) + "\n")
        f_write_explain.write("index=" + str(index) + "\t" + "grp=" + str(count) + "\t"+ "feat_name=" + text_feat_name + "\t" + "feat=" + text_feature_list[i].encode("utf-8") + "\n")
        index+=1
    
    f_write.close()
    f_write_explain.close()
    print '..done.. dumping group names to'  + str(grp_out_file)    
 
def extract_text_features(rows, feature_name):
    print 'Extarcting text features: ' + str(feature_name)
    text_row = []
    for row in rows:
        text_row.append(row[feature_name])
    print 'done.. iterating ..'
    print ' Extarcting text features: ' + str(feature_name)

    text_feat_array = categorizer.fit_transform(text_row, )
    print '.. done .. Extarcting text features: ' + str(feature_name)
    
    return text_feat_array, categorizer.steps[0][1].get_feature_names()
    
if __name__ == '__main__':
    input_train_file = sys.argv[1]
    input_test_file = sys.argv[2]
    
    output_train_libsvm_file  = sys.argv[1] + ".libfm"
    output_test_libsvm_file  = sys.argv[2] + ".libfm"
    
    load_file(input_train_file)
    print 'done iterating %s file.', input_train_file
    len_train = len(rating_rows)

    load_file(input_test_file)
    print 'done iterating %s file.', input_test_file

    # text
    X_0_text_feat_bus_name, feature_name_bus_name = extract_text_features(text_rows, 'bus_name')
    x_shape, y_shape = X_0_text_feat_bus_name.shape
        
    # numeric
    X_1_norm_feat = norm_float_headers(numeric_rows)

    # category
    vec = DictVectorizer()
    print 'Transforming to dict.'
    X_2_cat_feat = vec.fit_transform(category_rows)
    

    from scipy.sparse import hstack

    
    Y_temp = hstack((X_2_cat_feat,X_1_norm_feat))
    Y_temp_2 = hstack((Y_temp,X_0_text_feat_bus_name))
    Y = Y_temp_2.tocsr()
    

    dump_group_names(vec.get_feature_names(), feature_name_bus_name, 'bus_name',float_header_list,  output_train_libsvm_file + '.grp', y_shape, )

    
    print 'Dumping train in SVMLight.'
    dump_svmlight_file(Y[0:len_train], rating_rows[0:len_train], output_train_libsvm_file )

    print 'Dumping test in SVMLight.'
    dump_svmlight_file(Y[len_train:], rating_rows[len_train:], output_test_libsvm_file )
    
    print 'done... Dumping in SVMLight.'


