# Verified Chain-of-Thought Distillation for Reasoning LoRAs

An end-to-end pipeline for the NVIDIA Nemotron Reasoning Challenge: generate
chain-of-thought traces, keep only the ones that verify correct, and distill
them into a LoRA adapter.


## Results

Trained a LoRA on Qwen2.5-7B. Held-out accuracy across the six puzzle types
(puzzles not used in training, verified with the same solvers):

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

## Data pipeline

- **6,126 verified-correct traces** generated across all six types (kept only
  traces whose boxed answer passed the type's solver).
- **2,372 of those** were solved entirely by the Python solvers (no model call).
- **2,813 balanced examples** sampled per type (caps: numeral 300, gravitational
  400, unit 700, text 700, bit 607, equation 106) — this is the training set.

## Generation performance

Trace generation runs on Qwen2.5-7B via **vLLM batched inference** on Kaggle's
free 2× Tesla T4. Measured throughput: **~1.06 puzzles/sec batched**, versus
**~0.01 puzzles/sec** with naive one-at-a-time `model.generate` — roughly a
**100× speedup from batched vLLM inference** over sequential generation.
(Note: T4 requires `dtype=float16`, not bfloat16.)

## How it works

1. **Per-type solvers** (`vcd/solvers/`) — each verifies answers and, where
   possible, cracks the puzzle in pure Python:
   - **Text encryption**: cipher cracker — builds the substitution key from
     examples, fills gaps from a harvested vocabulary (0% -> 90% at generation).
   - **Bit manipulation**: per-bit boolean-function learner — searches candidate
     functions (constants, XOR/AND/OR, majority) per output bit (8% -> 48%).
   - **Equation transformation**: operator-focused structural hint (the hardest
     type; ~0-5%, genuinely underdetermined — matches the field's ~13%).
   - Numeral / unit / gravitational: numeric and exact-match verification.

2. **Verified-CoT generation** — hybrid: Python solves what it can (2,372
   traces), the model handles the rest with solver hints; only correct traces
   are kept.

3. **LoRA training** — 2,813 balanced chat examples, QLoRA rank 32, 2 epochs,
   via Unsloth on the free T4.

## Key findings

- The model learned a solving *method* from Python-generated traces:
  text encryption reached 80% held-out with the model solving unaided.
- Hinting the model on puzzles Python already solved made it *worse* (bit
  manipulation 48% Python-alone -> 32% with model) — so the model is used only
  where Python fails.
- Equation transformation stayed hard (~0%), consistent with it being the
  field's hardest type.

## Note on scale

Trained on Qwen2.5-7B (fits free hardware). The competition's target,
Nemotron-3-Nano-30B, needs an ~80GB A100; swapping it in is a one-line change.

## Structure
- `vcd/solvers/` — the six solvers + registry
- `vcd/vocab.py`, `vcd/detect.py`, `vcd/data.py` — support
- `vcd/verify/extract.py` — boxed-answer extraction
- `notebooks/` — Kaggle generation + training notebooks
