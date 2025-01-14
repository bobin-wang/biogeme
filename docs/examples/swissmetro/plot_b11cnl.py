"""

Cross-nested logit
==================

 Example of a cross-nested logit model with two nests:

 - one with existing alternatives (car and train),
 - one with public transportation alternatives (train and Swissmetro)

:author: Michel Bierlaire, EPFL
:date: Sun Apr  9 18:06:44 2023

"""

import biogeme.biogeme_logging as blog
import biogeme.biogeme as bio
from biogeme import models
from biogeme.expressions import Beta
from biogeme.nests import OneNestForCrossNestedLogit, NestsForCrossNestedLogit

# %%
# See the data processing script: :ref:`swissmetro_data`.
from swissmetro_data import (
    database,
    CHOICE,
    SM_AV,
    CAR_AV_SP,
    TRAIN_AV_SP,
    TRAIN_TT_SCALED,
    TRAIN_COST_SCALED,
    SM_TT_SCALED,
    SM_COST_SCALED,
    CAR_TT_SCALED,
    CAR_CO_SCALED,
)

logger = blog.get_screen_logger(level=blog.INFO)
logger.info('Example b11cnl.py')

# %%
# Parameters to be estimated.
ASC_CAR = Beta('ASC_CAR', 0, None, None, 0)
ASC_TRAIN = Beta('ASC_TRAIN', 0, None, None, 0)
ASC_SM = Beta('ASC_SM', 0, None, None, 1)
B_TIME = Beta('B_TIME', 0, None, None, 0)
B_COST = Beta('B_COST', 0, None, None, 0)

# %% Nest parameters.
MU_EXISTING = Beta('MU_EXISTING', 1, 1, 10, 0)
MU_PUBLIC = Beta('MU_PUBLIC', 1, 1, 10, 0)

# %%
# Nest membership parameters.
ALPHA_EXISTING = Beta('ALPHA_EXISTING', 0.5, 0, 1, 0)
ALPHA_PUBLIC = 1 - ALPHA_EXISTING

# %%
# Definition of the utility functions
V1 = ASC_TRAIN + B_TIME * TRAIN_TT_SCALED + B_COST * TRAIN_COST_SCALED
V2 = ASC_SM + B_TIME * SM_TT_SCALED + B_COST * SM_COST_SCALED
V3 = ASC_CAR + B_TIME * CAR_TT_SCALED + B_COST * CAR_CO_SCALED

# %%
# Associate utility functions with the numbering of alternatives
V = {1: V1, 2: V2, 3: V3}

# %%
# Associate the availability conditions with the alternatives
av = {1: TRAIN_AV_SP, 2: SM_AV, 3: CAR_AV_SP}

# %%
# Definition of nests.

nest_existing = OneNestForCrossNestedLogit(
    nest_param=MU_EXISTING,
    dict_of_alpha={1: ALPHA_EXISTING, 2: 0.0, 3: 1.0},
    name='existing',
)

nest_public = OneNestForCrossNestedLogit(
    nest_param=MU_PUBLIC, dict_of_alpha={1: ALPHA_PUBLIC, 2: 1.0, 3: 0.0}, name='public'
)

nests = NestsForCrossNestedLogit(
    choice_set=[1, 2, 3], tuple_of_nests=(nest_existing, nest_public)
)

# %%
# The choice model is a cross-nested logit, with availability conditions.
logprob = models.logcnl(V, av, nests, CHOICE)

# %%
# Create the Biogeme object
the_biogeme = bio.BIOGEME(database, logprob)
the_biogeme.modelName = 'b11cnl'

# %%
# Estimate the parameters.
results = the_biogeme.estimate()

# %%
print(results.short_summary())

# %%
pandas_results = results.get_estimated_parameters()
pandas_results
