import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def mean(values):
    values = [float(v) for v in values]
    return sum(values) / len(values) if values else float("nan")


def proportion(rows, key):
    return mean([int(r[key]) for r in rows])


def print_participant_summary(participants):
    print("Participant summary by condition")
    print("condition,n,mean_age,female,prior_adas")
    by_condition = defaultdict(list)
    for row in participants:
        by_condition[row["condition_label"]].append(row)
    for condition, rows in by_condition.items():
        female = sum(1 for r in rows if r["gender"] == "female")
        prior = sum(int(r["prior_adas_use"]) for r in rows)
        print(f"{condition},{len(rows)},{mean([r['age'] for r in rows]):.1f},{female},{prior}")


def print_trial_summary(trials):
    print("\nTrial-level acceptance and verification by condition")
    print("condition,accept_correct,accept_incorrect,verification_incorrect,calibration_gap")
    by_condition = defaultdict(list)
    for row in trials:
        by_condition[row["condition_code"]].append(row)
    label_lookup = {
        "NE_AUTO": "No explanation + automatic intervention",
        "NE_CTRL": "No explanation + user-controllable intervention",
        "EU_AUTO": "Evidence + uncertainty + automatic intervention",
        "EU_CTRL": "Evidence + uncertainty + user-controllable intervention",
    }
    for code, rows in by_condition.items():
        correct = [r for r in rows if r["ai_correct"] == "1"]
        incorrect = [r for r in rows if r["ai_correct"] == "0"]
        accept_correct = proportion(correct, "accepted_intervention")
        accept_incorrect = proportion(incorrect, "accepted_intervention")
        verify_incorrect = proportion(incorrect, "verified_before_response")
        gap = accept_correct - accept_incorrect
        print(f"{label_lookup[code]},{accept_correct:.2f},{accept_incorrect:.2f},{verify_incorrect:.2f},{gap:.2f}")


def main():
    participants = read_csv(DATA / "participants_synthetic.csv")
    trials = read_csv(DATA / "trials_synthetic.csv")
    print_participant_summary(participants)
    print_trial_summary(trials)


if __name__ == "__main__":
    main()
