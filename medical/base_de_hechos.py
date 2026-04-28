from __future__ import annotations

from engine import Facts


def construir_base_de_hechos(hechos_iniciales: Facts) -> Facts:
    hechos = dict(hechos_iniciales)
    hechos["high_fever"] = hechos["temperature"] > 39.0
    return hechos