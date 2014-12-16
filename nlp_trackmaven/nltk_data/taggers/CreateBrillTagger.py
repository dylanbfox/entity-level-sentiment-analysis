from __future__ import division

import nltk

from nltk.tag import brill, brill_trainer
from nltk.tag import UnigramTagger, BigramTagger, TrigramTagger, DefaultTagger
from nltk.corpus import treebank

def create_backoff_tagger():
	"""
	Run to create the backoff tagger, used to
	tag sentences with correct POS, and to save
	the tagger for later use.
	"""
	tagged_posts = nltk.corpus.nps_chat.tagged_posts()

	patterns = [
	    (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
	    (r'.*ould$', 'MD'),
	    (r'.*ing$', 'VBG'),
	    (r'.*ed$', 'VBD'),
	    (r'.*ness$', 'NN'),
	    (r'.*ment$', 'NN'),
	    (r'.*ful$', 'JJ'),
	    (r'.*ious$', 'JJ'),
	    (r'.*ble+$', 'JJ'),
	    (r'.*ic$', 'JJ'),
	    (r'.*ive$', 'JJ'),
	    (r'.*ic$', 'JJ'),
	    (r'.*est$', 'JJ'),
	    (r'^a$', 'PREP'),
	    (r'.*', 'NN')
	]

	regexp_tagger = nltk.RegexpTagger(patterns)
	affix_tagger = nltk.AffixTagger(tagged_posts, backoff=regexp_tagger)
	unigram_tagger = nltk.UnigramTagger(tagged_posts, backoff=affix_tagger)
	bigram_tagger = nltk.BigramTagger(tagged_posts, backoff=unigram_tagger)
	tbuar_tagger = nltk.TrigramTagger(tagged_posts, backoff=bigram_tagger)
	return tbuar_tagger

templates = [
	brill.Template(brill.Pos([-1])),
	brill.Template(brill.Pos([1])),
	brill.Template(brill.Pos([-2])),
	brill.Template(brill.Pos([2])),
	brill.Template(brill.Pos([-2, -1])),
	brill.Template(brill.Pos([1, 2])),
	brill.Template(brill.Pos([-3, -2, -1])),
	brill.Template(brill.Pos([1, 2, 3])),
	brill.Template(brill.Pos([-1]), brill.Pos([1])),
	brill.Template(brill.Word([-1])),
	brill.Template(brill.Word([1])),
	brill.Template(brill.Word([-2])),
	brill.Template(brill.Word([2])),
	brill.Template(brill.Word([-2, -1])),
	brill.Template(brill.Word([1, 2])),
	brill.Template(brill.Word([-3, -2, -1])),
	brill.Template(brill.Word([1, 2, 3])),
	brill.Template(brill.Word([-1]), brill.Pos([1])),
]

train_sents = nltk.corpus.nps_chat.tagged_posts()
initial_tagger = create_backoff_tagger()
trainer = brill_trainer.BrillTaggerTrainer(initial_tagger, templates, deterministic=True)
brill_tagger = trainer.train(train_sents)

from pickle import dump
output = open('brill_tagger.pk1', 'wb')
dump(brill_tagger, output, -1)
output.close()

# import pickle
# f = open('brill_tagger.pickle', 'wb')
# pickle.dump(brill_tagger, f)
# f.close()