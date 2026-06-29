# actualizar_elo.py

import csv
from elo import expected_score, update_rating, rating_pred

JUGADORES_FILE = "jugadores.csv"
PARTIDOS_FILE = "partidos.csv"


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


def guardar_jugadores(jugadores):
    with open(JUGADORES_FILE, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["nombre", "rating_global", "rating_hard", "rating_clay", "rating_grass"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for nombre, r in jugadores.items():
            writer.writerow({
                "nombre": nombre,
                "rating_global": r["global"],
                "rating_hard": r["hard"],
                "rating_clay": r["clay"],
                "rating_grass": r["grass"],
            })


def get_surface_key(superficie: str) -> str:
    superficie = superficie.lower()
    if superficie == "hard":
        return "hard"
    if superficie == "clay":
        return "clay"
    if superficie == "grass":
        return "grass"
    return "hard"  # por defecto


def procesar_partidos(jugadores):
    with open(PARTIDOS_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            jugador_a = row["jugador_a"]
            jugador_b = row["jugador_b"]
            ganador = row["ganador"]
            superficie = row["superficie"]

            if jugador_a not in jugadores:
                jugadores[jugador_a] = {"global": 1500.0, "hard": 1500.0, "clay": 1500.0, "grass": 1500.0}
            if jugador_b not in jugadores:
                jugadores[jugador_b] = {"global": 1500.0, "hard": 1500.0, "clay": 1500.0, "grass": 1500.0}

            key = get_surface_key(superficie)

            r_a_global = jugadores[jugador_a]["global"]
            r_b_global = jugadores[jugador_b]["global"]
            r_a_surface = jugadores[jugador_a][key]
            r_b_surface = jugadores[jugador_b][key]

            r_a_pred = rating_pred(r_a_global, r_a_surface)
            r_b_pred = rating_pred(r_b_global, r_b_surface)

            e_a = expected_score(r_a_pred, r_b_pred)
            e_b = 1 - e_a

            if ganador == jugador_a:
                s_a, s_b = 1.0, 0.0
            elif ganador == jugador_b:
                s_a, s_b = 0.0, 1.0
            else:
                print(f"Ganador inválido en fila: {row}")
                continue

            jugadores[jugador_a]["global"] = update_rating(r_a_global, s_a, e_a)
            jugadores[jugador_b]["global"] = update_rating(r_b_global, s_b, e_b)

            jugadores[jugador_a][key] = update_rating(r_a_surface, s_a, e_a)
            jugadores[jugador_b][key] = update_rating(r_b_surface, s_b, e_b)

            print(f"{jugador_a} vs {jugador_b} ({superficie}) -> gana {ganador}")
            print(f"  {jugador_a} global: {r_a_global:.1f} -> {jugadores[jugador_a]['global']:.1f}")
            print(f"  {jugador_b} global: {r_b_global:.1f} -> {jugadores[jugador_b]['global']:.1f}")
            print("-" * 40)


def main():
    jugadores = cargar_jugadores()
    procesar_partidos(jugadores)
    guardar_jugadores(jugadores)


if __name__ == "__main__":
    main()
