from math              import sin;
from hyperopt          import fmin, tpe, hp;
from hyperopt.mongoexp import MongoTrials;
from env               import portID, \
                              urlRel;

import myMongod;

myMongod.main(nworkers = 4);

trials = MongoTrials('mongo://localhost:%(portID)d%(urlRel)s' % vars(),
                     exp_key   = 'exp1');
best   = fmin       (sin, 
                     hp.uniform('x', -3, 3), 
                     trials    = trials, 
                     algo      = tpe.suggest, 
                     max_evals = 30)

print best;

myMongod.terminate();


