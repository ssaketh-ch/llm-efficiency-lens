import json
from pathlib import Path

class EfficiencyAnalyzer:
    """
    Correlates technical throughput with cloud infrastructure costs.
    Calculates Economic ROI for LLM inference.
    """
    
    def __init__(self, pricing_path: str = "metadata/cloud_pricing.json"):
        with open(pricing_path, 'r') as f:
            self.pricing_data = json.load(f)

    def calculate_economics(self, throughput_tps: float, provider: str, gpu_instance: str):
        """
        Calculates cost metrics based on throughput and hourly rates.
        """
        try:
            hourly_rate = self.pricing_data["providers"][provider][gpu_instance]["hourly"]
        except KeyError:
            return {"error": "Provider or Instance not found in metadata."}

        # Calculate Tokens per Dollar (T/$)
        # Formula: (Tokens/Sec * 3600 Sec) / Hourly Rate
        tokens_per_dollar = (throughput_tps * 3600) / hourly_rate
        
        # Calculate Cost per 1M Tokens
        # Formula: (Hourly Rate / (Tokens/Sec * 3600)) * 1,000,000
        cost_per_m_tokens = (hourly_rate / (throughput_tps * 3600)) * 1_000_000

        return {
            "tokens_per_dollar": round(tokens_per_dollar, 2),
            "cost_per_1m_tokens_usd": round(cost_per_m_tokens, 4),
            "config": f"{provider} ({gpu_instance})"
        }

if __name__ == "__main__":
    analyzer = EfficiencyAnalyzer()
    # Example: Llama 3.1-8B reaching 4500 TPS on an H100
    results = analyzer.calculate_economics(4500, "lambda_labs", "h100_pcie")
    print(f"Economic Analysis: {results}")
