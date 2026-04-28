from __future__ import annotations

from engine import Facts


def construir_base_de_hechos(hechos_iniciales: Facts) -> Facts:
    hechos = dict(hechos_iniciales)
    income = hechos["income"]
    debts = hechos["debts"]
    debt_ratio = debts / income if income > 0 else 1.0

    hechos["debt_ratio"] = debt_ratio
    hechos["debt_ratio_percent"] = debt_ratio * 100.0
    hechos["income_ok"] = income > 20000
    hechos["debt_ok"] = debt_ratio <= 0.30
    hechos["no_late_payments"] = not hechos["late_payments"]
    return hechos