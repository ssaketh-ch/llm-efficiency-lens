# Quantization Benchmark Suite

This repository contains the final benchmark data and automation for comparing quantized instruction-tuned LLMs on an NVIDIA H200 MIG server. The benchmark covers model quality and serving throughput for 40 model-quantization configurations across common open LLM families.

The clean data files are in `data/`. Raw run artifacts remain under `results/` for auditability.

## Final Data Files

| File | Rows | Purpose |
| --- | ---: | --- |
| `data/accuracy.csv` | 240 | Final quality scores. One row per model, quantization, and benchmark task. |
| `data/throughput.csv` | 275 | Final vLLM serving throughput measurements. |
| `data/model_inventory.csv` | 40 | Model and quantization coverage inventory. |
| `data/accuracy_leaderboard.csv` | 6 | Best accuracy result per benchmark task. |
| `data/throughput_leaderboard.csv` | 10 | Best throughput by request rate and by quantization. |

Mirror copies of the two main final tables are also stored at:

- `results/accuracy/final/accuracy.csv`
- `results/throughput/final/throughput.csv`

## Hardware And Runtime Stack

The benchmark was run on a local Slurm-managed H200 system.

| Component | Details |
| --- | --- |
| GPU | NVIDIA H200 NVL |
| MIG usage | Mainly `mig-3g.71gb` for full sweeps |
| Driver snapshot | NVIDIA driver 570.133.20 |
| CUDA snapshot | CUDA 12.8 |
| Scheduler | Slurm, partition `mig_nodes` |
| Target node | `sssihl_h200` |
| Serving engine | vLLM OpenAI-compatible server in Docker |
| Main vLLM image | `vllm/vllm-openai:v0.19.0` |
| Gemma image | `vllm/vllm-openai:gemma4` |
| Quality harness | `lm_eval` with `local-completions` |
| Throughput harness | `vllm bench serve` |
| Dataset cache | Local Hugging Face cache in `models/` |
| Offline mode | `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1` |

## Model Coverage

The benchmark covers 40 model-quantization configurations.

| Family | Configurations |
| --- | ---: |
| DeepSeek-R1-Distill-Qwen | 11 |
| Qwen3 | 8 |
| Qwen2.5 | 8 |
| Gemma | 4 |
| Llama-3.1 | 4 |
| Llama-3.2 | 4 |
| Other DeepSeek/Qwen variant | 1 |

Model sizes covered:

- 3B
- 7B
- 8B
- 14B
- 31B
- 32B

Quantization labels covered:

- `bf16`
- `fp8`
- `awq`
- `gptq`
- `nvfp4`

## Quality Benchmarks

Each model-quantization configuration has one row for every quality task, giving 40 complete rows per task.

| Task | Tier | Few-shot | What it measures |
| --- | --- | ---: | --- |
| `mmlu_abstract_algebra` | tier1 | 5 | Fast MMLU STEM smoke test |
| `hellaswag` | tier1 | 10 | Commonsense continuation |
| `winogrande` | tier1 | 5 | Commonsense reasoning |
| `arc_challenge` | tier1 | 25 | Science QA |
| `gsm8k` | tier2 | 5 | Multi-step math reasoning |
| `mmlu` | tier2 | 5 | Broad academic knowledge |

Quality evaluation uses:

```bash
lm_eval \
  --model local-completions \
  --model_args model=<MODEL>,base_url=http://localhost:<PORT>/v1/completions,tokenizer_backend=huggingface,tokenizer=<MODEL> \
  --apply_chat_template \
  --tasks <TASK> \
  --num_fewshot <N> \
  --batch_size 1
```

## Accuracy Leaderboard

Best final score per task:

| Task | Best model | Quant | Accuracy |
| --- | --- | --- | ---: |
| `arc_challenge` | `Qwen/Qwen2.5-32B-Instruct-AWQ` | `awq` | 0.7090 |
| `gsm8k` | `RedHatAI/gemma-4-31B-it-NVFP4` | `nvfp4` | 0.9340 |
| `hellaswag` | `Qwen/Qwen2.5-32B-Instruct-AWQ` | `awq` | 0.6844 |
| `mmlu` | `RedHatAI/gemma-4-31B-it-FP8-block` | `fp8` | 0.8754 |
| `mmlu_abstract_algebra` | `google/gemma-4-31B-it` | `bf16` | 0.8732 |
| `winogrande` | `hugging-quants/Meta-Llama-3.1-8B-Instruct-AWQ-INT4` | `awq` | 0.7782 |

## Throughput Benchmarks

Throughput uses vLLM's serving benchmark with the ShareGPT prompt dataset.

Request rates:

- 1 request/s
- 2 requests/s
- 4 requests/s
- 8 requests/s
- 16 requests/s

Primary throughput metrics:

- `req_throughput`: completed requests per second.
- `output_tok_throughput`: generated output tokens per second.
- `total_tok_throughput`: input plus output tokens per second.
- `mean_ttft_ms`: mean time to first token.
- `mean_tpot_ms`: mean time per output token.
- `p99_ttft_ms` and `p99_tpot_ms`: tail latency.

Best output token throughput by request rate:

| Request rate | Best model | Quant | Output tok/s | Mean TTFT ms | Mean TPOT ms |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | `RedHatAI/gemma-4-31B-it-FP8-block` | `fp8` | 216.93 | 2702.92 | 29.69 |
| 2 | `Qwen/Qwen3-8B-FP8` | `fp8` | 424.53 | 28.45 | 6.01 |
| 4 | `Qwen/Qwen3-8B-FP8` | `fp8` | 867.83 | 29.48 | 6.23 |
| 8 | `Qwen/Qwen3-8B-FP8` | `fp8` | 1594.12 | 32.50 | 6.69 |
| 16 | `Qwen/Qwen3-8B-FP8` | `fp8` | 3150.57 | 46.73 | 8.37 |

Best output token throughput by quantization:

| Quant | Best model | Rate | Output tok/s | Total tok/s |
| --- | --- | ---: | ---: | ---: |
| `awq` | `AngelSlim/Deepseek_r1_distill_qwen-7b_int4_awq` | 16 | 3141.13 | 6649.51 |
| `bf16` | `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` | 16 | 3102.81 | 6577.31 |
| `fp8` | `Qwen/Qwen3-8B-FP8` | 16 | 3150.57 | 6606.96 |
| `gptq` | `jakiAJK/DeepSeek-R1-Distill-Qwen-7B_GPTQ-int4` | 16 | 3126.08 | 6635.00 |
| `nvfp4` | `RedHatAI/gemma-4-31B-it-NVFP4` | 4 | 639.36 | 1270.88 |

## Repository Layout

```text
data/                     Final CSV files for GitHub and Hugging Face
datasets/                 ShareGPT serving benchmark dataset
models/                   Ignored local model and dataset cache
results/accuracy/         Raw and final lm_eval quality artifacts
results/throughput/       Raw and final vLLM serving artifacts
scripts/                  Runners, parsers, and Slurm sweep scripts
scripts/accuracy/         Quality sweep scripts by model family
scripts/throughput/       Throughput sweep scripts by model family
scripts/archive/          Older scripts retained for reproducibility
```

## Rebuild Final Tables

Regenerate final CSVs from raw outputs:

```bash
cd /home/saketh-msc/quantization
python3 scripts/build_final_tables.py
```

This scans `results/accuracy/evals/`, keeps the latest real JSON result for each `(model, quant, task)`, and writes:

- `data/accuracy.csv`
- `data/throughput.csv`
- `data/model_inventory.csv`
- `data/accuracy_leaderboard.csv`
- `data/throughput_leaderboard.csv`
- `results/accuracy/final/accuracy.csv`
- `results/throughput/final/throughput.csv`

## What To Commit

Track:

- `data/*.csv`
- `README.md`
- subfolder `README.md` files
- `scripts/`
- `datasets/README.md`
- `models/README.md`

Do not track:

- `models/` cache contents
- raw logs
- raw `lm_eval` JSONs unless you explicitly want an audit artifact
- raw vLLM `rate*.txt` outputs
