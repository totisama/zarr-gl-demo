from flask import Flask, send_from_directory, abort, Response
from flask_cors import CORS
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

app = Flask(__name__, static_folder=None)
CORS(app, resources={r"/zarr/*": {"origins": ["http://127.0.0.1:5173", "http://localhost:5173"]}})

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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)