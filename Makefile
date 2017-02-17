
PYTHON=python3
DATADIR=data

$(DATADIR)/text/reviews.sents.csv : scripts/extract_review_sentences.py \
	$(DATADIR)/reviews/
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@
	
$(DATADIR)/models/%.doc2vec.pickle : scripts/train_doc2vec.py \
	$(DATADIR)/text/%.sents.csv
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@
