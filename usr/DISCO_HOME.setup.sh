#!/bin/sh

tab="          ";

echo "# Info: DISCO package";
(  
  cd `dirname $0`                                              && \
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
