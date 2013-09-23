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
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import MultinomialNB

from common.utils import FILE_SEPERATOR 
cat_headers = set()
cat_headers.add('urlid')
cat_headers.add('alchemy_category')
cat_headers.add('news_front_page')
cat_headers.add('frameBased')
cat_headers.add('alchemy_category')
cat_headers.add('is_news')
cat_headers.add('hasDomainLink')
cat_headers.add('lengthyLinkDomain')


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
transformer = TfidfVectorizer(min_df=3,  max_features=None, strip_accents='unicode',  
      analyzer='word',token_pattern=r'\w{1,}',ngram_range=(1, 2), use_idf=1,smooth_idf=1,sublinear_tf=1, norm='l2')

categorizer = pipeline.Pipeline(
    [ ('transformer', transformer),]
)


rd = lm.LogisticRegression(penalty='l2', dual=True, tol=0.0001, 
                             C=1, fit_intercept=True, intercept_scaling=1.0, 
                             class_weight=None, random_state=None)

#my_svm =svm.SVC(kernel='linear', gamma=10, C=1,)
my_svm =svm.LinearSVC(penalty='l2', loss='l2', )


#rf = RandomForestRegressor(n_estimators=1000,verbose=2,n_jobs=20,min_samples_split=5,random_state=1034324)

naive = MultinomialNB(alpha=0.5)
trainer  = [ 
    ['lr' , rd],
    ['svm' , my_svm],
    ['naive', naive], 
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
 
def extract_text_features(rows, feature_name, headers):
    print 'Extracting text features: ' + str(feature_name)
    text_row = []
    
    for row in rows:
        if headers:
            for key in headers:
                dict_row = json.loads(row[feature_name])
                if( key in dict_row and dict_row[key] is not None):
                    text_row.append(dict_row[key])
        else:
            text_row.append(row[feature_name])

    text_feat_array = categorizer.fit_transform(text_row, )
    print 'done ..'
    return text_feat_array, categorizer.steps[0][1].get_feature_names()

def save_methods_accuracy_score(mode, method, score):

    with open("./scores/" + "methods." + mode + ".score", "a") as myfile:
        myfile.write(method + ",%.4f" % (score) + "\n")

def save_best_accuracy_score(file_name, mode, method, score):

    with open("./scores/" + file_name  + ".score", "a") as myfile:
        myfile.write(mode + "," + method + ",%.4f" % (score) + "\n")
        
def get_text_feature(text_rows, text_field):       
    feature_list = None
    feature_name_list = None
    if (len(text_rows) > 0):
        feature_list, feature_name_list = extract_text_features(text_rows, text_field, ['body', 'title'])

    return feature_list, feature_name_list

def run_pickle_data(input_train_file, input_test_file):

    print 'running pickle data'
    load_file(input_train_file)
    print 'done iterating %s file.', input_train_file
    len_train = len(rating_rows)
    load_file(input_test_file)
    print 'done iterating %s file.', input_test_file

    X_1_norm_feat = []
    if len(numeric_rows) > 0:
        X_1_norm_feat = norm_float_headers(numeric_rows)
#    X_1_norm_feat = numeric_rows

    import pdb
    pdb.set_trace()
    # category
    X_2_cat_feat = None
    if(len(category_rows) > 0 ):
        vec = DictVectorizer()
        print 'Transforming to dict.'
        X_2_cat_feat = vec.fit_transform(category_rows)

    y_all = np.array(rating_rows)

    import pdb
    pdb.set_trace()    
    text_feats, text_feat_vocab = get_text_feature(text_rows, 'boilerplate')

    import pdb
    pdb.set_trace()    
    
    from scipy.sparse import hstack
    if (len(X_1_norm_feat) > 0 and len(text_rows) > 0 and len(category_rows) > 0):
        X_all = hstack((X_1_norm_feat, text_feats)) 
        X_all = hstack((X_all, X_2_cat_feat)).tocsr() 

    else:
        if len(X_1_norm_feat) > 0 and len(text_rows) > 0:
            X_all = hstack((X_1_norm_feat, text_feats)).tocsr() 
        elif len(X_1_norm_feat) > 0 and len(category_rows) > 0:
            X_all = hstack((X_1_norm_feat, X_2_cat_feat)).tocsr() 
        elif len(text_rows) > 0 and len(category_rows) > 0:
            X_all = hstack((text_feats, X_2_cat_feat)).tocsr() 
        elif len(text_rows) > 0:
            X_all = text_feats 
        elif len(category_rows) > 0:
            X_all = X_2_cat_feat 
        elif len(X_1_norm_feat) > 0:
            X_all = X_1_norm_feat 
            

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

    print 'input file train:' + input_train_file 
    print 'input file test:' + input_test_file 

    raw_input('Press enter:')
    
    X_all = dump_data['x']
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
    
    import pdb
    pdb.set_trace()
    save_best_accuracy_score("best_cv_score", exp_type, best_method_name, best_score)        
    best_method.fit(X_train,y_train)

    X_test = X_all[len_train:]
    pred = best_method.predict_proba(X_test)

    print 'Dumping train in SVMLight.'
#    dump_svmlight_file(X_train, y_train, output_train_libsvm_file )

    print 'Dumping test in SVMLight.'
#    dump_svmlight_file(X_test, pred, output_test_libsvm_file )
 
    testfile = p.read_csv('../data/test.tsv', sep="\t", na_values=['?'], index_col=1)
    pred_df = p.DataFrame(pred, index=testfile.index, columns=['label'])
    pred_df.to_csv("results/" + exp_type + 'benchmark.csv')
    print "submission file created.."
