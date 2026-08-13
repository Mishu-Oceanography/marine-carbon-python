# # """
# # bob_poc_chl_diagnostics.py
# #
# # POC:Chl-a diagnostic analysis for the Northern Bay of Bengal.
# #
# # This version directly loads:
# #     1. MODIS POC NetCDF
# #     2. MODIS Chlorophyll-a NetCDF
# #
# # It calculates:
# #     POC:Chl-a = POC / Chlorophyll-a
# #
# # and performs three diagnostics:
# #
# # (a) Basin-wide histogram of POC:Chl-a
# #     - Rouf et al. range: 240.91-294.68
# #     - Fraction below, within, and above the range
# #
# # (b) Seasonal fraction below the lower threshold
# #     - POC:Chl-a < 240.91
# #     - Monthly climatology
# #     - JJAS vs other months
# #
# # (c) JJAS spatial analysis
# #     - Mean POC:Chl-a
# #     - Fraction of JJAS months flagged below 240.91
# #
# # IMPORTANT:
# # The 240.91-294.68 range is kept exactly as provided.
# # This script does NOT derive, fit, or modify the threshold.
# #
# # """
#
# import numpy as np
# import xarray as xr
# import matplotlib.pyplot as plt
# from pathlib import Path
#
#
# # ======================================================================
# # 1. INPUT FILES
# # ======================================================================
#
# POC_FILE = Path(
#     r"E:\DATASETS\POC\MODIS\POC_timeseries_2003_2025.nc"
# )
#
# CHL_FILE = Path(
#     r"E:\CHLOROPHYLL DATA\MODIS\MODIS_CHL_2003_2025_timeseries.nc"
# )
#
#
# # ======================================================================
# # 2. LITERATURE THRESHOLDS
# # ======================================================================
#
# POC_CHL_BASELINE_LOW = 240.91
# POC_CHL_BASELINE_HIGH = 294.68
#
# # JJAS = June, July, August, September
# JJAS_MONTHS = [6, 7, 8, 9]
#
#
# # ======================================================================
# # 3. OUTPUT DIRECTORY
# # ======================================================================
#
# OUTPUT_DIR = Path(r"E:\CHLOROPHYLL DATA\bob_poc_chl_diagnostics_output")
# OUTPUT_DIR.mkdir(exist_ok=True)
#
#
# # ======================================================================
# # 4. LOAD POC AND CHL-A
# # ======================================================================
#
# def load_poc_chl():
#
#     print("\nLoading POC file:")
#     print(POC_FILE)
#
#     print("\nLoading Chlorophyll-a file:")
#     print(CHL_FILE)
#
#     if not POC_FILE.exists():
#         raise FileNotFoundError(
#             f"POC file not found:\n{POC_FILE}"
#         )
#
#     if not CHL_FILE.exists():
#         raise FileNotFoundError(
#             f"Chlorophyll-a file not found:\n{CHL_FILE}"
#         )
#
#     # Open datasets
#     poc_ds = xr.open_dataset(POC_FILE)
#     chl_ds = xr.open_dataset(CHL_FILE)
#
#     # Check required variables
#     if "poc" not in poc_ds:
#         raise ValueError(
#             "The POC file does not contain a variable named 'poc'."
#         )
#
#     if "chlor_a" not in chl_ds:
#         raise ValueError(
#             "The Chlorophyll-a file does not contain a variable named "
#             "'chlor_a'."
#         )
#
#     poc = poc_ds["poc"]
#     chl = chl_ds["chlor_a"]
#
#     print("\nPOC variable:")
#     print(poc)
#
#     print("\nChlorophyll-a variable:")
#     print(chl)
#
#     # --------------------------------------------------------------
#     # Check dimensions
#     # --------------------------------------------------------------
#
#     print("\nChecking dimensions...")
#
#     print("POC dimensions:", poc.dims)
#     print("Chl-a dimensions:", chl.dims)
#
#     if poc.shape != chl.shape:
#         raise ValueError(
#             f"POC and Chl-a shapes do not match!\n"
#             f"POC: {poc.shape}\n"
#             f"Chl-a: {chl.shape}"
#         )
#
#     # --------------------------------------------------------------
#     # Check coordinates
#     # --------------------------------------------------------------
#
#     if not np.allclose(poc.lat.values, chl.lat.values):
#         raise ValueError(
#             "POC and Chl-a latitude grids do not match."
#         )
#
#     if not np.allclose(poc.lon.values, chl.lon.values):
#         raise ValueError(
#             "POC and Chl-a longitude grids do not match."
#         )
#
#     print("✓ Latitude grids match.")
#     print("✓ Longitude grids match.")
#     print("✓ Array dimensions match.")
#
#     # --------------------------------------------------------------
#     # Calculate POC:Chl-a
#     # --------------------------------------------------------------
#
#     print("\nCalculating POC:Chl-a ratio...")
#
#     # Avoid division by zero
#     chl = chl.where(chl > 0)
#
#     ratio = poc / chl
#
#     ratio.name = "poc_chl_ratio"
#
#     ratio.attrs["long_name"] = "POC:Chlorophyll-a ratio"
#     ratio.attrs["units"] = "mg POC / mg Chl-a"
#
#     ds = xr.Dataset({
#         "poc": poc,
#         "chl": chl,
#         "poc_chl_ratio": ratio
#     })
#
#     print("✓ POC:Chl-a calculated.")
#
#     return ds
#
#
# # ======================================================================
# # 5. DIAGNOSTIC A — BASIN-WIDE HISTOGRAM
# # ======================================================================
#
# def diagnostic_a_histogram(ds):
#
#     print("\n" + "=" * 70)
#     print("DIAGNOSTIC A — BASIN-WIDE POC:CHL-A DISTRIBUTION")
#     print("=" * 70)
#
#     ratio = ds["poc_chl_ratio"].values.flatten()
#
#     # Remove NaN and infinity
#     ratio = ratio[np.isfinite(ratio)]
#
#     if ratio.size == 0:
#         raise ValueError(
#             "No valid POC:Chl-a values were found."
#         )
#
#     # Fractions
#     within_range = np.logical_and(
#         ratio >= POC_CHL_BASELINE_LOW,
#         ratio <= POC_CHL_BASELINE_HIGH
#     )
#
#     frac_within = within_range.mean()
#
#     frac_below = (
#         ratio < POC_CHL_BASELINE_LOW
#     ).mean()
#
#     frac_above = (
#         ratio > POC_CHL_BASELINE_HIGH
#     ).mean()
#
#     median_ratio = np.median(ratio)
#     mean_ratio = np.mean(ratio)
#
#     print(f"\nValid pixel-months: {ratio.size}")
#     print(f"Mean POC:Chl-a ratio:   {mean_ratio:.2f}")
#     print(f"Median POC:Chl-a ratio: {median_ratio:.2f}")
#
#     print(
#         f"\nBelow {POC_CHL_BASELINE_LOW}: "
#         f"{frac_below:.1%}"
#     )
#
#     print(
#         f"Within {POC_CHL_BASELINE_LOW}-"
#         f"{POC_CHL_BASELINE_HIGH}: "
#         f"{frac_within:.1%}"
#     )
#
#     print(
#         f"Above {POC_CHL_BASELINE_HIGH}: "
#         f"{frac_above:.1%}"
#     )
#
#     # --------------------------------------------------------------
#     # Plot
#     # --------------------------------------------------------------
#
#     fig, ax = plt.subplots(figsize=(8, 5))
#
#     # Clip extreme tail only for visualization
#     plot_max = np.percentile(ratio, 99)
#
#     ax.hist(
#         ratio[ratio <= plot_max],
#         bins=80
#     )
#
#     ax.axvline(
#         POC_CHL_BASELINE_LOW,
#         linestyle="--",
#         linewidth=2,
#         label=f"Rouf lower bound ({POC_CHL_BASELINE_LOW})"
#     )
#
#     ax.axvline(
#         POC_CHL_BASELINE_HIGH,
#         linestyle="--",
#         linewidth=2,
#         label=f"Rouf upper bound ({POC_CHL_BASELINE_HIGH})"
#     )
#
#     ax.axvline(
#         median_ratio,
#         linestyle="-",
#         linewidth=2,
#         label=f"Basin median ({median_ratio:.1f})"
#     )
#
#     ax.set_xlabel("POC:Chl-a ratio")
#     ax.set_ylabel("Pixel-month count")
#
#     ax.set_title(
#         "Basin-wide POC:Chl-a distribution\n"
#         "vs. Rouf et al. literature range"
#     )
#
#     ax.legend(fontsize=8)
#
#     fig.tight_layout()
#
#     output_file = OUTPUT_DIR / "fig_a_histogram.png"
#
#     fig.savefig(
#         output_file,
#         dpi=150,
#         bbox_inches="tight"
#     )
#
#     plt.close(fig)
#
#     print(f"\nFigure saved:\n{output_file}")
#
#     return (
#         "=== (a) Basin-wide distribution ===\n"
#         f"Valid pixel-months: {ratio.size}\n"
#         f"Mean ratio: {mean_ratio:.2f}\n"
#         f"Median ratio: {median_ratio:.2f}\n"
#         f"Fraction below 240.91: {frac_below:.1%}\n"
#         f"Fraction within 240.91-294.68: {frac_within:.1%}\n"
#         f"Fraction above 294.68: {frac_above:.1%}\n"
#     )
#
#
# # ======================================================================
# # 6. DIAGNOSTIC B — SEASONAL FRACTION
# # ======================================================================
#
# def diagnostic_b_seasonal(ds):
#
#     print("\n" + "=" * 70)
#     print("DIAGNOSTIC B — SEASONAL FRACTION BELOW 240.91")
#     print("=" * 70)
#
#     ratio = ds["poc_chl_ratio"]
#
#     # Flag pixels below threshold
#     below = ratio < POC_CHL_BASELINE_LOW
#
#     # Spatial dimensions
#     spatial_dims = [
#         d for d in below.dims
#         if d != "time"
#     ]
#
#     # Average spatial fraction for every month
#     frac_by_month = (
#         below
#         .mean(dim=spatial_dims)
#         .groupby("time.month")
#         .mean(dim="time")
#     )
#
#     months = frac_by_month["month"].values
#     fracs = frac_by_month.values
#
#     # JJAS
#     jjas_mask = np.isin(
#         months,
#         JJAS_MONTHS
#     )
#
#     jjas_frac = fracs[jjas_mask].mean()
#
#     other_frac = fracs[~jjas_mask].mean()
#
#     print(
#         f"\nMean fraction flagged during JJAS: "
#         f"{jjas_frac:.1%}"
#     )
#
#     print(
#         f"Mean fraction flagged during other months: "
#         f"{other_frac:.1%}"
#     )
#
#     print("\nMonthly values:")
#
#     for month, fraction in zip(months, fracs):
#
#         print(
#             f"Month {int(month):2d}: "
#             f"{fraction:.1%}"
#         )
#
#     # --------------------------------------------------------------
#     # Plot
#     # --------------------------------------------------------------
#
#     fig, ax = plt.subplots(figsize=(8, 5))
#
#     bar_colors = [
#         "firebrick" if m in JJAS_MONTHS
#         else "steelblue"
#         for m in months
#     ]
#
#     ax.bar(
#         months,
#         fracs * 100,
#         color=bar_colors
#     )
#
#     ax.set_xticks(range(1, 13))
#
#     ax.set_xlabel("Month")
#
#     ax.set_ylabel(
#         "% pixels with POC:Chl-a < 240.91"
#     )
#
#     ax.set_title(
#         "Seasonal fraction of pixels below "
#         "Rouf et al. lower bound\n"
#         "(JJAS highlighted)"
#     )
#
#     fig.tight_layout()
#
#     output_file = (
#         OUTPUT_DIR /
#         "fig_b_seasonal_fraction.png"
#     )
#
#     fig.savefig(
#         output_file,
#         dpi=150,
#         bbox_inches="tight"
#     )
#
#     plt.close(fig)
#
#     print(f"\nFigure saved:\n{output_file}")
#
#     return (
#         "\n=== (b) Seasonal fraction ===\n"
#         f"Mean JJAS fraction flagged: {jjas_frac:.1%}\n"
#         f"Mean other-month fraction flagged: "
#         f"{other_frac:.1%}\n"
#         + "".join(
#             f"Month {int(m):2d}: {f:.1%}\n"
#             for m, f in zip(months, fracs)
#         )
#     )
#
#
# # ======================================================================
# # 7. DIAGNOSTIC C — JJAS SPATIAL PATTERN
# # ======================================================================
#
# def diagnostic_c_spatial(ds):
#
#     print("\n" + "=" * 70)
#     print("DIAGNOSTIC C — JJAS SPATIAL PATTERN")
#     print("=" * 70)
#
#     # Select June-September
#     jjas = ds.sel(
#         time=ds["time"].dt.month.isin(JJAS_MONTHS)
#     )
#
#     # Mean ratio
#     mean_ratio_jjas = (
#         jjas["poc_chl_ratio"]
#         .mean(dim="time")
#     )
#
#     # Fraction flagged
#     frac_flagged_jjas = (
#         jjas["poc_chl_ratio"] <
#         POC_CHL_BASELINE_LOW
#     ).mean(dim="time")
#
#     # --------------------------------------------------------------
#     # Plot
#     # --------------------------------------------------------------
#
#     fig, axes = plt.subplots(
#         1,
#         2,
#         figsize=(13, 5),
#         constrained_layout=True
#     )
#
#     mean_ratio_jjas.plot(
#         ax=axes[0],
#         cmap="viridis",
#         cbar_kwargs={
#             "label": "Mean POC:Chl-a (JJAS)"
#         }
#     )
#
#     axes[0].set_title(
#         "Mean POC:Chl-a ratio — JJAS"
#     )
#
#     frac_flagged_jjas.plot(
#         ax=axes[1],
#         cmap="Reds",
#         vmin=0,
#         vmax=1,
#         cbar_kwargs={
#             "label": "Fraction of JJAS months flagged"
#         }
#     )
#
#     axes[1].set_title(
#         "Fraction flagged — JJAS\n"
#         "(POC:Chl-a < 240.91)"
#     )
#
#     output_file = (
#         OUTPUT_DIR /
#         "fig_c_jjas_spatial.png"
#     )
#
#     fig.savefig(
#         output_file,
#         dpi=150,
#         bbox_inches="tight"
#     )
#
#     plt.close(fig)
#
#     print(f"\nFigure saved:\n{output_file}")
#
#     return (
#         "\n=== (c) JJAS spatial pattern ===\n"
#         "Inspect the spatial figure for clustering of "
#         "low POC:Chl-a values near the coastline and "
#         "river-mouth region.\n"
#         f"Figure saved to: {output_file}\n"
#     )
#
#
# # ======================================================================
# # 8. MAIN
# # ======================================================================
#
# def main():
#
#     print("\n")
#     print("=" * 70)
#     print("POC:CHL-A BASIN DIAGNOSTICS")
#     print("Northern Bay of Bengal")
#     print("=" * 70)
#
#     # Load data and calculate ratio
#     ds = load_poc_chl()
#
#     # Run diagnostics
#     summary_a = diagnostic_a_histogram(ds)
#
#     summary_b = diagnostic_b_seasonal(ds)
#
#     summary_c = diagnostic_c_spatial(ds)
#
#     # --------------------------------------------------------------
#     # Save summary
#     # --------------------------------------------------------------
#
#     summary_file = (
#         OUTPUT_DIR /
#         "bob_poc_chl_diagnostics_summary.txt"
#     )
#
#     with open(
#         summary_file,
#         "w",
#         encoding="utf-8"
#     ) as f:
#
#         f.write(
#             "POC:Chl-a basin diagnostics\n"
#             "Northern Bay of Bengal\n\n"
#         )
#
#         f.write(
#             "This analysis uses the fixed Rouf et al. "
#             "literature range:\n"
#         )
#
#         f.write(
#             "240.91-294.68 mg POC / mg Chl-a\n\n"
#         )
#
#         f.write(summary_a)
#         f.write("\n")
#         f.write(summary_b)
#         f.write("\n")
#         f.write(summary_c)
#
#     print("\n" + "=" * 70)
#     print("ALL DIAGNOSTICS COMPLETED")
#     print("=" * 70)
#
#     print(
#         f"\nResults are saved in:\n"
#         f"{OUTPUT_DIR.resolve()}"
#     )
#
#     print(
#         f"\nSummary file:\n"
#         f"{summary_file.resolve()}"
#     )
#
#
# # ======================================================================
# # 9. RUN
# # ======================================================================
#
# if __name__ == "__main__":
#     main()
#
