import nltk

class RegexpChunker(object):

	def __init__(self):
		self.grammar = r"""
			NP: {<CD>(<\^?JJ>)?(<\^?NN.*>+|<\^?VB.*>(<\^?JJ>)?<\^?NN.*>+)}
				{<DT><\^?VBG>}
				{<\^?VB.*>(<\^?JJ>)?<\^?NN.*>+}
				{(<\^?JJ>)?<\^?NN.*>+<BES>(<\^?JJ>)?<\^?NN.*>+}
				{(<\^?JJ>)?<\^?NN.*>+<POS>(<\^?JJ>)?<\^?NN.*>+}
				{(<\^?JJ>)?<\^?NN.*>+<BES>}
				{(<\^?JJ>)?<\^?NN.*>+<POS>}
				{(<\^?JJ>)?<\^?NN.*>+}
		"""

		self.chunker = nltk.RegexpParser(self.grammar, loop=2)

	def create_chunks(self, sentence):
		return self.chunker.parse(sentence)

	def traverse_trees(self, trees):
		def traversetree(tree):
			leaves = []

			def traverse(tree):
				for subtree in tree:
					try:
						leaves.append(subtree.leaves()) 
					except:
						pass
					else:
						traverse(subtree)

			traverse(tree)
			return leaves

		sents_leaves = []
		for tree in trees:
			sents_leaves.append(traversetree(tree))

		return sents_leaves

# def regexp_chunker(sentence):
# 	"""
# 	Returns a tree for the sentence
# 	passed in.
# 	"""
# 	grammar = r"""
# 		NP: {<CD>(<\^?JJ>)?(<\^?NN.*>+|<\^?VB.*>(<\^?JJ>)?<\^?NN.*>+)}
# 			{<DT><\^?VBG>}
# 			{<\^?VB.*>(<\^?JJ>)?<\^?NN.*>+}
# 			{(<\^?JJ>)?<\^?NN.*>+<BES>(<\^?JJ>)?<\^?NN.*>+}
# 			{(<\^?JJ>)?<\^?NN.*>+<POS>(<\^?JJ>)?<\^?NN.*>+}
# 			{(<\^?JJ>)?<\^?NN.*>+<BES>}
# 			{(<\^?JJ>)?<\^?NN.*>+<POS>}
# 			{(<\^?JJ>)?<\^?NN.*>+}
# 	"""

# 	cp = nltk.RegexpParser(grammar, loop=2)
# 	return cp.parse(sentence)