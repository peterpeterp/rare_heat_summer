import numpy as np
import xarray as xr

# general functions
def weighted_probability(
        tas, 
        weight, 
        threshold
        ):
    return float(((tas >= threshold) * weight).sum() / weight.sum())

def weighted_expected_value(
        tas, 
        weight, 
        threshold,
        x,
        ):
    return ((tas >= threshold) * x * weight).sum('sim') / ((tas >= threshold) * weight).sum('sim')

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

def weighted_expected_quantile(
        tas, 
        weight, 
        threshold,
        x,
        quantiles,
        ):
    weight[tas < threshold] = 0
    l = []
    for t in x.time.values:
        l.append( weighted_quantile(x.loc[:,t], quantiles, weight) )
    return xr.DataArray(np.array(l), dims=['time','quantile'], coords=dict(time=x.time, quantile=quantiles))


# REA ensemble
def adjust_weights(
        tas, 
        weight, 
        adjust_value, 
        reference_ensemble
        ):
    p_ref = float(weighted_probability(reference_ensemble['data']['tas_anom'].mean('time'), reference_ensemble['data']['weight'], adjust_value))
    o_s = weight[tas < adjust_value].sum()
    o_g = weight[tas >= adjust_value].sum()
    o_s_new = (o_g / p_ref - o_g)
    factor = o_s_new / o_s
    weight[tas < adjust_value] *= factor
    return weight

def merge_ensembles(ensembles, ens_names, climate, variables, merge_stats=True):
    ens_ini = ensembles[f"{climate}-initial"]
    ens = {
        'data' : {},
        'color' : ens_ini['color'],
        'linestyle' : '--',
        'marker' : (2, 0, -60),
        'climate' : climate,
    }
    for var in variables:
        l = []
        for ens_name in ens_names:
            x__ = ensembles[ens_name]['data'][var]
            x__ = x__.assign_coords(sim=x__.sim.values.astype(str))
            x__ = x__.assign_coords(time=np.arange(90))
            l.append(x__)
        ens['data'][var] = xr.concat(l, dim='sim').sortby('sim')
    
    if merge_stats:
        ens['stats'] = {}
        for var in ensembles[ens_name]['stats'].keys():
            l = []
            for ens_name in ens_names:
                x__ = ensembles[ens_name]['stats'][var]
                x__ = x__.assign_coords(sim=x__.sim.values.astype(str))
                l.append(x__)
            ens['stats'][var] = xr.concat(l, dim='sim').sortby('sim')


    for var in ['prob','weight']:
        l = []
        for ens_name in ens_names:
            x__ = ensembles[ens_name]['data'][var]
            x__ = x__.assign_coords(sim=x__.sim.values.astype(str))
            l.append(x__)
        ens['data'][var] = xr.concat(l, dim='sim').sortby('sim')

    ens['data']['i_ens'] = ens['data']['weight'].copy()
    ens['data']['i_ens'].values = np.array([int(s.split('_')[0].split('.')[0][1:]) for s in ens['data'][var].sim.values])

    return ens

class rea_multi_ensemble():
    def __init__(self, ens):
        self._ens = ens
        self._weight = self._ens['data']['weight'].copy()
        self._ens_i = np.array([int(s.split('_')[0].split('.')[0][1:]) for s in self._weight.sim.values])
        self._bootstrapping_method = 'ens_blocks'

        for e in np.unique(self._ens_i):
            w = self._weight[self._ens_i==e]
            w /= w.sum()
            self._weight[self._ens_i==e] = w

    # bootstrapping versions
    def bootstrapping_naive_all(self, n_bootstrap):
        ids = np.arange(0, self._ens_i.shape[0], 1, 'int')
        list_of_ids = []
        for _ in range(n_bootstrap):
            ids_ = np.random.choice(ids, len(ids), replace=True)
            list_of_ids.append(ids_)

        return list_of_ids

    def bootstrapping_ens_blocks(self, n_bootstrap):
        ids = np.arange(0, self._ens_i.shape[0], 1, 'int')
        available_ensembles = np.unique(self._ens_i)
        n_available_ensembles = len(available_ensembles)
        n_sims = self._ens_i.shape[0]
        n_sims_per_ensemble = int(n_sims / n_available_ensembles)
        list_of_ids = []
        for _ in range(n_bootstrap):
            ids_ = np.array([], 'int')
            selected_ensembles = np.random.choice(
                available_ensembles, 
                int(len(available_ensembles)),
                replace=True)
            for ensemble in selected_ensembles:
                ids_ = np.append(ids_, np.random.choice(ids[self._ens_i == ensemble], n_sims_per_ensemble, replace=True))
            list_of_ids.append(ids_)
        
        return list_of_ids
    
    def bootstrap_wrapper(self, n_bootstrap):
        if self._bootstrapping_method == 'ens_blocks':
            return self.bootstrapping_ens_blocks(n_bootstrap)
        elif self._bootstrapping_method == 'naive_all':
            return self.bootstrapping_naive_all(n_bootstrap)
        asdas

    # statistics
    def exceedance_probability(self, threshold, n_bootstrap=0):
        l = []
        for e in np.unique(self._ens_i):
            w = self._weight[self._ens_i==e].copy()
            w /= w.sum()
            l.append(w)
        weight = xr.concat(l, dim='sim').values
        tas = self._ens['data']['tas_anom'].mean('time').values
        ids = np.arange(0, weight.shape[0], 1, 'int')

        prob = weighted_probability(tas, weight, threshold)

        if n_bootstrap == 0:
            return prob

        list_of_ids = self.bootstrap_wrapper(n_bootstrap)
        l = np.array([])
        for ids_ in list_of_ids:
            l = np.append(l, weighted_probability(tas[ids_], weight[ids_], threshold))
        
        return prob, l
    
    def return_level(self, level, n_bootstrap=0):
        l = []
        for e in np.unique(self._ens_i):
            w = self._weight[self._ens_i==e].copy()
            w /= w.sum()
            l.append(w)
        weight = xr.concat(l, dim='sim').values
        tas = self._ens['data']['tas_anom'].mean('time').values
        
        rt = weighted_quantile(tas, (1 - 1/level), sample_weight=self._weight)

        if n_bootstrap == 0:
            return rt
        
        list_of_ids = self.bootstrap_wrapper(n_bootstrap)
        l = np.array([])
        for ids_ in list_of_ids:
            l = np.append(l, weighted_quantile(tas[ids_], (1 - 1/level), sample_weight=weight[ids_]))
        return rt, l

    def return_level_wrapper(self, level, n_bootstrap=0):
        return self.return_level_ens_blocks(level, n_bootstrap)


    def adjust_weights_for_threshold(self, threshold):
        tas = self._ens['data']['tas_anom'].mean('time')
        weight = self._weight.copy()
        for e in np.unique(self._ens_i):
            weight[self._ens_i==e] = weight[self._ens_i==e] / weight[self._ens_i==e].sum()
        weight[tas < threshold] = 0
        return weight

    def expected_value(self, variable_name, realm_name, threshold, n_bootstrap=0):
        tas = self._ens['data']['tas_anom'].mean('time')
        weight = self.adjust_weights_for_threshold(threshold)
        
        x = self._ens[realm_name][variable_name]
        expect = weighted_expected_value(tas=tas, weight=weight, threshold=threshold, x=x)

        if n_bootstrap == 0:
            return expect

        list_of_ids = self.bootstrap_wrapper(n_bootstrap)
        l = np.array([])
        for ids_ in list_of_ids:
            l = np.append(l, weighted_expected_value(tas[ids_], weight[ids_], threshold, x[ids_]))
        
        return expect, l

    def expected_percentile(self, variable_name, realm_name, threshold, quantiles, n_bootstrap=0):
        tas = self._ens['data']['tas_anom'].mean('time')
        weight = self.adjust_weights_for_threshold(threshold)
        
        x = self._ens[realm_name][variable_name]

        expect = weighted_expected_quantile(tas=tas, weight=weight, threshold=threshold, x=x, quantiles=quantiles)

        if n_bootstrap == 0:
            return expect



# LE dummy
class LE_ensemble():
    def __init__(self, ens):
        self._ens = ens      

    def exceedance_probability(self, threshold, n_bootstrap=0):
        tas = self._ens['data']['tas_anom'].mean('time').values
        prob = float((tas >= threshold).sum() / tas.shape[0])

        if n_bootstrap == 0:
            return prob

        ids = np.arange(0, tas.shape[0], 1, 'int')
        l = np.array([])
        for _ in range(n_bootstrap):
            ids_ = np.random.choice(ids, len(ids), replace=True)
            l = np.append(l, float((tas[ids_] >= threshold).sum() / tas.shape[0]))
        
        return prob, l

    def return_level(self, level, n_bootstrap=0):
        tas = self._ens['data']['tas_anom'].mean('time').values
        weight = tas.copy() * 0 + 1
        rt = weighted_quantile(tas, (1 - 1/level), sample_weight=weight)

        if n_bootstrap == 0:
            return rt

        ids = np.arange(0, weight.shape[0], 1, 'int')
        l = np.array([])
        for _ in range(n_bootstrap):
            ids_ = np.random.choice(ids, len(ids), replace=True)
            l = np.append(l, weighted_quantile(tas[ids_], (1 - 1/level), sample_weight=weight[ids_]))
        
        return rt, l

    def adjust_weights_for_threshold(self, threshold):
        tas = self._ens['data']['tas_anom'].mean('time')
        weight = tas.copy() * 0 + 1
        weight[tas < threshold] = 0
        return weight

    def expected_value(self, variable_name, realm_name, threshold, n_bootstrap=0):
        tas = self._ens['data']['tas_anom'].mean('time')
        weight = tas.copy() * 0 + 1
        x = self._ens[realm_name][variable_name]

        if threshold == None:
            expect = x.mean('sim')
        else:
            expect = weighted_expected_value(tas=tas, weight=weight, threshold=threshold, x=x)

        if n_bootstrap == 0:
            return expect

        ids = np.arange(0, weight.shape[0], 1, 'int')
        l = np.array([])
        for _ in range(n_bootstrap):
            ids_ = np.random.choice(ids, len(ids), replace=True)
            if threshold == None:
                l = np.append(l, x[ids_].mean())
            else:
                l = np.append(l, weighted_expected_value(tas[ids_], weight[ids_], threshold, x[ids_]))
        
        return expect, l


    def expected_percentile(self, variable_name, realm_name, threshold, quantiles, n_bootstrap=0):
        tas = self._ens['data']['tas_anom'].mean('time')
        weight = tas.copy() * 0 + 1
        
        x = self._ens[realm_name][variable_name]

        expect = weighted_expected_quantile(tas=tas, weight=weight, threshold=threshold, x=x, quantiles=quantiles)

        return expect