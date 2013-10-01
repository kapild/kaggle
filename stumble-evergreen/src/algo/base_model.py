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
#
	@staticmethod
	def none_comma(val):
		return val if val else ''
	
	@staticmethod
	def precison(val):
		return "%.2f" % (val)
