import nltk
import re

def replace_repeaters(tokenized_sents):
	replacer = RepeatReplacer()
	sents = [[replacer.replace(word.lower()) for word in sent] for sent in tokenized_sents]
	return sents

class RepeatReplacer(object):

	def __init__(self):
		nltk.data.path.append('./nltk_data/')
		self.eng_words = nltk.corpus.words.words('en')
		self.lemmatizer = nltk.stem.WordNetLemmatizer()
		self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
		self.repl = r'\1\2\3'

	def replace(self, word):
		word = word.lower()
		if word in self.eng_words or self.lemmatizer.lemmatize(word) in self.eng_words:
			return word
		repl_word = self.repeat_regexp.sub(self.repl, word)

		if repl_word != word:
			return self.replace(repl_word)
		else:
			return repl_word