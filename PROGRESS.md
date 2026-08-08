# Project Progress

## What this is
Verified chain-of-thought distillation for the NVIDIA Nemotron Reasoning
Challenge. Generate reasoning traces, keep only correct ones, train a LoRA.
Goal: match the notebooks' accuracy (~0.72), provable via Kaggle late submission.

## All six solvers built + measured (Qwen 7B, self-tested)
| Type | Result |
|------|--------|
| numeral_conversion | ~93% |
| gravitational_constant | ~87% |
| unit_conversion | ~75% |
| text_encryption | 0% -> 90% (full cipher cracker + vocab) |
| bit_manipulation | 8% -> 48% Python-alone (boolean fn learner) |
| equation_transformation | 0% -> 5% (operator-focus hint; the hard one) |

Solvers in `vcd/solvers/`, registry in `vcd/solvers/registry.py`.
Support: `vcd/data.py`, `vcd/detect.py`, `vcd/vocab.py`, `vcd/verify/extract.py`.

## Key findings (interview-worthy)
- Model IGNORES/OVERRIDES correct Python answers: bit puzzles went 48%
  Python-alone -> 32% when the model "helped". Rule: use the model ONLY
  where Python fails, never to double-check correct Python output.
- Bit solver overfits on 8-9 examples -> some wrong answers, but the verify
  step filters those from training data (that's the whole "verified" point).
- Equation transformation genuinely underdetermined (why the field got ~13%).
  Operator-focus hint beat 0% but stays weakest; 7B < 30B is part of the gap.

## Setup gotchas
- Qwen2.5-7B-Instruct via vLLM, dtype=float16 (T4 needs float16 NOT bfloat16),
  tensor_parallel_size=2, gpu_memory_utilization=0.90
- Kaggle: clone repo, add competition data as input, call set_vocab() before use
- 3,648 verified easy-type traces already generated (traces.jsonl, on laptop)
- Competition CLOSED but late submission gives a real self-visible score

## Next steps
1. Generate full verified dataset: run all 6 solvers across train.csv, keep correct
2. Combine + sample per-type (like notebook: ~300-700 per type)
3. Phase 3: train LoRA on Nemotron-30B-A3B  <-- NEEDS competition GPU (unconfirmed)
4. Phase 4: benchmark (vLLM latency/throughput/VRAM) + late submission for real score