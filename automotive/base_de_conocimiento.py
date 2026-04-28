from __future__ import annotations

from engine import Condition, Rule


def construir_base_de_conocimiento() -> list[Rule]:
    return [
        Rule(
            name="Batería con bajo voltaje",
            conditions=[Condition("battery_low", "==", True, "voltaje menor a 12V")],
            conclusion_fact="problem",
            conclusion_value="Batería con bajo voltaje",
            conclusion_label="problem",
            explanation="Un voltaje por debajo de 12V indica una batería debilitada.",
        ),
        Rule(
            name="Batería descargada probable",
            conditions=[
                Condition("starter_click", "==", True, "motor de arranque con clic"),
                Condition("dashboard_flicker", "==", True, "luces del tablero parpadean"),
                Condition("battery_low", "==", True, "batería por debajo de 12V"),
            ],
            conclusion_fact="diagnosis",
            conclusion_value="Batería descargada",
            conclusion_label="diagnosis",
            explanation="El clic del arranque junto con el parpadeo del tablero apunta a una batería descargada.",
        ),
        Rule(
            name="Recomendación de reemplazo",
            conditions=[Condition("diagnosis", "==", "Batería descargada", "diagnóstico de batería descargada")],
            conclusion_fact="recommendation",
            conclusion_value="Cambiar la batería y revisar el sistema de carga",
            conclusion_label="recommendation",
            explanation="Con una batería descargada, la recomendación inmediata es reemplazarla y verificar alternador/cables.",
        ),
    ]