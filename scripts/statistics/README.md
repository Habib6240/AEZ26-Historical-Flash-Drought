# Statistics
| Script | Purpose |
|---|---|
| `association_tests_reproduction.py` | independent recomputation of all 46 association tests (seed 20261112 permutations, 20260826 bootstrap) |
| `cross_response_exact_permutation.py` | 2,000,000-permutation re-estimate of the six cross-response pairs (seed 20261113) |
| `consensus_event_analysis.py` | consensus-event analysis; asserts that the pre-specification section of `documentation/PRESPEC_consensus_analysis.md` still matches its recorded SHA-256 |
| `seasonal_control_audit.py` | checks 1–3 of the seasonal-control audit (seed 20261112) |
| `response_minimum_window_fraction.py` | post hoc check 4 |

These are independent re-implementations. The original Phase 2G notebook is in `notebooks/`; it fixes its random seeds and reproduces the stored p-values exactly, whereas these scripts use their own seeds and agree with the stored p-values within Monte Carlo error. Long-record trend and source-agreement statistics are in `notebooks/AEZ26_Phase7A_Extended_Robustness_*`. Outputs go to `results/phase1_closure/`.
