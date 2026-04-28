from __future__ import annotations

from engine import Facts


def construir_base_de_hechos(hechos_iniciales: Facts) -> Facts:
    hechos = dict(hechos_iniciales)
    hechos["battery_low"] = hechos["battery_voltage"] < 12.0
    return hechos