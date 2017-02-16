"""Configure the python path to provide access to the reviews package."""
import sys
from os.path import dirname, realpath, sep, pardir
    
sys.path.append(sep.join([dirname(realpath(__file__)), pardir]))

# Configure logging as well while we're at it
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)
