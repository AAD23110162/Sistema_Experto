from __future__ import annotations

import argparse

from engine import ask_yes_no, get_scenarios, print_header, run_scenario


def choose_scenario() -> str | None:
    scenarios = get_scenarios()

    print("\nCasos disponibles:")
    for index, scenario in enumerate(scenarios, start=1):
        print(f"{index}. {scenario.title}")
    print("0. Salir")

    while True:
        raw_value = input("Elige una opción: ").strip()
        if raw_value == "0":
            return None
        if raw_value.isdigit():
            selected = int(raw_value)
            if 1 <= selected <= len(scenarios):
                return scenarios[selected - 1].key
        print("Opción inválida. Intenta otra vez.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sistema experto de terminal con tres ejemplos.")
    return parser.parse_args()


def main() -> None:
    parse_args()
    scenarios = {scenario.key: scenario for scenario in get_scenarios()}

    print_header()

    while True:
        selected_key = choose_scenario()
        if selected_key is None:
            print("\nSaliendo del sistema experto.")
            return

        run_scenario(scenarios[selected_key])

        if not ask_yes_no("\n¿Deseas evaluar otro caso? (s/n): "):
            print("\nSaliendo del sistema experto.")
            return


if __name__ == "__main__":
    main()