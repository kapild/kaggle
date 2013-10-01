import string
from string import lower

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing
from sklearn_pandas import DataFrameMapper
from sklearn.datasets.svmlight_format import dump_svmlight_file
from algo.base_mode import BaseModel
from sklearn_pandas import DataFrameMapper
from common.utils import FILE_SEPERATOR
from sklearn import pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


output_train_libsvm_file  = "../data/train.libfm"

def get_text_transformer():

   return TfidfVectorizer(min_df=3, max_features=None,
                                      strip_accents='unicode',
                                      analyzer='word', token_pattern=r'\w{1,}',
                                      ngram_range=(1, 2), use_idf=1, smooth_idf=1,
                                      sublinear_tf=1, norm='l2')

#def get_dict_pipeline():
#    return pipeline.Pipeline(
#        [('vectorizer', CountVectorizer()), ('transformer', TfidfTransformer()), ])

def get_dict_pipeline():
   return DictVectorizer()

def get_norm_scaler():
   return preprocessing.StandardScaler()     

class LibFMFeatures(BaseModel):
   def __init__(self, stumble_data):
       super(LibFMFeatures, self).__init__(stumble_data)
       self.feat_head = self.get_feature_list()
       

   def get_tranform_features(self):
       return self.transform_features()
   
   def get_feature_list(self):

#        ['field_name', 'ignored_function_name', 'pipeline_fit', 'is_dict', 'is_enabled']
       feat_head = [
           #			['label', 'get_label', None, True],
#             ['alchemy_category', None, get_dict_pipeline(), True],
#             ['urlid', None, get_dict_pipeline(), True],
#            ['alchemy_category_score', None,get_norm_scaler(), True],
#            ['avglinksize', None, get_norm_scaler(), True],
#            ['commonlinkratio_1', None, get_norm_scaler(), True],
#            ['commonlinkratio_2', None, get_norm_scaler(), True],
#            ['commonlinkratio_3', None, get_norm_scaler(),  True],
#            ['commonlinkratio_4', None, get_norm_scaler(), True],
#            ['news_front_page', None, get_dict_pipeline(), True],
#             ['framebased', None, get_dict_pipeline(),True], #
#             ['is_news', None, get_dict_pipeline(),True],
#            ['hasDomainLink', None, get_dict_pipeline(),True],
#            ['lengthyLinkDomain', None, get_dict_pipeline(), True],
#            ['non_markup_alphanum_characters', None, get_norm_scaler(), True],
#            ['numberOfLinks', None, get_norm_scaler(), True],
#            ['embed_ratio', None, get_norm_scaler(), True],
#            ['frameTagRatio', None, get_norm_scaler(), True],
#            ['html_ratio', None, get_norm_scaler(), True],
#            ['linkwordscore', None, get_norm_scaler(), True],
#            ['numwords_in_url', None, get_norm_scaler(), True],
#            ['parametrizedLinkRatio', None, get_norm_scaler(), True],
#            ['spelling_errors_ratio', None, get_norm_scaler(),  True],
#            ['compression_ratio', None, get_norm_scaler(),  True],
#            ['image_ratio', None, get_norm_scaler(),  True],
            ['boilerplate', None, get_text_transformer(), True],
#            ['boilerplate_body', None, get_text_transformer(), True],
#            ['boilerplate_title', None, get_text_transformer(), True],
#            ['boilerplate_url', None, get_text_transformer(), True],
#            ['boilerplate_body_len', self.get_boilerplate_body_len, get_norm_scaler(), True],
#            ['boilerplate_url_len', self.get_boilerplate_url_len, get_norm_scaler(), True],
#            ['boilerplate_title_len', self.get_boilerplate_title_len, get_norm_scaler(), True],
#            ['boilerplate_title_num_word', self.get_boilerplate_title_num_word, get_norm_scaler(), True],
#            ['boilerplate_body_num_word', self.get_boilerplate_body_num_word, get_norm_scaler(), True],
#            ['boilerplate_url_num_word', self.get_boilerplate_url_num_word, get_norm_scaler(), True],
       ]
       return feat_head


   def transform_features(self):
       totransform = []
       for index, item in enumerate(self.feat_head):
           field = item[0]
           func_name = item[1]
           transform = item[2]
           is_enable = item[3]

           if is_enable:
               if not field in self.stumble_data.get_features():
                   print 'field not in feature..generating:' +  field
                   func_name(field)
               totransform.append((field, transform))

       if len(totransform):
           mapper = DataFrameMapper(totransform)
           mapper.fit(self.stumble_data.all_pd[:self.stumble_data.len_train])
           #
           X_transformed_train = mapper.transform(
               self.stumble_data.all_pd[:self.stumble_data.len_train])
           X_transformed_test = mapper.transform(
               self.stumble_data.all_pd[self.stumble_data.len_train:])

           for index, item in enumerate(self.feat_head):
               field = item[0]
               is_enable = item[3]
               if is_enable and field in self.stumble_data.get_features():
                   del self.stumble_data.all_pd[field]

           import pdb
           pdb.set_trace()

           from scipy.sparse import hstack

           X_train = X_transformed_train
           X_test = X_transformed_test
           y_train = self.stumble_data.all_pd[:self.stumble_data.len_train]['label']
#            print 'Dumping train in SVMLight.'
           dump_svmlight_file(X_train, y_train, output_train_libsvm_file )

#            print 'Dumping test in SVMLight.'
#            dump_svmlight_file(X_test, pred, output_test_libsvm_file )

       else:
           X_train = X_train.as_matrix()
           X_test = X_test.as_matrix()


       return X_train, y_train, X_test

   def get_boilerplate_url_len(self, key):
       
       apply_key =  'boilerplate_url'
       X= self.stumble_data.all_pd
       X[key] = X[apply_key].fillna("").apply(
           lambda x: len(x) if len(x) else None)
       X[key] = X[key].fillna(X[key].mean())

   def get_boilerplate_title_len(self, key):

       apply_key =  'boilerplate_title'
       X= self.stumble_data.all_pd
       X[key] = X[apply_key].fillna("").apply(
           lambda x: len(x) if len(x) else None)
       X[key] = X[key].fillna(X[key].mean())

   def get_boilerplate_body_len(self, key):
       
       apply_key =  'boilerplate_body'
       X= self.stumble_data.all_pd
       X[key] = X[apply_key].fillna("").apply(
           lambda x: len(x) if len(x) else None)
       X[key] = X[key].fillna(X[key].mean())

   def get_boilerplate_body_num_word(self, key):

       apply_key =  'boilerplate_body'
       X= self.stumble_data.all_pd
       X[key] = X[apply_key].map(lambda x: len(x.split()) if not isinstance(x, float) else False)


   def get_boilerplate_title_num_word(self, key):

       apply_key =  'boilerplate_title'
       X= self.stumble_data.all_pd
       X[key] = X[apply_key].map(lambda x: len(x.split()) if not isinstance(x, float) else False)

   def get_boilerplate_url_num_word(self, key):

       apply_key =  'boilerplate_url'
       X= self.stumble_data.all_pd
       X[key] = X[apply_key].map(lambda x: len(x.split()) if not isinstance(x, float) else False)

   def get_func_val(self, func_name, page, page_test, page_item, field):

       if func_name is not None:
           return func_name(self.page, self.page_test, page_item)
       else:
           return self.get_field_value(self.page, self.page_test, page_item,
                                       field)
   def precison(self, val):
       return "%.2f" % (val)

