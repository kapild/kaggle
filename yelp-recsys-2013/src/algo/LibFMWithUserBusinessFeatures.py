from base_model import BaseModel
import string
from string import lower
class LibFMWithUserBusinessFeatures(BaseModel):

	def __init__(self, bus, user, test_bus, test_user):
		super(LibFMWithUserBusinessFeatures, self).__init__(bus, user, test_bus, test_user)
		self.feat_head = self.get_feature_list()


	def get_feature_list(self):

		feat_head = [
			['rating', self.get_rating, True],
			['user_id', self.get_user_id, True],
			['business_id', self.get_business_id, True],
			['bus_avg_stars', self.get_business_avg_stars, True],
			['user_avg_starts', self.get_user_avg_stars, True],
			['user_avg_review', self.get_user_avg_review, True],
			['bus_avg_review', self.get_business_review_count, True],
			['business_cat1,business_cat2', self.get_category_feat_line, True],
			['bus_is_open', self.get_business_is_open, True],
			['bus_name' , self.get_bus_name, True],
			['city_text', self.get_bus_city_text, True],
		]
		return feat_head

	def get_output_line(self, review_item):

		out_line = ''

		for index, item in enumerate(self.feat_head):
			text = item[0]
			func_name = item[1]
			is_enable = item[2]

			if is_enable:
				out_line += str(func_name(self.bus, self.user, review_item, self.test_bus, self.test_user))
				if (index < len(self.feat_head) - 1):
					out_line += ","

		out_line += "\n"
		return out_line

	def get_header_text(self, output_header):

		output_header_text = ''
		for index, item in enumerate(output_header):
		    head_text = item[0]
		    func_name = item[1]
		    is_enabled = item[2]
		    if is_enabled:
		        output_header_text += head_text
		        if (index < len(output_header) - 1):
		            output_header_text += ','
		return output_header_text

	def get_category_feat_line(self, bus, user, review_item, bus_test, user_test):

		bus_first_cat = self.get_category_feat(bus_test, user_test, review_item)

		out_line = ''
		if len(bus_first_cat) == 1:
			out_line += str(bus_first_cat[0])
			out_line += ","
		else:
			out_line += str(bus_first_cat[0])
			out_line += "," + str(bus_first_cat[1])

		return str(out_line)

	def precison(self, val):
		return "%.2f" % (val)

