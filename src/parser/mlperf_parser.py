import re
import json
import pandas as pd
from pathlib import Path

class MLPerfParser:
    """
    A professional parser for MLPerf Inference LoadGen logs.
    Focuses on extracting throughput and latency for vLLM-served models.
    """
    
    def __init__(self, log_path: str):
        self.log_path = Path(log_path)
        if not self.log_path.exists():
            raise FileNotFoundError(f"Log file not found at {log_path}")

    def parse_summary(self) -> dict:
        """
        Parses the mlperf_log_summary.txt to extract key performance metrics.
        """
        metrics = {}
        patterns = {
            "samples_per_second": r"Samples per second: (\d+\.\d+)",
            "min_latency": r"Min latency \(ns\)\s+: (\d+)",
            "max_latency": r"Max latency \(ns\)\s+: (\d+)",
            "mean_latency": r"Mean latency \(ns\)\s+: (\d+)",
            "p99_latency": r"99th percentile latency \(ns\): (\d+)"
        }

        with open(self.log_path, 'r') as f:
            content = f.read()
            for key, pattern in patterns.items():
                match = re.search(pattern, content)
                if match:
                    # Convert nanoseconds to milliseconds for readability
                    val = float(match.group(1))
                    metrics[key] = val / 1e6 if "latency" in key else val
        
        return metrics

if __name__ == "__main__":
    # Example usage for the dev community
    print("MLPerf Parser Initialized. Ready for log ingestion.")
