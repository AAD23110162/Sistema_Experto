from engine import run_scenario, build_medical_scenario


def main() -> None:
    run_scenario(build_medical_scenario())


if __name__ == "__main__":
    main()