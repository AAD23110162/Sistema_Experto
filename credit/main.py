from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from engine import Scenario, print_header
from credit.adquisicion_de_conocimiento import obtener_hechos_iniciales
from credit.base_de_conocimiento import construir_base_de_conocimiento
from credit.base_de_hechos import construir_base_de_hechos
from credit.interfase_y_usuario import mostrar_inicio, mostrar_resultados
from credit.motor_de_inferencia import ejecutar_inferencia


def construir_escenario() -> Scenario:
    return Scenario(
        key="credit",
        title="Aprobación de Créditos Bancarios",
        intro="Sistema experto para evaluar una solicitud con reglas de riesgo simples.",
        collect_facts=obtener_hechos_iniciales,
        rules=construir_base_de_conocimiento(),
        target_fact="decision",
        target_label="decisión final",
    )


def ejecutar_caso() -> None:
    scenario = construir_escenario()
    print_header()
    mostrar_inicio(scenario)
    hechos_iniciales = obtener_hechos_iniciales()
    base_de_hechos = construir_base_de_hechos(hechos_iniciales)
    resultado = ejecutar_inferencia(base_de_hechos, scenario.rules)
    mostrar_resultados(scenario, resultado)


def main() -> None:
    ejecutar_caso()


if __name__ == "__main__":
    main()