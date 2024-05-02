import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

tips = pd.read_csv('../data/tips_success.csv')

tips_night = tips[tips['version'] == 'night']
tips_day = tips[tips['version'] == 'day']

n_night = len(tips_night)
n_day = len(tips_day)
successes = [tips_night.conversion.sum(), tips_day.conversion.sum()]
nobs = [n_night, n_day]

z_stat, pval = proportions_ztest(successes, nobs=nobs)

print(f'conversion rate for day shift: {tips_day.conversion.sum()/n_day}')
print(f'conversion rate for night shift: {tips_night.conversion.sum()/n_night}')
print(f'z statistic: {z_stat:.2f}')
print(f'p-value: {pval:.3f}')



# tips = pd.read_csv('../data/tips_too_small_diff.csv')

# tips_night = tips[tips['version'] == 'night']
# tips_day = tips[tips['version'] == 'day']

# n_night = len(tips_night)
# n_day = len(tips_day)
# successes = [tips_night.conversion.sum(), tips_day.conversion.sum()]
# nobs = [n_night, n_day]

# z_stat, pval = proportions_ztest(successes, nobs=nobs)

# print(f'conversion rate for day shift: {tips_day.conversion.sum()/n_day}')
# print(f'conversion rate for night shift: {tips_night.conversion.sum()/n_night}')
# print(f'z statistic: {z_stat:.2f}')
# print(f'p-value: {pval:.3f}')


# import scipy.stats as sps

# tips = pd.read_csv('../data/tips_means.csv')

# tips_night = tips['night']
# tips_day = tips['day']

# test_statistic, pvalue = sps.ttest_ind(tips_day, tips_night)
# print(f'average tips for day shift: {tips_day.mean()}')
# print(f'average tips for night shift {tips_night.mean()}')
# print (test_statistic, pvalue)