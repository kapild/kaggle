import sys
import json
import csv
import numpy as np
from sklearn.datasets.svmlight_format import dump_svmlight_file
from sklearn.feature_extraction import DictVectorizer, FeatureHasher
from sklearn.preprocessing  import normalize
from sklearn import cross_validation, linear_model, pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
features_headers= [
    "ratings", 
    "user_id", 
    "business_id",
    "business_cat1",
    "business_cat2",
    "business_cat3",
    'bus_avg_stars', 
    'user_avg_starts',
    'user_avg_review',
    'bus_avg_review',
    'is_open',
    'bus_name',
]

float_headers = set()
float_headers.add('bus_avg_stars')
float_headers.add('user_avg_starts')
float_headers.add('user_avg_review')
float_headers.add('bus_avg_review')

delete_headers = set()
delete_headers.add('ratings')

vectorizer = CountVectorizer()
transformer = TfidfTransformer()

#categorizer = vectorizer

categorizer = pipeline.Pipeline(
    [('vectorizer', vectorizer), ('transformer', transformer),]
)

#categorizer.fit(titles, )

def load_file(file_name, data_rows, ratings):

    print 'Openning CSV file'
    con = open(file_name, "r")
    data = csv.DictReader(con, fieldnames=features_headers)
    
    print 'Iterating over rows'
    count = 0
    for row in data:
        if ( count % 100000 == 0):
            print count
        count+=1    
        for header in row.keys():
            if header in float_headers:
                row[header]= float(row[header])
        ratings.append(float(row['ratings']))
        for header in delete_headers:            
            del row[header]            
        data_rows.append(row)

    return data_rows, ratings

def norm_float_headers(data):
    count = 0
    data_norm = []
    for row in data:
        data_row = {}
        if ( count % 100000 == 0):
            print count
        count+=1    
        for header in row.keys():
            if header in float_headers:
                data_row[header]= row[header]
        data_norm.append(data_row)

    final_norm = normalize(data_norm, axis=0)
    return final_norm
    
def dump_group_names(feature_list, grp_out_file, y_shape):

    print 'dumping group names to'  + str(grp_out_file)    
    f_write = open(grp_out_file, "w")
    f_write_explain = open(grp_out_file + ".explain", "w")
    
    grp_features = set()
    count= -1
    
    index = 0
    for feat in feature_list:
        tokens = feat.split('=')
        if(len(tokens) >= 2):
            feat_id = tokens[0]
        else:
            feat_id = feat
        if not feat_id in grp_features:
            count+=1
            grp_features.add(feat_id)
        f_write.write(str(count) + "\n")
        f_write_explain.write(str(index) + "\t" + str(count) + "\t"+ feat_id + "\t" + feat + "\n")
        index+=1
    
    count+=1
    for i in range(y_shape):
        f_write.write(str(count) + "\n")
        f_write_explain.write(str(index) + "\t" + str(count) + "\t"+ feat_id + "\t" + feat + "\n")
        index+=1
        
    f_write.close()
    f_write_explain.close()
    print '..done.. dumping group names to'  + str(grp_out_file)    
 
def extract_text_features(rows, feature_name):
    print 'Extarcting text features: ' + str(feature_name)
    text_row = []
    for row in rows:
        text_row.append(row[feature_name])
        del row[feature_name] 
    print 'done.. iterating ..'
    print ' Extarcting text features: ' + str(feature_name)

    text_feat_array = categorizer.fit_transform(text_row, )
    print '.. done .. Extarcting text features: ' + str(feature_name)

    return text_feat_array
    
if __name__ == '__main__':
    input_train_file = sys.argv[1]
    input_test_file = sys.argv[2]
    
    output_train_libsvm_file  = sys.argv[1] + ".libfm"
    output_test_libsvm_file  = sys.argv[2] + ".libfm"
    
    data_rows = []
    ratings = []
    
    data_rows, ratings = load_file(input_train_file, data_rows, ratings)
    print 'done iterating %s file.', input_train_file
    
    len_train = len(data_rows)
    
    data_rows, ratings = load_file(input_test_file, data_rows, ratings)
    print 'done iterating %s file.', input_test_file

    text_feat = extract_text_features(data_rows, 'bus_name')

    x_shape, y_shape = text_feat.shape
    #  v.transform
    vec = DictVectorizer()
    print 'Transforming to dict.'
    X = vec.fit_transform(data_rows)
    
    from scipy.sparse import hstack
    
    Y_COO = hstack((X,text_feat))
    Y = Y_COO.tocsr()

    #print vec.get_feature_names()
    print 'done.. Transforming to dict.'
    import pdb
    pdb.set_trace()
    dump_group_names(vec.get_feature_names(), output_train_libsvm_file + '.grp', y_shape)
    
    print 'Dumping train in SVMLight.'
    dump_svmlight_file(Y[0:len_train], ratings[0:len_train], output_train_libsvm_file )

    print 'Dumping test in SVMLight.'
    dump_svmlight_file(Y[len_train:], ratings[len_train:], output_test_libsvm_file )
    
    print 'done... Dumping in SVMLight.'


