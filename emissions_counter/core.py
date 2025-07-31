"""
core.py  –  Industry-average electricity / water / carbon calculator
           based on “How Hungry is AI?” (July 2025).

Public entry point:
    calculate_impact(model_name, tokens_out, tps, latency_s, provider)

All lookup tables are in DEFAULTS.  Update them as better data arrives.
"""

from typing import Dict, Tuple


# ────────────────────────────────────────────────────────────────────
#  Lookup tables  (all numbers are per *DGX node* unless stated)
# ────────────────────────────────────────────────────────────────────
DEFAULTS: Dict[str, Dict] = {

    # ❶ Menu names  →  internal spec (class bucket + hardware key)
    "models": {
        "GPT-4o":            {"class": "Micro", "hardware": "H100"},
        "Claude-3.7 Sonnet": {"class": "Large", "hardware": "H100"},
        "o3":                {"class": "XL",    "hardware": "H100x2"},
        "DeepSeek-R1":       {"class": "XL",    "hardware": "H100x2"},
    },

    # ❷ Node power (IT only, kW)
    "hardware": {
        "H100":   {"node_kw": 10.2},   # 1 DGX H100
        "A100":   {"node_kw": 6.5},    # 1 DGX A100
        "H100x2": {"node_kw": 20.4},   # 2 H100 nodes used together
    },

    # ❸ Average utilisation per model-class
    #     (GPU% + non-GPU% of node power, batch-8, latency-sensitive)
    "utilisation": {
        "Micro":  {"gpu": 0.012, "non_gpu": 0.014},   # GPT-4o
        "Medium": {"gpu": 0.035, "non_gpu": 0.031},
        "Large":  {"gpu": 0.082, "non_gpu": 0.059},
        "XL":     {"gpu": 0.55,  "non_gpu": 0.10},    # o3 / DeepSeek-R1 long-context
    },

    # ❹ Environmental multipliers  (PUE, WUEsite, WUEsrc, carbon-intensity)
    "env": {
        "azure-us": {
            "pue": 1.12, "wue_site": 0.30, "wue_src": 3.142, "cif": 0.3528
        },
        "aws-us": {
            "pue": 1.14, "wue_site": 0.18, "wue_src": 3.142, "cif": 0.385
        },
        "deepseek-cn": {        # mainland-China profile (coal-heavy grid)
            "pue": 1.27, "wue_site": 1.20, "wue_src": 6.016, "cif": 0.60
        },
    },
}


# ────────────────────────────────────────────────────────────────────
#  Equations (from the paper)
# ────────────────────────────────────────────────────────────────────
def eq_energy(
    tokens_out: int,
    tps: int,
    latency_s: float,
    node_kw: float,
    util_gpu: float,
    util_nongpu: float,
    pue: float,
) -> float:
    """Energy per query in kWh."""
    hours = (tokens_out / tps + latency_s) / 3600
    it_kw = node_kw * (util_gpu + util_nongpu)
    return hours * it_kw * pue


def eq_water(e_kwh: float, pue: float, wue_site: float, wue_src: float) -> float:
    """Total water (site + source) in litres."""
    return (e_kwh / pue) * wue_site + e_kwh * wue_src


def eq_carbon(e_kwh: float, cif: float) -> float:
    """Carbon footprint in kg CO₂e."""
    return e_kwh * cif


# ────────────────────────────────────────────────────────────────────
#  Public helper
# ────────────────────────────────────────────────────────────────────
def calculate_impact(
    model_name: str = "GPT-4o",
    tokens_out: int = 300,
    tps: int = 400,
    latency_s: float = 0.075,
    provider: str = "azure-us",
) -> Tuple[float, float, float]:
    """
    Return (energy_kWh, water_L, carbon_kg) for one query.

    * model_name  – "GPT-4o", "Claude-3.7 Sonnet", "o3", "DeepSeek-R1"
    * tokens_out  – expected output tokens
    * tps         – decoding speed (tokens per second)
    * latency_s   – added latency before first token
    * provider    – "azure-us", "aws-us", "deepseek-cn"
    """
    cfg   = DEFAULTS
    spec  = cfg["models"][model_name]
    hw    = cfg["hardware"][spec["hardware"]]
    util  = cfg["utilisation"][spec["class"]]
    env   = cfg["env"][provider]

    e = eq_energy(
        tokens_out, tps, latency_s,
        hw["node_kw"],
        util["gpu"], util["non_gpu"],
        env["pue"]
    )
    w = eq_water(e, env["pue"], env["wue_site"], env["wue_src"])
    c = eq_carbon(e, env["cif"])
    return e, w, c

