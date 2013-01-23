PyCon 2013 Applied Parallel Computing
=====================================

Applied Parallel Computing tutorial material for PyCon 2013 (Minesh Amin, Ian Ozsvald)
https://us.pycon.org/2013/schedule/presentation/27/

This tutorial covers:
 * Moving a single threaded CPU bound process (Mandelbrot set) to a multi core and multi machine solution, with a review of other queue-based approaches
 * Map/Reduce (disco) on a NLP computing problem on a Tweet set with visualisations (word clouds)
 * Parallel hyperparameter optimization



Installation:
------------

    $ pip install -r requirements.txt  # install dependencies
    $ cd 2_MapReduceDisco/word_count_cloud/word_cloud
    $ python setup.py build_ext -i  # build word_cloud locally
