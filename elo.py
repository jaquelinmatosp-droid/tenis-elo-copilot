
# elo.py

K_DEFAULT = 32  # puedes cambiarlo si quieres

def expected_score(r_a: float, r_b: float) -> float:
    """
    Probabilidad esperada de que A gane contra B según Elo.
    """
    return 1 / (1 + 10 ** ((r_b - r_a) / 400))


def update_rating(r_old: float, score: float, expected: float, k: float = K_DEFAULT) -> float:
    """
    Actualiza el rating Elo de un jugador.
    r_old: rating actual
    score: resultado real (1 si gana, 0 si pierde)
    expected: probabilidad esperada de victoria
    k: factor K
    """
    return r_old + k * (score - expected)
