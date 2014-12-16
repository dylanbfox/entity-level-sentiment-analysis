import requests
from collections import defaultdict

def get_subject_phrase_sentiments(subjects, phrases):
	result = {"subjects": []}
	for subject in subjects:
		for phrase in phrases:
			if subject in phrase:
				sentiment, score = get_document_sentiment(phrase)
				result["subjects"].append({
					"name": subject,
					"sentiment": sentiment,
					"score": score,
					"phrase": phrase
				})
				
	return result 

def get_document_sentiment(raw_text):
	"""
	Pass raw text in! Send off to 3rd party
	API to determine sentiment analysis.

	Eventually send each sentence and chunk off
	to be analyzed.

	Eventually use own prediction model hosted
	with Goolge API.
	"""

	url = "http://text-processing.com/api/sentiment/"
	payload = {'text': raw_text}

	try:
		response = requests.post(url, data=payload)
	except:
		print "[WARNING] Sentiment API Error for %s" % raw_text		
		return '0', 0

	try:
		data = response.json()
	except:
		print "[WARNING] Sentiment API Error for %s" % raw_text
		return '0', 0
		
	# print data
	sentiment = data['label']
	neg_score = data['probability']['neg']
	pos_score = data['probability']['pos']
	neutral_score = data['probability']['neutral']
	score = max(neg_score, pos_score, neutral_score)

	if neutral_score < 0.50:
		if neg_score > 0.47:
			sentiment = 'neg'
			score = neg_score

	if neg_score > 0.65:
		sentiment = 'neg'
		score = neg_score

	if pos_score > 0.61:
		sentiment = 'pos'
		score = pos_score

	return sentiment, score