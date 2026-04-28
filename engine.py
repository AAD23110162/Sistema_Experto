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


def build_medical_scenario() -> Scenario:
    def collect_facts() -> Facts:
        print("\nIntroduce los datos del paciente:")
        temperature = ask_float("Temperatura corporal en °C: ", min_value=30.0)
        throat_pain = ask_yes_no("¿Tiene dolor de garganta? (s/n): ")
        white_plaques = ask_yes_no("¿Presenta placas blancas en la garganta? (s/n): ")
        cough = ask_yes_no("¿Tiene tos? (s/n): ")

        return {
            "temperature": temperature,
            "throat_pain": throat_pain,
            "white_plaques": white_plaques,
            "cough": cough,
        }

    rules = [
        Rule(
            name="Faringitis estreptocócica probable",
            conditions=[
                Condition("temperature", ">", 39.0, "fiebre mayor a 39°C"),
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
                Condition("temperature", "<", 39.0, "fiebre menor a 39°C"),
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

    return Scenario(
        key="medical",
        title="Diagnóstico Médico",
        intro="Sistema experto para infecciones de garganta con explicación de diagnóstico y tratamiento.",
        collect_facts=collect_facts,
        rules=rules,
        target_fact="treatment",
        target_label="tratamiento sugerido",
    )


def build_automotive_scenario() -> Scenario:
    def collect_facts() -> Facts:
        print("\nIntroduce los datos del vehículo:")
        vehicle = ask_text("Marca y modelo del auto: ")
        battery_voltage = ask_float("Voltaje de la batería: ", min_value=0.0)
        starter_click = ask_yes_no("¿El motor de arranque hace 'clic'? (s/n): ")
        dashboard_flicker = ask_yes_no("¿Las luces del tablero parpadean? (s/n): ")

        return {
            "vehicle": vehicle,
            "battery_voltage": battery_voltage,
            "starter_click": starter_click,
            "dashboard_flicker": dashboard_flicker,
            "battery_low": battery_voltage < 12.0,
        }

    rules = [
        Rule(
            name="Batería con bajo voltaje",
            conditions=[Condition("battery_voltage", "<", 12.0, "voltaje menor a 12V")],
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

    return Scenario(
        key="automotive",
        title="Diagnóstico Automotriz",
        intro="Sistema experto para detectar fallas eléctricas básicas en el taller.",
        collect_facts=collect_facts,
        rules=rules,
        target_fact="recommendation",
        target_label="recomendación final",
    )


def build_credit_scenario() -> Scenario:
    def collect_facts() -> Facts:
        print("\nIntroduce la información financiera del solicitante:")
        applicant = ask_text("Nombre del solicitante: ")
        income = ask_float("Ingresos mensuales: ", min_value=0.0)
        debts = ask_float("Deudas actuales: ", min_value=0.0)
        late_payments = ask_yes_no("¿Tiene atrasos previos? (s/n): ")

        debt_ratio = debts / income if income > 0 else 1.0

        return {
            "applicant": applicant,
            "income": income,
            "debts": debts,
            "late_payments": late_payments,
            "debt_ratio": debt_ratio,
            "debt_ratio_percent": debt_ratio * 100.0,
            "income_ok": income > 20000,
            "debt_ok": debt_ratio <= 0.30,
        }

    rules = [
        Rule(
            name="Aprobación de crédito",
            conditions=[
                Condition("income_ok", "==", True, "ingresos mayores a 20,000"),
                Condition("debt_ok", "==", True, "deuda menor o igual al 30% del ingreso"),
                Condition("late_payments", "==", False, "sin atrasos previos"),
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
            conditions=[Condition("late_payments", "==", True, "atrasos previos en pagos")],
            conclusion_fact="decision",
            conclusion_value="Rechazado",
            conclusion_label="decision",
            explanation="El historial con atrasos aumenta el riesgo y bloquea la aprobación.",
        ),
    ]

    return Scenario(
        key="credit",
        title="Aprobación de Créditos Bancarios",
        intro="Sistema experto para evaluar una solicitud con reglas de riesgo simples.",
        collect_facts=collect_facts,
        rules=rules,
        target_fact="decision",
        target_label="decisión final",
    )


def get_scenarios() -> List[Scenario]:
    return [
        build_medical_scenario(),
        build_automotive_scenario(),
        build_credit_scenario(),
    ]


def print_header() -> None:
    print("=" * 72)
    print("SISTEMA EXPERTO - INTERFAZ DE TERMINAL")
    print("=" * 72)
    print("Selecciona uno de los tres ejemplos disponibles y responde las preguntas.")


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