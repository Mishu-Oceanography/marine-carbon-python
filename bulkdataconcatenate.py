import xarray as xr
import pandas as pd

VARIABLE_NAME = "fgco2"        # e.g., "dic", "spco2", "ph_total"
START_YEAR = 2014            # start year
END_YEAR = 2022            # end year

LAT_MIN, LAT_MAX = 5.0, 25.0
LON_MIN, LON_MAX = 80.0, 100.0

INPUT_FILE = r"E:\MODIS\NCEI-ESA\0220059\5.5\data\0-data\OceanSODA_ETHZ-v2023.OCADS.01_1982-2022.nc"
OUTPUT_FILE = (
    rf"E:\MODIS\NCEI-ESA\{VARIABLE_NAME}_Bay_of_Bengal_{START_YEAR}_{END_YEAR}.nc"
)

ds = xr.open_dataset(INPUT_FILE)

if VARIABLE_NAME not in ds.data_vars:
    raise ValueError(
        f"Variable '{VARIABLE_NAME}' not found.\n"
        f"Available variables: {list(ds.data_vars)}"
    )

start_time = f"{START_YEAR}-01-01"
end_time = f"{END_YEAR}-12-31"


ds_bob = ds[VARIABLE_NAME].sel(
    time=slice(start_time, end_time),
    lat=slice(LAT_MIN, LAT_MAX),
    lon=slice(LON_MIN, LON_MAX)
)

ds_bob.to_netcdf(OUTPUT_FILE)

print(f" Extracted '{VARIABLE_NAME}' for Bay of Bengal")
print(f" Period: {START_YEAR}–{END_YEAR}")
print(f" Saved as: {OUTPUT_FILE}")
print(f" Shape: {ds_bob.shape}")


