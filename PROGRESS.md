# Project Progress

## What this is
Verified chain-of-thought distillation for the NVIDIA Nemotron Reasoning
Challenge. Generate reasoning traces, keep only correct ones, train a LoRA.
Goal: match the notebooks' accuracy (~0.72), provable via Kaggle late submission.

## Done
- **Solvers (6 types)** — all built and tested, in `vcd/solvers/`
  - numeral, unit, gravitational: simple verify, pass at 76-93%
  - text_encryption: full cipher cracker + vocab gap-fill. **0% -> 90%**
  - bit_manipulation: per-bit boolean function learner. **8% -> 48% Python-alone**
  - equation_transformation: verify only, NO solver yet (the hard one)
- **Registry** (`vcd/solvers/registry.py`) — one lookup for all solvers
- **Data loader** (`vcd/data.py`), **type detector** (`vcd/detect.py`)
- **Vocab harvester** (`vcd/vocab.py`) — 177 words from training answers
- **Extractor** (`vcd/verify/extract.py`) — pulls \boxed{} answers
- **vLLM generation** working on Kaggle (2x T4, ~100x faster than baseline)
- **3,648 verified easy-type traces** generated, saved to traces.jsonl (on laptop, NOT in git)

## Key findings
- Model IGNORES/OVERRIDES hints: giving bit puzzles to the model made it
  WORSE (48% Python-alone -> 32% with model). Design rule: use the model
  ONLY where Python fails, never to double-check correct Python answers.
- Bit solver overfits sometimes (8-9 examples) -> some wrong answers, but
  the verify step filters those out of training data anyway.

## Setup notes
- Generation model: Qwen2.5-7B-Instruct via vLLM, dtype=float16 (T4 needs
  float16 NOT bfloat16), tensor_parallel_size=2
- Kaggle: clone repo, add competition data as input, set_vocab() before use
- Competition is CLOSED but late submission gives a real (self-visible) score

## Next steps
1. Equation transformation solver (the differentiator — no notebook cracked it)
2. Generate traces for the 3 hard types (with the solvers)
3. Combine all verified traces into the training dataset
4. Phase 3: train LoRA on Nemotron-30B (needs the competition GPU)
5. Phase 4: benchmark + late submission for a real score