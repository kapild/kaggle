from base_model import BaseModel
import string
from string import lower
class LibFMWithUserBusinessFeatures(BaseModel):

	def __init__(self, bus, user, test_bus, test_user):
		super(LibFMWithUserBusinessFeatures, self).__init__(bus, user, test_bus, test_user)

	def get_output_line(self, item):

		user_id = item.user_id
		business_id = item.business_id

		out_line = ''
		rating = 3.5
		if item.stars:
			rating = item.stars
			
		bus_avg_stars = self.get_business_avg_stars(self.bus, self.user, item, self.test_bus, self.test_user)
		user_avg_starts = self.get_user_avg_stars(self.bus, self.user, item, self.test_bus, self.test_user)
		user_avg_review = self.get_user_avg_review(self.bus, self.user, item, self.test_bus, self.test_user)
		bus_avg_review= self.get_business_review_count(self.bus, self.user, item, self.test_bus, self.test_user)
		bus_first_cat = self.get_category_feat(self.bus, self.user, item)
		bus_is_open = self.get_business_is_open(self.bus, self.user, item, self.test_bus, self.test_user)
		bus_name = lower(self.get_bus_name(self.bus, self.user, item, self.test_bus, self.test_user))
		
		out_line += str(rating) + "," + str(user_id) + "," + str(business_id) 
		if len(bus_first_cat) == 1:
			out_line +=  "," + str(bus_first_cat[0])
			out_line +=  "," + str(bus_first_cat[0])
		else:
			out_line +=  "," + str(bus_first_cat[0])
			out_line +=  "," + str(bus_first_cat[1])

		out_line +=  "," + self.precison(bus_avg_stars) 
		out_line += "," + self.precison(user_avg_starts)
		out_line += "," + self.precison(user_avg_review)
		out_line += "," + self.precison(bus_avg_review)
		out_line += "," + str(bus_is_open)
		out_line+="," + str(self.string_format(bus_name))
		
		out_line += "\n"
		return out_line


	def string_format(self, bus_name):
		bus_name = string.replace(bus_name, "\'", "", 2)
		bus_name = string.replace(bus_name, ",", " ", 2)
#		bus_name = string.replace(bus_name, "&", " ", 2)
#		bus_name = string.replace(bus_name, ".", " ", 2)
#		bus_name = string.replace(bus_name, "&", " ", 2)
#		bus_name = string.replace(bus_name, "+", " ", 2)

		return (bus_name.encode("utf-8"))
		
	def precison(self, val):
		return "%.2f" % (val)
