from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


Facts = Dict[str, Any]


def format_value(value: Any) -> str:
    if isinstance(value, bool):
        return "sí" if value else "no"
    if isinstance(value, float):
        if value.is_integer():
            return f"{value:.0f}"
        return f"{value:.2f}".rstrip("0").rstrip(".")
    return str(value)


@dataclass(frozen=True)
class Condition:
    fact: str
    operator: str
    expected: Any
    label: str

    def evaluate(self, facts: Facts) -> bool:
        if self.fact not in facts:
            return False

        actual = facts[self.fact]

        if self.operator == "==":
            return actual == self.expected
        if self.operator == "!=":
            return actual != self.expected
        if self.operator == ">":
            return actual > self.expected
        if self.operator == ">=":
            return actual >= self.expected
        if self.operator == "<":
            return actual < self.expected
        if self.operator == "<=":
            return actual <= self.expected

        raise ValueError(f"Operador no soportado: {self.operator}")

    def describe(self, facts: Facts) -> str:
        actual = facts.get(self.fact, "desconocido")
        return f"{self.label} (observado: {format_value(actual)}, esperado: {format_value(self.expected)})"


@dataclass(frozen=True)
class Rule:
    name: str
    conditions: List[Condition]
    conclusion_fact: str
    conclusion_value: Any
    conclusion_label: str
    explanation: str

    def matches(self, facts: Facts) -> bool:
        return all(condition.evaluate(facts) for condition in self.conditions)


@dataclass
class InferenceResult:
    facts: Facts
    fired_rules: List[Rule]


@dataclass(frozen=True)
class Scenario:
    key: str
    title: str
    intro: str
    collect_facts: Callable[[], Facts]
    rules: List[Rule]
    target_fact: str
    target_label: str


def ask_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ingresa un valor válido.")


def ask_float(prompt: str, min_value: Optional[float] = None) -> float:
    while True:
        raw_value = input(prompt).strip().replace(",", ".")
        try:
            value = float(raw_value)
        except ValueError:
            print("Ingresa un número válido.")
            continue

        if min_value is not None and value < min_value:
            print(f"El valor debe ser mayor o igual a {format_value(min_value)}.")
            continue

        return value


def ask_yes_no(prompt: str) -> bool:
    while True:
        raw_value = input(prompt).strip().lower()
        if raw_value in {"s", "si", "sí", "y", "yes"}:
            return True
        if raw_value in {"n", "no"}:
            return False
        print("Responde con 's' o 'n'.")


def run_inference(initial_facts: Facts, rules: List[Rule]) -> InferenceResult:
    facts = dict(initial_facts)
    fired_rules: List[Rule] = []

    while True:
        applied_any_rule = False

        for rule in rules:
            if rule.conclusion_fact in facts:
                continue

            if rule.matches(facts):
                facts[rule.conclusion_fact] = rule.conclusion_value
                fired_rules.append(rule)
                applied_any_rule = True

        if not applied_any_rule:
            break

    return InferenceResult(facts=facts, fired_rules=fired_rules)


def print_facts(title: str, facts: Facts) -> None:
    print(f"\n{title}")
    for key, value in facts.items():
        print(f"- {key}: {format_value(value)}")


def print_rule_trace(result: InferenceResult) -> None:
    if not result.fired_rules:
        print("No se activó ninguna regla.")
        return

    print("Reglas activadas:")
    for index, rule in enumerate(result.fired_rules, start=1):
        print(f"{index}. {rule.name}")
        for condition in rule.conditions:
            print(f"   - {condition.describe(result.facts)}")
        print(f"   - Conclusión: {rule.conclusion_label} = {format_value(rule.conclusion_value)}")
        print(f"   - Explicación: {rule.explanation}")


def print_header() -> None:
    print("=" * 72)
    print("SISTEMA EXPERTO - INTERFAZ DE TERMINAL")
    print("=" * 72)


def run_scenario(scenario: Scenario) -> None:
    print(f"\n{scenario.title}")
    print(scenario.intro)

    facts = scenario.collect_facts()
    result = run_inference(facts, scenario.rules)

    print_facts("Base de hechos", result.facts)

    if scenario.target_fact in result.facts:
        print(f"\nResultado: {scenario.target_label} -> {format_value(result.facts[scenario.target_fact])}")
    else:
        print(f"\nResultado: no se pudo derivar una {scenario.target_label} concluyente.")

    print()
    print_rule_trace(result)