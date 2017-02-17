import _path_config

import sys
import csv

from reviews import spacy_nlp
from reviews.data import reviews_in_directory

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 extract_review_sentences.py reviews-dir/ sents.csv')
        print('Extracts review sentences from all files in the given directory and writes')
        print('them to sents.csv along with other metadata.')
    else:
        _, reviews_dir, sents_fname = sys.argv
        
        with open(sents_fname, 'w') as sents_file:
            sents_csv = csv.writer(sents_file)
            sents_csv.writerow(['rid', 'sent_index', 'tokens', 'overall',
                                'helpful'])
            for review in reviews_in_directory(reviews_dir, 0.1):
                sents = list(review.doc.sents)
                sents.insert(0, spacy_nlp(review.summary))
                for sent_index, sent in enumerate(review.doc.sents):
                    sents_csv.writerow([review.id, sent_index,
                            ' '.join(map(str, sent)), review.overall,
                            ' '.join(map(str, review.helpful))])
            
