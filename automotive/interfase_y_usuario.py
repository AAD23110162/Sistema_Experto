from __future__ import annotations

from engine import InferenceResult, Scenario, print_facts, print_rule_trace


def mostrar_inicio(scenario: Scenario) -> None:
    print(f"\n{scenario.title}")
    print(scenario.intro)


def mostrar_resultados(scenario: Scenario, result: InferenceResult) -> None:
    print_facts("Base de hechos", result.facts)

    if scenario.target_fact in result.facts:
        print(f"\nResultado: {scenario.target_label} -> {result.facts[scenario.target_fact]}")
    else:
        print(f"\nResultado: no se pudo derivar una {scenario.target_label} concluyente.")

    print()
    print_rule_trace(result)