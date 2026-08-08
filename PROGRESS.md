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
3. Phase 3: train LoRA on Nemotron-30B-A3B
   - GPU finding: competition Blackwell GPU is GONE (only T4x2 / P100 free now)
   - BUT late submission WORKS (button confirmed) -> can still get a real score
   - FREE PATH TO TRY: Unsloth has day-0 support for Nemotron-3-Nano-30B.
     It's a MoE (only ~3B active), runs on 24GB. With 4-bit QLoRA it MIGHT
     fit on free T4x2 (32GB). Borderline but worth attempting.
     Ref: unsloth.ai/docs/models/nemotron-3
   - If it fits: train free on Kaggle -> late submit -> real comparable score
   - If not: rent an A100 for a few hours (~$10-30) as fallback
4. Phase 4: benchmark (vLLM latency/throughput/VRAM) + late submission

## Proven training recipe (extracted from the 0.72 CoT notebook)
The notebooks trained on the RTX PRO 6000 Blackwell GPU in FULL bf16 (no
quantization). We adapt the SAME recipe but add 4-bit QLoRA to fit smaller GPUs.

Confirmed hyperparameters from the notebook:
- LoRA rank = 32, alpha = 32
- target modules: in_proj, out_proj, up_proj, down_proj (or "all-linear")
- per_device_train_batch_size = 1
- gradient_accumulation_steps = 8
- num_train_epochs = 2
- max_length = 4096
- learning_rate = 1e-4, cosine scheduler, warmup 0.05
- gradient_checkpointing = ON
- device_map = "auto"

Our adaptation for smaller hardware:
- ADD 4-bit quantization (QLoRA) via Unsloth or bitsandbytes
- Keep everything else the same as above
- bf16 on Blackwell/A100; use fp16 or Unsloth's handling on T4