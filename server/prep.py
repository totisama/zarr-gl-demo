import xarray as xr
import numpy as np
from ndpyramid import pyramid_reproject
import rioxarray  # noqa

x = np.arange(-180, 180, 0.25)
y = np.arange(-90, 90.25, 0.25)
da = xr.DataArray(
    data=np.ones((len(y), len(x))),
    coords={"y": y, "x": x},
    dims=["y", "x"],
    name="my_array",
)
da = da * (np.abs(da.y) + np.abs(da.x) + 1)

ds = xr.Dataset({"my_array": da})
ds = ds.rio.write_crs("EPSG:4326")

pyramids = pyramid_reproject(ds, levels=6, resampling="bilinear")
print("Pyramids structure:", pyramids)
print("Available data variables:", list(pyramids.ds.data_vars) if hasattr(pyramids, 'ds') else 'No ds attribute')

# Fix for TypeError: Expected a BytesBytesCodec. Got <class 'numcodecs.zlib.Zlib'> instead.
# Use zarr format v2 for better compatibility
pyramids.to_zarr("./example.zarr", consolidated=True, mode="w", zarr_format=2)
print("Result saved to ./example.zarr")