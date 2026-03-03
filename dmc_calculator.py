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
    {"inspection": "Propeller Change",      "int1": None, "param1": None,     "int2": 6000,  "param2": "FC",  "mh": 40,    "mat": 90000.00,   "category": "Heavy Components"},
    {"inspection": "Engine Change (1EA)",   "int1": None, "param1": None,     "int2": 8000,  "param2": "FH",  "mh": 180,   "mat": 1200000.00, "category": "Heavy Components"},
    {"inspection": "Landing Gear Overhaul", "int1": 144,  "param1": "Months", "int2": 22000, "param2": "FC",  "mh": 85,    "mat": 456801.70,  "category": "Heavy Components"},
    {"inspection": "Brakes",                "int1": None, "param1": None,     "int2": 3000,  "param2": "FC",  "mh": 2,     "mat": 93084.12,   "category": "Heavy Components"},
    {"inspection": "APU Overhaul",          "int1": None, "param1": None,     "int2": 8000,  "param2": "FC",  "mh": 20,    "mat": 220000.00,  "category": "Heavy Components"},
]

TIME_CONTROLLED_FLAT_RATE = 40.0


# ----------------------------------------------------------------
# DMC CALCULATION ENGINE
# ----------------------------------------------------------------
def calculate_dmc(data, fh_yr, fc_yr, apu_hrs_yr, labour_rate, env_factor, gravel_factor, stol_factor):
    results = []
    total_ops_factor = env_factor * gravel_factor * stol_factor

    for item in data:
        int1 = item["int1"]
        param1 = item["param1"]
        int2 = item["int2"]
        param2 = item["param2"]
        mh = item["mh"]
        mat = item["mat"]

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

        dmc_labour_adj = dmc_labour * total_ops_factor
        dmc_material_adj = dmc_material * total_ops_factor
        dmc_total = dmc_labour_adj + dmc_material_adj

        results.append({
            "Category": item["category"],
            "Inspection": item["inspection"],
            "Interval 1": f"{int1} {param1}" if int1 and param1 else " -- ",
            "Interval 2": f"{int(int2)} {param2}" if int2 and param2 else " -- ",
            "MH": mh,
            "Material (EUR)": mat,
            "Occ/yr (Cal)": round(occ1, 4),
            "Occ/yr (Usage)": round(occ2, 4),
            "Occ/yr (Used)": round(occ, 4),
            "Driver": occ_source,
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
    page = st.radio("Navigation", ["Home", "Setup", "Calculate", "Report"], label_visibility="collapsed")
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
# SETUP
# ================================================================
elif st.session_state.page == "Setup":

    st.markdown(f"""
    <div class="hero" style="padding:2rem 2.5rem 1.5rem 2.5rem;">
        <div class="hero-brand">{svg_icon("settings", 14)} Configuration</div>
        <div class="hero-title" style="font-size:2rem;">Operational <span>Setup</span></div>
        <div class="hero-sub">Define your aircraft, operator, utilization profile, and operating environment.</div>
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

    # Summary
    st.markdown("---")
    gf = 1.0 + (s["gravel_pct"] / 100) * 0.15
    sf = 1.0 + (s["stol_pct"] / 100) * 0.10
    combined = ef * gf * sf

    st.markdown(f"""
    <div class="metrics">
        <div class="metric"><div class="metric-label">Aircraft</div><div class="metric-val" style="font-size:1rem;">{s["aircraft_type"]}</div><div class="metric-unit">{s["operator"] or "N/A"} | {s["base_country"] or "N/A"}</div></div>
        <div class="metric"><div class="metric-label">Utilization</div><div class="metric-val" style="font-size:1rem;">{s["fh_per_year"]:,} FH / {s["fc_per_year"]:,} FC</div><div class="metric-unit">APU: {s["apu_hrs_per_year"]:,} hrs | Ratio: {ratio}</div></div>
        <div class="metric"><div class="metric-label">Combined Factor</div><div class="metric-val">x{combined:.3f}</div><div class="metric-unit">Env x{ef:.2f} | Gravel x{gf:.2f} | STOL x{sf:.2f}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="info-box info-green">{svg_icon("check", 16)} <strong>Setup complete.</strong> Navigate to <strong>Calculate</strong> to compute DMC.</div>', unsafe_allow_html=True)
    st.session_state.setup = s


# ================================================================
# CALCULATE
# ================================================================
elif st.session_state.page == "Calculate":

    st.markdown(f"""
    <div class="hero" style="padding:2rem 2.5rem 1.5rem 2.5rem;">
        <div class="hero-brand">{svg_icon("chart", 14)} DMC Engine</div>
        <div class="hero-title" style="font-size:2rem;">Cost <span>Calculation</span></div>
        <div class="hero-sub">Direct Maintenance Cost breakdown for Do 328-100 based on your operational setup.</div>
    </div>
    """, unsafe_allow_html=True)

    s = st.session_state.setup
    if s["fh_per_year"] == 0 or s["fc_per_year"] == 0:
        st.error("Please complete the Setup page first.")
        st.stop()

    ef = ENVIRONMENT_FACTORS[s["environment"]]
    gf = 1.0 + (s["gravel_pct"] / 100) * 0.15
    sf = 1.0 + (s["stol_pct"] / 100) * 0.10

    results = calculate_dmc(DO328_100_DATA, s["fh_per_year"], s["fc_per_year"],
        s["apu_hrs_per_year"], s["labour_rate"], ef, gf, sf)
    df = pd.DataFrame(results)

    total_labour = df["DMC Labour (EUR/FH)"].sum() + TIME_CONTROLLED_FLAT_RATE
    total_material = df["DMC Material (EUR/FH)"].sum()
    total_dmc = total_labour + total_material

    st.markdown(f"""
    <div class="metrics">
        <div class="metric"><div class="metric-label">Total DMC</div><div class="metric-val">EUR {total_dmc:,.2f}</div><div class="metric-unit">per Flight Hour</div></div>
        <div class="metric"><div class="metric-label">Labour DMC</div><div class="metric-val">EUR {total_labour:,.2f}</div><div class="metric-unit">per Flight Hour</div></div>
        <div class="metric"><div class="metric-label">Material DMC</div><div class="metric-val">EUR {total_material:,.2f}</div><div class="metric-unit">per Flight Hour</div></div>
        <div class="metric"><div class="metric-label">Annual DMC</div><div class="metric-val">EUR {total_dmc * s["fh_per_year"]:,.0f}</div><div class="metric-unit">at {s["fh_per_year"]:,} FH/yr</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Category summary
    st.markdown(f'<div class="sec-head">{svg_icon("layers", 20)} <span>Category</span> Breakdown</div>', unsafe_allow_html=True)

    cat_sum = df.groupby("Category").agg({
        "DMC Labour (EUR/FH)": "sum", "DMC Material (EUR/FH)": "sum", "DMC Total (EUR/FH)": "sum"
    }).reset_index()
    tc_row = pd.DataFrame([{"Category": "Time Controlled Items",
        "DMC Labour (EUR/FH)": TIME_CONTROLLED_FLAT_RATE, "DMC Material (EUR/FH)": 0.0,
        "DMC Total (EUR/FH)": TIME_CONTROLLED_FLAT_RATE}])
    cat_sum = pd.concat([cat_sum, tc_row], ignore_index=True).sort_values("DMC Total (EUR/FH)", ascending=False)

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
    st.dataframe(cat_disp.style.format({
        "DMC Labour (EUR/FH)": "EUR {:.2f}", "DMC Material (EUR/FH)": "EUR {:.2f}",
        "DMC Total (EUR/FH)": "EUR {:.2f}", "% of Total": "{:.1f}%"}),
        use_container_width=True, hide_index=True)

    # Detail table
    st.markdown(f'<div class="sec-head">{svg_icon("search", 20)} <span>Detailed</span> Item Breakdown</div>', unsafe_allow_html=True)
    categories = ["All"] + sorted(df["Category"].unique().tolist())
    sel_cat = st.selectbox("Filter by Category", categories)
    df_show = df if sel_cat == "All" else df[df["Category"] == sel_cat]

    st.dataframe(df_show.style.format({
        "Material (EUR)": "EUR {:,.2f}", "Occ/yr (Cal)": "{:.4f}", "Occ/yr (Usage)": "{:.4f}",
        "Occ/yr (Used)": "{:.4f}", "DMC Labour (EUR/FH)": "EUR {:.4f}",
        "DMC Material (EUR/FH)": "EUR {:.4f}", "DMC Total (EUR/FH)": "EUR {:.4f}"}),
        use_container_width=True, hide_index=True, height=600)

    st.markdown(f'<div class="info-box info-amber">Time Controlled Items: Flat rate of <strong>EUR {TIME_CONTROLLED_FLAT_RATE:.0f}/FH</strong> added to total (not in detail table).</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div class="info-box info-slate">
        <strong>Parameters:</strong> {s["aircraft_type"]} | {s["operator"] or "N/A"} | {s["base_country"] or "N/A"}<br>
        Utilization: {s["fh_per_year"]:,} FH/yr | {s["fc_per_year"]:,} FC/yr | APU: {s["apu_hrs_per_year"]:,} hrs/yr | Labour: EUR {s["labour_rate"]:.2f}/hr<br>
        Factors: Env x{ef:.2f} | Gravel x{gf:.2f} | STOL x{sf:.2f} | Combined x{ef*gf*sf:.3f}
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
        <div class="hero-sub">Download the complete DMC breakdown for your records.</div>
    </div>
    """, unsafe_allow_html=True)

    s = st.session_state.setup
    if s["fh_per_year"] == 0 or s["fc_per_year"] == 0:
        st.error("Please complete Setup and Calculate first.")
        st.stop()

    ef = ENVIRONMENT_FACTORS[s["environment"]]
    gf = 1.0 + (s["gravel_pct"] / 100) * 0.15
    sf = 1.0 + (s["stol_pct"] / 100) * 0.10

    results = calculate_dmc(DO328_100_DATA, s["fh_per_year"], s["fc_per_year"],
        s["apu_hrs_per_year"], s["labour_rate"], ef, gf, sf)
    df = pd.DataFrame(results)

    total_labour = df["DMC Labour (EUR/FH)"].sum() + TIME_CONTROLLED_FLAT_RATE
    total_material = df["DMC Material (EUR/FH)"].sum()
    total_dmc = total_labour + total_material

    st.markdown(f"""
    <div class="metrics">
        <div class="metric"><div class="metric-label">Total DMC</div><div class="metric-val">EUR {total_dmc:,.2f} /FH</div></div>
        <div class="metric"><div class="metric-label">Labour</div><div class="metric-val">EUR {total_labour:,.2f} /FH</div></div>
        <div class="metric"><div class="metric-label">Material</div><div class="metric-val">EUR {total_material:,.2f} /FH</div></div>
    </div>
    """, unsafe_allow_html=True)

    csv_data = df.to_csv(index=False)
    op_name = s["operator"].replace(" ", "_") if s["operator"] else "Generic"
    st.download_button(
        label="Download Full DMC Report (CSV)",
        data=csv_data,
        file_name=f"MaintEdge_DMC_{s['aircraft_type'].replace(' ', '_')}_{op_name}_{s['fh_per_year']}FH.csv",
        mime="text/csv",
    )

    st.markdown("---")
    st.markdown(f'<div class="sec-head">{svg_icon("settings", 20)} <span>Report</span> Parameters</div>', unsafe_allow_html=True)

    params = {
        "Parameter": [
            "Aircraft Type", "Operator", "Base Country", "FH/Year", "FC/Year",
            "APU Hrs/Year", "FH/FC Ratio", "Labour Rate", "Environment",
            "Environment Factor", "Gravel %", "Gravel Factor", "STOL %", "STOL Factor",
            "Combined Ops Factor", "Time Controlled Items",
        ],
        "Value": [
            s["aircraft_type"], s["operator"] or "N/A", s["base_country"] or "N/A",
            f"{s['fh_per_year']:,}", f"{s['fc_per_year']:,}", f"{s['apu_hrs_per_year']:,}",
            f"{s['fh_fc_ratio']:.2f}", f"EUR {s['labour_rate']:.2f}/hr", s["environment"],
            f"x{ef:.2f}", f"{s['gravel_pct']}%", f"x{gf:.2f}", f"{s['stol_pct']}%", f"x{sf:.2f}",
            f"x{ef*gf*sf:.3f}", f"EUR {TIME_CONTROLLED_FLAT_RATE:.0f}/FH (flat)",
        ],
    }
    st.dataframe(pd.DataFrame(params), use_container_width=True, hide_index=True)


# Footer
st.markdown('<div class="footer"><strong>MaintEdge</strong> by Deutsche Aircraft GmbH -- DMC Calculator v1.0.0<br>Confidential -- For authorized use only</div>', unsafe_allow_html=True)
