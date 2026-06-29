import csv
from elo import expected_score, rating_pred

JUGADORES_FILE = "jugadores.csv"
PARTIDOS_FILE = "partidos.csv"
SALIDA = "predicciones_diarias.csv"

def cargar_jugadores():
    jugadores = {}
    with open(JUGADORES_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            jugadores[row["nombre"]] = {
                "global": float(row["rating_global"]),
                "hard": float(row.get("rating_hard", row["rating_global"])),
                "clay": float(row.get("rating_clay", row["rating_global"])),
                "grass": float(row.get("rating_grass", row["rating_global"]))
            }
    return jugadores

def get_surface_key(superficie):
    superficie = superficie.lower()
    if superficie in ["hard", "clay", "grass"]:
        return superficie
    return "hard"

def predecir(jugadores, partido):
    a = partido["jugador_a"]
    b = partido["jugador_b"]
    superficie = get_surface_key(partido["superficie"])

    r_a = rating_pred(jugadores[a]["global"], jugadores[a][superficie])
    r_b = rating_pred(jugadores[b]["global"], jugadores[b][superficie])

    p_a = expected_score(r_a, r_b)
    p_b = 1 - p_a

    favorito = a if p_a > p_b else b

    return {
        "fecha": partido["fecha"],
        "superficie": superficie,
        "jugador_a": a,
        "jugador_b": b,
        "prob_a": round(p_a, 4),
        "prob_b": round(p_b, 4),
        "favorito": favorito
    }

def main():
    jugadores = cargar_jugadores()

    with open(PARTIDOS_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        partidos = list(reader)

    predicciones = [predecir(jugadores, p) for p in partidos]

    with open(SALIDA, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["fecha","superficie","jugador_a","jugador_b","prob_a","prob_b","favorito"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in predicciones:
            writer.writerow(p)

    print(f"Predicciones generadas en {SALIDA}")

if __name__ == "__main__":
    main()
