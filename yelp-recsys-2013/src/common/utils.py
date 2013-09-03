
DEBUG_INT = 0
INFO_INT = 1

DEGUG_LEVEL = 1


def print_debug(text, debug=2, same_line=False):

	if debug >= DEGUG_LEVEL:
		if (same_line == True):
			print text,
		else:
			print text

def output_line(bus, user, item, bus_test, user_test):
	
	user_id = item.user_id
	business_id = item.business_id
	
	out_line = ''
	rating = 3.5
	if item.stars:
		rating = item.stars
	out_line += str(rating) +"," + str(user_id) + "," + str(business_id)
	out_line += "," + str(more_features(bus, user, item, bus_test, user_test))  
	out_line+="\n"
	return out_line

def more_features(bus, user, review_item, bus_test, user_test):


	#cat_feat = get_category_feat(bus, user, review_item)
	bus_stars_feat = get_business_avg_stars(bus, user, review_item, bus_test, user_test)
	bus_review_count = get_business_review_count(bus, user, review_item, bus_test, user_test)
	user_stars_feat = get_user_avg_stars(bus, user, review_item, bus_test, user_test)
	user_rating_feat = get_user_avg_review(bus, user, review_item, bus_test, user_test)

	
	out_feat = ''
	out_feat+=bus_stars_feat
	out_feat+="," + bus_review_count 
	out_feat+="," + user_stars_feat  
	out_feat+="," + user_rating_feat 
	#+ "," + cat_feat
	
	return out_feat


def get_business_avg_stars(bus, user, review_item, bus_test, user_test):

#	import pdb
#	pdb.set_trace()

	business_id = review_item.business_id
	# is in test data, which is train for train
	if bus_test.is_exists(business_id): 
		bus_avg_stars =  bus_test.get_item_rating(business_id)
		if bus_avg_stars == 0:
			bus_avg_stars =  _get_business_train_avg_stars(bus, business_id)
	else:
		bus_avg_stars =  _get_business_train_avg_stars(bus, business_id)

	return "%.2f" % (bus_avg_stars) 
def _get_business_train_avg_stars(bus, business_id):
	if bus.is_exists(business_id):
		bus_avg_stars =  bus.get_item_rating(business_id)
	else:
		bus_avg_stars = bus.get_avg_bus_stars()
	return bus_avg_stars
		

def get_user_avg_stars(bus, user, review_item, bus_test, user_test):

	user_id = review_item.user_id
	# is in test data, which is train for train
	if user_test.is_exists(user_id): 
		user_avg_stars =  user_test.get_user_stars(user_id)
		if user_avg_stars == 0:
			user_avg_stars =  _get_user_train_avg_stars(user, user_id)
	else:
		user_avg_stars =  _get_user_train_avg_stars(user, user_id)
	return "%.2f" % (user_avg_stars) 
def _get_user_train_avg_stars(user, user_id):
	if user.is_exists(user_id):
		user_avg_stars =  user.get_user_stars(user_id)
	else:
		user_avg_stars = user.get_avg_user_stars()	
	return user_avg_stars


def get_user_avg_review(bus, user, review_item, bus_test, user_test):

	user_id = review_item.user_id
	# is in test data, which is train for train
	if user_test.is_exists(user_id): 
		user_avg_stars =  user_test.get_user_review_count(user_id)
		if user_avg_stars == 0:
			user_avg_stars =  _get_user_train_avg_review(user, user_id)
	else:
		user_avg_stars =  _get_user_train_avg_review(user, user_id)
	return "%.2f" % (user_avg_stars) 
def _get_user_train_avg_review(user, user_id):
	if user.is_exists(user_id):
		user_avg_stars =  user.get_user_review_count(user_id)
	else:
		user_avg_stars = user.get_avg_user_review_count()	
	return user_avg_stars

def get_business_review_count(bus, user, review_item, bus_test, user_test):

	business_id = review_item.business_id
	# is in test data, which is train for train
	if bus_test.is_exists(business_id): 
		bus_avg_stars =  bus_test.get_item_review_count(business_id)
		if bus_avg_stars == 0:
			bus_avg_stars =  _get_business_train_avg_review_count(bus, business_id)
	else:
		bus_avg_stars =  _get_business_train_avg_review_count(bus, business_id)

	return "%.2f" % (bus_avg_stars) 
def _get_business_train_avg_review_count(bus, business_id):
	if bus.is_exists(business_id):
		bus_avg_stars =  bus.get_item_review_count(business_id)
	else:
		bus_avg_stars = bus.get_avg_bus_review_count()
	return bus_avg_stars


def get_category_feat(bus, user, review_item):
	default_cat = bus.get_max_cat_id()

	r_bus_id = review_item.business_id
	try:
	    bus_cat = bus.get_item(r_bus_id).categories
	    if len(bus_cat) > 0:
	        cat_str = bus.get_cat_id(bus_cat[0])
	        return str(cat_str)
	except KeyError:
	    return default_cat

	return default_cat
