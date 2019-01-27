# Learning

Repo for storing Machine Learning utilities, helper code, etc...

Stuff that might live in here would be for manipulating images, working with datasets, like [COCO Dataset](http://cocodataset.org)

## Installation

```
pip install -r requirements.txt
```

To use one's own data, see the [example.ipynb](https://github.com/aaronlelevier/mlearning/blob/master/example.ipynb) and the instructions there

## Contents

The main contents so far are `coco.py`'s `Annotation` class that converts [labelme](https://github.com/wkentaro/labelme) annotations to [COCO Dataset 2014](http://cocodataset.org/#home) annotations.

### Example

There is an example Jupyter Notebook using one's own data converted from `labelme` style annotations to COCO annotations then being displayed here: [example.ipynb](https://github.com/aaronlelevier/mlearning/blob/master/example.ipynb)

## Tests

To run the test suite, run these commands:

```
pip install pytest

# from the top level project dir
py.test
```

## Licence

MIT
