#!/bin/sh

sudo -n pwd > /dev/null 2>&1;
if [ $? != 0 ]; then
   echo "#";
   echo "# Error: Seems like 'sudo' is setup to prompt for";
   echo "#        password. Please augment /etc/sudoers by";
   echo "#        including the following line";
   echo "          ${HOME} ALL=(ALL) NOPASSWD: ALL";
   echo "#";
   exit 1;
fi;

echo "# Info: Installing required packages ...";
sudo apt-get install -y     \
        libblas-dev         \
	liblapack-dev       \
	gfortran            \
	python-dev          \
	python-pip          \
                            \
        &&                  \
                            \
sudo pip install            \
        -b /dev/shm         \
        -r requirements.txt \
                            \
        &&                  \
                            \
sudo apt-get install -y     \
	python-scipy        \
                            \
        > /dev/null 2>&1;
	;

if [ $? != 0 ]; then
   echo "#";
   echo "# Error: Could not install packages. Am quitting.";
   echo "#";
   exit 1;
fi;

exit 0;
