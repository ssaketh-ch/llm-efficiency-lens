# Contributing to LLM Efficiency Lens  

First off, thank you for considering contributing to LLM Efficiency Lens! It's people like you that make the open-source community such a great place to learn, inspire, and create.

## How Can I Contribute?

###  Updating Pricing Data
The most helpful contribution is keeping our `metadata/cloud_pricing.json` up to date. 
- Find current hourly rates for H100, A100, or L4 GPUs from major providers.
- Submit a Pull Request with the updated values.
- Please include a link to the source of the pricing in your PR description.

###  Improving Parsers
We currently support **vLLM** and **MLPerf**. If you use other engines like **TensorRT-LLM**, **TGI**, or **DeepSpeed-MII**, we would love your help:
1. Create a new parser in `src/parser/`.
2. Ensure it returns a standardized dictionary of metrics.
3. Add a sample log to `data/samples/`.

###  Reporting Bugs
- Use the GitHub Issues tab.
- Describe the bug and provide the log file that caused the error.
- Explain what the expected output was versus what actually happened.

## Pull Request Process
1. Fork the repo and create your branch from `main`.
2. If you've added code, ensure it follows the existing style (clean Python classes).
3. Update the `README.md` if your change adds new functionality.
4. Submit your PR and wait for a review!

---
*By contributing, you agree that your contributions will be licensed under the project's Apache 2.0 License.*
