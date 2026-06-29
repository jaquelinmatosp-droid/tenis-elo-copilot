# actualizar_elo.py

import csv
from elo import expected_score, update_rating

JUGADORES_FILE = "jugadores.csv"
PARTIDOS_FILE = "partidos.csv"


def cargar_jugadores():
    jugadores = {}
    with open(JUGADORES_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nombre = row["nombre"]
            rating = float(row["rating_global"])
            jugadores[nombre] = rating
    return jugadores


def guardar_jugadores(jugadores):
    with open(JUGADORES_FILE, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["nombre", "rating_global"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for nombre, rating in jugadores.items():
            writer.writerow({"nombre": nombre, "rating_global": rating})


def procesar_partidos(jugadores):
    with open(PARTIDOS_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            jugador_a = row["jugador_a"]
            jugador_b = row["jugador_b"]
            ganador = row["ganador"]  # debe ser igual a jugador_a o jugador_b

            # ratings actuales
            r_a = jugadores.get(jugador_a, 1500.0)
            r_b = jugadores.get(jugador_b, 1500.0)

            # probabilidad esperada
            e_a = expected_score(r_a, r_b)
            e_b = 1 - e_a

            # resultado real
            if ganador == jugador_a:
                s_a, s_b = 1.0, 0.0
            elif ganador == jugador_b:
                s_a, s_b = 0.0, 1.0
            else:
                # si hay error en el CSV, saltamos
                print(f"Partido con ganador inválido: {row}")
                continue

            # actualizar ratings
            r_a_nuevo = update_rating(r_a, s_a, e_a)
            r_b_nuevo = update_rating(r_b, s_b, e_b)

            jugadores[jugador_a] = r_a_nuevo
            jugadores[jugador_b] = r_b_nuevo

            print(f"{jugador_a} vs {jugador_b} -> gana {ganador}")
            print(f"  {jugador_a}: {r_a:.1f} -> {r_a_nuevo:.1f}")
            print(f"  {jugador_b}: {r_b:.1f} -> {r_b_nuevo:.1f}")
            print("-" * 40)


def main():
    jugadores = cargar_jugadores()
    procesar_partidos(jugadores)
    guardar_jugadores(jugadores)


if __name__ == "__main__":
    main()

