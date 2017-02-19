import _path_config
import logging

from flask import Flask, request, jsonify
app = Flask(__name__)

logging.info('loading models...')

from reviews.scrape import scrape_reviews_from_url
from reviews.data import reviews_to_phrases 
from reviews.cluster import cluster_phrases

from gensim.models import Doc2Vec
doc2vec = Doc2Vec.load('data/models/reviews.sample.doc2vec.pickle')
doc2vec.make_cum_table()

logging.info('models loaded')

@app.route('/analyze-reviews/')
def analyze_reviews():
    product_url = request.args.get('url')
    if product_url is not None:
        logging.info('scraping reviews from %s', product_url)
        reviews = scrape_reviews_from_url(product_url)
        logging.info('read %d reviews from %s', len(reviews), product_url)
        phrases = reviews_to_phrases(reviews)
        logging.info('extracted %d phrases', len(phrases))
        for phrase in phrases:
            phrase.infer_vector(doc2vec)
        eps = float(request.args.get('eps', '0.5'))
        minpts = int(request.args.get('minpts', '5'))
        clusters = cluster_phrases(phrases, eps, minpts)
        logging.info('found %d clusters', len(clusters))
        
        json_clusters = []
        for cluster in clusters.values():
            json_clusters.append([phrase.to_json() for phrase in cluster])
        return jsonify(json_clusters)
    else:
        return jsonify({})

if __name__ == '__main__':
    app.run()
