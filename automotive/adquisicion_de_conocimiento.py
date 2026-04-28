from __future__ import annotations

from engine import Facts, ask_float, ask_text, ask_yes_no


def obtener_hechos_iniciales() -> Facts:
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
    }