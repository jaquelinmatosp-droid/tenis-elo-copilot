name: Actualizar Elo diario

on:
  schedule:
    - cron: "0 6 * * *"
  workflow_dispatch:

jobs:
  run-elo:
    runs-on: ubuntu-latest

    steps:
      - name: Descargar repositorio
        uses: actions/checkout@v3

      - name: Instalar Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Descargar partidos del día
        run: python descargar_partidos_diarios.py

      - name: Ejecutar Elo
        run: python actualizar_elo.py

      - name: Guardar cambios
        uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: "Elo actualizado automáticamente"
