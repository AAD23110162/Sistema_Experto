from __future__ import annotations

from engine import Facts, ask_float, ask_text, ask_yes_no


MODEL_OPTIONS = [
    "Ford Fiesta",
    "Chevrolet Aveo",
    "Nissan Versa",
    "Volkswagen Jetta",
    "Toyota Corolla",
]


def elegir_modelo() -> str:
    print("\nSelecciona el modelo del auto:")
    for index, model in enumerate(MODEL_OPTIONS, start=1):
        print(f"{index}. {model}")

    while True:
        raw_value = ask_text("Ingresa el número de modelo: ")
        if raw_value.isdigit():
            selected = int(raw_value)
            if 1 <= selected <= len(MODEL_OPTIONS):
                return MODEL_OPTIONS[selected - 1]
        print("Opción inválida. Ingresa solo el número de la lista.")


def obtener_hechos_iniciales() -> Facts:
    print("\nIntroduce los datos del vehículo:")
    vehicle = elegir_modelo()
    battery_voltage = ask_float("Voltaje de la batería: ", min_value=0.0)
    starter_click = ask_yes_no("¿El motor de arranque hace 'clic'? (s/n): ")
    dashboard_flicker = ask_yes_no("¿Las luces del tablero parpadean? (s/n): ")

    return {
        "vehicle": vehicle,
        "battery_voltage": battery_voltage,
        "starter_click": starter_click,
        "dashboard_flicker": dashboard_flicker,
    }