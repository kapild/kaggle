from base_model import BaseModel

class NMFwithLibFM(BaseModel):

	def __init__(self, bus, user, test_bus, test_user):
		super(NMFwithLibFM, self).__init__(bus, user, test_bus, test_user)

	def get_output_line(self, item):

		user_id = item.user_id
		business_id = item.business_id

		out_line = ''
		rating = 3.5
		if item.stars:
			rating = item.stars
		out_line += str(rating) + "::" + str(user_id) + "::" + str(business_id)
		out_line += "\n"
		return out_line
