from sklearn.cluster import DBSCAN
from reviews.nlp import ngrams
from reviews.data import Phrase

import string

def cluster_phrases(phrases, eps=0.5, min_samples=5):
    dbscanner = DBSCAN(metric='cosine', algorithm='brute', eps=eps, min_samples=min_samples)
    labels = dbscanner.fit_predict([phrase.vector for phrase in phrases])
    clusters = {}
    for i in range(len(phrases)):
        label = labels[i] or -1
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(phrases[i])
    return clusters

class NGramCluster(object):
    """
    Represents a cluster constructed around an n-gram that users are discussing
    in reviews.
    """
    
    def __init__(self, ngram):
        """
        Create an empty cluster around the given n-gram.
        """
        self.ngram = ngram
        self.phrases = []
        self.reviews = set()
        self.log_prob = float('nan')
        
    def add_phrase(self, phrase):
        self.phrases.append(phrase)
        self.reviews.add(phrase.review)
        
    def add_review(self, review):
        self.phrases.append(None)
        self.reviews.add(review)
        
    def to_json(self):
        return {'ngram': list(self.ngram), 'ngram_text': ' '.join(self.ngram),
                'size': len(self.reviews), 'reviews': [review.to_json() for
                review in self.reviews], 'log_prob': self.log_prob}
        
def is_punctuation(word):
    """
    Returns True if this word is punctuation.
    """
    
    return not any(char in string.ascii_letters for char in word)

def build_ngram_clusters(reviews, ngram_model, num_clusters = 100):
    """
    Given a list of phrases, builds clusters based on the ngrams in the
    phrases and then returns the top clusters based on their size and the
    log probabilities from the given ngram model.
    """
    
    clusters = {}
    for review in reviews:
        for n in range(1, 10):
            for ngram in ngrams(review.get_tokens(), n):
                if ngram not in clusters:
                    clusters[ngram] = NGramCluster(ngram)
                clusters[ngram].add_review(review)
    for ngram, cluster in clusters.items():
        cluster.log_prob = ngram_model.log_prob(tuple(
                map(lambda s: s.lower(), ngram)))
        
    for ngram in list(clusters):
        num_non_stop = 0
        for word in ngram:
            if ngram_model.log_prob((word,)) >= 12:
                num_non_stop += 1
        if num_non_stop < 2 or is_punctuation(ngram[0]) or \
                is_punctuation(ngram[-1]):
            del clusters[ngram]
        
    clusters = list(filter(lambda cluster: len(cluster.reviews) >= 2,
                           clusters.values()))
    clusters.sort(key=lambda cluster: len(cluster.reviews) *
                  (2) ** cluster.log_prob, reverse=True)
    print(sum(len(cluster.phrases) for cluster in clusters))
    print(len(clusters))
    
    unique_clusters = []
    for cluster in clusters:
        is_unique = True
        for past_cluster in unique_clusters:
            if ' '.join(cluster.ngram) in ' '.join(past_cluster.ngram):
                is_unique = False
        if is_unique:
            unique_clusters.append(cluster)
        if len(unique_clusters) >= num_clusters:
            break
    
    return unique_clusters[:num_clusters]

    clusters = clusters[:num_clusters]
            
    ngram_phrases = []
    for cluster in clusters:
        ngram_phrase = Phrase(list(cluster.ngram), None)
    #    ngram_phrase.infer_vector(doc2vec)
        ngram_phrases.append(ngram_phrase)
            
    print(len(ngram_phrases))
    ngram_clusters = cluster_phrases(ngram_phrases, 0.3, 4)
    return ngram_clusters
    