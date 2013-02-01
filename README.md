PyCon 2013 Applied Parallel Computing
=====================================

Applied Parallel Computing tutorial material for PyCon 2013 (Minesh B. Amin, Ian Ozsvald)
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

Building the world-cloud viewer (from https://github.com/amueller/word_cloud/ - thanks Andreas):

    $ cd 2_MapReduceDisco/word_count_cloud/word_cloud
    $ python setup.py build_ext -i  # build word_cloud locally
    $ mv word_cloud/query_integral_image.so .  # not sure why it is put into word_cloud, it needs to be in . to be visible
    $ python wordcloud.py  # test that the wordcloud library runs, it should make a small PIL image based on constitution.txt

Disco needs to be checked out of the github repository, use this specific check-in "f193331965e8aac459ff9a4115cef522e357098b" by doing:

    $ git clone git://github.com/discoproject/disco.git  # fetch current HEAD
    $ git checkout f193331965e8aac459ff9a4115cef522e357098b  # go back in time to the version that fits this tutorial

DISCO_HOME should have been configured if you followed DISCO_INSTALL_NOTES.txt, you will have done something like:

    $ export DISCO_HOME=~/workspace/DISCO_HOME  # where ~/workspace/DISCO_HOME is the git directory you checked out

DISCO has some binaries that are convenient to access from the command line, adding the DISCO bin directory to your search path is easiest e.g.

    $ export PATH=$PATH:$DISCO_HOME/bin  # putting this in ~/.bashrc would be better

You can test that DISCO is setup correctly by running:

    $ discocli.py client_version  # should report "0.4.4" 

Now read the DISCO_INSTALL_NOTES.txt in 2_MapReduceDisco and hope you get it working (we won't provide support if you can't).

Confirm that you have all the required libraries:
=======
Finally, confirm that you have all the required libraries:

    $ python run_this_to_confirm_you_have_the_correct_libraries.py

