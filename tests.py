import scripts._path_config
import json
from reviews.data import Review, Phrase, json2review
from reviews.cluster import *
from gensim.models import Doc2Vec

model = Doc2Vec.load('data/models/reviews.sample.doc2vec.pickle')
model.make_cum_table()

phrases = []
with open('data/reviews_Electronics_5.json') as file:
    linenum = 0
    for line in file:
        if linenum > 100:
            break
        data = json.loads(line)
        review = json2review(data)
        for sent in review.doc.sents:
            phrase = Phrase(list(map(str, sent)), sent, review)
            phrase.infer_vector(model)
            phrases.append(phrase)
        linenum +=1

phrasecluster = cluster_phrases(phrases)
print(phrasecluster)
