from base_model import BaseModel

class AverageModel(BaseModel):

	def __init__(self, bus, user, test_bus, test_user):
		super(AverageModel, self).__init__(bus, user, test_bus, test_user)

	def get_output_line(self, review_item):
		
		bus_rating = BaseModel.get_business_avg_stars(
			self.bus, 
			self.user, 
			review_item,
			self.test_bus, 
			self.test_user
		)

		user_rating = BaseModel.get_user_avg_stars(
			self.bus, 
			self.user, 
			review_item,
			self.test_bus, 
			self.test_user
		)


		prediction = float(bus_rating + user_rating)/2
		return prediction