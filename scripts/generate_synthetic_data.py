import csv
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RNG = random.Random(260073206)


CONDITIONS = [
    {
        "code": "NE_AUTO",
        "label": "No explanation + automatic intervention",
        "explanation": "no_explanation",
        "control": "automatic",
        "n": 48,
        "mean_age": 30.8,
        "female": 22,
        "prior_adas": 31,
        "scales": {
            "perceived_transparency": (2.64, 0.72),
            "perceived_control": (3.08, 0.76),
            "autonomy_threat": (3.61, 0.81),
            "privacy_concern": (3.10, 0.78),
            "perceived_care": (3.02, 0.74),
            "workload": (3.42, 0.69),
        },
        "accept_correct": 0.72,
        "accept_incorrect": 0.55,
        "verify_correct": 0.10,
        "verify_incorrect": 0.18,
    },
    {
        "code": "NE_CTRL",
        "label": "No explanation + user-controllable intervention",
        "explanation": "no_explanation",
        "control": "user_controllable",
        "n": 48,
        "mean_age": 31.5,
        "female": 24,
        "prior_adas": 30,
        "scales": {
            "perceived_transparency": (2.71, 0.70),
            "perceived_control": (3.78, 0.73),
            "autonomy_threat": (2.94, 0.77),
            "privacy_concern": (3.03, 0.76),
            "perceived_care": (3.36, 0.70),
            "workload": (3.55, 0.72),
        },
        "accept_correct": 0.77,
        "accept_incorrect": 0.48,
        "verify_correct": 0.17,
        "verify_incorrect": 0.29,
    },
    {
        "code": "EU_AUTO",
        "label": "Evidence + uncertainty + automatic intervention",
        "explanation": "evidence_plus_uncertainty",
        "control": "automatic",
        "n": 48,
        "mean_age": 30.2,
        "female": 23,
        "prior_adas": 33,
        "scales": {
            "perceived_transparency": (4.02, 0.68),
            "perceived_control": (3.55, 0.72),
            "autonomy_threat": (3.02, 0.75),
            "privacy_concern": (3.33, 0.80),
            "perceived_care": (3.74, 0.68),
            "workload": (3.68, 0.71),
        },
        "accept_correct": 0.84,
        "accept_incorrect": 0.39,
        "verify_correct": 0.25,
        "verify_incorrect": 0.37,
    },
    {
        "code": "EU_CTRL",
        "label": "Evidence + uncertainty + user-controllable intervention",
        "explanation": "evidence_plus_uncertainty",
        "control": "user_controllable",
        "n": 48,
        "mean_age": 31.1,
        "female": 25,
        "prior_adas": 32,
        "scales": {
            "perceived_transparency": (4.15, 0.66),
            "perceived_control": (4.29, 0.62),
            "autonomy_threat": (2.31, 0.69),
            "privacy_concern": (3.28, 0.79),
            "perceived_care": (4.06, 0.62),
            "workload": (3.62, 0.70),
        },
        "accept_correct": 0.88,
        "accept_incorrect": 0.31,
        "verify_correct": 0.34,
        "verify_incorrect": 0.52,
    },
]


def clipped_normal(mean, sd, low=1.0, high=5.0, digits=2):
    value = RNG.gauss(mean, sd)
    value = max(low, min(high, value))
    return round(value, digits)


def deterministic_flags(n, count):
    flags = [1] * count + [0] * (n - count)
    RNG.shuffle(flags)
    return flags


def generate_ages(n, target_mean):
    ages = [int(round(max(20, min(48, RNG.gauss(target_mean, 5.2))))) for _ in range(n)]
    target_sum = int(round(target_mean * n))
    current_sum = sum(ages)
    guard = 0
    while current_sum != target_sum and guard < 10000:
        guard += 1
        idx = guard % n
        if current_sum < target_sum and ages[idx] < 48:
            ages[idx] += 1
            current_sum += 1
        elif current_sum > target_sum and ages[idx] > 20:
            ages[idx] -= 1
            current_sum -= 1
    RNG.shuffle(ages)
    return ages


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_participants():
    rows = []
    pid = 1
    for condition in CONDITIONS:
        female_flags = deterministic_flags(condition["n"], condition["female"])
        adas_flags = deterministic_flags(condition["n"], condition["prior_adas"])
        ages = generate_ages(condition["n"], condition["mean_age"])
        for i in range(condition["n"]):
            participant_id = f"P{pid:03d}"
            row = {
                "participant_id": participant_id,
                "condition_code": condition["code"],
                "condition_label": condition["label"],
                "explanation_condition": condition["explanation"],
                "intervention_authority": condition["control"],
                "age": ages[i],
                "gender": "female" if female_flags[i] else "male_or_other",
                "valid_driving_license": 1,
                "prior_adas_use": adas_flags[i],
                "baseline_trust_automation": clipped_normal(3.25, 0.72),
                "driving_confidence": clipped_normal(3.60, 0.65),
            }
            for scale, (mean, sd) in condition["scales"].items():
                row[scale] = clipped_normal(mean, sd)
            correct_accept = condition["accept_correct"]
            incorrect_accept = condition["accept_incorrect"]
            row["trust_calibration_index"] = round(correct_accept - incorrect_accept + RNG.gauss(0, 0.08), 2)
            row["overall_acceptance_rate"] = round((correct_accept + incorrect_accept) / 2 + RNG.gauss(0, 0.05), 2)
            rows.append(row)
            pid += 1
    return rows


def allocate_binary(total, probability):
    count = int(round(total * probability))
    values = [1] * count + [0] * (total - count)
    RNG.shuffle(values)
    return values


def generate_trials(participants):
    rows = []
    grouped = {}
    for p in participants:
        grouped.setdefault(p["condition_code"], []).append(p)

    by_code = {c["code"]: c for c in CONDITIONS}
    trial_id = 1
    for code, plist in grouped.items():
        condition = by_code[code]
        correct_slots = []
        incorrect_slots = []
        for p in plist:
            for block in ["fatigue", "stress"]:
                order = [1, 1, 1, 0, 0, 0]
                RNG.shuffle(order)
                for block_trial, is_correct in enumerate(order, start=1):
                    slot = (p, block, block_trial, is_correct)
                    if is_correct:
                        correct_slots.append(slot)
                    else:
                        incorrect_slots.append(slot)

        correct_accepts = allocate_binary(len(correct_slots), condition["accept_correct"])
        incorrect_accepts = allocate_binary(len(incorrect_slots), condition["accept_incorrect"])
        correct_verifies = allocate_binary(len(correct_slots), condition["verify_correct"])
        incorrect_verifies = allocate_binary(len(incorrect_slots), condition["verify_incorrect"])

        for slots, accepts, verifies in [
            (correct_slots, correct_accepts, correct_verifies),
            (incorrect_slots, incorrect_accepts, incorrect_verifies),
        ]:
            for slot, accepted, verified in zip(slots, accepts, verifies):
                p, block, block_trial, is_correct = slot
                inferred_state = block if is_correct else ("stress" if block == "fatigue" else "fatigue")
                if accepted:
                    response = "accept" if condition["control"] == "user_controllable" else "allow_to_continue"
                else:
                    response = RNG.choice(["postpone", "reject"]) if condition["control"] == "user_controllable" else "override"
                response_time = int(max(450, RNG.gauss(1750 if condition["control"] == "user_controllable" else 1250, 420)))
                lane_base = 0.28 if block == "fatigue" else 0.34
                speed_base = 4.8 if block == "fatigue" else 6.2
                rows.append({
                    "trial_id": f"T{trial_id:04d}",
                    "participant_id": p["participant_id"],
                    "condition_code": p["condition_code"],
                    "explanation_condition": p["explanation_condition"],
                    "intervention_authority": p["intervention_authority"],
                    "scenario_block": block,
                    "block_trial": block_trial,
                    "ai_inferred_state": inferred_state,
                    "ai_correct": is_correct,
                    "accepted_intervention": accepted,
                    "verified_before_response": verified,
                    "response": response,
                    "response_time_ms": response_time,
                    "lane_deviation_m": round(max(0.05, RNG.gauss(lane_base, 0.08)), 3),
                    "speed_variability_kmh": round(max(1.2, RNG.gauss(speed_base, 1.1)), 2),
                    "confidence_displayed": round(RNG.uniform(0.61, 0.84), 2)
                    if p["explanation_condition"] == "evidence_plus_uncertainty" else "",
                    "data_type": "synthetic_example",
                })
                trial_id += 1
    rows.sort(key=lambda r: (r["participant_id"], r["scenario_block"], int(r["block_trial"])))
    for i, row in enumerate(rows, start=1):
        row["trial_id"] = f"T{i:04d}"
    return rows


def write_reference_tables():
    scale_rows = []
    for condition in CONDITIONS:
        row = {
            "condition": condition["label"],
            "perceived_transparency_mean": condition["scales"]["perceived_transparency"][0],
            "perceived_control_mean": condition["scales"]["perceived_control"][0],
            "autonomy_threat_mean": condition["scales"]["autonomy_threat"][0],
            "privacy_concern_mean": condition["scales"]["privacy_concern"][0],
            "privacy_concern_sd": condition["scales"]["privacy_concern"][1],
            "perceived_care_mean": condition["scales"]["perceived_care"][0],
            "perceived_care_sd": condition["scales"]["perceived_care"][1],
            "workload_mean": condition["scales"]["workload"][0],
            "workload_sd": condition["scales"]["workload"][1],
        }
        scale_rows.append(row)
    write_csv(DATA / "scale_summary_from_manuscript.csv", scale_rows, list(scale_rows[0].keys()))

    behavior_rows = []
    for condition in CONDITIONS:
        behavior_rows.append({
            "condition": condition["label"],
            "acceptance_when_ai_correct": condition["accept_correct"],
            "acceptance_when_ai_incorrect": condition["accept_incorrect"],
            "verification_on_incorrect_trials": condition["verify_incorrect"],
            "calibration_gap": round(condition["accept_correct"] - condition["accept_incorrect"], 2),
        })
    write_csv(DATA / "trial_behavior_summary_from_manuscript.csv", behavior_rows, list(behavior_rows[0].keys()))

    hypothesis_rows = [
        {
            "hypothesis": "H1",
            "test": "Explanation -> perceived transparency",
            "result": "F(1,188) = 54.62, p < .001, partial eta squared = .23",
            "interpretation": "Supported",
        },
        {
            "hypothesis": "H2",
            "test": "Explanation with uncertainty -> trust calibration",
            "result": "F(1,188) = 31.45, p < .001, partial eta squared = .14",
            "interpretation": "Supported",
        },
        {
            "hypothesis": "H3",
            "test": "User control -> perceived control and acceptance",
            "result": "F(1,188) = 38.17, p < .001, partial eta squared = .17",
            "interpretation": "Supported",
        },
        {
            "hypothesis": "H4",
            "test": "Perceived control mediation",
            "result": "indirect b = .19, 95% CI [.11, .29]",
            "interpretation": "Supported",
        },
        {
            "hypothesis": "H5",
            "test": "Explanation x AI correctness on overreliance",
            "result": "F(1,188) = 8.72, p = .004, partial eta squared = .04",
            "interpretation": "Supported",
        },
    ]
    write_csv(DATA / "hypothesis_tests_from_manuscript.csv", hypothesis_rows, list(hypothesis_rows[0].keys()))


def write_dictionary():
    rows = [
        ("participant_id", "Synthetic participant identifier; no real identity is included.", "participants/trials"),
        ("condition_code", "Experimental condition code: NE_AUTO, NE_CTRL, EU_AUTO, or EU_CTRL.", "participants/trials"),
        ("condition_label", "Human-readable condition label.", "participants"),
        ("explanation_condition", "No explanation or evidence-plus-uncertainty explanation.", "participants/trials"),
        ("intervention_authority", "Automatic intervention or user-controllable intervention.", "participants/trials"),
        ("age", "Synthetic age generated to match the manuscript-level participant profile.", "participants"),
        ("gender", "Synthetic gender category used only for example-data structure.", "participants"),
        ("valid_driving_license", "All synthetic participants are coded as licensed drivers.", "participants"),
        ("prior_adas_use", "Synthetic prior ADAS-use indicator matched to condition-level counts.", "participants"),
        ("baseline_trust_automation", "Synthetic baseline trust in automation score, 1-5.", "participants"),
        ("driving_confidence", "Synthetic driving confidence score, 1-5.", "participants"),
        ("perceived_transparency", "Synthetic scale score, 1-5.", "participants"),
        ("perceived_control", "Synthetic scale score, 1-5.", "participants"),
        ("autonomy_threat", "Synthetic scale score, 1-5.", "participants"),
        ("privacy_concern", "Synthetic scale score, 1-5.", "participants"),
        ("perceived_care", "Synthetic scale score, 1-5.", "participants"),
        ("workload", "Synthetic workload score, 1-5.", "participants"),
        ("trust_calibration_index", "Synthetic participant-level behavioral alignment index.", "participants"),
        ("overall_acceptance_rate", "Synthetic participant-level acceptance proportion.", "participants"),
        ("trial_id", "Synthetic trial identifier.", "trials"),
        ("scenario_block", "Fatigue or stress driving block.", "trials"),
        ("block_trial", "Trial number within the fatigue or stress block.", "trials"),
        ("ai_inferred_state", "AI-presented affective-state inference.", "trials"),
        ("ai_correct", "Whether the scripted AI inference matched the scenario and cue pattern.", "trials"),
        ("accepted_intervention", "Whether the intervention was accepted or allowed to continue.", "trials"),
        ("verified_before_response", "Whether the participant opened the evidence/status panel before responding.", "trials"),
        ("response", "accept, postpone, reject, allow_to_continue, or override.", "trials"),
        ("response_time_ms", "Synthetic response time in milliseconds.", "trials"),
        ("lane_deviation_m", "Synthetic post-prompt lane deviation metric.", "trials"),
        ("speed_variability_kmh", "Synthetic post-prompt speed variability metric.", "trials"),
        ("confidence_displayed", "Displayed confidence value in explanation conditions; blank otherwise.", "trials"),
        ("data_type", "Always synthetic_example.", "trials"),
    ]
    write_csv(DATA / "data_dictionary.csv", [
        {"variable": v, "description": d, "file": f} for v, d, f in rows
    ], ["variable", "description", "file"])


def main():
    DATA.mkdir(exist_ok=True)
    participants = generate_participants()
    trials = generate_trials(participants)
    write_csv(DATA / "participants_synthetic.csv", participants, list(participants[0].keys()))
    write_csv(DATA / "trials_synthetic.csv", trials, list(trials[0].keys()))
    write_reference_tables()
    write_dictionary()
    print(f"Wrote {len(participants)} participant rows and {len(trials)} trial rows to {DATA}")


if __name__ == "__main__":
    main()
