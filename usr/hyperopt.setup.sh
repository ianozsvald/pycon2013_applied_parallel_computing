#!/bin/sh

tab="          ";

echo "# Info: hyperopt package";
(  
  cd `dirname $0`                                             && \
  sudo rm -rf                                    ./hyperopt   && \
  echo "#${tab}Downloading ..."                               && \
  git clone git://github.com/jaberg/hyperopt.git ./hyperopt >/dev/null 2>&1 && \
  cd                                             ./hyperopt   && \
  git checkout c0ea11a8bbad13020159abc48ebba6e58b143cd8     >/dev/null 2>&1 && \
  echo "#${tab}Installing ..."                                && \
  sudo python ./setup.py install                            >/dev/null 2>&1 && \
  sudo rm -rf ./build;
);

if [ $? != 0 ]; then
   echo "#";
   echo "# Error: Could not install packages. Am quitting.";
   echo "#";
   exit 1;
fi;

exit 0;
