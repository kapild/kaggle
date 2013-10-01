import json
import csv
import numpy as np
import pandas as pd
from common.preprocess import  preprocess_pipeline

# helper class for Panda related objects
class PageManager:

	def __init__(self, page_file):

		self.page_file = page_file
		self.panda_data = self.load_page_data(self.page_file)

	def load_page_data(self, page_file):

		data = pd.read_csv(
			page_file, 
			sep='\t',
			index_col=None,
			na_values=['?'],
			dtype={	
				'url' : np.str_, 
				'urlid' : np.str_,
				'non_markup_alphanum_characters' : 'int8',
				'numberOfLinks' : 'int8',
				'boilerplate' : np.str_, 
				'alchemy_category' : np.str_, 
				'framebased' : np.str_, 
				'hasDomainLink' : np.str_, 
				'is_news' : np.str_, 
				'lengthyLinkDomain' : np.str_, 
				'news_front_page' : np.str_, 
				'label' : np.float64, 
				'alchemy_category_score' : np.float64, 
				'avglinksize' : np.float64, 
				'commonlinkratio_1' : np.float64, 
				'commonlinkratio_2' : np.float64, 
				'commonlinkratio_3' : np.float64, 
				'commonlinkratio_4' : np.float64, 
				'compression_ratio' : np.float64, 
				'embed_ratio' : np.float64, 
				'frameTagRatio' : np.float64, 
				'html_ratio' : np.float64, 
				'linkwordscore' : np.float64, 
				'numwords_in_url' : np.float64, 
				'parametrizedLinkRatio' : np.float64, 
				'spelling_errors_ratio' : np.float64, 
				'image_ratio' : np.float64,
			},
#			index_col='urlid',
		)
#		data = PageManager.convert(data, 'boilerplate')
		return data

 	def get_item(self, id):
 	 raise NotImplementedError
 	
 	def get_all_item_keys(self):
 	 raise NotImplementedError 	
 	
 	def is_exists(self, id):
 	 raise NotImplementedError

	@staticmethod
	def pre_process_text( text):
		return preprocess_pipeline(text, "english", "PorterStemmer", True, False, False)
#		return preprocess_pipeline(observation, "english", "WordNetLemmatizer", True, False, False)
	@staticmethod
	def convert(X, key):

		if  key not in X:
			return
		
		x_old = X[key]		

		rows = []		
		for index in x_old.index:
			item = x_old[index]
			new_dict = json.loads(item)
			if isinstance(new_dict, dict):
				item_dict  = dict()
				for subkey, subvalue in new_dict.items():
					process_val = subvalue
					if subvalue is not None:
						process_val = PageManager.pre_process_text(subvalue)
					item_dict['%s_%s' % (key, subkey)] = process_val
				rows.append(item_dict)
		new_data = pd.DataFrame(rows)
		del X[key]
		X = pd.concat([X, new_data], axis=1)
		return X
