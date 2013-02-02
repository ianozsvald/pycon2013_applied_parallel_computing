#!/bin/sh

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

exit 0;
