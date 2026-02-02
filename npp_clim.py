import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset(r"E:\DATASETS\NPP\cmems_mod_glo_bgc-bio_anfc_0.25deg_P1D-m_1769926987371.nc")
print(ds.data_vars)
clim = ds['nppv'].groupby('time.month').mean(dim='time')

#fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(8,6))
clim.to_netcdf(r"E:\DATASETS\NPP_monthly_climatology.nc")
months = range(1, 13)

month_names = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']

fig, axes = plt.subplots(3, 4, figsize=(19,10), constrained_layout=True)

vmin = 1.9382246
vmax = 1719.9738

for i, ax in enumerate(axes.flat):
    # Select by number, not string
    import matplotlib.colors as colors

    clim.sel(month=i + 1).plot(
        ax=ax,
        cmap='YlOrRd',
        norm=colors.LogNorm(vmin=1, vmax=2000),
        add_colorbar=False
    )
    clim = clim.where(clim > 0)
    # Use month name only for title
    ax.set_title(month_names[i])
    ax.set_xlabel("")
    ax.set_ylabel("")

# Single shared colorbar
cbar = fig.colorbar(
    axes[0,0].collections[0],
    ax=axes,
    fraction=0.025,
    pad=0.02
)
cbar.set_label("nppv[mg/m3/day]")

fig.suptitle("Monthly Climatology of net primary production of Bay of Bengal", fontsize=14)
plt.show()
