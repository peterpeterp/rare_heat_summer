
import os,sys,glob
import xarray as xr
import numpy as np

import regionmask

def shift_lon(nc):
    nc.coords['lon'] = (nc.coords['lon'] + 180) % 360 - 180
    nc = nc.sortby(nc.lon)
    return nc

def create_or_load_regional_mask(regional_mask_file, slice_lat, slice_lon):
    if os.path.isfile(regional_mask_file):
        return xr.open_dataset(regional_mask_file)['mask'] 
    else:
        # create
        h1_file = f"/work/bb1152/u290372/cesm215_archive/b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000/atm/hist/b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000.cam.h1.0873-01-02-00000.nc"
        with xr.open_dataset(h1_file) as nc:
            nc = shift_lon(nc)
            y = nc['TREFHT'].sel(lat=slice_lat, lon=slice_lon)[0]
            sst = nc['SST'].sel(lat=slice_lat, lon=slice_lon)[0]

        # create mask
        regional_mask = y.copy() * 0
        # weight by latitude
        regional_mask += np.cos(np.radians(y.lat))
        # ignore ocean cells
        regional_mask.values[sst != 0] = 0
        # normalize for summing
        regional_mask /= regional_mask.sum()

        # save regional_mask for later usage
        xr.Dataset({'mask':regional_mask}).to_netcdf(regional_mask_file)
    return regional_mask

def regional_average(y, regional_mask):
    return (y.sel(dict(lat = regional_mask.lat.values, lon = regional_mask.lon.values), method='nearest') * regional_mask.values).sum(('lat','lon'))


def main_observable(archive_path):
    h_files = glob.glob(f"{archive_path}/atm/hist/*h1*")
    assert len(h_files) > 0, f"h-file missing - {archive_path}"
    assert len(h_files) == 1, f"multiple h1-files available - {archive_path}"

    # regional mask
    regional_mask = create_or_load_regional_mask(
        regional_mask_file = f"/work/bb1152/u290372/GKLT/regions/wEU.nc",
        slice_lat=slice(44,55), 
        slice_lon=slice(-4,12),
        )

    with xr.open_dataset(h_files[0]) as nc:
        nc = shift_lon(nc)
        obs = nc['TREFHT'] - 273.15
        obs = regional_average(obs, regional_mask)
        return obs.mean()