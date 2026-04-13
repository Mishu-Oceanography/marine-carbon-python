import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# -------------------------------------------------
# 1. Open CROCO Mmean file
# -------------------------------------------------
file_path = r"E:\croco_output\croco_mean\croco_Mmean_final_cp.nc"

with Dataset(file_path) as nc:

    print("Temp shape:", nc.variables['temp'].shape)

    temp = nc.variables['temp'][:]
    lon = nc.variables['lon_rho'][:]
    lat = nc.variables['lat_rho'][:]

    time_index = 0
    vertical_level = -1   # surface

    surface_temp = temp[time_index, vertical_level, :, :]

# -------------------------------------------------
# 2. Define smaller scale range
# -------------------------------------------------

# Option A (Manual range — adjust based on your data)
vmin = 26
vmax = 30

# Option B (Automatic tighter range around mean)
# mean_val = np.nanmean(surface_temp)
# vmin = mean_val - 2
# vmax = mean_val + 2

# -------------------------------------------------
# 3. Plot
# -------------------------------------------------
plt.figure(figsize=(8,6))

pcm = plt.pcolormesh(lon, lat, surface_temp,
                     shading='auto',
                     cmap='RdBu_r',
                     vmin=vmin,
                     vmax=vmax)

plt.colorbar(pcm, label='Temperature (°C)')
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Surface Temperature Distribution (CROCO Mmean)")

plt.tight_layout()
plt.show()