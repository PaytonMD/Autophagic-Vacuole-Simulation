# -*- coding: utf-8 -*-
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.gofplots import qqplot_2samples

#Test 1:
'''statsA = [500, 500, 325, 875, 1000, 765, 425, 320] #Random Variables
statsB = [465, 441, 1353, 489, 1281, 221, 437, 1481] #From sliceDefault data


#statsmodels.graphics.gofplots.qqplot_2samples(statsA, statsB, xlabel=None, ylabel=None)
plotA = sm.ProbPlot(statsA)
plotB = sm.ProbPlot(statsB)
qqplot_2samples(plotA,plotB)

plt.show()'''

#Test 2:
'''x = np.random.normal(loc=8.5, scale=2.5, size=37)
y = np.random.normal(loc=8.0, scale=3.0, size=37)
pp_x = sm.ProbPlot(x)
pp_y = sm.ProbPlot(y)
qqplot_2samples(pp_x, pp_y)
plt.show()'''

#Plots will appear inthe 'Plot' tab.


#Test 3:
    
statsA = [500, 500, 325, 875, 1000, 765, 425, 320] #Random Variables
statsB = [465, 441, 1353, 489, 1281, 221, 437, 1481] #From sliceDefault data
aArray = np.array(statsA)
bArray = np.array(statsB)

#statsmodels.graphics.gofplots.qqplot_2samples(statsA, statsB, xlabel=None, ylabel=None)
plotA = sm.ProbPlot(aArray)
plotB = sm.ProbPlot(bArray)
qqplot_2samples(plotA,plotB)

plt.show()