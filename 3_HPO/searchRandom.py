from   math              import sin;
from   hyperopt          import fmin, tpe, hp;
from   hyperopt.mongoexp import MongoTrials;
from   util.env          import portID, \
                                urlRel;
import util.spawn as            spawn;

spawn.main(nworkers = 4);

trials = MongoTrials('mongo://localhost:%(portID)d%(urlRel)s' % vars(),
                     exp_key   = 'exp1');
best   = fmin       (sin, 
                     hp.uniform('x', -3, 3), 
                     trials    = trials, 
                     algo      = tpe.suggest, 
                     max_evals = 30)

print best;

spawn.terminate();


