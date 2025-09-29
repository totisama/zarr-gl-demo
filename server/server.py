from flask import Flask, send_from_directory, abort, Response
from flask_cors import CORS
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("DATA_DIR") or (BASE_DIR / "data"))
if not DATA_DIR.exists():
    alt = (BASE_DIR.parent / "data")
    if alt.exists():
        DATA_DIR = alt

app = Flask(__name__, static_folder=None)
CORS(app, resources={r"/zarr/*": {"origins": "*"}})

@app.route("/zarr/<zarr_name>/<path:subpath>")
def zarr_files(zarr_name: str, subpath: str):
    zarr_dir = DATA_DIR / zarr_name
    file_path = zarr_dir / subpath
    if not file_path.exists():
        abort(404)
    return send_from_directory(zarr_dir, subpath, conditional=True)

@app.route("/zarr/<zarr_name>")
def zarr_root(zarr_name: str):
    # Return .zmetadata if it exists
    zarr_dir = DATA_DIR / zarr_name
    return send_from_directory(zarr_dir, ".zmetadata", conditional=True)

@app.get("/healthz")
def healthz():
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)