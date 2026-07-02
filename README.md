# Affective Cockpit AI Example Data Package

This repository provides an openly accessible example data package for the manuscript:

**Designing Explainable and Controllable Affective Cockpit AI: Uncertainty Disclosure, User Control, and Calibrated Driver Reliance**

The files are structured to document the study design, variable names, analysis logic, and manuscript-level descriptive patterns for a 2 x 2 driving-simulator experiment on affective cockpit AI.

## Important Data Status

The participant-level and trial-level CSV files in this repository are **synthetic example data** generated from the manuscript description and aggregate results. They are intended to support editorial data-availability checks, transparent variable documentation, and reproducible example analyses.

They should not be interpreted as raw identifiable participant records. Original records that may contain identifiable information, such as simulator logs linked to individuals, facial/video data, or physiological traces, are not included for participant-privacy and institutional-ethics reasons.

## Study Structure Represented

- Design: 2 x 2 between-subjects driving-simulator experiment
- Factors: explanation strategy and intervention authority
- Conditions:
  - No explanation + automatic intervention
  - No explanation + user-controllable intervention
  - Evidence + uncertainty + automatic intervention
  - Evidence + uncertainty + user-controllable intervention
- Participants represented: 192 synthetic participants, 48 per condition
- Trials represented: 2,304 synthetic trial-level observations, 12 per participant
- Scenario blocks: fatigue and stress
- AI correctness: 1,152 correct-inference trials and 1,152 incorrect-inference trials

## Files

| Path | Description |
|---|---|
| `data/participants_synthetic.csv` | Synthetic participant-level data with condition assignment, demographics, scale scores, and aggregate behavioral indices. |
| `data/trials_synthetic.csv` | Synthetic trial-level behavioral data with AI correctness, acceptance, verification, response type, and driving-response indicators. |
| `data/scale_summary_from_manuscript.csv` | Aggregate condition means and standard deviations reported or implied in the manuscript tables. |
| `data/trial_behavior_summary_from_manuscript.csv` | Manuscript-level acceptance, verification, and calibration-gap summary by condition. |
| `data/hypothesis_tests_from_manuscript.csv` | Hypothesis-test summary reported in the manuscript. |
| `data/data_dictionary.csv` | Variable definitions for the synthetic participant-level and trial-level files. |
| `scripts/generate_synthetic_data.py` | Deterministic script used to regenerate the synthetic CSV files. |
| `scripts/reproduce_descriptives.py` | Minimal script to reproduce participant and trial-level descriptive summaries from the CSV files. |
| `DATA_AVAILABILITY_STATEMENT.txt` | Suggested manuscript Data Availability Statement. |

## Reproduce Example Descriptives

From the repository root:

```bash
python scripts/reproduce_descriptives.py
```

The generated summaries should closely match the manuscript-level design and behavioral patterns, while retaining the status of the records as synthetic example data.

## Suggested Citation

Wang, Z., Wang, J., You, F., & Hansen, P. Designing Explainable and Controllable Affective Cockpit AI: Uncertainty Disclosure, User Control, and Calibrated Driver Reliance.
