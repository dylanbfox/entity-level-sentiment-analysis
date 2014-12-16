def create_subjects(sents_leaves):
	blacklist = ["today", "time", "bigger", "had", "tomorrow", "now",
	"lot", "fun"]

	subjects = []
	for sent_leaves in sents_leaves:
		for leaf in sent_leaves:
			name = ' '.join([w for (w,t) in leaf])
			if name.lower() in blacklist:
				continue
			subjects.append(name)

	return subjects