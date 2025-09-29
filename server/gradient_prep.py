# gradient_prep.py
import shutil
from pathlib import Path

import numpy as np
import xarray as xr
import zarr
from ndpyramid import pyramid_reproject
from rasterio.transform import from_bounds
import rioxarray  # noqa: F401

CURRENT_VERSION = "v1"
VAR_NAME = "precip"
LEVELS = 8
TILE = 128

def strip_and_chunk_tree(node: "xr.DataTree"):
    """Recursively enforce: float32, chunks=(128,128), compressor=None."""
    if getattr(node, "ds", None) is not None:
        ds = node.ds.copy()
        for v in ds.data_vars:
            ds[v] = ds[v].astype("float32")
            ds[v] = ds[v].chunk({"y": TILE, "x": TILE})
            ds[v].encoding["compressor"] = None
        node.ds = ds
    for child in node.children.values():
        strip_and_chunk_tree(child)

def main():
    # --- base gradient 0..100 on a WGS84 grid ---
    h, w = 1800, 3600
    arr = np.linspace(0, 100, h * w, dtype="float32").reshape(h, w)
    y = np.linspace(90, -90, h, endpoint=False)
    x = np.linspace(-180, 180, w, endpoint=False)

    da = xr.DataArray(arr, dims=("y", "x"), coords={"y": y, "x": x}, name=VAR_NAME)
    ds = da.to_dataset()

    # CRS + geotransform for (-180,-90, 180,90)
    transform = from_bounds(-180.0, -90.0, 180.0, 90.0, w, h)
    ds = ds.rio.write_crs("EPSG:4326").rio.write_transform(transform)

    out = Path(f"data/{CURRENT_VERSION}/gradient.zarr")
    if out.exists():
        shutil.rmtree(out)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Build Web-Mercator pyramid; ndpyramid defaults to EPSG:3857
    pyr = pyramid_reproject(
        ds,
        levels=LEVELS,
        resampling="average",
        pixels_per_tile=TILE,
        clear_attrs=True,
    )

    # Disable any default compressor and normalize dtype/chunks
    zarr.storage.default_compressor = None
    strip_and_chunk_tree(pyr)

    # Write consolidated Zarr v2 (what zarr-gl expects)
    pyr.to_zarr(str(out), zarr_format=2, consolidated=True)
    print(f"✅ Wrote UNCOMPRESSED Zarr pyramid to {out}")
    print(f"   • var={VAR_NAME}, dtype=float32, chunks={TILE}×{TILE}, levels={LEVELS}")

if __name__ == "__main__":
    main()