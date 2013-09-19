import sys
import json
import csv
from string import lower
import cPickle as pickle

import numpy as np
from sklearn.datasets.svmlight_format import dump_svmlight_file
from sklearn.feature_extraction import DictVectorizer, FeatureHasher
from sklearn.preprocessing  import normalize
from sklearn import cross_validation, linear_model, pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
import sklearn.linear_model as lm
from sklearn import svm
from sklearn import metrics,preprocessing,cross_validation
import pandas as p
from common.utils import FILE_SEPERATOR 
cat_headers = set()
cat_headers.add('urlid')
cat_headers.add('alchemy_category')


float_headers = set()
float_headers.add('alchemy_category_score')
float_headers.add('avglinksize')
float_headers.add('commonlinkratio_1')
float_headers.add('commonlinkratio_2')
float_headers.add('commonlinkratio_3')
float_headers.add('commonlinkratio_4')

float_header_list = None
text_headers = set()
text_headers.add('boilerplate')

rating_header = 'label'

delete_headers = set()
delete_headers.add('label')

vectorizer = CountVectorizer()
transformer = TfidfTransformer()

categorizer = pipeline.Pipeline(
    [('vectorizer', vectorizer), ('transformer', transformer),]
)

rd = lm.LogisticRegression(penalty='l2', dual=True, tol=0.0001, 
                             C=1, fit_intercept=True, intercept_scaling=1.0, 
                             class_weight=None, random_state=None)

#my_svm =svm.SVC(kernel='linear', gamma=10, C=1,)
my_svm =svm.LinearSVC(penalty='l2', loss='l2', )



trainer  = [ 
    ['lr' , rd],
    ['svm' , my_svm] 
]
category_rows = []
numeric_rows = []
text_rows = []
rating_rows  = []

def load_file(file_name):

    global float_header_list


    print 'Openning CSV file'
    con = open(file_name, "r")
    data = csv.DictReader(con, delimiter=FILE_SEPERATOR)
    
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
            if row[header] == '':
                continue
            if header in cat_headers:
                cat_row[header] = row[header]
            elif header in float_headers:
                num_row.append(float(row[header]))
                if float_header_list is None:
                    local_float_header_list.append(header)
            elif header in text_headers:
                text_row[header] = row[header]
        category_rows.append(cat_row)
        if len(num_row) > 0: 
            numeric_rows.append(num_row)
        if len(text_row.keys()) > 0: 
            text_rows.append(text_row)
        rating_rows.append(int(row[rating_header]))
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
 
def load_train_features(pkl_filename):
    pkl_filename = "./data/" + pkl_filename
    print 'trying to load pickle data from: ' + pkl_filename
    pkl_file = open(pkl_filename, 'rb')
    data = pickle.load(pkl_file)
    pkl_file.close()
    print 'done loading.'
    return data

def save_train_features(data, pkl_filename):
    pkl_filename = "./data/" + pkl_filename
    print 'trying to save pickle data to: ' + pkl_filename
    pkl_file = open(pkl_filename, 'wb')
    pickle.dump(data, pkl_file, -1)
    print 'done saving.'
    pkl_file.close()
 
def extract_text_features(rows, feature_name):
    print 'Extracting text features: ' + str(feature_name)
    text_row = []
    for row in rows:
        text_row.append(row[feature_name])

    text_feat_array = categorizer.fit_transform(text_row, )
    print 'done ..'
    return text_feat_array, categorizer.steps[0][1].get_feature_names()

def save_methods_accuracy_score(mode, method, score):

    with open("./scores/" + "methods." + mode + ".score", "a") as myfile:
        myfile.write(method + ",%.2f" % (score) + "\n")

def save_best_accuracy_score(file_name, mode, method, score):

    with open("./scores/" + file_name  + ".score", "a") as myfile:
        myfile.write(mode + "," + method + ",%.2f" % (score) + "\n")
        
def run_pickle_data(input_train_file, input_test_file):

    print 'running pickle data'
    load_file(input_train_file)
    print 'done iterating %s file.', input_train_file
    len_train = len(rating_rows)
    load_file(input_test_file)
    print 'done iterating %s file.', input_test_file

#    X_1_norm_feat = norm_float_headers(numeric_rows)
    X_1_norm_feat = numeric_rows

    y_all = np.array(rating_rows)
    X_0_text_feat_bus_name, feature_name_bus_name = extract_text_features(text_rows, 'boilerplate')

    from scipy.sparse import hstack
    import pdb
    pdb.set_trace()
    if (len(X_1_norm_feat) > 0 and  X_0_text_feat_bus_name.shape[0] > 0):
        X_all = hstack((X_1_norm_feat, X_0_text_feat_bus_name))
    else:
        if len(X_1_norm_feat) > 0:
            X_all = X_1_norm_feat
        else:
            X_all = X_0_text_feat_bus_name

    dump_data = { 'x' : X_all,
                   'y' : y_all,
                   'train_len' : len_train 
                 
    }
    return dump_data

if __name__ == '__main__':

    exp_type = str(raw_input('Enter your experiment type:'))
    
    if len(sys.argv) == 3:
        input_train_file = sys.argv[1]
        input_test_file = sys.argv[2]
        output_train_libsvm_file  = sys.argv[1] + ".libfm"
        output_test_libsvm_file  = sys.argv[2] + ".libfm"
        
    else:
        input_train_file = "../data/train.feat"
        input_test_file = "../data/test.feat"
        output_train_libsvm_file  = "train."  + exp_type  + ".libfm"
        output_test_libsvm_file  = "test."  + exp_type  + ".libfm"
    
    try:
        dump_data = load_train_features(exp_type + '.data.pickle')
    except IOError:
        print 'error loading pickle data.'
        dump_data = run_pickle_data(input_train_file, input_test_file)
        save_train_features(dump_data, exp_type  + '.data.pickle')
        
    
    X_all = dump_data['x'].tocsr() 
    y_all = dump_data['y']
    len_train = dump_data['train_len']
    X_train = X_all[:len_train]
    y_train = y_all[:len_train]
        
    print "running cross validation on all methods:"
    best_method = None
    best_score = None
    best_method_name  =None
    for name, method in trainer:
        print '\nrunning method:' + name
        score = np.mean(cross_validation.cross_val_score(method, X_train, y_train, cv=10))
        print 'CV score for: ' + name + ' ' + str(score)
        save_methods_accuracy_score( exp_type, name , score)
        if best_score is None or score > best_score:
            best_score = score
            best_method = method
            best_method_name = name 
            print 'best method:' + name
    
    save_best_accuracy_score("best_cv_score", exp_type, best_method_name, best_score)        
    best_method.fit(X_train,y_train)

    X_test = X_all[len_train:]
    pred = best_method.predict_proba(X_test)[:,1]

    print 'Dumping train in SVMLight.'
    dump_svmlight_file(X_train, y_train, output_train_libsvm_file )

    print 'Dumping test in SVMLight.'
    dump_svmlight_file(X_test, pred, output_test_libsvm_file )
 
    testfile = p.read_csv('../data/test.tsv', sep="\t", na_values=['?'], index_col=1)
    pred_df = p.DataFrame(pred, index=testfile.index, columns=['label'])
    pred_df.to_csv(exp_type + 'benchmark.csv')
    print "submission file created.."
