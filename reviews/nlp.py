
import pickle
from numpy import log2

def ngrams(tokens, n):
    for i in range(len(tokens) - n + 1):
        yield tuple(tokens[i:i + n])

class NGramModel(object):
    """
    Model that tracks frequencies and probabilities of various n-grams. Uses
    simple add-1 smoothing and estimates higher n-gram probabilities with
    combinations of lower n-grams.
    """
    
    def __init__(self, ngrams_fname):
        """
        Loads ngram counts from the given file to initialize this model.
        """
        
        with open(ngrams_fname, 'rb') as ngrams_file:
            self.ngram_counts, self.ngram_freqs = pickle.load(ngrams_file)
        
    def prob(self, ngram):
        """
        Returns the probability of this ngram occuring.
        """
        
        n = len(ngram)
        if n == 1 or self.ngram_freqs[ngram] != 0:
            return (self.ngram_freqs[ngram] + 1) / self.ngram_counts[n]
        else:
            prob = 1
            for word in ngram:
                prob *= self.prob((word,))
            return prob
            
    def log_prob(self, ngram):
        """
        Returns the -log of the probability of this ngram.
        """
        
        return -log2(self.prob(ngram))
