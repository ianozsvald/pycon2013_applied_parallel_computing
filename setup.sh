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
(
  tab="          ";
  for pkg in git                 \
             libblas-dev         \
  	     liblapack-dev       \
    	     gfortran            \
  	     python-dev          \
	     python-pip          \
             python-dateutil     \
             python-numpy        \
             cython              \
             python-scipy        \
             python-sklearn      \
             ; do                
     echo "#${tab}${pkg} " ;
     sudo rm -rf /dev/shm/[Pp]illow* \
                                    \
                                 && \
                                    \
     sudo apt-get install           \
            -y ${pkg}               \
            >/dev/null 2>&1;

     if [ $? != 0 ]; then 
        exit 1;
     fi;
  done;                  

  echo "#${tab}pillow" ;
  sudo pip install       \
        -d /dev/shm      \
           pillow        \
        >  /dev/null 2>&1;

  if [ $? != 0 ]; then 
     exit 1;
  fi;
);

if [ $? != 0 ]; then
   echo "#";
   echo "# Error: Could not install packages. Am quitting.";
   echo "#";
   exit 1;
fi;

exit 0;
