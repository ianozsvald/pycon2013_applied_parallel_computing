#!/usr/bin/python -Bu

from env import portID, \
                urlRel, \
                tmpRel;

def main(nworkers = 4):
    import os as py_os;

    print '    # Info: Enforcing assumptions ...';
    __assert    (nworkers);
    print '    # Info: About to terminate existing daemons ...';    
    terminate   ();
    print '    # Info: About to launch mongod daemon ...';
    __launch    (file = '/usr/bin/mongod',
                 args = ('--dbpath=/tmp',
                         '--noprealloc',
                         '--port=%(portID)d' % globals(),
                         ));
    print '    # Info: About to launch workers ...';
    for nworkers in range(0, nworkers):
        __launch(file = '/usr/bin/python',
                 args = ('%(parent)s/../../usr/hyperopt/scripts/hyperopt-mongo-worker' % dict(parent = py_os.path.dirname(__file__)),
                         '--mongo=localhost:22334/demoDB',
                         '--poll-interval=0.1',
                         ));

    return;

def __assert(nworkers):
    import commands as py_commands;

    if (nworkers <= 0):
        print '    # Error: invalid value for nworkers (%d)' % nworkers;
        exit(1);
    if (py_commands.getstatusoutput('sudo -n pwd')[0] != 0):
        print '    # Error: setup account so that \'sudo\' does not require password.';
        exit(1);

    return;
        
def terminate():
    """
    Kill any process that has '__PYCON2013_DEMO3_PROCESS__' defined in its environ;
    """
    import psutil   as py_psutil;
    import glob     as py_glob;
    import os       as py_os;
    import commands as py_commands;

    for proc in py_psutil.get_process_list():
        try:
            if (proc.name not in ('python', 'mongod')):
                continue;
            if (not filter((lambda x: 
                            (x.split('=')[0] == '__PYCON2013_DEMO3_PROCESS__')),
                           open('/proc/%(pid)s/environ' % dict(pid = proc.pid)).read().split('\x00'))):
                continue;
        except IOError,    e:
            continue;
        except ValueError, e:
            continue;
        except py_psutil.error.NoSuchProcess, e:
	    continue;
        print '    # Info: About to kill mongod (pid=%d)' % (proc.pid,);
        py_commands.getoutput('kill -2 %(pid)d' % dict(pid = proc.pid));

    return;

def __launch(file, args):
    """
    From the classic UNIX book by W. Richard Stevens.
    """
    import os  as py_os;
    import sys as py_sys;

    try:
        pid = py_os.fork();
        if (pid > 0):
            (pid_, stat_) = py_os.waitpid(pid, 0);
            if ((pid != pid_) or 
                (not py_os.WIFEXITED  (stat_))):
                print 'status ->', py_os.WEXITSTATUS(stat_);
                raise OSError("**");
            return;
    except OSError, e:
        print '    # Error: Cannot launch mongod as a daemon. Am quitting.';
        exit(1);

    # Point stdin/out/err to '/dev/null'
    try:
        py_os.environ['__PYCON2013_DEMO3_PROCESS__'] = "1"; # Tag all processes hence forth to enable cleanup.
        py_os.chdir ('/dev/shm');
        py_os.setsid();
        py_os.umask (0);
        nopRD = open("/dev/null", "r"); 
        nopWR = open("/dev/null", "a+");
        py_os.dup2(nopRD.fileno(),         py_sys.stdin .fileno());
        py_os.dup2(nopWR.fileno(),         py_sys.stdout.fileno());
        py_os.dup2(py_sys.stdout.fileno(), py_sys.stderr.fileno());
        for fd in range(3, 1024):
            try:
                py_os.close(fd);
            except:
                pass;
    except Exception, e:
        exit(1);

    # Finally, fork one more time.
    try:
        pid = py_os.fork();
        if (pid > 0):
            exit(0);
    except OSError, e:
        exit(1);

    py_os.execl(file, file, *args);
    exit       (0);
