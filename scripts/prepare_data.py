from pathlib import Path
import geopandas as gpd
import pandas as pd
import math
from shapely.geometry import box

RAW = Path("data/raw")
BOUNDARY_FILE = RAW / "Frankfurt_am_Main_Stadtteile_5461406520595846193.geojson"
DISTRICT = "Sossenheim"
STATIONS_FILE = RAW / "Ladesaeulenregister_BNetzA_2026-11-12.csv"
STATION_COLUMNS = ["Ladeeinrichtungs-ID", "Betreiber", "Postleitzahl", "Ort", "Straße", "Hausnummer", "Art der Ladeeinrichtung", "Nennleistung Ladeeinrichtung [kW]", "Breitengrad", "Längengrad", "Status", "Anzahl Ladepunkte"]
STATUS_BETRIEB = "In Betrieb"
OUT = Path("data")

def load_boundary(path, district):
    gdf = gpd.read_file(path)
    selected = gdf[gdf['STTLNAME'] == district]          # nur die Zeile(n), deren STTLNAME == district ist
    if len(selected) != 1:
        raise ValueError(f"Stadtteil '{district}' {len(selected)}-mal gefunden, erwartet: 1")
    return selected


def load_stations(path, status_betrieb):
    df = pd.read_csv(path, skiprows=10, sep=';', decimal=',', encoding='cp1252', dtype={"Postleitzahl": str}, usecols=STATION_COLUMNS, )
    df = df[df['Status'] == status_betrieb] # nur die Zeilen, deren Status == status_Betrieb ist
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(x=df['Längengrad'], y=df['Breitengrad']),
        crs="EPSG:4326",
    )
    return gdf


def clip_to_boundary(stations, boundary):
    if stations.crs != boundary.crs:
        raise ValueError(f"CRS passen nicht: {stations.crs} vs. {boundary.crs}")
    return gpd.clip(stations, boundary)
    

def make_grid(boundary, size):
    boundary_3035 = boundary.to_crs("EPSG:3035")
    minx, miny, maxx, maxy = boundary_3035.total_bounds

    x_start = math.floor(minx / size) * size
    y_start = math.floor(miny / size) * size
    x_end = math.ceil(maxx / size) * size
    y_end = math.ceil(maxy / size) * size

    cells = []
    for x in range(int(x_start), int(x_end), size):
        for y in range(int(y_start), int(y_end), size):
            cells.append({
                "cell_id": f"CRS3035RES{size}mN{y}E{x}",
                "parent_500m": f"CRS3035RES500mN{(y // 500) * 500}E{(x // 500) * 500}",
                "geometry": box(x, y, x + size, y + size),
            })

    grid = gpd.GeoDataFrame(cells, crs="EPSG:3035")
    return grid[grid.intersects(boundary_3035.geometry.iloc[0])]



def assign_cells(stations, grid):
    stations_3035 = stations.to_crs(grid.crs)
    joined = gpd.sjoin(stations_3035, grid[["cell_id", "geometry"]], how="left", predicate="within")
    joined = joined.drop(columns="index_right")

    if joined['cell_id'].isnull().any():
        raise ValueError("Es gibt Stationen, die keiner Gitterzelle zugeordnet werden konnten.")

    if len(joined) != len(stations):
        raise ValueError("Die Anzahl der Stationen nach dem Join stimmt nicht mit der ursprünglichen Anzahl überein.")
    return joined


def main():
    boundary = load_boundary(BOUNDARY_FILE, DISTRICT)
    l_stations = load_stations(STATIONS_FILE, STATUS_BETRIEB)
    c_stations = clip_to_boundary(l_stations, boundary)
    print("Anzahl der Ladesäulen im Stadtteil:", len(c_stations))

    # Assign cells to stations and create a grid
    grid = make_grid(boundary, 250)
    assigned = assign_cells(c_stations, grid)
    print("Anzahl der zugewiesenen Gitterzellen:", assigned["cell_id"].nunique())

    # Dataoutput
    boundary.to_crs("EPSG:4326").to_file(OUT / "area_boundary.geojson")
    grid.to_crs("EPSG:4326").to_file(OUT / "grid_250m.geojson")
    assigned.to_crs("EPSG:4326").to_file(OUT / "stations.geojson")
    print(assigned["Betreiber"].value_counts())
    print(assigned.groupby("Betreiber")["Anzahl Ladepunkte"].sum())


if __name__ == "__main__":
    main()