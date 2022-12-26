import os


BASEPATH = os.path.abspath(os.environ.get('BASEPATH', '/src/data'))
STATICPATH = os.path.abspath(os.environ.get('STATICPATH', os.path.join(os.path.dirname(__file__), '..', 'static')))


# set some filenames
METADATA_FILE_NAME = 'metadata.csv'