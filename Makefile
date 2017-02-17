
PYTHON=python3
DATADIR=data

$(DATADIR)/text/reviews.sents.csv : scripts/extract_review_sentences.py \
	$(DATADIR)/reviews/
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@
