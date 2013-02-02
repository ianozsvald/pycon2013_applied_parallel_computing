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

checkSSH ()
{
    (
	/usr/bin/expect --<<EOF
             spawn ssh localhost pwd;
             expect {
               "Are you sure you want to continue connecting (yes/no)? " {
                 puts "About to generate key ...";
               }
               "localhost's password: " {
                 puts "About to generate key ...";
               }
               eof {
                 exit 0;
               }
             }
             spawn ssh-keygen -t rsa;
             expect {
               "Enter file in which to save the key (/home/*/.ssh/id_rsa): " {
                 send "\n" ;
                 exp_continue;
               }
               "Enter passphrase (empty for no passphrase): " {
                 send "\n" ;
                 exp_continue;
               }
               "Enter same passphrase again: " {
                 send "\n" ;
                 exp_continue;
               }
               "Overwrite (y/n)? " {
                 send "y\n" ;
                 exp_continue;
               }
               eof {
                 system ssh-add;
                 system cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys;
               }
             }
             system ls -la ~/.ssh;
             spawn ssh localhost pwd;
             expect {
               "Are you sure you want to continue connecting (yes/no)? " {
                 send "yes\n" ;
                 exp_continue;
               }
               eof {
                 exit 0;
               }
             }
             exit 1;
EOF
    ) > /dev/null 2>&1;

    if [ $? != 0 ]; then
	echo "#";
	echo "# Error: Seems like ssh requires password. Am quitting ...";
	echo "#";
	exit 1;
    fi;
}

# ---------------------------------------------------------------------------

pkgBasic()
{
    echo "# Info: Installing basic packages ...";
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
            python-psutil       \
            python-dateutil     \
            python-numpy        \
            python-matplotlib   \
            cython              \
            python-scipy        \
            python-sklearn      \
            \
            erlang-base         \
            erlang              \
            \
            mongodb             \
            redis-server        \
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
            hotqueue \
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

pkgRequired ()
{
    ./usr/DISCO_HOME.setup.sh;
    ./usr/hyperopt.setup.sh;
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

checkBasic  ;
pkgBasic    ;
checkSSH    ; # Must be after 'expect' is installed (!)
pkgRequired ;
pkgDemo     ;

# ---------------------------------------------------------------------------

