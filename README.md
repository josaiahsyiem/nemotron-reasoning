# Verified Chain-of-Thought Distillation for Reasoning LoRAs

An end-to-end pipeline for the NVIDIA Nemotron Reasoning Challenge: generate
chain-of-thought traces, keep only the ones that verify correct, and distill
them into a LoRA adapter.

## Results

Trained a LoRA on Qwen2.5-7B using 2,813 verified traces. Held-out accuracy
across the six puzzle types:

| Puzzle Type | Accuracy |
|-------------|----------|
| Numeral conversion | 100% |
| Gravitational constant | 90% |
| Text encryption | 80% |
| Unit conversion | 60% |
| Bit manipulation | 40% |
| Equation transformation | 0% |
| **Overall** | **62%** |

Training loss dropped from 1.24 to 0.36 over 2 epochs.

## How it works

1. **Per-type solvers** (`vcd/solvers/`) — each puzzle type has a solver that
   verifies answers and, where possible, cracks the puzzle in pure Python:
   - **Text encryption**: a cipher cracker that builds the substitution key
     from examples and fills gaps from a harvested vocabulary (0% -> 90% at
     data-generation time)
   - **Bit manipulation**: a per-bit boolean-function learner that searches
     candidate functions (constants, XOR/AND/OR, majority) per output bit
   - **Equation transformation**: an operator-focused structural hint (the
     type no public solver cracked; genuinely underdetermined)
   - Numeral / unit / gravitational: numeric and exact-match verification

2. **Verified-CoT generation** — puzzles are solved (by Python where possible,
   else a model with solver hints), the boxed answer is verified, and only
   correct traces are kept. Produced 6,126 verified traces (2,372 from the
   Python solvers alone).

3. **Balanced sampling + LoRA training** — traces sampled per type into 2,813
   chat examples, trained with QLoRA (rank 32, 2 epochs) via Unsloth.

## Key findings

- The model can be taught a solving *method* from Python-generated traces:
  text encryption reached 80% held-out with the model solving unaided.
- Giving the model hints for puzzles Python already solved made it *worse*
  (it overrode correct answers) — so the model is used only where Python fails.
- Equation transformation stayed hard (~0%), consistent with it being the
  field's hardest type.

## Note on scale

Trained on Qwen2.5-7B (fits free hardware). The competition's target,
Nemotron-3-Nano-30B, needs an ~80GB A100; swapping it in is a one-line change.

## Structure
- `vcd/solvers/` — the six puzzle solvers + registry
- `vcd/vocab.py`, `vcd/detect.py`, `vcd/data.py` — support
- `vcd/verify/extract.py` — boxed-answer extraction
- `notebooks/` — Kaggle generation + training notebooks