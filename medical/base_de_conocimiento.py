from __future__ import annotations

from engine import Condition, Rule


def construir_base_de_conocimiento() -> list[Rule]:
    return [
        Rule(
            name="Faringitis estreptocócica probable",
            conditions=[
                Condition("high_fever", "==", True, "fiebre mayor a 39°C"),
                Condition("throat_pain", "==", True, "dolor de garganta"),
                Condition("white_plaques", "==", True, "placas blancas"),
            ],
            conclusion_fact="diagnosis",
            conclusion_value="Infección por estreptococo",
            conclusion_label="diagnosis",
            explanation="Los síntomas coinciden con una infección por estreptococo.",
        ),
        Rule(
            name="Faringitis viral probable",
            conditions=[
                Condition("high_fever", "==", False, "ausencia de fiebre alta"),
                Condition("throat_pain", "==", True, "dolor de garganta"),
                Condition("cough", "==", True, "tos"),
                Condition("white_plaques", "==", False, "ausencia de placas blancas"),
            ],
            conclusion_fact="diagnosis",
            conclusion_value="Probable infección viral",
            conclusion_label="diagnosis",
            explanation="La combinación de fiebre moderada, tos y ausencia de placas blancas sugiere un cuadro viral.",
        ),
        Rule(
            name="Tratamiento con penicilina",
            conditions=[
                Condition("diagnosis", "==", "Infección por estreptococo", "diagnóstico de estreptococo"),
            ],
            conclusion_fact="treatment",
            conclusion_value="Penicilina",
            conclusion_label="treatment",
            explanation="La base médica indica que la penicilina es el tratamiento recomendado para estreptococo.",
        ),
        Rule(
            name="Tratamiento sintomático",
            conditions=[
                Condition("diagnosis", "==", "Probable infección viral", "diagnóstico viral"),
            ],
            conclusion_fact="treatment",
            conclusion_value="Tratamiento sintomático e hidratación",
            conclusion_label="treatment",
            explanation="En un cuadro viral, el manejo suele ser sintomático y de soporte.",
        ),
    ]