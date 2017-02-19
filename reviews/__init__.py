
import spacy
import os

from nltk.parse.stanford import StanfordParser

# Load spaCy
spacy_nlp = spacy.load('en')

# Load Stanford parser
os.environ['CLASSPATH'] = 'data/models/stanford-parser-full-2016-10-31:data/models/stanford-postagger-full-2016-10-31:data/models/stanford-ner-2016-10-31'
os.environ['STANFORD_MODELS'] = 'data/models/stanford-postagger-full-2016-10-31/models:data/models/stanford-ner-2016-10-31/classifiers:data/models/stanford-parser-full-2016-10-31'
stanford_parser = StanfordParser(model_path='edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
