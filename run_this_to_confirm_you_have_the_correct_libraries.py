#!/usr/bin/python
"""This module confirms that you have the right libraries and warns if things are missing"""

# Usage:
# $ python run_this_to_confirm_you_have_the_correct_libraries.py
# and it should tell you if everything appears to be installed or if you're
# either missing libraries or your libraries are of the wrong version

EXPECTED_PP_VERSION = "1.6.3"
EXPECTED_MATPLOTLIB_VERSION = "1.1.1rc"
EXPECTED_NUMPY_VERSION = "1.6.1"

libraries_missing_or_wrong_version = False

try:
    import multiprocessing
    nbr_cpus = multiprocessing.cpu_count()
    print "Multiprocessing reports that you have {} CPUs".format(nbr_cpus)
    if nbr_cpus == 1:
        print "Note that we expect 2 or more CPUs, you only have 1, you won't see any benefit from running the code in parallel if you only have 1 CPU"
    else:
        print "Since you have >1 CPU you will be able to observe speed-ups when we run tasks in parallel"

except ImportError as err:
    print "You are missing the multiprocessing module - this is serious. This code is designed for Python 2.7, multiprocessing should be an included module. I don't know how you can solve this."
    libraries_missing_or_wrong_version = True

try:
    import pp
    pp_version = pp.version
    if pp_version != EXPECTED_PP_VERSION:
        print "You don't have the expected version of the parallelpython module"
        print "We're expecting you to have {} and you have {}".format(EXPECTED_PP_VERSION, pp_version)
        print "If your version is newer then you are probably ok, if it is older then you probably should upgrade via http://www.parallelpython.com/content/view/18/32/"
        libraries_missing_or_wrong_version = True
except ImportError as err:
    print "You are missing 'pp', install it via: http://www.parallelpython.com/content/view/18/32/ or 'pip install pp'"
    libraries_missing_or_wrong_version = True

try:
    import numpy
    numpy_version = numpy.__version__
    if numpy_version != EXPECTED_NUMPY_VERSION:
        print "You don't have the expected version of numpy"
        print "We're expecting you to have {} and you have {}".format(EXPECTED_NUMPY_VERSION, numpy_version)
        print "If your version is newer or similar then you're probably ok, if it is much older then you should upgrade via: http://scipy.org/Download"
        libraries_missing_or_wrong_version = True
except ImportError as err:
    print "You are missing 'numpy', install it via: http://scipy.org/Download or 'pip install numpy'"
    libraries_missing_or_wrong_version = True

try:
    import matplotlib
    matplotlib_version = matplotlib.__version__
    if matplotlib_version != EXPECTED_MATPLOTLIB_VERSION:
        print "You have a different version {} of matplotlib than the {} that we expect".format(matplotlib_version, EXPECTED_MATPLOTLIB_VERSION)
        print "If your version is similar or newer (or at least better than 1.0.0) then you are probably ok"
        print "You can upgrade or check the latest version here: http://matplotlib.org/downloads.html"
        libraries_missing_or_wrong_version = True
except ImportError as err:
    print "You are missing 'matplotlib', install it via http://matplotlib.org/downloads.html or 'pip install matplotlib'"
    libraries_missing_or_wrong_version = True

if libraries_missing_or_wrong_version:
    print "NOTE you've been issued with some warnings or errors, you ought to fix these before running the code in this tutorial"
else:
    print "You have the All Clear, it looks like everything we need for this tutorial is installed."
