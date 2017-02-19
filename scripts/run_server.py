import _path_config
import logging

from flask import Flask, request, jsonify
from flask import render_template

app = Flask(__name__)
app.debug = True


logging.info('loading models...')

from reviews.scrape import scrape_reviews_from_url
from reviews.data import reviews_to_phrases 
from reviews.cluster import cluster_phrases, build_ngram_clusters

#from gensim.models import Doc2Vec
#doc2vec = Doc2Vec.load('data/models/reviews.sample.doc2vec.pickle')
#doc2vec.make_cum_table()

from reviews.nlp import NGramModel
ngrams = NGramModel('data/models/reviews.sample.ngrams.pickle')

logging.info('models loaded')

@app.route('/analyze-reviews/')
def analyze_reviews():
    product_url = request.args.get('url')
    if product_url is not None:
        logging.info('scraping reviews from %s', product_url)
        reviews = scrape_reviews_from_url(product_url)
        logging.info('scraped %d reviews', len(reviews))
        #phrases = reviews_to_phrases(reviews)
        #logging.info('extracted %d phrases', len(phrases))
        clusters = build_ngram_clusters(reviews, ngrams)
        logging.info('found %d clusters', len(clusters))
        
        json_clusters = [cluster.to_json() for cluster in clusters]
        return jsonify(json_clusters)
    else:
        return jsonify({})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/review')
def review():
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
        review_clusters = []
        for cluster in clusters.values():
            phrase_array = [' '.join(phrase.tokens) for phrase in cluster]
            review_clusters.append((phrase_array[0], len(phrase_array, phrase_array[0].title())))
            # json_clusters.append([phrase.to_json() for phrase in cluster])


    return render_template('review.html', item_name="The unstoppable passage of time #entropyalwaysincreases", overall=-1, reviews=review_clusters, num_stars=4)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
