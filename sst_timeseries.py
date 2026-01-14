import xarray as xr
import glob
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 14


# 1. Path to EN4 files (ALL files in one folder)
data_path = r"E:\EN4 DATASETS\EN-4_TEMP+SAL\*.nc"  # edit if needed
files = sorted(glob.glob(data_path))

# 2. Open multiple files (keeps time dimension)
ds = xr.open_mfdataset(
    files,
    combine="by_coords",
    data_vars="all",
    decode_times=True
)
# 3. Select Bay of Bengal region
ds_bob = ds.sel(
    lat=slice(5, 25),
    lon=slice(78, 100)
)

# 4. Extract SST (surface temperature)
sst = ds_bob["temperature"].sel(depth=0, method="nearest")

# 5.Convert Kelvin to Celsius
sst = sst - 273.15
sst.attrs["units"] = "°C"

# 6.Spatial mean over Bay of Bengal
sst_bob_mean = sst.mean(dim=["lat", "lon"], skipna=True)

# 7. Select time period: 2014–2024
sst_bob_mean = sst_bob_mean.sel(
    time=slice("2014-01-01", "2024-12-31")
)

# 8.plotting sst time series
plt.figure(figsize=(12, 5))
plt.plot(
    sst_bob_mean.time,
    sst_bob_mean,
    color="#d62728",
    linewidth=2
)

plt.xlabel("Year")
plt.ylabel("Sea Surface Temperature (°C)")
plt.title("Bay of Bengal Mean SST (EN4)")
plt.grid(True, linestyle="-", linewidth=0.6, alpha=0.8)
plt.tight_layout()
plt.show()

