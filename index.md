---
layout: default
title: Home
nav_order: 1
---

<p align="center">
  <img src="logo.png" width="600" alt="LLM Efficiency Lens Logo">
</p>

# LLM Efficiency Lens
### Bridging the Gap Between Benchmarks and Budgets

Welcome to the official documentation for the **LLM Efficiency Lens**, a framework developed to bring economic transparency to Large Language Model inference.

---

##  Why LLM Efficiency Lens?
In the current AI landscape, throughput (tokens/sec) is only half the story. The true challenge for enterprises and researchers is **Efficiency per Dollar**. Our framework correlates:
* **vLLM Performance Data**
* **MLPerf Inference LoadGen Logs**
* **Real-time Cloud Pricing Metadata**

---

##  Quick Start

### Installation
```bash
pip install -r requirements.txt

from src.parser.analyzer import EfficiencyAnalyzer

analyzer = EfficiencyAnalyzer()
report = analyzer.calculate_economics(
    throughput_tps=4500, 
    provider="lambda_labs", 
    gpu_instance="h100_pcie"
)
