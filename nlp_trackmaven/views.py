from nlp_trackmaven import app
from nlp.tokenizers import tokenize_sents, tokenize_words, PhraseExtractor
from nlp.normalizers import replace_repeaters
from nlp.taggers import PosBackoffTagger
from nlp.chunkers import RegexpChunker
from nlp.utils import create_subjects
from nlp.sentiment import get_subject_phrase_sentiments

from flask import render_template
from flask import jsonify

@app.route('/')
def hello_world():
	raw = "The speaker was great but the video in the beginning was terrible."
	sents = tokenize_sents(raw)
	tokenized_sents = tokenize_words(sents)
	normalized_sents = replace_repeaters(tokenized_sents)

	pos_tagger = PosBackoffTagger()
	tagged_sents = [pos_tagger.tag(sent) for sent in normalized_sents]

	chunker = RegexpChunker()
	trees = [chunker.create_chunks(sent) for sent in tagged_sents]
	sents_leaves = chunker.traverse_trees(trees)
	subjects = create_subjects(sents_leaves)

	extractor = PhraseExtractor()
	phrases = extractor.extract_phrases(tagged_sents, subjects)
	result = get_subject_phrase_sentiments(subjects, phrases)

	return jsonify(**result)