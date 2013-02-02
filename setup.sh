#!/bin/sh

tab="          ";

# ---------------------------------------------------------------------------

checkBasic ()
{
    # sudo must work without prompting for password!
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

    # DISCO_HOME must point to './usr/DISCO_HOME'
    discoHome=`cd \`dirname $0\` && pwd`/usr/DISCO_HOME;
    if [ "${DISCO_HOME}" != ${discoHome} ]; then
	echo "#";
	echo "# Error: 'DISCO_HOME' must be set to:";
	echo "          ${discoHome}";
	echo "#";
	exit 1;
    fi;
}

# ---------------------------------------------------------------------------

pkgBasic()
{
    echo "# Info: Installing required packages ...";
    (
	for pkg in              \
	    git                 \
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
	    sudo apt-get install  \
		-y ${pkg}         \
		>/dev/null 2>&1;
	    if [ $? != 0 ]; then 
		exit 1;
	    fi;
	done;                  

	for pkg in \
	    pillow \
            pp     \
            ; do 
	    (cd /dev/shm ; ls -1 | grep -i ${pkg} | xargs -n 1 sudo rm -rf) > /dev/null 2>&1;
	    echo "#${tab}${pkg}" ;
	    sudo pip install     \
		-b /dev/shm      \
		${pkg}           \
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
}

# ---------------------------------------------------------------------------

pkgDISCO ()
{
    ./usr/DISCO_HOME.setup.sh;
}

# ---------------------------------------------------------------------------

pkgDemo ()
{
    echo "# Info: Compiling demos ...";
    (cd ./2_MapReduceDisco/word_count_cloud/word_cloud; make) > /dev/null 2>&1;
    if [ $? != 0 ]; then
	echo "#";
	echo "# Error: Could not compile demos. Am quitting.";
	echo "#";
	exit 1;
    fi;
    
    exit 0;
}

# ---------------------------------------------------------------------------

checkBasic;
pkgBasic  ;
pkgDISCO  ;
pkgDemo   ;

# ---------------------------------------------------------------------------

