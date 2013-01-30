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

If you are *not* using the PyCon VirtualBox image that we provide for PyCon 2013, you will need to install the following dependencies.

If you *are* using the VirtualBox image that we provide then skip to the end for `run_this_to_confirm_you_have_the_correct_libraries.py and confirm that everything is configured as we expect.

    $ pip install -r requirements.txt  # install dependencies
    $ cd 2_MapReduceDisco/word_count_cloud/word_cloud
    $ python setup.py build_ext -i  # build word_cloud locally

Disco needs to be checked out of the github repository, use this specific check-in "f193331965e8aac459ff9a4115cef522e357098b" by doing:

    $ git clone git://github.com/discoproject/disco.git  # fetch current HEAD
    $ git checkout f193331965e8aac459ff9a4115cef522e357098b  # go back in time to the version that fits this tutorial
    Now read the DISCO_INSTALL_NOTES.txt in 2_MapReduceDisco and hope you get it working (we won't provide support if you can't)

Confirm that you have all the required libraries:

    $ python run_this_to_confirm_you_have_the_correct_libraries.py

