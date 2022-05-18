import os
from .__version__ import __version__

# set input variables
BASEPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dev'))
INPUT_DIR = os.environ.get('INPUT_DIR', os.path.join(BASEPATH, 'input_dir'))
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', os.path.join(BASEPATH, 'output_dir'))
EZG_DIR = os.environ.get('EZG_DIR', os.path.join(BASEPATH, 'ezgs'))
