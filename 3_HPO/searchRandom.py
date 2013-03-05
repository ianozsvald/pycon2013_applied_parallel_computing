from   math              import sin;
from   hyperopt          import fmin, tpe, hp, Trials;
from   hyperopt.mongoexp import MongoTrials;
from   util.env          import portID, \
                                urlRel;
import util.spawn as            spawn;

# ----------------------------------------------------------------------

scan = [];

def f(x):
    global scan;

    rval = sin(x);
    scan.append((x, rval));

    return rval;

best   = fmin       (fn        = f,
                     space     = hp.uniform('x', -3, 3), 
                     trials    = Trials(), 
                     algo      = tpe.suggest, 
                     max_evals = 60);
print 'min(x^2+0.25) for x in [-3, 3] =>', best;
import matplotlib.pyplot as py_plt;
import time              as py_time;

py_plt.ion();
f = py_plt.figure();
py_plt.xlim([-3.5, +3.5]);
py_plt.ylim([-1.5, +1.5]);
py_plt.draw();
for i in range(len(scan)): 
    py_plt.plot(scan[i][0], scan[i][1],
                marker = 'o', 
                color  = 'r',
                ls     = '');
    py_plt.show();
    py_plt.draw();
    py_time.sleep(0.01);

# ----------------------------------------------------------------------

spawn.main(nworkers = 2);
trials = MongoTrials('mongo://localhost:%(portID)d%(urlRel)s' % vars(),
                     exp_key   = 'exp2');
best   = fmin       (fn        = sin,
                     space     = hp.uniform('x', -3, 3), 
                     trials    = trials, 
                     algo      = tpe.suggest, 
                     max_evals = 60)
print 'min(sin(x))   for x in [-3, 3] =>', best;
spawn.terminate();

# ----------------------------------------------------------------------



