import datetime
import random
import glob
import gzip
import logging
import csv
from collections import namedtuple

from reviews import spacy_nlp, stanford_parser

from gensim.models.doc2vec import LabeledSentence
from nltk.tree import Tree

class Phrase(object):
    """
    Represents a phrase somebody used in a review.
    """
    
    def __init__(self, tokens, review):
        """
        Creates a new Phrase with the given data. tokens is a list of spaCy
        tokens and review is the review the phrase came from.
        """
        self.tokens = tokens
        self.review = review
    
    def infer_vector(self, doc2vec, steps=100):
        """
        Infer a vector representation for this phrase using the given doc2vec
        model.
        """
        self.vector = doc2vec.infer_vector(self.tokens, alpha=doc2vec.alpha,
                                           steps=100)

class Review(object):
    """
    Represents an Amazon review.
    """
    
    def __init__(self, text, summary, overall, helpful, review_time,
                 rid=None):
        """
        Creates a new Review with the given data. text is the text of the
        review, summary is the title, overall is the overall rating given
        (1-5 stars), helpful is a tuple (a, b) which means a out of b found
        this review helpful, and review_time is a datetime for the review.
        You can also pass an optional review ID.
        """
        
        self.id = rid
        self.text = text
        self.summary = summary
        self.overall = overall
        self.helpful = helpful
        self.review_time = review_time
        
        self.doc = spacy_nlp(self.text)
        
Sentence = namedtuple('Sentence', ['tokens', 'review'])

def extract_phrases(tree, labels={'S', 'SBAR'}):
    """
    Given a parse tree, extracts all phrases that occur under the given labels
    and yields them as lists of tokens.
    """
    
    if isinstance(tree, Tree):
        if tree.label() in labels:
            yield list(tree.flatten())
        for subtree in tree:
            for phrase in extract_phrases(subtree, labels):
                yield phrase
        
def reviews_to_phrases(reviews):
    """
    Given a list of reviews, returns a list of all the phrases they contain.
    """
    
    sentences = []
    for review in reviews:
        sentences.append(Sentence(list(map(str, spacy_nlp(review.summary))),
                                  review))
        for sent in review.doc.sents:
            sentences.append(Sentence(list(map(str, sent)), review))
    
    parses = stanford_parser.parse_sents([sent.tokens for sent in sentences])
    phrases = []
    for trees, sentence in zip(parses, sentences):
        trees = list(trees)
        parse = trees[0]
        for phrase_tokens in extract_phrases(parse):
            phrases.append(Phrase(phrase_tokens, sentence.review))
    
    return phrases
    
def json2review(json_dict):
    """
    Given a review as JSON data (like from the reviews corpus), returns a
    Review object with that data.
    """
    
    text = json_dict['reviewText']
    summary = json_dict['summary']
    overall = json_dict['overall']
    helpful = tuple(json_dict['helpful'])
    review_time = datetime.datetime.fromtimestamp(json_dict['unixReviewTime'])
    rid = json_dict['asin'] + '_' + json_dict['reviewerID']
    return Review(text, summary, overall, helpful, review_time, rid)

def reviews_in_directory(reviews_dir, sample = 1):
    """
    Yields all the reviews in all files in the given directory, optionally
    choosing a random sample.
    """
    
    for reviews_fname in glob.glob(reviews_dir + '/reviews_*.json.gz'):
        logging.info('reading reviews from %s', reviews_fname)
        with gzip.open(reviews_fname, 'r') as reviews_file:
            for line in reviews_file:
                line = line.decode('utf-8')
                if random.random() < sample:
                    yield json2review(eval(line))

class ReviewsCorpus(object):
    """
    Iterable that yields TaggedSentences given a CSV file of sentences.
    """
    
    def __init__(self, sents_fname):
        self.sents_fname = sents_fname
        
    def __iter__(self):
        with open(self.sents_fname, 'r') as sents_file:
            sents_csv = csv.reader(sents_file)
            next(sents_csv) # Ignore header
            for rid, sent_index, tokens, overall, helpful in sents_csv:
                labels = [rid + '_' + str(sent_index)] 
                tokens = tokens.lower().split(' ')
                yield LabeledSentence(words=tokens, tags=labels)   