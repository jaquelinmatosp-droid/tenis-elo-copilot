import csv
import requests
from datetime import datetime

# URLs de los partidos del día anterior (ATP + WTA)
ATP_URL = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2024.csv"
WTA_URL = "https://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_matches_2024.csv"

PARTIDOS_FILE = "partidos.csv"

def descargar_csv(url):
    r = requests.get(url)
    r.raise_for_status()
    lines = r.text.splitlines()
    return list(csv.DictReader(lines))

def convertir_partido(row):
    superficie = row.get("surface", "Hard")
    jugador_a = row["winner_name"]
    jugador_b = row["loser_name"]
    ganador = jugador_a
    fecha = row["tourney_date"]

    return {
        "fecha": fecha,
        "superficie": superficie.lower(),
        "jugador_a": jugador_a,
        "jugador_b": jugador_b,
        "ganador": ganador,
        "cuota_a": "",
        "cuota_b": ""
    }

def guardar_partidos(partidos):
    with open(PARTIDOS_FILE, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["fecha","superficie","jugador_a","jugador_b","ganador","cuota_a","cuota_b"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for p in partidos:
            writer.writerow(p)

def main():
    print("Descargando partidos ATP y WTA...")

    atp = descargar_csv(ATP_URL)
    wta = descargar_csv(WTA_URL)

    hoy = datetime.now().strftime("%Y%m%d")

    partidos_hoy = []

    for row in atp:
        if row["tourney_date"] == hoy:
            partidos_hoy.append(convertir_partido(row))

    for row in wta:
        if row["tourney_date"] == hoy:
            partidos_hoy.append(convertir_partido(row))

    if partidos_hoy:
        guardar_partidos(partidos_hoy)
        print(f"Guardados {len(partidos_hoy)} partidos.")
    else:
        print("No hay partidos hoy.")

if __name__ == "__main__":
    main()
