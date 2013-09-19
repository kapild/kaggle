
class BaseModel(object):

	def __init__(self, page, page_test):
		self.page = page
		self.page_test = page_test

	def get_output_line(self, review_item):
		raise NotImplementedError

	@staticmethod
	def get_label(page, page_test, page_item):
		
		if page_item.label:
			return page_item.label
		else:
			return 0
#			lab= BaseModel.precison(page_item.label)
#		else: 
#			lab = BaseModel.precison(0)
#		return lab 

	@staticmethod
	def get_url_id(page, page_test, page_item):
		return page_item.urlid

	@staticmethod
	def get_alchemy_category(page, page_test, page_item):
		return BaseModel.none_comma(page_item.alchemy_category)
	
	def get_alchemy_category_score(self, page, page_test, page_item):
		if page.is_exists(page_item.urlid) and page_item.alchemy_category_score is not None:
			return BaseModel.precison(page_item.alchemy_category_score)

		if page_test.is_exists(page_item.urlid) and page_item.alchemy_category_score is not None:
			return BaseModel.precison(page_item.alchemy_category_score)

		return BaseModel.precison(page.get_avg_alchemy_category_score())

	def get_avglinksize(self, page, page_test, page_item):
		if page.is_exists(page_item.urlid) and page_item.avglinksize is not None:
			return BaseModel.precison(page_item.avglinksize)

		if page_test.is_exists(page_item.urlid) and page_item.avglinksize is not None:
			return BaseModel.precison(page_item.avglinksize)

		return BaseModel.precison(page.get_avg_avglinksize())

	def get_commonlinkratio_1(self, page, page_test, page_item):
		if page.is_exists(page_item.urlid) and page_item.commonLinkRatio_1 is not None:
			return BaseModel.precison(page_item.commonLinkRatio_1)

		if page_test.is_exists(page_item.urlid) and page_item.commonLinkRatio_1 is not None:
			return BaseModel.precison(page_item.commonLinkRatio_1)

		return BaseModel.precison(page.get_avg_commonlinkratio_1())

	def get_commonlinkratio_2(self, page, page_test, page_item):
		if page.is_exists(page_item.urlid) and page_item.commonLinkRatio_2 is not None:
			return BaseModel.precison(page_item.commonLinkRatio_2)

		if page_test.is_exists(page_item.urlid) and page_item.commonLinkRatio_2 is not None:
			return BaseModel.precison(page_item.commonLinkRatio_2)

		return BaseModel.precison(page.get_avg_commonlinkratio_2())

	def get_commonlinkratio_3(self, page, page_test, page_item):
		if page.is_exists(page_item.urlid) and page_item.commonLinkRatio_3 is not None:
			return BaseModel.precison(page_item.commonLinkRatio_3)

		if page_test.is_exists(page_item.urlid) and page_item.commonLinkRatio_3 is not None:
			return BaseModel.precison(page_item.commonLinkRatio_3)

		return BaseModel.precison(page.get_avg_commonlinkratio_3())

	def get_commonlinkratio_4(self, page, page_test, page_item):
		if page.is_exists(page_item.urlid) and page_item.commonLinkRatio_4 is not None:
			return BaseModel.precison(page_item.commonLinkRatio_4)

		if page_test.is_exists(page_item.urlid) and page_item.commonLinkRatio_4 is not None:
			return BaseModel.precison(page_item.commonLinkRatio_4)

		return BaseModel.precison(page.get_avg_commonlinkratio_4())

#			['avglinksize', self.get_avglinksize, True],
#			['', self.get_commonlinkratio_1, True],
#			['commonlinkratio_2', self.get_commonlinkratio_2, True],
#			['commonlinkratio_3', self.get_commonlinkratio_3, True],
#			['commonlinkratio_4', self.get_commonlinkratio_4, True],

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

	def get_boilerplate(self, page, page_test, page_item):
		if page.is_exists(page_item.urlid) and page_item.boilerplate is not None:
			return (page_item.boilerplate)

		if page_test.is_exists(page_item.urlid) and page_item.boilerplate is not None:
			return (page_item.boilerplate)

		return ''
	@staticmethod
	def none_comma(val):
		return val if val else ''
	
	@staticmethod
	def precison(val):
		return "%.2f" % (val)
