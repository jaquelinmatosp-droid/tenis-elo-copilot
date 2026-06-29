# prediccion_partidos.py

import csv
from elo import expected_score, rating_pred

JUGADORES_FILE = "jugadores.csv"


def cargar_jugadores():
    jugadores = {}
    with open(JUGADORES_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nombre = row["nombre"]
            jugadores[nombre] = {
                "global": float(row["rating_global"]),
                "hard": float(row["rating_hard"]),
                "clay": float(row["rating_clay"]),
                "grass": float(row["rating_grass"]),
            }
    return jugadores


def get_surface_key(superficie: str) -> str:
    superficie = superficie.lower()
    if superficie == "hard":
        return "hard"
    if superficie == "clay":
        return "clay"
    if superficie == "grass":
        return "grass"
    return "hard"


def cuota_justa(prob: float) -> float:
    return 1.0 / prob


def valor_cuota(prob: float, cuota_mercado: float) -> float:
    cuota_fair = cuota_justa(prob)
    return (cuota_mercado - cuota_fair) / cuota_fair


def predecir_partido(jugadores, jugador_a, jugador_b, superficie, cuota_a=None, cuota_b=None):
    key = get_surface_key(superficie)

    if jugador_a not in jugadores or jugador_b not in jugadores:
        print("Jugador no encontrado en jugadores.csv")
        return

    r_a_global = jugadores[jugador_a]["global"]
    r_b_global = jugadores[jugador_b]["global"]
    r_a_surface = jugadores[jugador_a][key]
    r_b_surface = jugadores[jugador_b][key]

    r_a_pred = rating_pred(r_a_global, r_a_surface)
    r_b_pred = rating_pred(r_b_global, r_b_surface)

    e_a = expected_score(r_a_pred, r_b_pred)
    e_b = 1 - e_a

    print(f"Predicción {jugador_a} vs {jugador_b} en {superficie}")
    print(f"  Prob {jugador_a}: {e_a:.3f}")
    print(f"  Prob {jugador_b}: {e_b:.3f}")

    if cuota_a is not None and cuota_b is not None:
        cuota_a = float(cuota_a)
        cuota_b = float(cuota_b)
        fair_a = cuota_justa(e_a)
        fair_b = cuota_justa(e_b)
        val_a = valor_cuota(e_a, cuota_a)
        val_b = valor_cuota(e_b, cuota_b)

        print(f"  Cuota mercado {jugador_a}: {cuota_a} (justa: {fair_a:.2f}, valor: {val_a:.2%})")
        print(f"  Cuota mercado {jugador_b}: {cuota_b} (justa: {fair_b:.2f}, valor: {val_b:.2%})")

        if val_a > 0:
            print(f"  -> Valor en {jugador_a}")
        if val_b > 0:
            print(f"  -> Valor en {jugador_b}")


if __name__ == "__main__":
    jugadores = cargar_jugadores()
    # ejemplo de uso:
    predecir_partido(jugadores,
                     jugador_a="Novak Djokovic",
                     jugador_b="Carlos Alcaraz",
                     superficie="hard",
                     cuota_a=1.60,
                     cuota_b=2.40)
