import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import math

# ----------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------
st.set_page_config(
    page_title="MaintEdge - DMC Calculator | Deutsche Aircraft",
    page_icon="https://img.icons8.com/fluency/48/airplane-mode-on.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------
# DO 328-100 MAINTENANCE DATA (baseline from Excel)
# ----------------------------------------------------------------
DO328_100_DATA = [
    {"inspection": "LC",              "int1": 15,   "param1": "Days",   "int2": 60,    "param2": "FH",      "mh": 8,     "mat": 40.00,      "category": "Airframe Checks"},
    {"inspection": "A1",              "int1": 7.5,  "param1": "Months", "int2": 500,   "param2": "FH",      "mh": 80,    "mat": 91.23,      "category": "Airframe Checks"},
    {"inspection": "A2",              "int1": 15,   "param1": "Months", "int2": 1000,  "param2": "FH",      "mh": 50,    "mat": 10847.72,   "category": "Airframe Checks"},
    {"inspection": "A3",              "int1": 15,   "param1": "Months", "int2": 1500,  "param2": "FH",      "mh": 20,    "mat": 11383.37,   "category": "Airframe Checks"},
    {"inspection": "A4",              "int1": 30,   "param1": "Months", "int2": 2000,  "param2": "FH",      "mh": 18,    "mat": 136.86,     "category": "Airframe Checks"},
    {"inspection": "A5",              "int1": 30,   "param1": "Months", "int2": 2500,  "param2": "FH",      "mh": 75,    "mat": 566.35,     "category": "Airframe Checks"},
    {"inspection": "C1",              "int1": 30,   "param1": "Months", "int2": 5000,  "param2": "FH",      "mh": 360,   "mat": 8682.17,    "category": "Airframe Checks"},
    {"inspection": "C2",              "int1": 60,   "param1": "Months", "int2": 10000, "param2": "FH",      "mh": 270,   "mat": 1824.69,    "category": "Airframe Checks"},
    {"inspection": "C3",              "int1": 90,   "param1": "Months", "int2": 15000, "param2": "FH",      "mh": 30,    "mat": 182.47,     "category": "Airframe Checks"},
    {"inspection": "C4",              "int1": 120,  "param1": "Months", "int2": 20000, "param2": "FH",      "mh": 140,   "mat": 2982.48,    "category": "Airframe Checks"},
    {"inspection": "APU500",          "int1": None, "param1": None,     "int2": 500,   "param2": "APU Hrs", "mh": 2.5,   "mat": 217.62,     "category": "APU Inspections"},
    {"inspection": "APU800",          "int1": None, "param1": None,     "int2": 8000,  "param2": "APU Hrs", "mh": 8,     "mat": 249.02,     "category": "APU Inspections"},
    {"inspection": "APU1000",         "int1": None, "param1": None,     "int2": 1000,  "param2": "APU Hrs", "mh": 11,    "mat": 0,          "category": "APU Inspections"},
    {"inspection": "APU5000",         "int1": None, "param1": None,     "int2": 5000,  "param2": "APU Hrs", "mh": 10,    "mat": 255.00,     "category": "APU Inspections"},
    {"inspection": "FH1000",          "int1": None, "param1": None,     "int2": 1000,  "param2": "FH",      "mh": 10.5,  "mat": 0,          "category": "FH-Based Tasks"},
    {"inspection": "FH1200",          "int1": None, "param1": None,     "int2": 1200,  "param2": "FH",      "mh": 2,     "mat": 0,          "category": "FH-Based Tasks"},
    {"inspection": "FH2000",          "int1": None, "param1": None,     "int2": 2000,  "param2": "FH",      "mh": 4,     "mat": 0,          "category": "FH-Based Tasks"},
    {"inspection": "FH4000",          "int1": None, "param1": None,     "int2": 4000,  "param2": "FH",      "mh": 11.5,  "mat": 0,          "category": "FH-Based Tasks"},
    {"inspection": "FH4000/60M",      "int1": 60,   "param1": "Months", "int2": 4000,  "param2": "FH",      "mh": 5,     "mat": 0,          "category": "FH-Based Tasks"},
    {"inspection": "FH8000",          "int1": None, "param1": None,     "int2": 8000,  "param2": "FH",      "mh": 3,     "mat": 0,          "category": "FH-Based Tasks"},
    {"inspection": "Weight & Balance","int1": 48,   "param1": "Months", "int2": None,  "param2": None,      "mh": 23,    "mat": 0,          "category": "FH-Based Tasks"},
    {"inspection": "FD-0101",         "int1": None, "param1": None,     "int2": 1000,  "param2": "FC",      "mh": 3,     "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-0202",         "int1": None, "param1": None,     "int2": 2000,  "param2": "FC",      "mh": 6,     "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-0303",         "int1": None, "param1": None,     "int2": 3000,  "param2": "FC",      "mh": 3,     "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-0404",         "int1": None, "param1": None,     "int2": 4000,  "param2": "FC",      "mh": 4,     "mat": 47.76,      "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-0602",         "int1": None, "param1": None,     "int2": 6000,  "param2": "FC",      "mh": 3,     "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-0606",         "int1": None, "param1": None,     "int2": 6000,  "param2": "FC",      "mh": 8,     "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-0808",         "int1": None, "param1": None,     "int2": 8000,  "param2": "FC",      "mh": 30,    "mat": 278.52,     "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-0808A",        "int1": None, "param1": None,     "int2": 8000,  "param2": "FC",      "mh": 18,    "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-1000",         "int1": None, "param1": None,     "int2": 10000, "param2": "FC",      "mh": 8,     "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-1212",         "int1": None, "param1": None,     "int2": 12000, "param2": "FC",      "mh": 9,     "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-1616",         "int1": None, "param1": None,     "int2": 16000, "param2": "FC",      "mh": 12,    "mat": 189.03,     "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-1616A",        "int1": None, "param1": None,     "int2": 16000, "param2": "FC",      "mh": 4,     "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-2000",         "int1": None, "param1": None,     "int2": 20000, "param2": "FC",      "mh": 3,     "mat": 4839.81,    "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-2208",         "int1": None, "param1": None,     "int2": 22000, "param2": "FC",      "mh": 3,     "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-2502",         "int1": None, "param1": None,     "int2": 25000, "param2": "FC",      "mh": 6,     "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-2503",         "int1": None, "param1": None,     "int2": 25000, "param2": "FC",      "mh": 3,     "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-2504",         "int1": None, "param1": None,     "int2": 25000, "param2": "FC",      "mh": 14,    "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-2506",         "int1": None, "param1": None,     "int2": 25000, "param2": "FC",      "mh": 45,    "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-2508",         "int1": None, "param1": None,     "int2": 25000, "param2": "FC",      "mh": 105,   "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-2508A",        "int1": None, "param1": None,     "int2": 25000, "param2": "FC",      "mh": 12,    "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-2510",         "int1": None, "param1": None,     "int2": 25000, "param2": "FC",      "mh": 24,    "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-2512",         "int1": None, "param1": None,     "int2": 25000, "param2": "FC",      "mh": 90,    "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "FD-2516",         "int1": None, "param1": None,     "int2": 25000, "param2": "FC",      "mh": 225,   "mat": 0,          "category": "Fatigue Damage (FD)"},
    {"inspection": "CP-2",            "int1": 24,   "param1": "Months", "int2": None,  "param2": None,      "mh": 5,     "mat": 0,          "category": "Corrosion Prevention (CP)"},
    {"inspection": "CP-2.5",          "int1": 30,   "param1": "Months", "int2": None,  "param2": None,      "mh": 20,    "mat": 0,          "category": "Corrosion Prevention (CP)"},
    {"inspection": "CP-4",            "int1": 48,   "param1": "Months", "int2": None,  "param2": None,      "mh": 10,    "mat": 0,          "category": "Corrosion Prevention (CP)"},
    {"inspection": "CP-5",            "int1": 60,   "param1": "Months", "int2": None,  "param2": None,      "mh": 35,    "mat": 0,          "category": "Corrosion Prevention (CP)"},
    {"inspection": "CP-10",           "int1": 96,   "param1": "Months", "int2": None,  "param2": None,      "mh": 105,   "mat": 0,          "category": "Corrosion Prevention (CP)"},
    {"inspection": "CP-10/5",         "int1": 120,  "param1": "Months", "int2": None,  "param2": None,      "mh": 5,     "mat": 0,          "category": "Corrosion Prevention (CP)"},
    {"inspection": "SSI-2",           "int1": 24,   "param1": "Months", "int2": None,  "param2": None,      "mh": 15,    "mat": 0,          "category": "Structural Sampling (SSI)"},
    {"inspection": "SSI-2.5",         "int1": 30,   "param1": "Months", "int2": None,  "param2": None,      "mh": 10,    "mat": 314.87,     "category": "Structural Sampling (SSI)"},
    {"inspection": "SSI-5",           "int1": 60,   "param1": "Months", "int2": None,  "param2": None,      "mh": 80,    "mat": 1096.10,    "category": "Structural Sampling (SSI)"},
    {"inspection": "SSI-10",          "int1": 120,  "param1": "Months", "int2": None,  "param2": None,      "mh": 220,   "mat": 2991.68,    "category": "Structural Sampling (SSI)"},
    {"inspection": "SSI-10/5",        "int1": 120,  "param1": "Months", "int2": None,  "param2": None,      "mh": 5,     "mat": 0,          "category": "Structural Sampling (SSI)"},
    {"inspection": "Propeller Change (2EA)",  "int1": None, "param1": None,     "int2": 6000,  "param2": "FC",  "mh": 80,    "mat": 180000.00,  "category": "Propellers"},
    {"inspection": "Engine Change (2EA)",    "int1": None, "param1": None,     "int2": 8000,  "param2": "FH",  "mh": 360,   "mat": 2400000.00, "category": "Engines"},
    {"inspection": "Landing Gear Overhaul",  "int1": 144,  "param1": "Months", "int2": 22000, "param2": "FC",  "mh": 85,    "mat": 456801.70,  "category": "Landing Gear"},
    {"inspection": "Brakes",                 "int1": None, "param1": None,     "int2": 3000,  "param2": "FC",  "mh": 2,     "mat": 93084.12,   "category": "Landing Gear"},
    {"inspection": "APU Overhaul",           "int1": None, "param1": None,     "int2": 8000,  "param2": "FC",  "mh": 20,    "mat": 220000.00,  "category": "APU"},
    {"inspection": "Time Controlled Items",  "int1": 12,   "param1": "Months", "int2": None,  "param2": None,  "mh": 400,   "mat": 800000.00,  "category": "Time Controlled Components"},
]


# ----------------------------------------------------------------
# CATEGORY-SPECIFIC FACTOR WEIGHTS
# ----------------------------------------------------------------
# Each environment/operational factor has different severity per category.
# Weight = how much of the base factor applies to this category.
# e.g., Tropical x1.12 with airframe weight 1.0 => full +12%
#        Tropical x1.12 with engine weight 0.3  => only +3.6%
# Formula per category: factor_applied = 1.0 + (base_factor - 1.0) * weight

# ENV_WEIGHTS[environment][category] = weight (0.0 to 1.5)
ENV_WEIGHTS = {
    "Temperate":        {"Airframe Checks": 1.0, "APU Inspections": 1.0, "FH-Based Tasks": 1.0, "Fatigue Damage (FD)": 1.0, "Corrosion Prevention (CP)": 1.0, "Structural Sampling (SSI)": 1.0, "Engines": 1.0, "Propellers": 1.0, "Landing Gear": 1.0, "APU": 1.0, "Time Controlled Components": 1.0},
    "Tropical / Humid": {"Airframe Checks": 1.3, "APU Inspections": 0.8, "FH-Based Tasks": 1.0, "Fatigue Damage (FD)": 0.6, "Corrosion Prevention (CP)": 1.5, "Structural Sampling (SSI)": 1.4, "Engines": 0.5, "Propellers": 0.4, "Landing Gear": 0.9, "APU": 0.7, "Time Controlled Components": 0.8},
    "Arid / Desert":    {"Airframe Checks": 0.5, "APU Inspections": 0.8, "FH-Based Tasks": 0.6, "Fatigue Damage (FD)": 0.3, "Corrosion Prevention (CP)": 0.2, "Structural Sampling (SSI)": 0.3, "Engines": 1.4, "Propellers": 1.5, "Landing Gear": 0.7, "APU": 0.9, "Time Controlled Components": 0.7},
    "Coastal / Marine":  {"Airframe Checks": 1.2, "APU Inspections": 0.7, "FH-Based Tasks": 0.9, "Fatigue Damage (FD)": 0.5, "Corrosion Prevention (CP)": 1.5, "Structural Sampling (SSI)": 1.5, "Engines": 0.4, "Propellers": 0.5, "Landing Gear": 1.3, "APU": 0.6, "Time Controlled Components": 0.7},
    "Cold / Arctic":     {"Airframe Checks": 0.6, "APU Inspections": 1.0, "FH-Based Tasks": 0.7, "Fatigue Damage (FD)": 0.4, "Corrosion Prevention (CP)": 0.3, "Structural Sampling (SSI)": 0.3, "Engines": 1.3, "Propellers": 0.8, "Landing Gear": 0.9, "APU": 1.2, "Time Controlled Components": 0.9},
    "High Altitude":     {"Airframe Checks": 0.2, "APU Inspections": 0.5, "FH-Based Tasks": 0.3, "Fatigue Damage (FD)": 0.3, "Corrosion Prevention (CP)": 0.1, "Structural Sampling (SSI)": 0.1, "Engines": 1.5, "Propellers": 1.3, "Landing Gear": 0.4, "APU": 0.6, "Time Controlled Components": 0.5},
}

# GRAVEL_WEIGHTS[category] = weight (how much gravel % affects this category)
GRAVEL_WEIGHTS = {
    "Airframe Checks": 0.6,
    "APU Inspections": 0.2,
    "FH-Based Tasks": 0.4,
    "Fatigue Damage (FD)": 0.3,
    "Corrosion Prevention (CP)": 0.5,
    "Structural Sampling (SSI)": 0.4,
    "Engines": 0.6,
    "Propellers": 1.5,
    "Landing Gear": 1.4,
    "APU": 0.2,
    "Time Controlled Components": 0.4,
}

# STOL_WEIGHTS[category] = weight (how much STOL % affects this category)
STOL_WEIGHTS = {
    "Airframe Checks": 0.5,
    "APU Inspections": 0.2,
    "FH-Based Tasks": 0.4,
    "Fatigue Damage (FD)": 1.5,
    "Corrosion Prevention (CP)": 0.2,
    "Structural Sampling (SSI)": 0.3,
    "Engines": 0.8,
    "Propellers": 1.2,
    "Landing Gear": 1.5,
    "APU": 0.3,
    "Time Controlled Components": 0.3,
}


def get_category_factor(category, environment, gravel_pct, stol_pct):
    """Compute combined adjustment factor for a specific category."""
    base_env = ENVIRONMENT_FACTORS[environment]
    env_weight = ENV_WEIGHTS.get(environment, {}).get(category, 1.0)
    env_applied = 1.0 + (base_env - 1.0) * env_weight

    gravel_base = (gravel_pct / 100) * 0.15
    gravel_weight = GRAVEL_WEIGHTS.get(category, 1.0)
    gravel_applied = 1.0 + gravel_base * gravel_weight

    stol_base = (stol_pct / 100) * 0.10
    stol_weight = STOL_WEIGHTS.get(category, 1.0)
    stol_applied = 1.0 + stol_base * stol_weight

    return env_applied * gravel_applied * stol_applied, env_applied, gravel_applied, stol_applied


# ----------------------------------------------------------------
# DMC CALCULATION ENGINE
# ----------------------------------------------------------------
def calculate_dmc(data, fh_yr, fc_yr, apu_hrs_yr, labour_rate, environment, gravel_pct, stol_pct):
    results = []

    for item in data:
        int1 = item["int1"]
        param1 = item["param1"]
        int2 = item["int2"]
        param2 = item["param2"]
        mh = item["mh"]
        mat = item["mat"]
        cat = item["category"]

        # Category-specific combined factor
        cat_factor, _, _, _ = get_category_factor(cat, environment, gravel_pct, stol_pct)

        # Occurrence 1 (calendar)
        occ1 = 0.0
        if int1 is not None and param1 is not None:
            p1 = param1.lower()
            if "day" in p1:
                occ1 = 365.0 / int1
            elif "month" in p1:
                occ1 = 12.0 / int1

        # Occurrence 2 (usage)
        occ2 = 0.0
        if int2 is not None and param2 is not None:
            p2 = param2.lower()
            if p2 == "fh":
                occ2 = fh_yr / int2
            elif p2 == "fc":
                occ2 = fc_yr / int2
            elif "apu" in p2:
                occ2 = apu_hrs_yr / int2
        elif int2 is not None and param2 is None:
            occ2 = fh_yr / int2

        occ = max(occ1, occ2)
        occ_source = "Calendar" if occ1 > occ2 else ("Usage" if occ2 > 0 else "Calendar")

        dmc_labour = (occ * labour_rate * mh) / fh_yr if fh_yr > 0 else 0
        dmc_material = (occ * mat) / fh_yr if fh_yr > 0 else 0

        dmc_labour_adj = dmc_labour * cat_factor
        dmc_material_adj = dmc_material * cat_factor
        dmc_total = dmc_labour_adj + dmc_material_adj

        results.append({
            "Category": cat,
            "Inspection": item["inspection"],
            "Interval 1": f"{int1} {param1}" if int1 and param1 else " -- ",
            "Interval 2": f"{int(int2)} {param2}" if int2 and param2 else " -- ",
            "MH": mh,
            "Material (EUR)": mat,
            "Occ/yr (Cal)": round(occ1, 4),
            "Occ/yr (Usage)": round(occ2, 4),
            "Occ/yr (Used)": round(occ, 4),
            "Driver": occ_source,
            "Adj. Factor": round(cat_factor, 4),
            "DMC Labour (EUR/FH)": round(dmc_labour_adj, 4),
            "DMC Material (EUR/FH)": round(dmc_material_adj, 4),
            "DMC Total (EUR/FH)": round(dmc_total, 4),
        })

    return results


# ----------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------
if "setup" not in st.session_state:
    st.session_state.setup = {
        "aircraft_type": "Do 328-100 (Turboprop)",
        "operator": "",
        "base_country": "",
        "fh_per_year": 2000,
        "fc_per_year": 2500,
        "fh_fc_ratio": 0.80,
        "apu_hrs_per_year": 2200,
        "environment": "Temperate",
        "gravel_pct": 0,
        "labour_rate": 85.0,
        "stol_pct": 0,
    }

if "page" not in st.session_state:
    st.session_state.page = "Home"


# ----------------------------------------------------------------
# ICON SVGs (inline, no emoji)
# ----------------------------------------------------------------
def svg_icon(name, size=20):
    icons = {
        "plane": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.8 19.2L16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/></svg>',
        "settings": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/></svg>',
        "chart": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        "file": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
        "wrench": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/></svg>',
        "engine": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>',
        "shield": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        "globe": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg>',
        "dollar": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>',
        "target": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
        "layers": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
        "zap": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        "search": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
        "download": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
        "check": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
        "cog": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 15a3 3 0 100-6 3 3 0 000 6z"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 11-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 11-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 11-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 110-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 112.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 114 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 112.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 110 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>',
        "wheel": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><line x1="12" y1="2" x2="12" y2="8"/><line x1="12" y1="16" x2="12" y2="22"/><line x1="2" y1="12" x2="8" y2="12"/><line x1="16" y1="12" x2="22" y2="12"/></svg>',
        "refresh": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/></svg>',
    }
    return icons.get(name, "")


# ----------------------------------------------------------------
# STYLING
# ----------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --navy-900: #0A0F1E;
    --navy-800: #0F172A;
    --navy-700: #1E293B;
    --navy-600: #334155;
    --slate-500: #64748B;
    --slate-400: #94A3B8;
    --slate-300: #CBD5E1;
    --slate-200: #E2E8F0;
    --slate-100: #F1F5F9;
    --slate-50: #F8FAFC;
    --blue-600: #2563EB;
    --blue-500: #3B82F6;
    --blue-400: #60A5FA;
    --blue-100: #DBEAFE;
    --cyan-400: #22D3EE;
    --green-500: #22C55E;
    --green-100: #DCFCE7;
    --amber-500: #F59E0B;
    --amber-100: #FEF3C7;
}

.stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--slate-50);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--navy-900) 0%, #0D1529 100%);
    border-right: 1px solid rgba(59,130,246,0.1);
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li,
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--slate-300) !important;
}
section[data-testid="stSidebar"] .stRadio label p {
    color: var(--slate-300) !important;
    font-weight: 500;
    font-size: 0.9rem;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, var(--navy-900) 0%, #101D3A 40%, #152952 70%, var(--blue-600) 100%);
    padding: 2.75rem 3rem 2.25rem 3rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(59,130,246,0.12);
    box-shadow: 0 4px 24px rgba(10,15,30,0.15);
}
.hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -40px;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(59,130,246,0.06) 0%, transparent 70%);
}
.hero::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--blue-400), var(--cyan-400), var(--blue-400), transparent);
}
.hero-brand {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 4px;
    text-transform: uppercase; color: var(--blue-400); margin-bottom: 0.6rem;
    display: flex; align-items: center; gap: 6px;
}
.hero-title {
    font-size: 2.6rem; font-weight: 800; color: #FFF; line-height: 1.15; letter-spacing: -0.5px;
}
.hero-title span {
    background: linear-gradient(135deg, var(--blue-400), var(--cyan-400));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1rem; color: var(--slate-400); font-weight: 400; margin-top: 0.6rem; line-height: 1.6;
    max-width: 650px;
}

/* Section */
.sec-head {
    font-size: 1.25rem; font-weight: 700; color: var(--navy-700);
    margin: 2.25rem 0 1rem 0; padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--slate-200);
    display: flex; align-items: center; gap: 8px;
}
.sec-head span { color: var(--blue-600); }

/* Cards grid */
.card-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
    gap: 1rem; margin: 1.25rem 0;
}
.card {
    background: #FFF; border: 1px solid var(--slate-200); border-radius: 12px;
    padding: 1.5rem; transition: all 0.2s ease; position: relative; overflow: hidden;
}
.card:hover {
    border-color: var(--blue-500);
    box-shadow: 0 8px 30px rgba(37,99,235,0.07);
    transform: translateY(-1px);
}
.card-accent {
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--blue-600), var(--cyan-400));
    opacity: 0; transition: opacity 0.2s;
}
.card:hover .card-accent { opacity: 1; }
.card-icon {
    width: 40px; height: 40px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 0.85rem; color: var(--blue-600);
}
.card-icon.blue { background: var(--blue-100); color: var(--blue-600); }
.card-icon.green { background: var(--green-100); color: #16a34a; }
.card-icon.amber { background: var(--amber-100); color: #d97706; }
.card-icon.slate { background: var(--slate-100); color: var(--navy-600); }
.card-t { font-size: 0.95rem; font-weight: 700; color: var(--navy-700); margin-bottom: 0.3rem; }
.card-d { font-size: 0.82rem; color: var(--slate-500); line-height: 1.55; }

/* Metric boxes */
.metrics { display: flex; gap: 0.85rem; margin: 1.5rem 0; flex-wrap: wrap; }
.metric {
    flex: 1; min-width: 170px;
    background: linear-gradient(135deg, var(--navy-900), #111D35);
    border-radius: 12px; padding: 1.15rem; text-align: center;
    border: 1px solid rgba(59,130,246,0.15);
    box-shadow: 0 2px 12px rgba(10,15,30,0.2);
}
.metric-label {
    font-size: 0.62rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: var(--blue-400); margin-bottom: 0.2rem;
}
.metric-val {
    font-family: 'JetBrains Mono', monospace; font-size: 1.35rem;
    font-weight: 700; color: #FFF;
}
.metric-unit { font-size: 0.7rem; color: var(--slate-400); }

/* Setup card */
.s-card {
    background: #FFF; border: 1px solid var(--slate-200); border-radius: 12px;
    padding: 1.5rem; margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}
.s-card-t {
    display: flex; align-items: center; gap: 8px;
    font-size: 0.95rem; font-weight: 700; color: var(--navy-800);
    margin-bottom: 1rem; padding-bottom: 0.65rem;
    border-bottom: 1px solid var(--slate-100);
}

/* Chips */
.chips { display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0.75rem 0; }
.chip {
    background: var(--blue-100); border: 1px solid #93C5FD; border-radius: 8px;
    padding: 0.3rem 0.7rem; font-size: 0.72rem; font-weight: 600; color: #1E40AF;
}

/* Info boxes */
.info-box {
    border-radius: 8px; padding: 0.65rem 1rem; font-size: 0.78rem; margin: 0.5rem 0;
}
.info-blue { background: #EFF6FF; border: 1px solid #BFDBFE; color: #1E40AF; }
.info-green { background: #F0FDF4; border: 1px solid #86EFAC; color: #166534; }
.info-amber { background: #FFFBEB; border: 1px solid #FDE68A; color: #92400E; }
.info-slate { background: var(--slate-50); border: 1px solid var(--slate-200); color: var(--slate-500); }

/* Footer */
.footer {
    text-align: center; padding: 1.75rem 0 1rem 0; margin-top: 3rem;
    border-top: 1px solid var(--slate-200); color: var(--slate-400); font-size: 0.75rem;
}
.footer strong { color: var(--slate-500); }

/* Step number */
.step-num {
    width: 32px; height: 32px; border-radius: 8px;
    background: var(--blue-600); color: #FFF;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.85rem; margin-bottom: 0.75rem;
}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------
# DATA
# ----------------------------------------------------------------
COUNTRIES = [
    "Germany", "France", "United Kingdom", "United States", "Canada",
    "Australia", "Brazil", "Guinea", "Nigeria", "South Africa",
    "India", "Japan", "South Korea", "China", "UAE",
    "Saudi Arabia", "Turkey", "Italy", "Spain", "Sweden",
    "Norway", "Switzerland", "Netherlands", "Austria", "Poland",
    "Czech Republic", "Greece", "Portugal", "Mexico", "Argentina",
    "Chile", "Colombia", "Peru", "Egypt", "Kenya",
    "Tanzania", "Ethiopia", "Morocco", "Thailand", "Indonesia",
    "Malaysia", "Philippines", "Vietnam", "New Zealand", "Singapore", "Other"
]

ENVIRONMENTS = ["Temperate", "Tropical / Humid", "Arid / Desert", "Coastal / Marine", "Cold / Arctic", "High Altitude"]

AIRCRAFT_TYPES = {
    "D328eco": {
        "full_name": "D328eco (Next-Gen Turboprop)", "engines": "PW127S-XT (x2)",
        "pax": "40", "description": "Next-generation regional turboprop with modern avionics.",
    },
    "Do 328-100 (Turboprop)": {
        "full_name": "Dornier 328-100 Turboprop", "engines": "PW119B / PW119C (x2)",
        "pax": "32", "description": "Proven regional turboprop with PW100-series engines.",
    },
    "Do 328-300 (Jet)": {
        "full_name": "Dornier 328-300 JET", "engines": "PW306B (x2)",
        "pax": "32-34", "description": "Jet variant with rear-mounted PW306B turbofans.",
    },
}

ENVIRONMENT_FACTORS = {
    "Temperate": 1.00, "Tropical / Humid": 1.12, "Arid / Desert": 1.08,
    "Coastal / Marine": 1.10, "Cold / Arctic": 1.06, "High Altitude": 1.04,
}


# ----------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.75rem 0 1.25rem 0;">
        <div style="width:48px; height:48px; background:linear-gradient(135deg, #2563EB, #22D3EE); border-radius:12px; display:flex; align-items:center; justify-content:center; margin:0 auto 0.6rem auto; box-shadow: 0 4px 12px rgba(37,99,235,0.3);">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.8 19.2L16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/></svg>
        </div>
        <div style="font-size:1.35rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.5px;">
            Maint<span style="background:linear-gradient(135deg,#60A5FA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Edge</span>
        </div>
        <div style="font-size:0.6rem; font-weight:600; letter-spacing:2.5px; color:#475569; text-transform:uppercase; margin-top:3px;">
            DMC Calculator
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["Home", "Setup & Calculate", "Report"], label_visibility="collapsed")
    st.session_state.page = page
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:0.75rem 0;">
        <div style="font-size:0.55rem; letter-spacing:2.5px; color:#475569; text-transform:uppercase; margin-bottom:4px;">Powered by</div>
        <div style="font-size:0.8rem; font-weight:700; color:#94A3B8;">Deutsche Aircraft GmbH</div>
        <div style="font-size:0.6rem; color:#475569; margin-top:3px;">v1.0.0</div>
    </div>
    """, unsafe_allow_html=True)


# ================================================================
# HOME
# ================================================================
if st.session_state.page == "Home":

    st.markdown(f"""
    <div class="hero">
        <div class="hero-brand">{svg_icon("plane", 14)} Deutsche Aircraft GmbH</div>
        <div class="hero-title">Maint<span>Edge</span></div>
        <div class="hero-title" style="font-size:1.45rem; font-weight:400; color:#CBD5E1; margin-top:0.15rem; letter-spacing:0;">
            Direct Maintenance Cost Calculator
        </div>
        <div class="hero-sub">
            Precision DMC modeling for the D328 family. From line maintenance to heavy checks,
            engine shop visits to component overhauls -- fully parameterized for your operation.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metrics">
        <div class="metric"><div class="metric-label">Aircraft Variants</div><div class="metric-val">3</div><div class="metric-unit">D328eco / 328-100 / 328JET</div></div>
        <div class="metric"><div class="metric-label">Maintenance Items</div><div class="metric-val">58+</div><div class="metric-unit">Checks / FD / CP / SSI / Heavy</div></div>
        <div class="metric"><div class="metric-label">Output</div><div class="metric-val">EUR/FH</div><div class="metric-unit">Labour + Material split</div></div>
        <div class="metric"><div class="metric-label">Adjustments</div><div class="metric-val">6</div><div class="metric-unit">Environment & ops factors</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="sec-head">{svg_icon("wrench", 20)} <span>Core</span> Capabilities</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card-grid">
        <div class="card"><div class="card-accent"></div>
            <div class="card-icon blue">{svg_icon("plane", 22)}</div>
            <div class="card-t">Airframe Checks</div>
            <div class="card-d">LC, A-checks (A1-A5), C-checks (C1-C4) with dual calendar/FH intervals. Automatic occurrence selection using the higher-frequency driver.</div>
        </div>
        <div class="card"><div class="card-accent"></div>
            <div class="card-icon amber">{svg_icon("engine", 22)}</div>
            <div class="card-t">Engine & Propeller</div>
            <div class="card-d">Engine shop visit at 8,000 FH and propeller change at 6,000 FC. Full labour + material amortization.</div>
        </div>
        <div class="card"><div class="card-accent"></div>
            <div class="card-icon green">{svg_icon("shield", 22)}</div>
            <div class="card-t">Structural & Fatigue</div>
            <div class="card-d">17 Fatigue Damage (FD), 6 Corrosion Prevention (CP), and 5 Structural Sampling (SSI) inspections.</div>
        </div>
        <div class="card"><div class="card-accent"></div>
            <div class="card-icon slate">{svg_icon("wheel", 22)}</div>
            <div class="card-t">Landing Gear & APU</div>
            <div class="card-d">LG overhaul (144mo/22,000FC), brakes (3,000FC), APU overhaul (8,000FC), plus 4 APU inspection tasks.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="sec-head">{svg_icon("zap", 20)} <span>Getting</span> Started</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card-grid">
        <div class="card"><div class="card-accent"></div>
            <div class="step-num">1</div>
            <div class="card-t">Setup</div>
            <div class="card-d">Select aircraft type, operator, utilization (FH/FC/APU hrs), environment, gravel %, labour rate, and STOL %.</div>
        </div>
        <div class="card"><div class="card-accent"></div>
            <div class="step-num">2</div>
            <div class="card-t">Calculate</div>
            <div class="card-d">Engine computes occurrences, selects the limiting interval, and calculates EUR/FH for every maintenance item.</div>
        </div>
        <div class="card"><div class="card-accent"></div>
            <div class="step-num">3</div>
            <div class="card-t">Report</div>
            <div class="card-d">View full breakdown by category, export detailed tables, and download CSV reports.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="chips">
        <span class="chip">D328eco -- Next-Gen Turboprop</span>
        <span class="chip">Do 328-100 -- Turboprop (PW119)</span>
        <span class="chip">Do 328-300 -- JET (PW306B)</span>
    </div>
    """, unsafe_allow_html=True)



# ================================================================
# SETUP & CALCULATE (merged)
# ================================================================
elif st.session_state.page == "Setup & Calculate":

    st.markdown(f"""
    <div class="hero" style="padding:2rem 2.5rem 1.5rem 2.5rem;">
        <div class="hero-brand">{svg_icon("settings", 14)} Configuration & Analysis</div>
        <div class="hero-title" style="font-size:2rem;">Setup & <span>Calculate</span></div>
        <div class="hero-sub">Define your operational parameters, then calculate DMC with one click.</div>
    </div>
    """, unsafe_allow_html=True)

    s = st.session_state.setup
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f'<div class="s-card"><div class="s-card-t">{svg_icon("plane", 18)} Aircraft & Operator</div></div>', unsafe_allow_html=True)
        aircraft_type = st.selectbox("Aircraft Type", list(AIRCRAFT_TYPES.keys()),
            index=list(AIRCRAFT_TYPES.keys()).index(s["aircraft_type"]))
        s["aircraft_type"] = aircraft_type
        ac = AIRCRAFT_TYPES[aircraft_type]
        st.markdown(f'<div class="info-box info-slate"><strong>{ac["full_name"]}</strong><br>Engines: {ac["engines"]} | Pax: {ac["pax"]}<br><span style="color:#94A3B8">{ac["description"]}</span></div>', unsafe_allow_html=True)
        s["operator"] = st.text_input("Operator Name", value=s["operator"], placeholder="e.g. UMSI Guinea, Nolinor Aviation")
        s["base_country"] = st.selectbox("Base Country", [""] + COUNTRIES,
            index=(COUNTRIES.index(s["base_country"]) + 1) if s["base_country"] in COUNTRIES else 0)

    with col2:
        st.markdown(f'<div class="s-card"><div class="s-card-t">{svg_icon("chart", 18)} Utilization Profile</div></div>', unsafe_allow_html=True)
        s["fh_per_year"] = st.number_input("Flight Hours / Year (FH/yr)", min_value=100, max_value=5000, value=s["fh_per_year"], step=50)
        s["fc_per_year"] = st.number_input("Flight Cycles / Year (FC/yr)", min_value=100, max_value=6000, value=s["fc_per_year"], step=50)
        s["apu_hrs_per_year"] = st.number_input("APU Hours / Year", min_value=100, max_value=5000, value=s["apu_hrs_per_year"], step=50,
            help="Annual APU operating hours for APU inspection intervals.")

        if s["fc_per_year"] > 0:
            ratio = round(s["fh_per_year"] / s["fc_per_year"], 2)
            avg_flt = round(s["fh_per_year"] / s["fc_per_year"] * 60, 0)
        else:
            ratio = 0.0
            avg_flt = 0
        s["fh_fc_ratio"] = ratio
        profile = "Short-haul" if ratio < 1.0 else ("Medium-haul" if ratio < 1.5 else "Long-haul")
        st.markdown(f'<div class="info-box info-blue"><strong>FH/FC Ratio: {ratio}</strong> | {profile} | Avg: {avg_flt:.0f} min/flight</div>', unsafe_allow_html=True)

    st.markdown("---")
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(f'<div class="s-card"><div class="s-card-t">{svg_icon("globe", 18)} Operating Environment</div></div>', unsafe_allow_html=True)
        s["environment"] = st.selectbox("Primary Environment", ENVIRONMENTS, index=ENVIRONMENTS.index(s["environment"]))
        ef = ENVIRONMENT_FACTORS[s["environment"]]
        env_desc = {"Temperate": "Baseline", "Tropical / Humid": "+12% corrosion & humidity",
            "Arid / Desert": "+8% dust & FOD ingestion", "Coastal / Marine": "+10% salt corrosion",
            "Cold / Arctic": "+6% cold-start & de-icing", "High Altitude": "+4% engine stress"}
        st.markdown(f'<div class="info-box info-amber">Environment Factor: <strong>x{ef:.2f}</strong> -- {env_desc[s["environment"]]}</div>', unsafe_allow_html=True)
        s["gravel_pct"] = st.slider("Gravel Runway Operations (%)", 0, 100, s["gravel_pct"], 5)

    with col4:
        st.markdown(f'<div class="s-card"><div class="s-card-t">{svg_icon("dollar", 18)} Cost & Operations</div></div>', unsafe_allow_html=True)
        s["labour_rate"] = st.number_input("Labour Cost / Hour (EUR/hr)", min_value=20.0, max_value=250.0,
            value=s["labour_rate"], step=5.0, format="%.2f")
        if s["labour_rate"] < 50:
            lr = "Low-cost region"
        elif s["labour_rate"] < 100:
            lr = "Mid-range (typical EASA/FAA MRO)"
        else:
            lr = "Premium (Western Europe / North America)"
        st.markdown(f'<div class="info-box info-slate">{lr}</div>', unsafe_allow_html=True)
        s["stol_pct"] = st.slider("STOL Operations (%)", 0, 100, s["stol_pct"], 5)

    st.session_state.setup = s

    # Compute factors
    gf = 1.0 + (s["gravel_pct"] / 100) * 0.15
    sf = 1.0 + (s["stol_pct"] / 100) * 0.10
    combined = ef * gf * sf

    # Summary bar
    st.markdown("---")
    st.markdown(f"""
    <div class="metrics">
        <div class="metric"><div class="metric-label">Aircraft</div><div class="metric-val" style="font-size:1rem;">{s["aircraft_type"]}</div><div class="metric-unit">{s["operator"] or "N/A"} | {s["base_country"] or "N/A"}</div></div>
        <div class="metric"><div class="metric-label">Utilization</div><div class="metric-val" style="font-size:1rem;">{s["fh_per_year"]:,} FH / {s["fc_per_year"]:,} FC</div><div class="metric-unit">APU: {s["apu_hrs_per_year"]:,} hrs | Ratio: {ratio}</div></div>
        <div class="metric"><div class="metric-label">Combined Factor</div><div class="metric-val">x{combined:.3f}</div><div class="metric-unit">Env x{ef:.2f} | Gravel x{gf:.2f} | STOL x{sf:.2f}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CALCULATE BUTTON ──
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        calculate_pressed = st.button(
            "CALCULATE DMC",
            use_container_width=True,
            type="primary",
        )

    if calculate_pressed:
        st.session_state.calculated = True

    if st.session_state.get("calculated", False):
        with st.spinner("Computing DMC for all maintenance items..."):
            results = calculate_dmc(DO328_100_DATA, s["fh_per_year"], s["fc_per_year"],
                s["apu_hrs_per_year"], s["labour_rate"], s["environment"], s["gravel_pct"], s["stol_pct"])
            df = pd.DataFrame(results)
            st.session_state.calc_results = results

        total_labour = df["DMC Labour (EUR/FH)"].sum()
        total_material = df["DMC Material (EUR/FH)"].sum()
        total_dmc = total_labour + total_material

        st.markdown("---")

        # Result metrics with highlighted total
        st.markdown(f"""
        <div class="metrics">
            <div class="metric" style="border: 1px solid rgba(34,197,94,0.3); box-shadow: 0 4px 20px rgba(34,197,94,0.15);">
                <div class="metric-label" style="color:#4ade80;">Total DMC</div>
                <div class="metric-val" style="font-size:1.6rem;">EUR {total_dmc:,.2f}</div>
                <div class="metric-unit">per Flight Hour</div>
            </div>
            <div class="metric">
                <div class="metric-label">Labour DMC</div>
                <div class="metric-val">EUR {total_labour:,.2f}</div>
                <div class="metric-unit">per Flight Hour</div>
            </div>
            <div class="metric">
                <div class="metric-label">Material DMC</div>
                <div class="metric-val">EUR {total_material:,.2f}</div>
                <div class="metric-unit">per Flight Hour</div>
            </div>
            <div class="metric">
                <div class="metric-label">Annual DMC</div>
                <div class="metric-val">EUR {total_dmc * s["fh_per_year"]:,.0f}</div>
                <div class="metric-unit">at {s["fh_per_year"]:,} FH/yr</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Labour vs Material split bar
        labour_pct = (total_labour / total_dmc * 100) if total_dmc > 0 else 0
        material_pct = 100 - labour_pct
        st.markdown(f"""
        <div style="margin:1.5rem 0;">
            <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:600; color:#475569; margin-bottom:4px;">
                <span>Labour: {labour_pct:.1f}%</span>
                <span>Material: {material_pct:.1f}%</span>
            </div>
            <div style="height:10px; border-radius:5px; background:#E2E8F0; overflow:hidden; display:flex;">
                <div style="width:{labour_pct}%; background:linear-gradient(90deg, #2563EB, #3B82F6); border-radius:5px 0 0 5px;"></div>
                <div style="width:{material_pct}%; background:linear-gradient(90deg, #22D3EE, #06B6D4); border-radius:0 5px 5px 0;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Category breakdown
        st.markdown(f'<div class="sec-head">{svg_icon("layers", 20)} <span>Category</span> Breakdown</div>', unsafe_allow_html=True)

        cat_sum = df.groupby("Category").agg({
            "DMC Labour (EUR/FH)": "sum", "DMC Material (EUR/FH)": "sum", "DMC Total (EUR/FH)": "sum"
        }).reset_index()
        cat_sum = cat_sum.sort_values("DMC Total (EUR/FH)", ascending=False)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            fig_pie = go.Figure(data=[go.Pie(
                labels=cat_sum["Category"], values=cat_sum["DMC Total (EUR/FH)"].round(2),
                hole=0.5, marker=dict(colors=["#2563EB", "#0891B2", "#059669", "#D97706", "#7C3AED", "#DC2626", "#475569", "#EC4899", "#F59E0B"]),
                textinfo="label+percent", textfont_size=10, textposition="outside",
            )])
            fig_pie.update_layout(title=dict(text="DMC Distribution by Category", font=dict(size=13, family="Plus Jakarta Sans")),
                height=420, margin=dict(t=50, b=20, l=20, r=20), showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_c2:
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(name="Labour", x=cat_sum["Category"], y=cat_sum["DMC Labour (EUR/FH)"].round(2), marker_color="#2563EB"))
            fig_bar.add_trace(go.Bar(name="Material", x=cat_sum["Category"], y=cat_sum["DMC Material (EUR/FH)"].round(2), marker_color="#22D3EE"))
            fig_bar.update_layout(title=dict(text="Labour vs Material (EUR/FH)", font=dict(size=13, family="Plus Jakarta Sans")),
                barmode="stack", height=420, margin=dict(t=50, b=100, l=50, r=20),
                xaxis=dict(tickangle=-40, tickfont=dict(size=9)),
                yaxis=dict(title=dict(text="EUR/FH", font=dict(size=11))),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_bar, use_container_width=True)

        # Category table
        st.markdown(f'<div class="sec-head">{svg_icon("file", 20)} <span>Category</span> Summary</div>', unsafe_allow_html=True)
        cat_disp = cat_sum.copy()
        cat_disp["% of Total"] = (cat_disp["DMC Total (EUR/FH)"] / total_dmc * 100).round(1)

        # Add per-category adjustment factors
        cat_factors_list = []
        for cat_name in cat_disp["Category"]:
            cf, _, _, _ = get_category_factor(cat_name, s["environment"], s["gravel_pct"], s["stol_pct"])
            cat_factors_list.append(round(cf, 4))
        cat_disp["Adj. Factor"] = cat_factors_list

        st.dataframe(cat_disp.style.format({
            "DMC Labour (EUR/FH)": "EUR {:.2f}", "DMC Material (EUR/FH)": "EUR {:.2f}",
            "DMC Total (EUR/FH)": "EUR {:.2f}", "% of Total": "{:.1f}%", "Adj. Factor": "x{:.4f}"}),
            use_container_width=True, hide_index=True)

        # Category factor breakdown
        st.markdown(f'<div class="sec-head">{svg_icon("target", 20)} <span>Category-Specific</span> Adjustment Factors</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-box info-blue">Factors are weighted per category. For example, tropical humidity affects Corrosion Prevention tasks more heavily than engine tasks.</div>', unsafe_allow_html=True)

        factor_rows = []
        all_cats = sorted(df["Category"].unique().tolist())
        for cat_name in all_cats:
            cf, ef_cat, gf_cat, sf_cat = get_category_factor(cat_name, s["environment"], s["gravel_pct"], s["stol_pct"])
            factor_rows.append({
                "Category": cat_name,
                "Env Factor": round(ef_cat, 4),
                "Gravel Factor": round(gf_cat, 4),
                "STOL Factor": round(sf_cat, 4),
                "Combined": round(cf, 4),
            })
        factor_df = pd.DataFrame(factor_rows)
        st.dataframe(factor_df.style.format({
            "Env Factor": "x{:.4f}", "Gravel Factor": "x{:.4f}",
            "STOL Factor": "x{:.4f}", "Combined": "x{:.4f}"}),
            use_container_width=True, hide_index=True)

        # Detail table
        st.markdown(f'<div class="sec-head">{svg_icon("search", 20)} <span>Detailed</span> Item Breakdown</div>', unsafe_allow_html=True)
        categories = ["All"] + sorted(df["Category"].unique().tolist())
        sel_cat = st.selectbox("Filter by Category", categories)
        df_show = df if sel_cat == "All" else df[df["Category"] == sel_cat]

        st.dataframe(df_show.style.format({
            "Material (EUR)": "EUR {:,.2f}", "Occ/yr (Cal)": "{:.4f}", "Occ/yr (Usage)": "{:.4f}",
            "Occ/yr (Used)": "{:.4f}", "Adj. Factor": "{:.4f}", "DMC Labour (EUR/FH)": "EUR {:.4f}",
            "DMC Material (EUR/FH)": "EUR {:.4f}", "DMC Total (EUR/FH)": "EUR {:.4f}"}),
            use_container_width=True, hide_index=True, height=600)


    else:
        # Pre-calculation state
        st.markdown("""
        <div style="text-align:center; padding:3rem 0; color:#94A3B8;">
            <div style="font-size:3rem; margin-bottom:0.5rem;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#CBD5E1" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            </div>
            <div style="font-size:1.1rem; font-weight:600; color:#64748B;">Ready to calculate</div>
            <div style="font-size:0.85rem; margin-top:0.25rem;">Verify your parameters above, then press CALCULATE DMC</div>
        </div>
        """, unsafe_allow_html=True)


# ================================================================
# REPORT
# ================================================================
elif st.session_state.page == "Report":

    st.markdown(f"""
    <div class="hero" style="padding:2rem 2.5rem 1.5rem 2.5rem;">
        <div class="hero-brand">{svg_icon("download", 14)} Export</div>
        <div class="hero-title" style="font-size:2rem;">DMC <span>Report</span></div>
        <div class="hero-sub">Generate and download professional DMC reports in PDF and Excel formats.</div>
    </div>
    """, unsafe_allow_html=True)

    s = st.session_state.setup
    if s["fh_per_year"] == 0 or s["fc_per_year"] == 0:
        st.error("Please complete Setup and Calculate first.")
        st.stop()

    ef = ENVIRONMENT_FACTORS[s["environment"]]
    gf = 1.0 + (s["gravel_pct"] / 100) * 0.15
    sf = 1.0 + (s["stol_pct"] / 100) * 0.10
    combined = ef * gf * sf

    results = calculate_dmc(DO328_100_DATA, s["fh_per_year"], s["fc_per_year"],
        s["apu_hrs_per_year"], s["labour_rate"], s["environment"], s["gravel_pct"], s["stol_pct"])
    df = pd.DataFrame(results)

    total_labour = df["DMC Labour (EUR/FH)"].sum()
    total_material = df["DMC Material (EUR/FH)"].sum()
    total_dmc = total_labour + total_material

    st.markdown(f"""
    <div class="metrics">
        <div class="metric"><div class="metric-label">Total DMC</div><div class="metric-val">EUR {total_dmc:,.2f} /FH</div></div>
        <div class="metric"><div class="metric-label">Labour</div><div class="metric-val">EUR {total_labour:,.2f} /FH</div></div>
        <div class="metric"><div class="metric-label">Material</div><div class="metric-val">EUR {total_material:,.2f} /FH</div></div>
        <div class="metric"><div class="metric-label">Annual</div><div class="metric-val">EUR {total_dmc * s['fh_per_year']:,.0f}</div></div>
    </div>
    """, unsafe_allow_html=True)

    op_name = s["operator"].replace(" ", "_") if s["operator"] else "Generic"
    base_filename = f"MaintEdge_DMC_{s['aircraft_type'].replace(' ', '_')}_{op_name}_{s['fh_per_year']}FH"

    # ── EXCEL EXPORT ──
    st.markdown(f'<div class="sec-head">{svg_icon("file", 20)} <span>Excel</span> Report</div>', unsafe_allow_html=True)

    def generate_excel():
        import io
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter

        wb = Workbook()

        # --- Sheet 1: Summary ---
        ws1 = wb.active
        ws1.title = "DMC Summary"

        # Colors
        navy_fill = PatternFill(start_color="0A1628", end_color="0A1628", fill_type="solid")
        blue_fill = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
        light_blue_fill = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")
        header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
        alt_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
        white_font = Font(name="Arial", color="FFFFFF", bold=True)
        blue_font = Font(name="Arial", color="2563EB", bold=True, size=11)
        title_font = Font(name="Arial", color="FFFFFF", bold=True, size=16)
        sub_font = Font(name="Arial", color="94A3B8", size=10)
        normal_font = Font(name="Arial", size=10)
        bold_font = Font(name="Arial", size=10, bold=True)
        thin_border = Border(
            left=Side(style="thin", color="E2E8F0"),
            right=Side(style="thin", color="E2E8F0"),
            top=Side(style="thin", color="E2E8F0"),
            bottom=Side(style="thin", color="E2E8F0"),
        )

        # Title banner
        for col in range(1, 9):
            ws1.cell(row=1, column=col).fill = navy_fill
            ws1.cell(row=2, column=col).fill = navy_fill
            ws1.cell(row=3, column=col).fill = navy_fill
        ws1.merge_cells("A1:H1")
        ws1.cell(row=1, column=1, value="MaintEdge -- DMC Report").font = title_font
        ws1.merge_cells("A2:H2")
        ws1.cell(row=2, column=1, value="Deutsche Aircraft GmbH -- Direct Maintenance Cost Calculator").font = sub_font
        ws1.merge_cells("A3:H3")
        from datetime import datetime
        ws1.cell(row=3, column=1, value=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}").font = sub_font

        # Parameters section
        row = 5
        ws1.cell(row=row, column=1, value="OPERATIONAL PARAMETERS").font = blue_font
        row = 6
        param_data = [
            ("Aircraft Type", s["aircraft_type"]),
            ("Operator", s["operator"] or "N/A"),
            ("Base Country", s["base_country"] or "N/A"),
            ("FH / Year", f"{s['fh_per_year']:,}"),
            ("FC / Year", f"{s['fc_per_year']:,}"),
            ("APU Hrs / Year", f"{s['apu_hrs_per_year']:,}"),
            ("FH/FC Ratio", f"{s['fh_fc_ratio']:.2f}"),
            ("Labour Rate (EUR/hr)", f"{s['labour_rate']:.2f}"),
            ("Environment", s["environment"]),
            ("Environment Factor", f"x{ef:.2f}"),
            ("Gravel Operations", f"{s['gravel_pct']}% (x{gf:.2f})"),
            ("STOL Operations", f"{s['stol_pct']}% (x{sf:.2f})"),
            ("Combined Factor", f"x{combined:.3f}"),
        ]
        for param, val in param_data:
            ws1.cell(row=row, column=1, value=param).font = bold_font
            ws1.cell(row=row, column=3, value=val).font = normal_font
            if row % 2 == 0:
                for c in range(1, 5):
                    ws1.cell(row=row, column=c).fill = alt_fill
            row += 1

        # Totals
        row += 1
        ws1.cell(row=row, column=1, value="DMC RESULTS").font = blue_font
        row += 1
        unsched_xl = total_dmc * 0.40
        logistics_xl = total_dmc * 0.15
        total_all_in_xl = total_dmc + unsched_xl + logistics_xl
        for label, val in [("Scheduled DMC (EUR/FH)", total_dmc), ("Labour DMC (EUR/FH)", total_labour),
                           ("Material DMC (EUR/FH)", total_material), ("Annual Scheduled DMC (EUR)", total_dmc * s["fh_per_year"]),
                           ("Unscheduled Maintenance (40%)", unsched_xl), ("Logistics & Customs (15%)", logistics_xl),
                           ("All-In DMC Estimate (EUR/FH)", total_all_in_xl), ("All-In Annual (EUR)", total_all_in_xl * s["fh_per_year"])]:
            ws1.cell(row=row, column=1, value=label).font = bold_font
            cell = ws1.cell(row=row, column=3, value=round(val, 2))
            cell.font = Font(name="Arial", size=11, bold=True, color="2563EB")
            cell.number_format = '#,##0.00'
            row += 1

        ws1.column_dimensions["A"].width = 22
        ws1.column_dimensions["B"].width = 5
        ws1.column_dimensions["C"].width = 25
        ws1.column_dimensions["D"].width = 15

        # --- Sheet 2: Category Summary ---
        ws2 = wb.create_sheet("Category Summary")
        cat_sum = df.groupby("Category").agg({
            "DMC Labour (EUR/FH)": "sum", "DMC Material (EUR/FH)": "sum", "DMC Total (EUR/FH)": "sum"
        }).reset_index()
        cat_sum = cat_sum.sort_values("DMC Total (EUR/FH)", ascending=False)
        cat_sum["% of Total"] = (cat_sum["DMC Total (EUR/FH)"] / total_dmc * 100).round(1)

        headers2 = ["Category", "Labour (EUR/FH)", "Material (EUR/FH)", "Total (EUR/FH)", "% of Total"]
        for c, h in enumerate(headers2, 1):
            cell = ws2.cell(row=1, column=c, value=h)
            cell.font = white_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center")
        for r_idx, row_data in enumerate(cat_sum.itertuples(index=False), 2):
            ws2.cell(row=r_idx, column=1, value=row_data[0]).font = normal_font
            for c in range(1, 4):
                cell = ws2.cell(row=r_idx, column=c+1, value=round(row_data[c], 2))
                cell.font = normal_font
                cell.number_format = '#,##0.00'
                cell.alignment = Alignment(horizontal="center")
            ws2.cell(row=r_idx, column=5, value=round(row_data[4], 1)).number_format = '0.0'
            if r_idx % 2 == 0:
                for c in range(1, 6):
                    ws2.cell(row=r_idx, column=c).fill = alt_fill
        for c in range(1, 6):
            ws2.column_dimensions[get_column_letter(c)].width = 22

        # --- Sheet 3: Full Detail ---
        ws3 = wb.create_sheet("Detailed Breakdown")
        detail_cols = ["Category", "Inspection", "Interval 1", "Interval 2", "MH",
                       "Material (EUR)", "Occ/yr (Used)", "Driver",
                       "DMC Labour (EUR/FH)", "DMC Material (EUR/FH)", "DMC Total (EUR/FH)"]
        for c, h in enumerate(detail_cols, 1):
            cell = ws3.cell(row=1, column=c, value=h)
            cell.font = white_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center")
        for r_idx, (_, row_data) in enumerate(df.iterrows(), 2):
            for c, col_name in enumerate(detail_cols, 1):
                val = row_data[col_name]
                cell = ws3.cell(row=r_idx, column=c, value=val)
                cell.font = normal_font
                if isinstance(val, float):
                    cell.number_format = '#,##0.0000' if "EUR/FH" in col_name else '#,##0.00'
                cell.alignment = Alignment(horizontal="center") if c > 2 else Alignment()
            if r_idx % 2 == 0:
                for c in range(1, len(detail_cols) + 1):
                    ws3.cell(row=r_idx, column=c).fill = alt_fill
        for c in range(1, len(detail_cols) + 1):
            ws3.column_dimensions[get_column_letter(c)].width = 20

        buffer = io.BytesIO()
        wb.save(buffer)
        return buffer.getvalue()

    excel_data = generate_excel()
    st.download_button(
        label="Download Excel Report (.xlsx)",
        data=excel_data,
        file_name=f"{base_filename}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # ── PDF EXPORT ──
    st.markdown(f'<div class="sec-head">{svg_icon("file", 20)} <span>PDF</span> Report</div>', unsafe_allow_html=True)

    def generate_pdf():
        import io
        from datetime import datetime
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm, cm
        from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
        from reportlab.pdfgen import canvas as pdfcanvas

        buffer = io.BytesIO()

        # Custom colors
        NAVY = colors.HexColor("#0A1628")
        DARK_BLUE = colors.HexColor("#1E293B")
        BRAND_BLUE = colors.HexColor("#2563EB")
        LIGHT_BLUE = colors.HexColor("#EFF6FF")
        CYAN = colors.HexColor("#22D3EE")
        SLATE_600 = colors.HexColor("#475569")
        SLATE_400 = colors.HexColor("#94A3B8")
        SLATE_200 = colors.HexColor("#E2E8F0")
        SLATE_100 = colors.HexColor("#F1F5F9")
        SLATE_50 = colors.HexColor("#F8FAFC")
        GREEN = colors.HexColor("#059669")
        WHITE = colors.white

        page_w, page_h = A4

        # Page template with header/footer
        class PDFTemplate:
            def __init__(self, doc):
                self.doc = doc

            def on_page(self, canvas, doc):
                canvas.saveState()
                # Header line
                canvas.setStrokeColor(BRAND_BLUE)
                canvas.setLineWidth(2)
                canvas.line(15*mm, page_h - 12*mm, page_w - 15*mm, page_h - 12*mm)

                # Header text
                canvas.setFont("Helvetica-Bold", 7)
                canvas.setFillColor(SLATE_400)
                canvas.drawString(15*mm, page_h - 10*mm, "MAINTEDGE  |  DIRECT MAINTENANCE COST REPORT")
                canvas.drawRightString(page_w - 15*mm, page_h - 10*mm, "DEUTSCHE AIRCRAFT GMBH")

                # Footer
                canvas.setStrokeColor(SLATE_200)
                canvas.setLineWidth(0.5)
                canvas.line(15*mm, 14*mm, page_w - 15*mm, 14*mm)
                canvas.setFont("Helvetica", 6.5)
                canvas.setFillColor(SLATE_400)
                canvas.drawString(15*mm, 10*mm, "CONFIDENTIAL  --  Deutsche Aircraft GmbH  --  For authorized use only")
                canvas.drawRightString(page_w - 15*mm, 10*mm, f"Page {doc.page}")
                canvas.restoreState()

            def on_first_page(self, canvas, doc):
                canvas.saveState()

                # Full-width navy header banner
                canvas.setFillColor(NAVY)
                canvas.rect(0, page_h - 55*mm, page_w, 55*mm, fill=1, stroke=0)

                # Accent line at bottom of banner
                canvas.setStrokeColor(BRAND_BLUE)
                canvas.setLineWidth(2.5)
                canvas.line(0, page_h - 55*mm, page_w, page_h - 55*mm)

                # Brand text
                canvas.setFont("Helvetica", 7)
                canvas.setFillColor(SLATE_400)
                canvas.drawString(20*mm, page_h - 15*mm, "DEUTSCHE AIRCRAFT GMBH")

                # Title
                canvas.setFont("Helvetica-Bold", 26)
                canvas.setFillColor(WHITE)
                canvas.drawString(20*mm, page_h - 28*mm, "MaintEdge")

                # Subtitle
                canvas.setFont("Helvetica", 13)
                canvas.setFillColor(colors.HexColor("#CBD5E1"))
                canvas.drawString(20*mm, page_h - 36*mm, "Direct Maintenance Cost Report")

                # Meta info
                canvas.setFont("Helvetica", 8)
                canvas.setFillColor(SLATE_400)
                canvas.drawString(20*mm, page_h - 46*mm,
                    f"{s['aircraft_type']}  |  {s['operator'] or 'N/A'}  |  {s['base_country'] or 'N/A'}  |  {datetime.now().strftime('%d %B %Y')}")

                # Right side: total DMC highlight box
                box_x = page_w - 70*mm
                box_y = page_h - 48*mm
                canvas.setFillColor(colors.HexColor("#162240"))
                canvas.roundRect(box_x, box_y, 52*mm, 28*mm, 3*mm, fill=1, stroke=0)
                canvas.setStrokeColor(colors.HexColor("#2563EB50"))
                canvas.setLineWidth(0.5)
                canvas.roundRect(box_x, box_y, 52*mm, 28*mm, 3*mm, fill=0, stroke=1)

                canvas.setFont("Helvetica", 6.5)
                canvas.setFillColor(colors.HexColor("#60A5FA"))
                canvas.drawCentredString(box_x + 26*mm, box_y + 21*mm, "TOTAL DMC")
                canvas.setFont("Helvetica-Bold", 16)
                canvas.setFillColor(WHITE)
                canvas.drawCentredString(box_x + 26*mm, box_y + 11*mm, f"EUR {total_dmc:,.2f}")
                canvas.setFont("Helvetica", 7)
                canvas.setFillColor(SLATE_400)
                canvas.drawCentredString(box_x + 26*mm, box_y + 4*mm, "per Flight Hour")

                # Footer on first page too
                canvas.setStrokeColor(SLATE_200)
                canvas.setLineWidth(0.5)
                canvas.line(15*mm, 14*mm, page_w - 15*mm, 14*mm)
                canvas.setFont("Helvetica", 6.5)
                canvas.setFillColor(SLATE_400)
                canvas.drawString(15*mm, 10*mm, "CONFIDENTIAL  --  Deutsche Aircraft GmbH  --  For authorized use only")
                canvas.drawRightString(page_w - 15*mm, 10*mm, f"Page {doc.page}")

                canvas.restoreState()

        tmpl = PDFTemplate(None)

        doc = SimpleDocTemplate(buffer, pagesize=A4,
            topMargin=60*mm, bottomMargin=20*mm, leftMargin=15*mm, rightMargin=15*mm)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="SH", fontName="Helvetica-Bold", fontSize=12,
            textColor=NAVY, spaceBefore=10, spaceAfter=6))
        styles.add(ParagraphStyle(name="SH2", fontName="Helvetica-Bold", fontSize=10,
            textColor=BRAND_BLUE, spaceBefore=8, spaceAfter=4))
        styles.add(ParagraphStyle(name="Body9", fontName="Helvetica", fontSize=9,
            textColor=SLATE_600, spaceAfter=3, leading=13))
        styles.add(ParagraphStyle(name="Small", fontName="Helvetica", fontSize=7.5,
            textColor=SLATE_400, spaceAfter=2))

        story = []

        # ── Section 1: Operational Parameters ──
        story.append(Paragraph("1. Operational Parameters", styles["SH"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=SLATE_200, spaceAfter=6))

        param_rows = [
            ["Parameter", "Value", "Parameter", "Value"],
            ["Aircraft Type", s["aircraft_type"], "Operator", s["operator"] or "N/A"],
            ["Base Country", s["base_country"] or "N/A", "Labour Rate", f"EUR {s['labour_rate']:.2f}/hr"],
            ["FH / Year", f"{s['fh_per_year']:,}", "FC / Year", f"{s['fc_per_year']:,}"],
            ["APU Hrs / Year", f"{s['apu_hrs_per_year']:,}", "FH/FC Ratio", f"{s['fh_fc_ratio']:.2f}"],
            ["Environment", s["environment"], "Env. Factor", f"x{ef:.2f}"],
            ["Gravel Ops", f"{s['gravel_pct']}% (x{gf:.2f})", "STOL Ops", f"{s['stol_pct']}% (x{sf:.2f})"],
            ["Combined Factor", f"x{combined:.3f}", "", ""],
        ]
        pt = Table(param_rows, colWidths=[38*mm, 42*mm, 38*mm, 42*mm])
        pt.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("BACKGROUND", (0, 0), (-1, 0), DARK_BLUE),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (2, 1), (2, -1), "Helvetica-Bold"),
            ("TEXTCOLOR", (0, 1), (0, -1), DARK_BLUE),
            ("TEXTCOLOR", (2, 1), (2, -1), DARK_BLUE),
            ("TEXTCOLOR", (1, 1), (1, -1), SLATE_600),
            ("TEXTCOLOR", (3, 1), (3, -1), SLATE_600),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, SLATE_50]),
            ("GRID", (0, 0), (-1, -1), 0.4, SLATE_200),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(pt)
        story.append(Spacer(1, 8*mm))

        # ── Section 2: DMC Summary ──
        story.append(Paragraph("2. DMC Summary", styles["SH"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=SLATE_200, spaceAfter=6))

        labour_pct_val = (total_labour / total_dmc * 100) if total_dmc > 0 else 0
        material_pct_val = 100 - labour_pct_val
        unsched = total_dmc * 0.40
        logistics = total_dmc * 0.15
        total_all_in = total_dmc + unsched + logistics

        sum_rows = [
            ["Component", "EUR / FH", "EUR / Year", "% of Total"],
            ["Scheduled DMC (Total)", f"{total_dmc:,.2f}", f"{total_dmc * s['fh_per_year']:,.0f}", "100.0%"],
            ["  Labour", f"{total_labour:,.2f}", f"{total_labour * s['fh_per_year']:,.0f}", f"{labour_pct_val:.1f}%"],
            ["  Material", f"{total_material:,.2f}", f"{total_material * s['fh_per_year']:,.0f}", f"{material_pct_val:.1f}%"],
            ["Unscheduled Maintenance (40%)", f"{unsched:,.2f}", f"{unsched * s['fh_per_year']:,.0f}", "40.0%"],
            ["Logistics & Customs (15%)", f"{logistics:,.2f}", f"{logistics * s['fh_per_year']:,.0f}", "15.0%"],
            ["All-In DMC Estimate", f"{total_all_in:,.2f}", f"{total_all_in * s['fh_per_year']:,.0f}", "155.0%"],
        ]
        st2 = Table(sum_rows, colWidths=[50*mm, 35*mm, 40*mm, 30*mm])
        st2.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#EFF6FF")),
            ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
            ("TEXTCOLOR", (1, 1), (1, 1), BRAND_BLUE),
            ("FONTSIZE", (1, 1), (1, 1), 10),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#0A1628")),
            ("TEXTCOLOR", (0, -1), (-1, -1), WHITE),
            ("FONTSIZE", (0, -1), (-1, -1), 10),
            ("ROWBACKGROUNDS", (0, 2), (-1, -2), [WHITE, SLATE_50]),
            ("GRID", (0, 0), (-1, -1), 0.4, SLATE_200),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (0, -1), 8),
        ]))
        story.append(st2)
        story.append(Spacer(1, 6*mm))

        # ── Section 3: Category Breakdown ──
        story.append(Paragraph("3. Category Breakdown", styles["SH"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=SLATE_200, spaceAfter=6))

        cat_sum_pdf = df.groupby("Category").agg({
            "DMC Labour (EUR/FH)": "sum", "DMC Material (EUR/FH)": "sum", "DMC Total (EUR/FH)": "sum"
        }).reset_index()
        cat_sum_pdf = cat_sum_pdf.sort_values("DMC Total (EUR/FH)", ascending=False)
        cat_sum_pdf["pct"] = (cat_sum_pdf["DMC Total (EUR/FH)"] / total_dmc * 100).round(1)

        cat_rows = [["#", "Category", "Labour (EUR/FH)", "Material (EUR/FH)", "Total (EUR/FH)", "%"]]
        for idx, (_, r) in enumerate(cat_sum_pdf.iterrows(), 1):
            cat_rows.append([str(idx), r["Category"], f"{r['DMC Labour (EUR/FH)']:.2f}",
                f"{r['DMC Material (EUR/FH)']:.2f}", f"{r['DMC Total (EUR/FH)']:.2f}", f"{r['pct']:.1f}%"])

        ct = Table(cat_rows, colWidths=[8*mm, 48*mm, 28*mm, 28*mm, 28*mm, 16*mm])
        ct.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BACKGROUND", (0, 0), (-1, 0), DARK_BLUE),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, SLATE_50]),
            ("GRID", (0, 0), (-1, -1), 0.4, SLATE_200),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ("ALIGN", (2, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (1, 0), (1, -1), 6),
        ]))
        story.append(ct)

        # ── Detailed Breakdown (continues on same page, no forced break) ──
        story.append(Spacer(1, 6*mm))
        story.append(Paragraph("4. Detailed Item Breakdown", styles["SH"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=SLATE_200, spaceAfter=4))
        story.append(Paragraph(
            f"All {len(df)} scheduled maintenance items with computed occurrences and DMC rates. "
            f"Category-specific adjustment factors applied per item.",
            styles["Small"]))
        story.append(Spacer(1, 2*mm))

        det_cols = ["Inspection", "Cat.", "Int 1", "Int 2", "MH", "Mat (EUR)", "Occ/yr", "Adj.F", "Total EUR/FH"]
        det_rows = [det_cols]
        for _, r in df.iterrows():
            cat_short = r["Category"].replace("Corrosion Prevention ", "").replace("Structural Sampling ", "").replace("Fatigue Damage ", "").replace("Time Controlled ", "TC ")
            det_rows.append([
                r["Inspection"], cat_short, r["Interval 1"], r["Interval 2"],
                f"{r['MH']}", f"{r['Material (EUR)']:,.0f}", f"{r['Occ/yr (Used)']:.3f}",
                f"{r['Adj. Factor']:.3f}", f"{r['DMC Total (EUR/FH)']:.4f}",
            ])

        dt = Table(det_rows, colWidths=[24*mm, 14*mm, 14*mm, 14*mm, 10*mm, 16*mm, 14*mm, 12*mm, 22*mm],
                   repeatRows=1)
        dt.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 6),
            ("FONTSIZE", (0, 1), (-1, -1), 5.8),
            ("BACKGROUND", (0, 0), (-1, 0), DARK_BLUE),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, SLATE_50]),
            ("GRID", (0, 0), (-1, -1), 0.25, SLATE_200),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (0, -1), 3),
        ]))
        story.append(dt)

        # ── Disclaimer ──
        story.append(Spacer(1, 8*mm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=SLATE_200, spaceAfter=4))
        story.append(Paragraph("Disclaimer & Notes", ParagraphStyle(name="DiscHead",
            fontName="Helvetica-Bold", fontSize=8, textColor=DARK_BLUE, spaceAfter=3)))

        disc_style = ParagraphStyle(name="Disc", fontName="Helvetica", fontSize=7,
            textColor=SLATE_600, leading=9.5, spaceAfter=2, alignment=TA_JUSTIFY)

        story.append(Paragraph(
            "1. This report is generated by MaintEdge v1.0, a Direct Maintenance Cost estimation tool developed by "
            "Deutsche Aircraft GmbH. All cost figures are estimates based on the OEM maintenance programme, assumed "
            "utilization profiles, and engineering-derived adjustment factors. Actual maintenance costs may vary "
            "depending on operator-specific practices, MRO capabilities, regulatory requirements, and supply chain conditions.",
            disc_style))
        story.append(Paragraph(
            "2. Unscheduled maintenance costs are estimated at 40% of scheduled DMC based on industry benchmarks for "
            "regional turboprop aircraft. Logistics and customs costs are estimated at 15% of scheduled DMC. These "
            "percentages are indicative and should be validated against operator-specific experience.",
            disc_style))
        story.append(Paragraph(
            "3. Category-specific environmental and operational adjustment factors are based on engineering judgement, "
            "OEM experience, and published industry data. They have not been statistically validated against a large "
            "in-service dataset for every environment-category combination. Users should apply professional judgement "
            "when interpreting results for contractual or financial planning purposes.",
            disc_style))
        story.append(Paragraph(
            "4. Material costs reflect current OEM catalogue pricing and may be subject to escalation, discount "
            "agreements, exchange rate fluctuations, and availability constraints. Labour rates are user-defined and "
            "should reflect the actual cost of certified maintenance personnel at the applicable MRO.",
            disc_style))
        story.append(Paragraph(
            "5. This document is provided for informational purposes only and does not constitute a binding cost "
            "commitment or warranty by Deutsche Aircraft GmbH. Any use of this data for lease agreements, maintenance "
            "reserve calculations, or financial planning is at the sole discretion and risk of the user.",
            disc_style))
        story.append(Spacer(1, 4*mm))
        story.append(Paragraph(
            "MaintEdge by Deutsche Aircraft GmbH  |  Confidential  |  For authorized use only",
            ParagraphStyle(name="FN", fontName="Helvetica-Bold", fontSize=7,
                textColor=SLATE_400, alignment=TA_CENTER)))

        doc.build(story,
            onFirstPage=tmpl.on_first_page,
            onLaterPages=tmpl.on_page)
        return buffer.getvalue()

    try:
        pdf_data = generate_pdf()
        st.download_button(
            label="Download PDF Report (.pdf)",
            data=pdf_data,
            file_name=f"{base_filename}.pdf",
            mime="application/pdf",
        )
    except ImportError:
        st.warning("PDF export requires reportlab. Install with: pip install reportlab")

    # Parameters reference
    st.markdown("---")
    st.markdown(f'<div class="sec-head">{svg_icon("settings", 20)} <span>Report</span> Parameters</div>', unsafe_allow_html=True)

    params = {
        "Parameter": [
            "Aircraft Type", "Operator", "Base Country", "FH/Year", "FC/Year",
            "APU Hrs/Year", "FH/FC Ratio", "Labour Rate", "Environment",
            "Environment Factor", "Gravel %", "Gravel Factor", "STOL %", "STOL Factor",
            "Factors", "Category-Specific",
        ],
        "Value": [
            s["aircraft_type"], s["operator"] or "N/A", s["base_country"] or "N/A",
            f"{s['fh_per_year']:,}", f"{s['fc_per_year']:,}", f"{s['apu_hrs_per_year']:,}",
            f"{s['fh_fc_ratio']:.2f}", f"EUR {s['labour_rate']:.2f}/hr", s["environment"],
            f"x{ef:.2f}", f"{s['gravel_pct']}%", f"x{gf:.2f}", f"{s['stol_pct']}%", f"x{sf:.2f}",
            "Env x Gravel x STOL", "Weighted per category (see Calculate page)",
        ],
    }
    st.dataframe(pd.DataFrame(params), use_container_width=True, hide_index=True)


# Footer
st.markdown('<div class="footer"><strong>MaintEdge</strong> by Deutsche Aircraft GmbH -- DMC Calculator v1.0.0<br>Confidential -- For authorized use only</div>', unsafe_allow_html=True)
