
# coding: utf-8

# In[1]:

import datetime
import pandas as pd
import numpy as np
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# In[2]:

import utils
import analytics
import portfolio
import backtester
import models
# import refresh
# refresh.run()


# In[3]:

data = analytics.cleaned_dataset()


# In[4]:

testModels = [('StrategyBottomTenofTopOneHundredMarketCap', 
                   models.StrategyBottomTenofTopOneHundredMarketCap),
              ('StrategyBottomTenofTopOneHundredMarketCapUnderTwentyCents', 
                   models.StrategyBottomTenofTopOneHundredMarketCapUnderTwentyCents), 
              ('StrategyBottomTenofTopOneHundredMarketCapUnderTwoMil', 
                   models.StrategyBottomTenofTopOneHundredMarketCapUnderTwoMil),
              ('StrategyTopMarketCap', 
                   models.StrategyTopMarketCap),
              ('StrategyTopTenofTopOneHundredMarketCapUnderTwentyCents', 
                   models.StrategyTopTenofTopOneHundredMarketCapUnderTwentyCents)]

for name, mdl in testModels:
    model = mdl(data)
    startDate = datetime.date(2017, 1, 1)
    endDate = datetime.date(2017, 12, 22)
    initialCash = 100

    print ("\nTesting model {}".format(name))
    tester = backtester.Backtester(data, model, startDate, endDate, (1, "m"), initialCash)
    tester.run(verbose=False)


# In[ ]:

model = models.StrategyTopMarketCap(data)

startDate = datetime.date(2017, 1, 1)
endDate = datetime.date(2017, 12, 22)
initialCash = 100

tester = backtester.Backtester(data, model, startDate, endDate, (1, "m"), initialCash)
tester.run(verbose=False)

