import numpy as np
import statsmodels.api as sm

# https://stackoverflow.com/questions/21844024/weighted-percentile-using-numpy
def weighted_quantile(values, quantiles, sample_weight=None):
    values = np.array(values)
    quantiles = np.array(quantiles)
    if sample_weight is None:
        sample_weight = np.ones(len(values))
    sample_weight = np.array(sample_weight)
    sorter = np.argsort(values)
    values = values[sorter]
    sample_weight = sample_weight[sorter]
    weighted_quantiles = np.cumsum(sample_weight) - 0.5 * sample_weight
    weighted_quantiles /= np.sum(sample_weight)
    return np.interp(quantiles, weighted_quantiles, values)


# https://stackoverflow.com/questions/1066758/find-length-of-sequences-of-identical-values-in-a-numpy-array-run-length-encodi
def rle(inarray):
    """ run length encoding. Partial credit to R rle function. 
        Multi datatype arrays catered for including non Numpy
        returns: tuple (runlengths, startpositions, values) """
    ia = np.asarray(inarray)                # force numpy
    n = len(ia)
    if n == 0: 
        return (None, None, None)
    else:
        y = ia[1:] != ia[:-1]               # pairwise unequal (string safe)
        i = np.append(np.where(y), n - 1)   # must include last element posi
        z = np.diff(np.append(-1, i))       # run lengths
        p = np.cumsum(np.append(0, z))[:-1] # positions
        return(z, p, ia[i])

def hw_stats(ens_data, thresh , greater=True):
    if greater:
        hot = (ens_data > thresh).astype(int)
    else:
        hot = (ens_data < thresh).astype(int)

    hw_len = np.array([], 'int')
    hw_start = np.array([], 'int')
    for sim in hot.sim.values:
        l,start,v = rle(hot.loc[sim].values)
        hw_len = np.append(hw_len, l[v == 1])
        hw_start = np.append(hw_start, start[v == 1])
    return hw_len,hw_start

def persistence_stats(condition_data):
    hw_len = {}
    hw_start = {}
    for sim in condition_data.sim.values:
        start,l,v = rle(condition_data.loc[sim].values)
        hw_len[sim] = l[v == 1]
        hw_start[sim] = start[v == 1]
    return hw_len,hw_start