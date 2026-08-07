from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DEFAULT_SCENARIOS_PATH = PROJECT_ROOT / "tests" / "scenarios.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run fixed prompt-coaching scenarios and write usage logs."
    )
    parser.add_argument(
        "--experiment",
        required=True,
        help="Experiment name written to logs, e.g. baseline or prompt_v2.",
    )
    parser.add_argument(
        "--scenarios",
        default=str(DEFAULT_SCENARIOS_PATH),
        help="Path to the scenario JSON file.",
    )
    parser.add_argument(
        "--case-id",
        default=None,
        help="Run only one case_id. By default, all cases run.",
    )
    parser.add_argument(
        "--skip-coach",
        action="store_true",
        help="Run analyzer only. Useful for quick analyzer-specific checks.",
    )
    return parser.parse_args()


def load_scenarios(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as file:
        scenarios = json.load(file)

    if not isinstance(scenarios, list):
        raise ValueError("Scenario file must contain a list.")

    return scenarios


def run_scenario(
    scenario: dict[str, Any],
    *,
    experiment: str,
    skip_coach: bool,
) -> None:
    from models.initial_state import create_initial_state
    from nodes.analyzer import analyze_prompt
    from nodes.coach import create_coaching_message

    case_id = scenario["case_id"]
    session_id = f"{experiment}_{case_id}"
    state = create_initial_state()

    print(f"Running {case_id}: {scenario.get('name', '')}")

    for index, prompt in enumerate(scenario["turns"], start=1):
        print(f"  turn {index}: {len(prompt)} chars")
        state = analyze_prompt(
            state,
            prompt,
            source="evaluation",
            experiment=experiment,
            case_id=case_id,
            session_id=session_id,
            turn_index=index,
        )

        if not skip_coach:
            create_coaching_message(
                state,
                source="evaluation",
                experiment=experiment,
                case_id=case_id,
                session_id=session_id,
                turn_index=index,
            )


def main() -> None:
    args = parse_args()
    scenarios = load_scenarios(Path(args.scenarios))

    if args.case_id is not None:
        scenarios = [
            scenario
            for scenario in scenarios
            if scenario.get("case_id") == args.case_id
        ]
        if not scenarios:
            raise ValueError(f"Unknown case_id: {args.case_id}")

    for scenario in scenarios:
        run_scenario(
            scenario,
            experiment=args.experiment,
            skip_coach=args.skip_coach,
        )

    print("Done. Usage logs were written to logs/llm_usage.jsonl.")


if __name__ == "__main__":
    main()
