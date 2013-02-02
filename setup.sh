#!/bin/sh

tab="          ";

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
  for pkg in git                 \
             openssh-server      \
             expect              \
                                 \
             libblas-dev         \
  	     liblapack-dev       \
    	     gfortran            \
                                 \
  	     python-dev          \
	     python-pip          \
             python-dateutil     \
             python-numpy        \
             cython              \
             python-scipy        \
             python-sklearn      \
                                 \
             erlang-base         \
             erlang              \
             ; do                
     echo "#${tab}${pkg} " ;
     sudo apt-get install           \
            -y ${pkg}               \
            >/dev/null 2>&1;

     if [ $? != 0 ]; then 
        exit 1;
     fi;
  done;                  

  for pkg in pillow \
             pp     \
             ; do 
     (cd /dev/shm ; ls -1 | grep -i ${pkg} | xargs -n 1 sudo rm -rf) > /dev/null 2>&1;
     echo "#${tab}${pkg}" ;
     sudo pip install        \
            -b /dev/shm      \
               ${pkg}        \
            >  /dev/null 2>&1;
     stat=$?;

     (cd /dev/shm ; ls -1 | grep -i ${pkg} | xargs -n 1 sudo rm -rf) > /dev/null 2>&1;
     if [ ${stat} != 0 ]; then 
        exit 1;
     fi;
  done;

  exit 0;
);

if [ $? != 0 ]; then
   echo "#";
   echo "# Error: Could not install packages. Am quitting.";
   echo "#";
   exit 1;
fi;

echo "# Info: DISCO package";
(  
  mkdir -p ./usr                                               && \
  cd       ./usr                                               && \
  sudo rm -rf                                     ./DISCO_HOME && \
  echo "#${tab}Downloading ..."                                && \
  git clone git://github.com/discoproject/disco.git DISCO_HOME >/dev/null 2>&1 && \
  cd                                                DISCO_HOME && \
  git checkout f193331965e8aac459ff9a4115cef522e357098b        >/dev/null 2>&1 && \
  echo "#${tab}Compling ..."                                   && \
  make                                                         >/dev/null 2>&1 && \
  cd lib                                                       && \
  echo "#${tab}Installing ..."                                 && \
  sudo python ./setup.py install                               >/dev/null 2>&1 ;
);

if [ $? != 0 ]; then
   echo "#";
   echo "# Error: Could not install packages. Am quitting.";
   echo "#";
   exit 1;
fi;

exit 0;
