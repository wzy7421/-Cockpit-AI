# Full Synthetic Data Generation

This repository contains sample CSV files for quick inspection and a deterministic generation script for the full synthetic example dataset.

To generate the full participant-level and trial-level CSV files, run:

```bash
python scripts/generate_synthetic_data.py
```

This creates:

- `data/participants_synthetic.csv`: 192 synthetic participants, 48 per experimental condition.
- `data/trials_synthetic.csv`: 2,304 synthetic trial-level observations, 12 trials per participant.
- `data/scale_summary_from_manuscript.csv`: manuscript-level scale summaries.
- `data/trial_behavior_summary_from_manuscript.csv`: acceptance, verification, and calibration-gap summaries.
- `data/hypothesis_tests_from_manuscript.csv`: hypothesis-test summary.
- `data/data_dictionary.csv`: variable definitions.

The generated participant profile matches the manuscript design:

| Condition | n | Mean age | Female | Prior ADAS use |
|---|---:|---:|---:|---:|
| No explanation + automatic intervention | 48 | 30.8 | 22 | 31 |
| No explanation + user-controllable intervention | 48 | 31.5 | 24 | 30 |
| Evidence + uncertainty + automatic intervention | 48 | 30.2 | 23 | 33 |
| Evidence + uncertainty + user-controllable intervention | 48 | 31.1 | 25 | 32 |

The generated trial-level behavioral summaries match the manuscript-level pattern:

| Condition | Acceptance when AI correct | Acceptance when AI incorrect | Verification on incorrect trials | Calibration gap |
|---|---:|---:|---:|---:|
| No explanation + automatic intervention | 0.72 | 0.55 | 0.18 | 0.17 |
| No explanation + user-controllable intervention | 0.77 | 0.48 | 0.29 | 0.29 |
| Evidence + uncertainty + automatic intervention | 0.84 | 0.39 | 0.37 | 0.45 |
| Evidence + uncertainty + user-controllable intervention | 0.88 | 0.31 | 0.52 | 0.57 |

These data are synthetic example records. They are provided to document the study structure, variable schema, and analysis logic. They are not raw identifiable participant records.
