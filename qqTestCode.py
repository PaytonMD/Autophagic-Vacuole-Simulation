# -*- coding: utf-8 -*-
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
from statsmodel.graphics.gofplots import qqplot_2samples

statsA = [500, 500, 325, 875, 1000, 765, 425, 320] #Random Variables
statsB = [465, 441, 1353, 489, 1281, 221, 437, 1481] #From sliceDefault data


#statsmodels.graphics.gofplots.qqplot_2samples(statsA, statsB, xlabel=None, ylabel=None)
plotA = sm.ProbPlot(statsA)
plotB = sm.ProbPlot(statsB)
qqplot_2samples(plotA,plotB)

plt.show()