from pathlib import Path
import geopandas as gpd

RAW = Path("data/raw")
BOUNDARY_FILE = RAW / "Frankfurt_am_Main_Stadtteile_5461406520595846193.geojson"
DISTRICT = "Sossenheim"


def load_boundary(path, district):
    gdf = gpd.read_file(path)
    selected = gdf[gdf['STTLNAME'] == district]          # nur die Zeile(n), deren STTLNAME == district ist
    if len(selected) != 1:
        raise ValueError(f"Stadtteil '{district}' {len(selected)}-mal gefunden, erwartet: 1")
    return selected


def main():
    boundary = load_boundary(BOUNDARY_FILE, DISTRICT)
    print(boundary)
    print(boundary.crs)


if __name__ == "__main__":
    main()