from __future__ import annotations

from engine import Facts, ask_float, ask_yes_no


def obtener_hechos_iniciales() -> Facts:
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