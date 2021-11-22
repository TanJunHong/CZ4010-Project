import math
import statistics

import statsmodels.sandbox.stats.runs


def get_z(lst, lst_median):
    runs, n1, n2 = 0, 0, 0

    # Checking for start of new run
    for k in range(len(lst)):
        # no. of runs
        if (lst[k] >= lst_median > lst[k - 1]) or (lst[k] < lst_median <= lst[k - 1]):
            runs += 1

        # no. of positive values
        if lst[k] >= lst_median:
            n1 += 1

        # no. of negative values
        else:
            n2 += 1

    runs_exp = ((2 * n1 * n2) / (n1 + n2)) + 1
    std_dev = math.sqrt((2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / (((n1 + n2) ** 2) * (n1 + n2 - 1)))

    z = (runs - runs_exp) / std_dev

    return z


def run_test(lst):
    print("z-statistic = ", abs(get_z(lst=lst, lst_median=statistics.median(data=lst))))
    print(statsmodels.sandbox.stats.runs.runstest_1samp(x=lst, correction=False))
