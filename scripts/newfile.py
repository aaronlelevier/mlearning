"""
Takes a file path and generates two files, a prod file and a test file

Example:

    $ python scripts/newfile.py -p mlearning/utils.py

    Two files generated are:
        - mlearning/utils.py
        - tests/test_utils.py
"""
import argparse
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="relative path for new file")
args = parser.parse_args()


def main():
    # write prod file
    with open(os.path.join(PROJECT_DIR, args.path), 'w'): pass

    # write test file
    filename = os.path.basename(args.path)
    with open(os.path.join(PROJECT_DIR, f'tests/test_{filename}'), 'w'): pass


if __name__ == '__main__':
    main()
