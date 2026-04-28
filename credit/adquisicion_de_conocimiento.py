from __future__ import annotations

from engine import Facts, ask_float, ask_text, ask_yes_no


def obtener_hechos_iniciales() -> Facts:
    print("\nIntroduce la información financiera del solicitante:")
    applicant = ask_text("Nombre del solicitante: ")
    income = ask_float("Ingresos mensuales: ", min_value=0.0)
    debts = ask_float("Deudas actuales: ", min_value=0.0)
    late_payments = ask_yes_no("¿Tiene atrasos previos? (s/n): ")

    return {
        "applicant": applicant,
        "income": income,
        "debts": debts,
        "late_payments": late_payments,
    }