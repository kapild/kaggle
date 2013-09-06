import string
from string import lower
class BaseModel(object):

	def __init__(self, bus, user, test_bus, test_user):
		self.bus = bus
		self.user = user
		self.test_bus= test_bus
		self.test_user = test_user

	def get_output_line(self, review_item):
		raise NotImplementedError

	@staticmethod
	def get_business_avg_stars(bus, user, review_item, bus_test, user_test):

		business_id = review_item.business_id
		# is in test data, which is train for train
		if bus_test.is_exists(business_id):
			bus_avg_stars = bus_test.get_item_rating(business_id)
			if bus_avg_stars == 0:
				bus_avg_stars = BaseModel._get_business_train_avg_stars(bus, business_id)
		else:
			bus_avg_stars = BaseModel._get_business_train_avg_stars(bus, business_id)

		return BaseModel.precison(bus_avg_stars)

	@staticmethod
	def _get_business_train_avg_stars(bus, business_id):
		if bus.is_exists(business_id):
			bus_avg_stars = bus.get_item_rating(business_id)
		else:
			bus_avg_stars = bus.get_avg_bus_stars()
		return bus_avg_stars

	@staticmethod
	def get_user_avg_stars(bus, user, review_item, bus_test, user_test):

		user_id = review_item.user_id
		# is in test data, which is train for train
		if user_test.is_exists(user_id):
			user_avg_stars = user_test.get_user_stars(user_id)
			if user_avg_stars == 0:
				user_avg_stars = BaseModel._get_user_train_avg_stars(user, user_id)
		else:
			user_avg_stars = BaseModel._get_user_train_avg_stars(user, user_id)
		return  BaseModel.precison(user_avg_stars)

	@staticmethod
	def _get_user_train_avg_stars(user, user_id):
		if user.is_exists(user_id):
			user_avg_stars = user.get_user_stars(user_id)
		else:
			user_avg_stars = user.get_avg_user_stars()
		return user_avg_stars

	@staticmethod
	def get_user_avg_review(bus, user, review_item, bus_test, user_test):

		user_id = review_item.user_id
		# is in test data, which is train for train
		if user_test.is_exists(user_id):
			user_avg_stars = user_test.get_user_review_count(user_id)
			if user_avg_stars == 0:
				user_avg_stars = BaseModel._get_user_train_avg_review(user, user_id)
		else:
			user_avg_stars = BaseModel._get_user_train_avg_review(user, user_id)
		return BaseModel.precison(user_avg_stars)

	@staticmethod
	def _get_user_train_avg_review(user, user_id):

		if user.is_exists(user_id):
			user_avg_stars = user.get_user_review_count(user_id)
		else:
			user_avg_stars = user.get_avg_user_review_count()
		return user_avg_stars

	@staticmethod
	def get_business_review_count(bus, user, review_item, bus_test, user_test):

		business_id = review_item.business_id
		# is in test data, which is train for train
		if bus_test.is_exists(business_id):
			bus_avg_stars = bus_test.get_item_review_count(business_id)
			if bus_avg_stars == 0:
				bus_avg_stars = BaseModel._get_business_train_avg_review_count(bus, business_id)
		else:
			bus_avg_stars = BaseModel._get_business_train_avg_review_count(bus, business_id)

		return BaseModel.precison(bus_avg_stars)

	@staticmethod
	def _get_business_train_avg_review_count(bus, business_id):
		if bus.is_exists(business_id):
			bus_avg_stars = bus.get_item_review_count(business_id)
		else:
			bus_avg_stars = bus.get_avg_bus_review_count()
		return bus_avg_stars


	@staticmethod
	def k_fold_cross_validation(X, K, randomise = False):
		"""
		Generates K (training, validation) pairs from the items in X.
	
		Each pair is a partition of X, where validation is an iterable
		of length len(X)/K. So each training iterable is of length (K-1)*len(X)/K.
	
		If randomise is true, a copy of X is shuffled before partitioning,
		otherwise its order is preserved in training and validation.
		"""
		if randomise: from random import shuffle; X=list(X); shuffle(X)
		for k in xrange(K):
			training = [x for i, x in enumerate(X) if i % K != k]
			validation = [x for i, x in enumerate(X) if i % K == k]
			yield training, validation


	@staticmethod
	def get_business_is_open(bus, user, review_item, bus_test, user_test):

		business_id = review_item.business_id
		# is in test data, which is train for train
		if bus_test.is_exists(business_id):
			bus_is_open = bus_test.get_item_is_open(business_id)
			if bus_is_open == True:
				return 1
			else:
				return 0
		else:
			return BaseModel._get_business_is_open_train(bus, business_id)

	@staticmethod
	def _get_business_is_open_train(bus, business_id):
		
		if bus.is_exists(business_id):
			bus_is_open = bus.get_item_is_open(business_id)
			if bus_is_open == True:
				return 1
			else:
				return 0
		else:
			return 1

	@staticmethod
	def get_category_feat(bus, user, review_item):

		default_cat = bus.get_max_cat_id()
	
		r_bus_id = review_item.business_id
		try:
		    bus_cat = bus.get_item(r_bus_id).categories
		    if len(bus_cat) > 0:
		    	list_cat  = []
		    	for cat in bus_cat:
	    			list_cat.append(bus.get_cat_id(cat))
	    		return list_cat
		except KeyError:
		    return [default_cat]
	
		return [default_cat]

	def get_bus_city_text(self, bus, user, review_item, bus_test, user_test):

		r_bus_id = review_item.business_id
		try:
		    return bus_test.get_bus_city_text(r_bus_id).encode("utf-8")
		except KeyError:
		    return bus.get_bus_city_text(r_bus_id).encode("utf-8")
	
	@staticmethod
	def string_format( bus_name):
		bus_name = string.replace(bus_name, "\'", "", 2)
		bus_name = string.replace(bus_name, ",", " ", 2)
		return (bus_name.encode("utf-8"))

	@staticmethod
	def get_bus_name(bus, user, review_item, bus_test, user_test):

		business_id = review_item.business_id
		# is in test data, which is train for train
		if bus_test.is_exists(business_id):
			bus_name = bus_test.get_item_name(business_id)
		else:
			bus_name = BaseModel._get_bus_avg_name(bus, business_id)

		return BaseModel.string_format(lower(bus_name))

	@staticmethod
	def _get_bus_avg_name(bus, business_id):
		if bus.is_exists(business_id):
			return bus.get_item_name(business_id)
		else:
			return ''

	def get_rating(self, bus, user, item, bus_test, user_test):

		rating = 3.5
		if item.stars:
			rating = item.stars
		
		return str(rating)

	def get_user_id(self, bus, user, item, bus_test, user_test):
		return str(item.user_id)

	def get_business_id(self, bus, user, item, bus_test, user_test):
		return str(item.business_id)

	@staticmethod
	def precison(val):
		return "%.2f" % (val)
