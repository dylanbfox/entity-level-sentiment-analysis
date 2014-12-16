import nltk
import os
from pickle import load

class PosBackoffTagger(object):

	def __init__(self):
		"""
		Loads the tagger and then uses it to
		tag the sentence with the correct POS.
		"""
		BASE_DIR = os.path.dirname(os.path.dirname((__file__)))
		taggerfile = open(BASE_DIR + '/nltk_data/taggers/brill_tagger.pk1', 'rb')
		self.tbuar_tagger = load(taggerfile)
		taggerfile.close()

	def tag(self, tokenized_sent):
		tagged_sent = self.tbuar_tagger.tag(tokenized_sent)
		return tagged_sent