import os

from mlearning.config import PROJECT_DIR

TEST_DIR = os.path.join(PROJECT_DIR, 'tests')
DATA_DIR = os.path.join(TEST_DIR, 'data')
ANNOTATIONS_DIR = os.path.join(DATA_DIR, 'annotations')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')
