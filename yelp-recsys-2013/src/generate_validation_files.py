import sys

class CrossValidation():


	def __init__(self, input_file_name, output_file_name, validation=10):
		self.input_file_name = input_file_name
		self.output_file_name = output_file_name
		self.validation = validation
		
		self.run(self.input_file_name, self.output_file_name, self.validation)

 	def run(self,input_file_name, output_file_name, validation):
 		
	 	with open(input_file_name) as f:
	 		X = f.readlines()
	 	
	 	count = 1
	 	for training, validation in CrossValidation.k_fold_cross_validation(X, validation):
	 		with open(output_file_name + "_train_" + str(count), "w") as f_train:
	 			for item in training:
	 				f_train.write(item)
	 		with open(output_file_name + "_valid_" + str(count), "w") as f_valid:
	 			for item in validation:
	 				f_valid.write(item)
	 		count+=1
		 		
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
			training = []
			validation = [] 
			for i,x in enumerate(X):
				if i % K == k:
					validation.append(x)
				else:
					training.append(x)
			yield training, validation

if __name__ == '__main__':
	input_file_name = sys.argv[1]
	output_file_name = sys.argv[2]
	try:
		validation = int(sys.argv[3])
	except Exception:
		validation = 10
		
	yelp_review = CrossValidation(input_file_name, output_file_name, validation)
