from pathlib import Path
import geopandas as gpd
import pandas as pd

RAW = Path("data/raw")
BOUNDARY_FILE = RAW / "Frankfurt_am_Main_Stadtteile_5461406520595846193.geojson"
DISTRICT = "Sossenheim"
STATIONS_FILE = RAW / "Ladesaeulenregister_BNetzA_2026-11-12.csv"
STATION_COLUMNS = ["Ladeeinrichtungs-ID", "Betreiber", "Postleitzahl", "Ort", "Straße", "Hausnummer", "Art der Ladeeinrichtung", "Nennleistung Ladeeinrichtung [kW]", "Breitengrad", "Längengrad", "Status", "Anzahl Ladepunkte"]
STATUS_BETRIEB = "In Betrieb"

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
    
    
def main():
    boundary = load_boundary(BOUNDARY_FILE, DISTRICT)
    l_stations = load_stations(STATIONS_FILE, STATUS_BETRIEB)
    c_stations = clip_to_boundary(l_stations, boundary)
    print(c_stations)
    print("Anzahl der Ladesäulen im Stadtteil:", len(c_stations))
    print(c_stations.crs)
    c_stations.to_file("data/tmp_stations.geojson")
    


if __name__ == "__main__":
    main()