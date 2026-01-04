import copernicusmarine


copernicusmarine.subset(
    dataset_id="METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2",
    variables=["analysed_sst"],
    minimum_longitude=78,
    maximum_longitude=100,
    minimum_latitude=5,
    maximum_latitude=25,
    start_datetime="2020-08-20",
    end_datetime="2024-12-31",
    coordinates_selection_method="strict-inside",
    netcdf_compression_level=1,
    disable_progress_bar=True,
    output_filename=r"E:\COPERNICUS\SST_bob.nc"
)
