from __future__ import annotations

from engine import Condition, Rule


def construir_base_de_conocimiento() -> list[Rule]:
    return [
        Rule(
            name="Aprobación de crédito",
            conditions=[
                Condition("income_ok", "==", True, "ingresos mayores a 20,000"),
                Condition("debt_ok", "==", True, "deuda menor o igual al 30% del ingreso"),
                Condition("no_late_payments", "==", True, "sin atrasos previos"),
            ],
            conclusion_fact="decision",
            conclusion_value="Aprobado",
            conclusion_label="decision",
            explanation="El solicitante cumple con la política de riesgo del banco.",
        ),
        Rule(
            name="Rechazo por ingresos bajos",
            conditions=[Condition("income_ok", "==", False, "ingresos no suficientes")],
            conclusion_fact="decision",
            conclusion_value="Rechazado",
            conclusion_label="decision",
            explanation="Los ingresos no alcanzan el umbral mínimo para este producto financiero.",
        ),
        Rule(
            name="Rechazo por exceso de deuda",
            conditions=[Condition("debt_ok", "==", False, "deuda por encima del 30% permitido")],
            conclusion_fact="decision",
            conclusion_value="Rechazado",
            conclusion_label="decision",
            explanation="La proporción de deuda supera el límite permitido por la política de crédito.",
        ),
        Rule(
            name="Rechazo por atrasos previos",
            conditions=[Condition("no_late_payments", "==", False, "atrasos previos en pagos")],
            conclusion_fact="decision",
            conclusion_value="Rechazado",
            conclusion_label="decision",
            explanation="El historial con atrasos aumenta el riesgo y bloquea la aprobación.",
        ),
    ]