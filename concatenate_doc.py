import xarray as xr

# Path to your NetCDF files (use wildcard if many files)
files = (r"folder path")

# Open and concatenate a long time dimension
ds = xr.open_mfdataset(files, combine="by_coords")

# Subset the region
ds_subset = ds.sel(
    lat=slice(5, 25.1),
    lon=slice(78, 100.1)
)

# Save the subset data
ds_subset.to_netcdf(r"E:\DATASETS\DOC\ESA\CONCATENATE_DOC.nc")

print("Subset and concatenation completed!")
