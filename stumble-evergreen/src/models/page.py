class Page:

	def __init__(self, dict):
		self.type = 'page'
#		import pdb
#		pdb.set_trace()
		self.url =  self.data(dict,'url')
		self.urlid =  self.data(dict,'urlid')
		self.boilerplate =  self.data(dict,'boilerplate')
		self.alchemy_category =  self.data(dict,'alchemy_category')
		self.alchemy_category_score =  self.data(dict,'alchemy_category_score', 2)

		self.avglinksize =  self.data(dict,'avglinksize', 2)
		self.commonLinkRatio_1 =  self.data(dict,'commonlinkratio_1', 2)
		self.commonLinkRatio_2 =  self.data(dict,'commonlinkratio_2', 2)
		self.commonLinkRatio_3 =  self.data(dict,'commonlinkratio_3', 2)
		self.commonLinkRatio_4 =  self.data(dict,'commonlinkratio_4', 2)

		self.compression_ratio =  self.data(dict,'compression_ratio', 2)
		self.embed_ratio =  self.data(dict,'embed_ratio', 2)
		self.frameBased =  self.data(dict,'framebased')
		self.frameTagRatio =  self.data(dict,'frametagratio', 2)
		
		self.hasDomainLink =  self.data(dict,'hasDomainLink')
		self.html_ratio =  self.data(dict,'html_ratio', 2)
		self.image_ratio =  self.data(dict,'image_ratio', 2)

		self.is_news =  self.data(dict,'is_news')
		self.lengthyLinkDomain =  self.data(dict,'lengthyLinkDomain')
		self.linkwordscore =  self.data(dict,'linkwordscore', 2)
		self.news_front_page =  self.data(dict,'news_front_page')
		
		self.non_markup_alphanum_characters =  self.data(dict,'non_markup_alphanum_characters', 1)
		self.numberOfLinks =  self.data(dict,'numberOfLinks', 1)
		self.numwords_in_url =  self.data(dict,'numwords_in_url', 2)
		self.parametrizedLinkRatio =  self.data(dict,'parametrizedLinkRatio', 2)
		self.spelling_errors_ratio =  self.data(dict,'spelling_errors_ratio', 2)
		self.label =  self.data(dict,'label')
		
		
	def data(self, dict, key, is_int=0):
		if key in dict:
			if (dict[key] == '?'):
				return None
			if is_int == 1:
				return int(dict[key])
			elif is_int == 2:
				return float(dict[key])
			else:
				return dict[key]

		if(is_int == 1):
			return 0
		return None


