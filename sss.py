import xarray as xr
import glob
import matplotlib.pyplot as plt

# File paths
sss_folder = r"E:\EN4 DATASETS\EN-4_TEMP+SAL\*.nc"  # all EN4 files

# Load all SSS files
sss_files = sorted(glob.glob(sss_folder))
ds_sss = xr.open_mfdataset(
    sss_files,
    combine='by_coords',
    decode_times=True
)

# Select region & surface
ds_sss_region = ds_sss.sel(lat=slice(5,25), lon=slice(78,100))
sss_surface = ds_sss_region['salinity'].isel(depth=0).mean(dim=['lat','lon']).compute()
time_sss = ds_sss_region['time'].compute()

# Resample monthly if needed
sss_surface = sss_surface.resample(time='1M').mean()
time_sss = sss_surface['time']

#  Plot SSS time series
plt.figure(figsize=(12,5))
plt.plot(time_sss, sss_surface, color='navy', marker='o', alpha=0.8, label='SSS (PSU)')
plt.xlabel('Time')
plt.ylabel('Sea Surface Salinity (PSU)')
plt.title('Monthly Sea Surface Salinity (5–25°N, 78–100°E)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
