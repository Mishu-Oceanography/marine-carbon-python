#
# import xarray as xr
# import pandas as pd
# import glob
# import os
# #
# # # Folder containing all monthly files
# # folder = r"E:\DATASETS\POC\MODIS\POC_MAPPED_month"
# #
# # files = sorted(glob.glob(os.path.join(folder, "*.nc")))
# #
# # datasets = []
# # times = []
# #
# # for f in files:
# #
# #     ds = xr.open_dataset(f)
# #
# #     # Extract date from filename
# #     fname = os.path.basename(f)
# #
# #     date_str = fname.split('.')[1][:8]
# #
# #     time = pd.to_datetime(date_str)
# #
# #     ds = ds.expand_dims(time=[time])
# #
# #     datasets.append(ds[['poc']])
# #
# # combined = xr.concat(datasets, dim='time')
# #
# # print(combined)
# #
# # combined.to_netcdf(
# #     r"E:\DATASETS\POC\MODIS\POC_timeseries_2003_2025.nc"
# # )
# # import xarray as xr
# # import matplotlib.pyplot as plt
# # from matplotlib.colors import LogNorm
# #
# # ds = xr.open_dataset(
# #     r"E:\DATASETS\POC\MODIS\POC_timeseries_2003_2025.nc"
# # )
# #
# # mean_poc = ds.poc.mean("time")
# #
# # plt.figure(figsize=(10,7))
# #
# # mean_poc.plot(
# #     cmap='jet',
# #     vmin=30, vmax=1000
# # )
# # plt.xlabel("Longitude (°E)", fontsize=12)
# # plt.ylabel("Latitude (°N)", fontsize=12)
# #
# # plt.title('Mean POC Climatology (2003-2025)')
# #
# # plt.show()
# import xarray as xr
# import matplotlib.pyplot as plt
# from matplotlib.colors import LogNorm
#
# ds = xr.open_dataset(
#     r"E:\DATASETS\POC\MODIS\POC_timeseries_2003_2025.nc"
# )
#
# monthly = ds.poc.groupby("time.month").mean()
#
# fig, axes = plt.subplots(
#     3, 4,
#     figsize=(16,12)
# )
#
# months = [
#     "Jan","Feb","Mar","Apr",
#     "May","Jun","Jul","Aug",
#     "Sep","Oct","Nov","Dec"
# ]
#
# for i, ax in enumerate(axes.flat):
#
#     monthly.isel(month=i).plot(
#         ax=ax,
#         cmap='viridis',
#         norm=LogNorm(vmin=30, vmax=1000),
#         add_colorbar=False
#     )
#
#     ax.set_title(months[i])
#
# plt.tight_layout()
# plt.show()
# import xarray as xr
# import matplotlib.pyplot as plt
# import matplotlib.ticker as mticker
# import numpy as np
#
# # ==========================================
# # LOAD POC DATA
# # ==========================================
#
# ds = xr.open_dataset(
#     r"E:\DATASETS\POC\MODIS\POC_timeseries_2003_2025.nc"
# )
#
# # Remove extreme outliers
# ds["poc"] = ds["poc"].where(
#     ds["poc"] < 1500
# )
#
# # ==========================================
# # LOAD INTERPOLATED GEBCO
# # ==========================================
#
# depth = xr.open_dataarray(
#     r"E:\GEBCO\gebco-on-modis.nc"
# )
#
# # ==========================================
# # DEFINE SEASONS
# # ==========================================
#
# season_map = {
#     12:"Winter",
#     1:"Winter",
#     2:"Winter",
#
#     3:"Pre-Monsoon",
#     4:"Pre-Monsoon",
#     5:"Pre-Monsoon",
#
#     6:"SW Monsoon",
#     7:"SW Monsoon",
#     8:"SW Monsoon",
#     9:"SW Monsoon",
#
#     10:"Post-Monsoon",
#     11:"Post-Monsoon"
# }
#
# season = [
#     season_map[m]
#     for m in ds.time.dt.month.values
# ]
#
# ds = ds.assign_coords(
#     season=("time", season)
# )
#
# seasonal = ds["poc"].groupby(
#     "season"
# ).mean()
#
# # ==========================================
# # FIGURE
# # ==========================================
#
# fig, axes = plt.subplots(
#     2,
#     2,
#     figsize=(14,10)
# )
#
# order = [
#     "Winter",
#     "Pre-Monsoon",
#     "SW Monsoon",
#     "Post-Monsoon"
# ]
#
# # ==========================================
# # PLOT
# # ==========================================
#
# for i, (ax, s) in enumerate(
#         zip(
#             axes.flat,
#             order
#         )):
#
#     data = seasonal.sel(
#         season=s
#     )
#
#     im = data.plot(
#         ax=ax,
#         cmap="jet",
#         vmin=30,
#         vmax=500,
#         add_colorbar=False
#     )
#
#     # 50 m contour
#     c50 = ax.contour(
#         depth.lon,
#         depth.lat,
#         depth,
#         levels=[-50],
#         colors="black",
#         linewidths=1
#     )
#
#     # 200 m contour
#     c200 = ax.contour(
#         depth.lon,
#         depth.lat,
#         depth,
#         levels=[-200],
#         colors="black",
#         linewidths=1.5,
#         linestyles="--"
#     )
#
#     ax.clabel(
#         c50,
#         fmt="50 m",
#         fontsize=8
#     )
#
#     ax.clabel(
#         c200,
#         fmt="200 m",
#         fontsize=8
#     )
#
#     ax.set_title(
#         s,
#         fontsize=16
#     )
#
#     # clean labels
#     ax.set_xlabel("")
#     ax.set_ylabel("")
#
#     # latitude only left
#     if i % 2 == 1:
#         ax.set_yticklabels([])
#
#     # longitude only bottom
#     if i < 2:
#         ax.set_xticklabels([])
#
#     ax.xaxis.set_major_formatter(
#         mticker.FuncFormatter(
#             lambda x, pos:
#             f"{x:.0f}°E"
#         )
#     )
#
#     ax.yaxis.set_major_formatter(
#         mticker.FuncFormatter(
#             lambda y, pos:
#             f"{y:.0f}°N"
#         )
#     )
#
# # ==========================================
# # COLORBAR
# # ==========================================
#
# cbar = fig.colorbar(
#     im,
#     ax=axes.ravel().tolist(),
#     orientation="vertical",
#     fraction=0.03,
#     pad=0.03
# )
#
# cbar.set_label(
#     "POC (mg m$^{-3}$)",
#     fontsize=13
# )
#
# # ==========================================
# # GLOBAL LABELS
# # ==========================================
#
# fig.supxlabel(
#     "Longitude (°E)",
#     fontsize=14
# )
#
# fig.supylabel(
#     "Latitude (°N)",
#     fontsize=14
# )
#
# # ==========================================
# # TITLE
# # ==========================================
#
# fig.suptitle(
#     "Seasonal Climatology of Surface POC (2003–2025)\nBay of Bengal",
#     fontsize=18,
#     y=0.97
# )
#
# plt.subplots_adjust(
#     right=0.88,
#     wspace=0.05,
#     hspace=0.08
# )
#
# # ==========================================
# # SAVE
# # ==========================================
#
# plt.savefig(
#     "Seasonal_POC_Isobath.png",
#     dpi=600,
#     bbox_inches="tight"
# )
#
# plt.show()
#
# import xarray as xr
# import matplotlib.pyplot as plt
# import matplotlib.ticker as mticker
#
# # ==============================
# # LOAD DATA
# # ==============================
#
# ds = xr.open_dataset(
#     r"E:\DATASETS\POC\MODIS\POC_timeseries_2003_2025.nc"
# )
#
# depth = xr.open_dataarray(
#     r"E:\GEBCO\gebco-on-modis.nc"
# )
#
# # =======================
# # CLEAN POC
# # =======================
#
# # Keep ocean only
# ocean = depth < 0
#
# ds["poc"] = ds["poc"].where(
#     ocean
# )
#
# # Remove extreme values
# ds["poc"] = ds["poc"].where(
#     (ds["poc"] > 0)
#     &
#     (ds["poc"] < 1500)
# )
#
# # ==============================
# # DEFINE SEASONS
# # ==============================
#
# season_map = {
#     11: "NDJF (NEM)",
#     12: "NDJF (NEM)",
#     1:  "NDJF (NEM)",
#     2:  "NDJF (NEM)",
#
#     3:  "MAM (Pre-Monsoon)",
#     4:  "MAM (Pre-Monsoon)",
#     5:  "MAM (Pre-Monsoon)",
#
#     6:  "JJA (SWM)",
#     7:  "JJA (SWM)",
#     8:  "JJA (SWM)",
#     9:  "JJA (SWM)",
#
#     10: "SO (Post-Monsoon)",
#
# }
#
# season = [
#     season_map[m]
#     for m in ds.time.dt.month.values
# ]
#
# ds = ds.assign_coords(
#     season=("time", season)
# )
#
# seasonal = ds.poc.groupby(
#     "season"
# ).mean()
#
# order = [
#     "NDJF (NEM)",
#     "MAM (Pre-Monsoon)",
#     "JJA (SWM)",
#     "SO (Post-Monsoon)"
# ]
#
# # ==============================
# # PLOT
# # ==============================
#
# fig, axes = plt.subplots(
#     2,
#     2,
#     figsize=(13,10),
#     constrained_layout=True
# )
#
# for i, (ax, s) in enumerate(
#         zip(
#             axes.flat,
#             order
#         )):
#
#     da = seasonal.sel(
#         season=s
#     )
#
#     im = da.plot(
#         ax=ax,
#         cmap="turbo",      # cleaner than jet
#         vmin=30,
#         vmax=500,
#         add_colorbar=False
#     )
#
#     # thin contours
#     ax.contour(
#         depth.lon,
#         depth.lat,
#         depth,
#         levels=[-50],
#         colors="black",
#         linewidths=0.8,
#         linestyles = "-"
#     )
#
#     ax.contour(
#         depth.lon,
#         depth.lat,
#         depth,
#         levels=[-200],
#         colors="black",
#         linewidths=1.0,
#         linestyles="--"
#     )
#
#     ax.set_title(
#         s,
#         fontsize=12,
#         pad=8,
#         weight="normal",
#     )
#
#     ax.set_xlabel("")
#     ax.set_ylabel("")
#
#     # only outer ticks
#     if i < 2:
#         ax.set_xticklabels([])
#
#     if i % 2 == 1:
#         ax.set_yticklabels([])
#
#     ax.xaxis.set_major_formatter(
#         mticker.FuncFormatter(
#             lambda x, pos:
#             f"{int(x)}°E"
#         )
#     )
#
#     ax.yaxis.set_major_formatter(
#         mticker.FuncFormatter(
#             lambda y, pos:
#             f"{int(y)}°N"
#         )
#     )
#
# # ==============================
# # GLOBAL LABELS
# # ==============================
#
# fig.supxlabel(
#     "Longitude",
#     fontsize=15,
# fontname="Times New Roman",
# )
#
# fig.supylabel(
#     "Latitude",
#     fontsize=15,
#     fontname="Times New Roman",
# )
#
# # ==============================
# # COLORBAR
# # ==============================
#
# cbar = fig.colorbar(
#     im,
#     ax=axes,
#     shrink=0.82,
#     pad=0.02
# )
#
# cbar.set_label(
#     "POC (mg m$^{-3}$)",
#     fontsize=14
# )
#
# # ==============================
# # MAIN TITLE
# # ==============================
#
# fig.suptitle(
#     "Seasonal Climatology of Surface POC (2003–2025) Bay of Bengal",
#     fontsize=12,
#     y=1.05
# )
#
# plt.savefig(
#     r"E:\DATASETS\POC\Seasonal_POC_Clean.png",
#     dpi=600,
#     bbox_inches="tight"
# )
#
# plt.show()

import xarray as xr
import numpy as np
import pandas as pd

# ======================================================
# FILE PATHS
# ======================================================

POC_FILE = r"E:\DATASETS\POC\MODIS\POC_timeseries_2003_2025.nc"
BATHY_FILE = r"E:\GEBCO\gebco_bob.nc"

OUT_CLIM = r"E:\DATASETS\POC\seasonal_POC_climatology.nc"
OUT_TABLE = r"E:\DATASETS\POC\seasonal_mean_POC_MEAN+SD.csv"

# ======================================================
# LOAD POC
# ======================================================

print("\nLoading POC...")

ds = xr.open_dataset(POC_FILE)

print(ds)

# -------- Auto-detect POC variable --------

possible = [
    v for v in ds.data_vars
    if "poc" in v.lower()
]

if len(possible) == 0:
    raise ValueError(
        "POC variable not found. Check dataset."
    )

POC = ds[possible[0]]

print(f"\nUsing POC variable: {POC.name}")

# ======================================================
# STANDARDIZE COORDINATES
# ======================================================

rename_dict = {}

for c in POC.coords:

    if c.lower() in ["latitude"]:
        rename_dict[c] = "lat"

    if c.lower() in ["longitude"]:
        rename_dict[c] = "lon"

if rename_dict:
    POC = POC.rename(rename_dict)

# ======================================================
# CREATE BAY OF BENGAL SEASONAL CLIMATOLOGY
# ======================================================

print("\nCreating Bay of Bengal seasonal climatology...")

season_dict = {
    "NDJF (NEM)": [12, 1, 2],
    "MAM (Pre-monsoon)": [3, 4, 5],
    "JJA (SWM)": [6, 7, 8, 9],
    "SO (Post-monsoon)": [10, 11]
}

seasonal_list = []

for season_name, months in season_dict.items():

    season_data = (
        POC
        .sel(time=POC.time.dt.month.isin(months))
        .mean(dim="time", skipna=True)
        .expand_dims(season=[season_name])
    )

    seasonal_list.append(season_data)

seasonal = xr.concat(seasonal_list, dim="season")

seasonal.to_netcdf(OUT_CLIM)

print("Seasonal climatology saved.")
# ======================================================
# LOAD BATHYMETRY
# ======================================================

print("\nLoading bathymetry...")

bathy = xr.open_dataset(BATHY_FILE)

print(bathy)

# -------- Auto-detect depth variable --------

depth_candidates = [
    v for v in bathy.data_vars
    if (
        "depth" in v.lower()
        or
        "elevation" in v.lower()
        or
        "z" == v.lower()
    )
]

if len(depth_candidates) == 0:
    raise ValueError(
        "Depth variable not found"
    )

depth = bathy[depth_candidates[0]]

print(f"Using depth: {depth.name}")

# ======================================================
# STANDARDIZE BATHY COORDS
# ======================================================

rename_bathy = {}

for c in depth.coords:

    if c.lower() in ["latitude"]:
        rename_bathy[c] = "lat"

    if c.lower() in ["longitude"]:
        rename_bathy[c] = "lon"

if rename_bathy:
    depth = depth.rename(rename_bathy)

depth = abs(depth)

# ======================================================
# INTERPOLATE TO POC GRID
# ======================================================

print("\nMatching bathymetry to POC grid...")

depth = depth.interp(
    lat=seasonal.lat,
    lon=seasonal.lon,
    method="nearest"
)

# ======================================================
# CREATE DEPTH MASKS
# ======================================================

coastal = depth < 50

shelf = (
    (depth >= 50)
    &
    (depth < 200)
)

basin = depth >= 200

print("Masks created")

# ======================================================
# CALCULATE SEASONAL REGIONAL STATISTICS
# ======================================================

results = []

for season_name in seasonal.season.values:

    data = seasonal.sel(season=season_name)

    regions = {
        "Coastal (<50 m)": coastal,
        "Shelf (50–200 m)": shelf,
        "Basin (>200 m)": basin
    }

    for region_name, mask in regions.items():

        values = data.where(mask).values.flatten()

        # Remove NaNs
        values = values[np.isfinite(values)]

        if len(values) == 0:

            mean = np.nan
            sd = np.nan
            median = np.nan
            minimum = np.nan
            maximum = np.nan
            cv = np.nan
            n = 0

        else:

            mean = np.mean(values)
            sd = np.std(values, ddof=1)
            median = np.median(values)
            minimum = np.min(values)
            maximum = np.max(values)
            cv = (sd / mean) * 100
            n = len(values)

        results.append([
            season_name,
            region_name,
            mean,
            sd,
            median,
            minimum,
            maximum,
            cv,
            n
        ])
#save the table
# table = pd.DataFrame(
#     results,
#     columns=[
#         "Season",
#         "Region",
#         "Mean",
#         "SD",
#         "Median",
#         "Minimum",
#         "Maximum",
#         "CV (%)",
#         "N"
#     ]
# )
#
# print(table)
#
# table.to_csv(
#     OUT_TABLE,
#     index=False
# )
# ======================================================
# CREATE MEAN ± SD TABLE
# ======================================================

regions = {
    "Coastal (<50 m)": coastal,
    "Shelf (50–200 m)": shelf,
    "Basin (>200 m)": basin
}

season_order = [
    "NDJF (NEM)",
    "MAM (Pre-monsoon)",
    "JJA (SWM)",
    "SO (Post-monsoon)"
]

table = pd.DataFrame(index=regions.keys(), columns=season_order)

for season_name in season_order:

    data = seasonal.sel(season=season_name)

    for region_name, mask in regions.items():

        values = data.where(mask).values.flatten()
        values = values[np.isfinite(values)]

        mean = np.mean(values)
        sd = np.std(values, ddof=1)

        table.loc[region_name, season_name] = (
            f"{mean:.2f} ± {sd:.2f}"
        )

table.index.name = "Region"

print(table)

table.to_csv(OUT_TABLE)