from __future__ import annotations

from engine import Facts, InferenceResult, Rule, run_inference


def ejecutar_inferencia(facts: Facts, rules: list[Rule]) -> InferenceResult:
    return run_inference(facts, rules)