import json
import csv
from models.page import Page

class PageManager:

	def __init__(self, page_file):

		self.page_file = page_file
		self.page_item_hash = {}
		self.field_value_sum = {}
		self.page_item_list = []
		self.cat_score_sum = 0.0
		self.avglinksize_sum = 0.0
		self.commonlinkratio_1_sum  = 0.0
		self.commonlinkratio_2_sum  = 0.0
		self.commonlinkratio_3_sum  = 0.0
		self.commonlinkratio_4_sum  = 0.0
		self.count = 0
		self.load_page_data(self.page_file)


	def load_page_data(self, page_file):

		page_item_hash = {}
		page_item_list = []
		con = open(page_file, "r")
		data = csv.DictReader(con, delimiter="\t")


 		count = 0
 		for row in data:
 			page_item = Page(row)
 			page_item_hash[page_item.urlid] = page_item
 			page_item_list.append(page_item.urlid)
 			if page_item.alchemy_category_score:
 				self.cat_score_sum+=page_item.alchemy_category_score
 			if page_item.avglinksize:
 				self.avglinksize_sum+=page_item.avglinksize
 			if page_item.commonLinkRatio_1:
 				self.commonlinkratio_1_sum+=page_item.commonLinkRatio_1
 			if page_item.commonLinkRatio_2:
 				self.commonlinkratio_2_sum+=page_item.commonLinkRatio_2
 			if page_item.commonLinkRatio_3:
 				self.commonlinkratio_3_sum+=page_item.commonLinkRatio_3
 			if page_item.commonLinkRatio_4:
 				self.commonlinkratio_4_sum+=page_item.commonLinkRatio_4
 			
# 			for key in row.keys():
#	 			if page_item.compression_ratio:
#	 				self.add_val_to_hash(self.field_value_sum, compression_ratio, page_item.compression_ratio)
 				
 			count+=1

 		self.page_item_list = page_item_list
 		self.page_item_hash = page_item_hash
 		self.count = count

 	def add_val_to_hash(self, hash_key, field, new_val):
 		val = 0
 		if field in hash_key:
 			val = hash_key.field
 	 	hash_key.field = val + new_val
 	 	
 	def get_avg_alchemy_category_score(self):
 		return float(self.cat_score_sum)/self.count

 	def get_avg_avglinksize(self):
 		return float(self.avglinksize_sum)/self.count

 	def get_avg_commonlinkratio_1(self):
 		return float(self.commonlinkratio_1_sum)/self.count

 	def get_avg_commonlinkratio_2(self):
 		return float(self.commonlinkratio_2_sum)/self.count

 	def get_avg_commonlinkratio_3(self):
 		return float(self.commonlinkratio_3_sum)/self.count

 	def get_avg_commonlinkratio_4(self):
 		return float(self.commonlinkratio_4_sum)/self.count
 	
 	def get_page_id_list(self):
 		return self.page_item_list
 	
# 	def get_avg_value(self, field):
# 		return self.

 	def get_item(self, id):
 		return self.page_item_hash[id] 		 		

 	def get_all_item_keys(self):
 		return self.page_item_hash.keys()

 	def is_exists(self, id):
 		return id in self.page_item_hash
