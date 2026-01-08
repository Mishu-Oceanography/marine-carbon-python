# Monthly DIC Anomaly Climatology — FIXED LAYOUT

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import xarray as xr
import calendar
import matplotlib as mpl

# Styling
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['mathtext.fontset'] = 'stix'

# Load data
ds = xr.open_dataset(
    r"E:\DATASETS\NCEI-ESA-concetenate\dic_monthly_climatology_Bay_of_Bengal_2014_2022.nc"
)
dic = ds["dic_clim"]
lat = ds["lat"]
lon = ds["lon"]

# Compute anomalies
dic_mean = dic.mean(dim="month")
dic_anom = dic - dic_mean

# Symmetric robust limits
vlim = float(np.abs(dic_anom).quantile(0.98))

# Figure & layout (NO constrained_layout)
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(
    3, 4,
    left=0.06, right=0.88,   # space for colorbar
    bottom=0.08, top=0.90,   # space for labels & title
    wspace=0.08, hspace=0.15
)

axes = []

for i in range(3):
    for j in range(4):
        ax = fig.add_subplot(gs[i, j], projection=ccrs.PlateCarree())
        axes.append(ax)

months = list(calendar.month_name)[1:]


# Plot loop
for i, ax in enumerate(axes):

    data = dic_anom.sel(month=i + 1)

    ax.set_extent([78, 100, 5, 25], crs=ccrs.PlateCarree())
    ax.set_aspect('auto')

    ax.add_feature(cfeature.LAND, facecolor='lightgrey')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.6)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.RIVERS, linewidth=0.4)

    im = ax.pcolormesh(
        lon, lat, data,
        cmap='RdBu_r',
        vmin=-vlim, vmax=vlim,
        shading='auto',
        transform=ccrs.PlateCarree()
    )

    # Zero contour
    ax.contour(
        lon, lat, data,
        levels=[0],
        colors='k',
        linewidths=0.8,
        transform=ccrs.PlateCarree()
    )

    ax.set_title(months[i], fontsize=12)

    # REMOVE ticks
    ax.set_xticks([])
    ax.set_yticks([])

# Global labels (OUTSIDE grid)
fig.text(0.47, 0.04, "Longitude (°E)", ha='center', fontsize=14)
fig.text(0.015, 0.50, "Latitude (°N)", va='center', rotation='vertical', fontsize=14)

# Colorbar
cax = fig.add_axes([0.90, 0.18, 0.015, 0.64])  # [left, bottom, width, height]
cbar = fig.colorbar(im, cax=cax)
cbar.set_label("DIC Anomaly (µmol kg⁻¹)", fontsize=14)


# Title (no overlap)
fig.suptitle(
    "Monthly Climatology of DIC Anomalies (2014–2022) Bay of Bengal",
    fontsize=16,
    y=0.96
)

plt.show()

