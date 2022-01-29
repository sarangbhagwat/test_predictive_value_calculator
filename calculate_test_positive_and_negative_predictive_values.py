# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 17:24:30 2022

@author: sarangbhagwat
"""

import numpy as np
from matplotlib import pyplot as plt
from pandas import DataFrame

def get_ppv_and_npv(
    incidence_rate = 0.132, # actual prevalence of infection as decimal # default value is India's Jan 27 2022 COVID-19 positivity rate from https://ourworldindata.org/explorers/coronavirus-data-explorer?zoomToSelection=true&time=2020-03-01..latest&uniformYAxis=0&pickerSort=asc&pickerMetric=location&Metric=Cases%2C+tests%2C+positive+and+reproduction+rate&Interval=7-day+rolling+average&Relative+to+Population=true&Color+by+test+positivity=false&country=USA~IND
    false_positive_rate = 1. - 0.989, # likelihood of a healthy person testing positive; 1 - specificity # default value from https://www.idsociety.org/covid-19-real-time-learning-network/diagnostics/RT-pcr-testing/
    false_negative_rate = 1. - 0.842, # likelihood of an infected person testing negative; 1 - sensitivity # default value from https://www.idsociety.org/covid-19-real-time-learning-network/diagnostics/RT-pcr-testing/
    sample_size = 1000., # arbitrary; use higher value if any of the above rates are very small
    ):
    
    actual_infected = sample_size * incidence_rate
    actual_healthy = sample_size - actual_infected
    
    false_negatives = actual_infected * false_negative_rate
    false_positives = actual_healthy * false_positive_rate
    
    true_negatives = actual_healthy - false_positives
    true_positives = actual_infected - false_negatives
    
    return true_positives/(true_positives+false_positives),\
            true_negatives/(true_negatives+false_negatives) 
# returns:
# positive predictive value; likelihood of being infected given a positive test result
# negative predictive value; likelihood of being healthy given a negative test result

#%% Plot 
incidence_rates_to_plot_across = np.linspace(0.01, 0.50, 50)
ppvs_and_npvs = [get_ppv_and_npv(x) for x in incidence_rates_to_plot_across]
# plt.plot(100*incidence_rates_to_plot_across, [100.*x[0] for x in ppvs_and_npvs], [100.*x[1] for x in ppvs_and_npvs])
ppvs_and_npvs_dict = {'Positive': [100*i[0] for i in ppvs_and_npvs], 'Negative': [100*i[1] for i in ppvs_and_npvs]}
ppvs_and_npvs_df = DataFrame(ppvs_and_npvs_dict, 100*incidence_rates_to_plot_across)
fig, ax = plt.subplots()
ax = ppvs_and_npvs_df.plot(xlabel='Incidence rate [%]', ylabel='Test predictive value [%]',
                 )
ax.set_ylim(ymin = 0)
ax.set_xlim(xmin = 0)
# ax.ticklabel_format(style='decimal', scilimits=(0,0), axis='y')
# plt.legend(loc='lower center', fontsize=9, ncol=1, bbox_to_anchor=(1.24, 0.32))
plt.show()
