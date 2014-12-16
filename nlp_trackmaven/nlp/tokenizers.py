import nltk
import re
import string

def tokenize_sents(raw):
	"""
	Load the Punkt tokenizer from a pickle file for speed.
	"""
	nltk.data.path.append('./nltk_data/')
	sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

	return sent_tokenizer.tokenize(raw)

def tokenize_words(sents):
	"""
	Default word tokenizer uses conventions found in Treebank corpus
	and splits on punctuation and contractions, creating new tokens. 
	"""
	sents = [nltk.word_tokenize(sent) for sent in sents]
	return sents

class PhraseExtractor(object):

	def __init__(self, separators=None):
		if separators:
			self.separators = separators
		else:
			self.separators = {
				"words": [
					"accordingly",
					"additionally",
					"also",
					"besides",
					"comparatively",
					"consequently",
					"conversely",
					"finally",
					"further",
					"furthermore",
					"elsewhere",
					"equally",
					"hence",
					"henceforth",
					"however",
					"in addition",
					"in comparison",
					"in contrast",
					"indeed",
					"instead",
					"likewise",
					"meanwhile",
					"moreover",
					"namely",
					"nevertheless",
					"nonetheless",
					"otherwise",
					"rather",
					"similarly",
					"subsequently",
					"then",
					"thereafter",
					"therefore",
					"thus",
					"yet",
					",",
					"...",
					"..",
					";",
				],
				"tags": [
					"CC",
					"SYM",
				]
			}

	def remove_extra_spaces(self, s):
		return ' '.join(s.split())

	def extract_phrases(self, tagged_sentences, subjects):
		self.phrases = []
		for sent in tagged_sentences:
			sent_phrases = []
			phrase_found_index = None			
			for index, (word, pos) in enumerate(sent):
				if index == 0:
					continue
				if word.lower() in self.separators['words'] or pos in self.separators['tags']:
					if phrase_found_index:
						phrase_found_index = phrase_found_index+1						
					else:
						phrase_found_index = 0						
					sent_phrases.append(' '.join(w for w, t in sent[phrase_found_index:index]))
					phrase_found_index = index					
			if phrase_found_index:
				sent_phrases.append(' '.join(w for w, t in sent[phrase_found_index+1:]))
			else:
				sent_phrases.append(' '.join(w for w, t in sent))

			if sent_phrases:
				self.phrases += self.clean_phrases(sent_phrases, subjects)
		return [self.remove_extra_spaces(s) for s in self.phrases]

	def clean_phrases(self, phrases, subjects):
		print phrases
		whitelist = string.letters + string.digits + ' '
		# subjects = [''.join(c for c in subject if c in whitelist) for subject in subjects]
		true_phrases = []
		partial_phrases = []
		for index, phrase in enumerate(phrases):
			# phrase = ''.join(c for c in phrase if c in whitelist)
			# check to see if length of actual words is >= 3 (remove punctuation, etc.)
			if any(subject in phrase for subject in subjects) and len(''.join(c for c in phrase if c in whitelist).split()) >= 3:
				true_phrases.append(phrase)
			else:
				partial_phrases.append((index, phrase))

		phrase_cache = ''
		subject_found = False
		partial_phrase = ' '.join(p for i, p in partial_phrases)
		if not true_phrases:
			true_phrases.append(partial_phrase)
		elif any(subject in partial_phrase for subject in subjects):
			true_phrases.append(partial_phrase)
		elif any(i==0 for i,p in partial_phrases):
			true_phrases[0] = partial_phrase + ' ' + true_phrases[0]
		else:
			true_phrases[0] += ' '+partial_phrase

		return true_phrases
