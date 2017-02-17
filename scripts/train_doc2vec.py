import _path_config

import sys
import csv

from reviews.data import ReviewsCorpus

from gensim.models import Doc2Vec

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 train_doc2vec.py sents.csv doc2vec.pickle')
        print('Reads sentences from sents.csv (as output by extract_review_sentences.py) and')
        print('trains a doc2vec model over them, writing it to doc2vec.pickle.')
    else:
        _, sents_fname, model_fname = sys.argv
        
        sentences = ReviewsCorpus(sents_fname)
        model = Doc2Vec(alpha=0.025, min_alpha=0.025)  # use fixed learning rate
        model.build_vocab(sentences)
        for epoch in range(10):
            model.train(sentences)
            model.alpha -= 0.002  # decrease the learning rate
            model.min_alpha = model.alpha  # fix the learning rate, no decay
            
        model.save(model_fname)
