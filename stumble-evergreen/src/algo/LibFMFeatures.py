from base_model import BaseModel
import string
from string import lower

from common.utils import FILE_SEPERATOR
class LibFMFeatures(BaseModel):

	def __init__(self, page, page_test):
		super(LibFMFeatures, self).__init__(page, page_test)
		self.feat_head = self.get_feature_list()


	def get_feature_list(self):

		feat_head = [
			['label', self.get_label, True],
			['urlid', self.get_url_id, True],
			['alchemy_category', self.get_alchemy_category, True],
			['alchemy_category_score', self.get_alchemy_category_score, True],
			['avglinksize', self.get_avglinksize, True],
			['commonlinkratio_1', self.get_commonlinkratio_1, True],
			['commonlinkratio_2', self.get_commonlinkratio_2, True],
			['commonlinkratio_3', self.get_commonlinkratio_3, True],
			['commonlinkratio_4', self.get_commonlinkratio_4, True],
			['news_front_page', self.get_news_front_page, True], 
			['frameBased', self.get_frameBased, True],
			['is_news', self.get_is_news, True],
			['hasDomainLink', self.get_hasDomainLink, True],
			['lengthyLinkDomain', self.get_lengthyLinkDomain, True],
			
			['boilerplate', self.get_boilerplate, True],

		]
		return feat_head


	def get_output_line(self, page_item):

		out_line = ''

		for index, item in enumerate(self.feat_head):
			field = item[0]
			func_name = item[1]
			is_enable = item[2]

			if is_enable:
				out_line += str(self.get_func_val(func_name, self.page, self.page_test, page_item, field))
				if (index < len(self.feat_head) - 1):
					out_line += FILE_SEPERATOR

		out_line += "\n"
		return out_line


	def get_field_value(self, page, page_test, page_item, field):

		if page.is_exists(page_item.urlid) and page_item.field is not None:
			return BaseModel.precison(page_item.field)

		if page_test.is_exists(page_item.urlid) and page_item.field is not None:
			return BaseModel.precison(page_item.field)

		return BaseModel.precison(page.get_avg_value(field))
		
		
	def get_func_val(self, func_name, page, page_test, page_item, field):
		
		if func_name is not None:
			return func_name(self.page, self.page_test, page_item)
		else:
			return self.get_field_value(self.page, self.page_test, page_item, field)
	
	
	def get_header_text(self, output_header):

		output_header_text = ''
		for index, item in enumerate(output_header):
		    head_text = item[0]
		    func_name = item[1]
		    is_enabled = item[2]
		    if is_enabled:
		        output_header_text += head_text
		        if (index < len(output_header) - 1):
		            output_header_text += FILE_SEPERATOR
		return output_header_text


	def precison(self, val):
		return "%.2f" % (val)

