import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import alpha

file_path = r"E:\DATASETS\DIC\copernicus\cmems_copenicus_DIC_0.25X0.25.nc"
ds = xr.open_dataset(file_path, decode_times=True)  # usually works for Copernicus

var_name = 'dissic'
data = ds[var_name]

# Spatial average (lat/lon, optionally depth)
dims_to_avg = [dim for dim in data.dims if dim != 'time']
ts = data.mean(dim=dims_to_avg).to_series()

# Full monthly range 2014-2024
full_time = pd.date_range('2014-01-01', '2024-12-31', freq='MS')

# Reindex to fill missing months with NaN
ts_full = ts.reindex(full_time, fill_value=np.nan)

# Plot
plt.figure(figsize=(12,5))
plt.plot(ts_full.index, ts_full.values, marker='o', linestyle='-', alpha=0.8, color='green')
plt.title(f'Time Series of {var_name} (2014-2024)')
plt.xlabel('Time')
plt.ylabel(var_name)
plt.grid(True)
plt.tight_layout()
plt.show()


