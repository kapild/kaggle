import pandas as pd
import numpy as np

class StumbleData:
	
	PROCESS_ATTRIBUTES_MEANS = set ([
		'alchemy_category_score',
		'avglinksize',
		'commonlinkratio_1',
		'commonlinkratio_2',
		'commonlinkratio_3',
		'commonlinkratio_4',
	])

	PROCESS_CAT_ATTRIBUTE_FILL_NAME = set ([
		'alchemy_category_score',
		'avglinksize',
		'commonlinkratio_1',
		'commonlinkratio_2',
		'commonlinkratio_3',
		'commonlinkratio_4',
	])

	PROCESS_ATTRIBUTES_GROUP = [
		['alchemy_category','avglinksize']
	]


#	X['name_u'] = X['name_u'].fillna("Unknown")

	def __init__(self, pd_train, pd_test):
		self.pd_train = pd_train
		self.pd_test = pd_test
		
		self.combine(self.pd_train, self.pd_test)
		self.process_attributes_cat()
		self.process_attributes()
		self.process_attributes_group()

	def combine(self, pd_train, pd_test):

		self.len_train = pd_train.shape[0]
		self.all_pd = pd.concat([pd_train, pd_test], ignore_index = True)		

	def process_attributes(self):
		
		for attrb in StumbleData.PROCESS_ATTRIBUTES_MEANS:
			self.all_pd[attrb].fillna(self.all_pd[attrb].mean(), inplace=True)

	def process_attributes_group(self):

		for grp_by, mean_by in StumbleData.PROCESS_ATTRIBUTES_GROUP:
			new_key = grp_by + '_grpby_' + mean_by
			self.all_pd[new_key] = self.all_pd[grp_by].map(self.all_pd.groupby(grp_by)[mean_by].mean())
			self.all_pd[new_key].fillna(self.
								all_pd[new_key].mean(), inplace=True)

	def process_attributes_cat(self):

		for attrs in self.all_pd.keys():
			att_dtype = self.all_pd[attrs].dtype 
			if not att_dtype == np.int64 and not att_dtype == np.int8 and not att_dtype == np.float64:
				self.all_pd[attrs].fillna('Un', inplace=True)
		
	def get_features(self):
		return set(self.all_pd.keys())

