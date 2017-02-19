import _path_config

import sys
import pickle
from collections import defaultdict

from reviews.data import ReviewsCorpus
from reviews.nlp import ngrams

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 build_dict.py sents.csv ngrams.pickle')
        print('Reads sentences from sents.csv (as output by extract_review_sentences.py) and')
        print('learns the frequency of n-grams for n=1..3.')
    else:
        _, sents_fname, ngrams_fname = sys.argv
        
        ns = range(1, 4)
    
        ngram_counts = {n: 0 for n in ns}
        ngram_freqs = defaultdict(int)
    
        sentences = ReviewsCorpus(sents_fname)
        for tagged_sentence in sentences:
            for n in ns:
                for ngram in ngrams(tagged_sentence.words, n):
                    ngram_freqs[ngram] += 1
                    ngram_counts[n] += 1
                
        with open(ngrams_fname, 'wb') as ngrams_file:
            pickle.dump((ngram_counts, ngram_freqs), ngrams_file)
