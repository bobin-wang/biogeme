import os
import unittest
import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
from biogeme import models
import biogeme.optimization as opt
from biogeme.expressions import Beta, DefineVariable

myPath = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(f'{myPath}/swissmetro.dat', sep='\t')
database = db.Database('swissmetro', df)

# The Pandas data structure is available as database.data. Use all the
# Pandas functions to invesigate the database
# print(database.data.describe())

globals().update(database.variables)

# Here we use the 'biogeme' way for backward compatibility
exclude = ((PURPOSE != 1) * (PURPOSE != 3) + (CHOICE == 0)) > 0
database.remove(exclude)


ASC_CAR = Beta('ASC_CAR', 0, None, None, 0)
ASC_TRAIN = Beta('ASC_TRAIN', 0, None, None, 0)
ASC_SM = Beta('ASC_SM', 0, None, None, 1)
B_TIME = Beta('B_TIME', 0, None, None, 0)
B_COST = Beta('B_COST', 0, None, None, 0)

SM_COST = SM_CO * (GA == 0)
TRAIN_COST = TRAIN_CO * (GA == 0)

CAR_AV_SP = DefineVariable('CAR_AV_SP', CAR_AV * (SP != 0), database)
TRAIN_AV_SP = DefineVariable('TRAIN_AV_SP', TRAIN_AV * (SP != 0), database)

TRAIN_TT_SCALED = DefineVariable('TRAIN_TT_SCALED', TRAIN_TT / 100.0, database)
TRAIN_COST_SCALED = DefineVariable(
    'TRAIN_COST_SCALED', TRAIN_COST / 100, database
)
SM_TT_SCALED = DefineVariable('SM_TT_SCALED', SM_TT / 100.0, database)
SM_COST_SCALED = DefineVariable('SM_COST_SCALED', SM_COST / 100, database)
CAR_TT_SCALED = DefineVariable('CAR_TT_SCALED', CAR_TT / 100, database)
CAR_CO_SCALED = DefineVariable('CAR_CO_SCALED', CAR_CO / 100, database)

V1 = ASC_TRAIN + B_TIME * TRAIN_TT_SCALED + B_COST * TRAIN_COST_SCALED
V2 = ASC_SM + B_TIME * SM_TT_SCALED + B_COST * SM_COST_SCALED
V3 = ASC_CAR + B_TIME * CAR_TT_SCALED + B_COST * CAR_CO_SCALED

# Associate utility functions with the numbering of alternatives
V = {1: V1, 2: V2, 3: V3}


# Associate the availability conditions with the alternatives

av = {1: TRAIN_AV_SP, 2: SM_AV, 3: CAR_AV_SP}


class test_01(unittest.TestCase):
    def testEstimationScipy(self):
        logprob = models.loglogit(V, av, CHOICE)
        biogeme = bio.BIOGEME(database, logprob, seed=10, numberOfThreads=1)
        biogeme.saveIterations = False
        biogeme.generateHtml = False
        biogeme.generatePickle = False
        biogeme.modelName = 'test_01'
        results = biogeme.estimate(bootstrap=10, algorithm=opt.scipy)
        self.assertAlmostEqual(results.data.logLike, -5331.252, 2)
        self.assertAlmostEqual(
            results.data.betas[0].bootstrap_stdErr, 0.04773096176427237, 2
        )

    def testEstimationLineSearch(self):
        logprob = models.loglogit(V, av, CHOICE)
        biogeme = bio.BIOGEME(database, logprob, seed=10, numberOfThreads=1)
        biogeme.saveIterations = False
        biogeme.generateHtml = False
        biogeme.generatePickle = False
        biogeme.modelName = 'test_01'
        results = biogeme.estimate(
            bootstrap=10, algorithm=opt.newtonLineSearchForBiogeme
        )
        self.assertAlmostEqual(results.data.logLike, -5331.252, 2)
        self.assertAlmostEqual(
            results.data.betas[0].bootstrap_stdErr, 0.04773096176427237, 2
        )

    def testEstimationTrustRegion(self):
        logprob = models.loglogit(V, av, CHOICE)
        biogeme = bio.BIOGEME(database, logprob, seed=10, numberOfThreads=1)
        biogeme.saveIterations = False
        biogeme.generateHtml = False
        biogeme.generatePickle = False
        biogeme.modelName = 'test_01'
        results = biogeme.estimate(
            bootstrap=10, algorithm=opt.newtonTrustRegionForBiogeme
        )
        self.assertAlmostEqual(results.data.logLike, -5331.252, 2)
        self.assertAlmostEqual(
            results.data.betas[0].bootstrap_stdErr, 0.04773096176427237, 2
        )


if __name__ == '__main__':
    unittest.main()
