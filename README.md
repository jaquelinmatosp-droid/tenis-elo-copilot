# Sistema Elo para tenis

Este proyecto calcula y actualiza ratings Elo para jugadores de tenis a partir de un archivo de partidos.

## Archivos

- `elo.py`: funciones de cálculo del Elo.
- `actualizar_elo.py`: script que lee partidos y actualiza los ratings.
- `jugadores.csv`: lista de jugadores y su rating global.
- `partidos.csv`: histórico de partidos (fecha, jugador_a, jugador_b, ganador).

## Uso

1. Edita `jugadores.csv` para añadir o modificar jugadores.
2. Añade partidos nuevos a `partidos.csv`.
3. Ejecuta:

   ```bash
   python actualizar_elo.py

