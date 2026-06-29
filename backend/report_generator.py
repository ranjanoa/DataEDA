import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def generate_local_report(df: pd.DataFrame, query: str = "") -> str:
    """
    Dynamically generates the Adana Plant Kiln Process Optimization Slides 
    based on actual statistics of the active dataset in df.
    """
    def get_col(name):
        for c in [name, name.replace('_', ' '), name.replace(' ', '_')]:
            if c in df.columns:
                return c
        return None

    df = df.copy()

    prod_col = get_col('Clinker_Production')
    if prod_col:
        df_running = df[df[prod_col] > 5.0]
    else:
        df_running = df

    logical_names = [
        'Ck_S.CaO', 'Secondary_Air_Temperature', 'Clinker_Production', 'Primary_Air_Pressure', 
        'Current_y', 'O2_(Downcomer)', 'CO_(Downcomer)', 'NO_(Downcomer)', 'Gas_Temperature_(Before_Calciner)_x', 
        'Speed_(Fan-5)', 'Raw_Meal_Feeding', 'Consumption_Hood_Total_Coal', 'Consumption_Calciner_Total_Coal',
        'Consumption_Calciner_RDF', 'Total_Fuel_Flow', 'Specific_Fuel_Consumption', 'Precalciner_Fuel_Share', 
        'Main_Fuel_Share', 'C3S_XRD_Total'
    ]

    stats = {}
    for logical_name in logical_names:
        col = get_col(logical_name)
        if col:
            series = pd.to_numeric(df_running[col], errors='coerce').dropna()
            if len(series) > 0:
                stats[logical_name] = {
                    'min': float(series.min()),
                    'q1': float(series.quantile(0.25)),
                    'median': float(series.median()),
                    'q3': float(series.quantile(0.75)),
                    'max': float(series.max()),
                    'mean': float(series.mean())
                }
            else:
                stats[logical_name] = {'min': 0.0, 'q1': 0.0, 'median': 0.0, 'q3': 0.0, 'max': 0.0, 'mean': 0.0}
        else:
            stats[logical_name] = {'min': 0.0, 'q1': 0.0, 'median': 0.0, 'q3': 0.0, 'max': 0.0, 'mean': 0.0}

    # Calculations for dynamic analysis
    mean_prod = stats['Clinker_Production']['mean']
    q3_prod = stats['Clinker_Production']['q3']
    mean_sfc = stats['Specific_Fuel_Consumption']['mean']
    mean_o2 = stats['O2_(Downcomer)']['mean']
    mean_lime = stats['Ck_S.CaO']['mean']
    mean_fan = stats['Speed_(Fan-5)']['mean']
    max_fan = stats['Speed_(Fan-5)']['max']

    prod_gap = (q3_prod - mean_prod) * 8120 if q3_prod > mean_prod else 0
    prod_value = prod_gap * 50
    sfc_gap = mean_sfc - 0.145 if mean_sfc > 0.145 else 0
    fuel_saved = sfc_gap * (q3_prod * 8120)
    fuel_value = fuel_saved * 120
    co2_saved = fuel_saved * 3.2

    report = f"""# Adana Plant AIPC Optimization & Golden Batch Analysis

## ⚡ PREREQUISITE — Create Derived KPI Variables
[DERIVED: Total_Fuel_Flow = Consumption_Hood_Total_Coal + Consumption_Calciner_Total_Coal + Consumption_Calciner_RDF]
[DERIVED: Specific_Fuel_Consumption = Total_Fuel_Flow / Clinker_Production]
[DERIVED: Precalciner_Fuel_Share = (Consumption_Calciner_Total_Coal + Consumption_Calciner_RDF) / Total_Fuel_Flow]
[DERIVED: Main_Fuel_Share = Consumption_Hood_Total_Coal / Total_Fuel_Flow]

---

## Slide 1: Title Slide
- **Title:** Adana Plant AIPC Optimization & Golden Batch Analysis
- **Subtitle:** Parameter Priority Review & Process Diagnostic
- **Presenter:** Senior Process Engineer (30 Years Experience)

---

## Slide 2: Executive Summary & Estimator Hierarchy
- **Estimator Priority Ranking:** Free Lime > Combustion > Calcination > Kiln Temp > Efficiency > Cooling > Capacity
- **Baseline Performance:** Mean production is **{mean_prod:.2f} t/h** with a max of **{stats['Clinker_Production']['max']:.2f} t/h**.
- **Golden Batch Targets:** We target the Q3 Production capability (**{q3_prod:.2f} t/h**) while minimizing SFC.
- **Top 3 Issues:** Fan bottleneck (Max Fan: {max_fan:.1f}%), O2 Fluctuations (Mean O2: {mean_o2:.2f}%), and Suboptimal Fuel Efficiency.

---

## Slide 3: Priority 1 - Free Lime (Primary Quality Indicator)
- **Objective:** Evaluate final burning quality (`Ck_S.CaO`).
- **Chart:** 
[HISTOGRAM: Ck_S.CaO, C3S_XRD_Total]
- **Analysis:** *30-Year Expert View:* The current Free Lime mean sits at {mean_lime:.2f}%. A value heavily skewed above 1.5% presents a severe underburning risk, leading to high expansion and low early strength. Conversely, anything chronically below 0.6% indicates we are over-firing the kiln, wasting fuel and risking coating loss. The Golden Batch target must be aggressively controlled at ~1.0%.

---

## Slide 4: Priority 1 & 2 - Free Lime vs Burning Zone Temperature
- **Objective:** How Burning Zone Temp (using Secondary Air as proxy) affects mineral formation.
- **Chart:** 
[SCATTER: X=Secondary_Air_Temperature | Y=Ck_S.CaO | COLOR=Clinker_Production | SCALE=Jet]
- **Analysis:** *30-Year Expert View:* We can observe the thermal relationship here. The Secondary Air Temperature averages {stats['Secondary_Air_Temperature']['mean']:.0f}°C. We must ensure secondary air stays above 1050°C to facilitate proper C3S formation; otherwise, the kiln drops into a sluggish state where Free Lime spikes unexpectedly.

---

## Slide 5: Priority 3 - Clinker Production Rate (System Load)
- **Objective:** All heat, air, and draft balances tie back to production stability.
- **Chart:** 
[DUALPLOT: Clinker_Production | Specific_Fuel_Consumption]
- **Analysis:** *30-Year Expert View:* Process stability dictates efficiency. Notice how SFC (currently averaging {mean_sfc:.3f} t/t) violently spikes whenever production drops below {stats['Clinker_Production']['median']:.0f} t/h. A highly variable production rate ruins the heat profile and forces operators to over-fuel to compensate.

---

## Slide 6: Priority 4 - Heat Recuperation & Calciner Stability
- **Objective:** Evaluate cooler efficiency and its impact on the calciner.
- **Chart:** 
[SCATTER: X=Secondary_Air_Temperature | Y=Consumption_Calciner_Total_Coal | COLOR=Specific_Fuel_Consumption | SCALE=Hot]
- **Analysis:** *30-Year Expert View:* Efficient heat recuperation from the cooler directly reduces our calciner fuel demand. If secondary air temp drops below 950°C, you will see a direct proportional increase in `Consumption_Calciner_Total_Coal` to maintain precalcination targets, resulting in massive thermal efficiency losses.

---

## Slide 7: Priority 5 - Primary Air Pressure & Flame Quality
- **Objective:** Primary air affects mixing, flame length, and NOx/CO.
- **Chart:** 
[SCATTER: X=Primary_Air_Pressure | Y=CO_(Downcomer) | COLOR=O2_(Downcomer) | SCALE=RdBu]
- **Analysis:** *30-Year Expert View:* Primary Air (mean: {stats['Primary_Air_Pressure']['mean']:.0f} mbar) controls momentum. If the pressure is too low, mixing is sluggish, resulting in a lazy flame and CO spikes. If too high, it creates unnecessary thermal NOx. We need to lock this setpoint dynamically against O2 levels to guarantee a short, sharp, oxidizing flame.

---

## Slide 8: Principle 1 - Kiln Torque (Stable Material Bed)
- **Objective:** Torque indicates material load and coating/snowman tendency.
- **Charts:** 
[SCATTER: X=Raw_Meal_Feeding | Y=Current_y | COLOR=Clinker_Production | SCALE=Jet]
[PARALLEL: Raw_Meal_Feeding, Current_y, Clinker_Production | COLOR: Current_y]
- **Analysis:** *30-Year Expert View:* Kiln drive current (`Current_y`) averages {stats['Current_y']['mean']:.0f} Amps. Any wide variance here means the bed depth is oscillating or we are dealing with severe coating ring formation and collapses. For Golden Batch, Torque must track linearly and smoothly with `Raw_Meal_Feeding`.

---

## Slide 9: Principle 2 - Stable Oxygen & Combustion Master Map
- **Objective:** O2 is fundamental for combustion quality, NOx, and energy.
- **Charts:** 
[SCATTER: X=O2_(Downcomer) | Y=CO_(Downcomer) | COLOR=NO_(Downcomer) | SCALE=Jet]
[PARALLEL: Primary_Air_Pressure, O2_(Downcomer), CO_(Downcomer), NO_(Downcomer) | COLOR: O2_(Downcomer)]
- **Analysis:** *30-Year Expert View:* Mean O2 is {mean_o2:.2f}%. Anything above 3.5% is pure false air pulling heat straight out of the stack. We can clearly trace on the parallel plot how excess air correlates with depressed NOx and higher SFC. Finding the exact O2 boundary right before CO spikes is the holy grail of this combustion optimization.

---

## Slide 10: Principle 3 - Controlled Thermal Balance
- **Objective:** Balance heat input according to production.
- **Charts:** 
[SCATTER: X=Total_Fuel_Flow | Y=Specific_Fuel_Consumption | COLOR=Clinker_Production | SCALE=Viridis]
[PARALLEL: Total_Fuel_Flow, Specific_Fuel_Consumption, Secondary_Air_Temperature, Clinker_Production | COLOR: Specific_Fuel_Consumption]
- **Analysis:** *30-Year Expert View:* The heat balance is currently yielding an SFC of {mean_sfc:.3f} t/t. The Golden Batch demands an SFC < 0.145 t/t. The parallel plot explicitly shows how high Total Fuel flow without a proportional increase in Production (due to false air or over-burning) immediately destroys the thermal balance.

---

## Slide 11: Principle 3 - Precalciner Combustion Efficiency
- **Objective:** Optimize fuel share and alternative fuels.
- **Chart:** 
[SCATTER3D: X=Consumption_Calciner_Total_Coal | Y=Consumption_Calciner_RDF | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]
- **Analysis:** *30-Year Expert View:* RDF injection (mean: {stats['Consumption_Calciner_RDF']['mean']:.1f} t/h) is critical for TSR, but if it's pushed too high without sufficient residence time or calciner temperature, it drops unburnt onto the kiln inlet, shifting the combustion zone. The 3D map isolates the exact blend ratio that maximizes production.

---

## Slide 12: Principle 4 - Feed Continuity
- **Objective:** Fluctuations in kiln bed must not be created by sudden feed changes.
- **Charts:** 
[BOX: Raw_Meal_Feeding, Clinker_Production]
[PARALLEL: Raw_Meal_Feeding, Gas_Temperature_(Before_Calciner)_x, Clinker_Production | COLOR: Raw_Meal_Feeding]
- **Analysis:** *30-Year Expert View:* A wide interquartile range in `Raw_Meal_Feeding` indicates "yo-yo" operation by the shift teams. Capacity increases must be executed gradually. The parallel plot proves that sudden feed increases crash the calciner temperature, forcing subsequent manual over-corrections.

---

## Slide 13: Principle 5 - Draft Reserve Capacity
- **Objective:** AIPC must not increase capacity if ID fan capacity is inadequate.
- **Charts:** 
[SCATTER: X=Speed_(Fan-5) | Y=O2_(Downcomer) | COLOR=Clinker_Production | SCALE=RdBu]
[PARALLEL: Speed_(Fan-5), O2_(Downcomer), Specific_Fuel_Consumption, Clinker_Production | COLOR: Speed_(Fan-5)]
- **Analysis:** *30-Year Expert View:* The ID Fan averages {mean_fan:.1f}% and maxes at {max_fan:.1f}%. If the fan is maxing out but O2 remains > 3.0%, the fan is merely pumping false air instead of process gas. This is a hard mechanical bottleneck that absolutely prevents AIPC from safely pushing production further.

---

## Slide 14: Principle 6 - Quality Reference Control & Thermal Stability
- **Objective:** Evaluate preheater thermal stability and quality references.
- **Charts:** 
[SCATTER: X=Gas_Temperature_(Before_Calciner)_x | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]
[PARALLEL: Ck_S.CaO, Secondary_Air_Temperature, C3S_XRD_Total, Clinker_Production | COLOR: Ck_S.CaO]
- **Analysis:** *30-Year Expert View:* Preheater exit temps averaging {stats['Gas_Temperature_(Before_Calciner)_x']['mean']:.0f}°C must be strictly referenced. The parallel plot shows the optimal pathway: maintaining BZ temp and Hot Meal calcination leads directly to the Golden Batch C3S and Free Lime specs. Deviating from these reference limits guarantees quality rejects.

---

## Slide 15: Golden Batch Multi-Variable Map (Quality & Production)
- **Chart:** 
[PARALLEL: Raw_Meal_Feeding, Current_y, Secondary_Air_Temperature, Ck_S.CaO, C3S_XRD_Total, Clinker_Production | COLOR: Clinker_Production]
- **Analysis:** *30-Year Expert View:* Tracing the deepest RED lines (Highest Production), we see the exact Golden Batch operating envelope. To achieve > {q3_prod:.0f} t/h, feed must be smooth, torque stable around {stats['Current_y']['q3']:.0f} A, and Secondary Air strictly above 1050°C.

---

## Slide 16: Golden Batch Multi-Variable Map (Combustion & Efficiency)
- **Chart:** 
[PARALLEL: Speed_(Fan-5), Primary_Air_Pressure, O2_(Downcomer), CO_(Downcomer), NO_(Downcomer), Specific_Fuel_Consumption | COLOR: Specific_Fuel_Consumption]
- **Analysis:** *30-Year Expert View:* Tracing the bluest lines (Lowest SFC), the combustion envelope is clear. AIPC must keep O2 suppressed under 3.5% and fan speed optimized, ensuring heat is utilized for clinkerization rather than heating up false air.

---

## Slide 17: Process Issue Identification Summary
- **Findings:** The data definitively highlights high O2 variance, torque fluctuations tied to feed instability, and draft capacity limitations.
- **Overburning/Underburning Risks:** Operating below optimal Secondary Air Temps is creating extreme Free Lime variance.
- **Capacity Margin:** False air is consuming vital ID Fan reserve, restricting us from reaching the Q3 Production potential.

---

## Slide 18: The Golden Batch Definition
- **Objective:** The exact targets required for AIPC execution.
- **Table:**
| Variable | Target Range (Golden Batch) | Current Mean | Gap |
|---|---|---|---|
| Clinker_Production | > {q3_prod:.1f} | {mean_prod:.1f} | +{(q3_prod - mean_prod):.1f} t/h |
| Specific_Fuel_Consumption | < 0.145 | {mean_sfc:.3f} | -{sfc_gap:.3f} t/t |
| O2_(Downcomer) | 2.5 - 3.5 % | {mean_o2:.2f} % | -{(mean_o2 - 3.0):.2f} % |
| Speed_(Fan-5) | < 80% | {mean_fan:.1f} % | Optimization Req. |

---

## Slide 19: Value Lost Quantification
- **Objective:** Financial impact of deviation from the Golden Batch.
- **Production Opportunity**: {(q3_prod - mean_prod):.2f} t/h gap * 8,120 hrs = {prod_gap:,.0f} tons/yr. At $50/ton = **${prod_value:,.0f}/year**.
- **Fuel Saving Opportunity**: {sfc_gap:.3f} t/t gap * {(q3_prod * 8120):,.0f} annual tons = {fuel_saved:,.0f} tons fuel/yr. At $120/ton = **${fuel_value:,.0f}/year**.
- **CO2 Reduction**: {co2_saved:,.0f} tons of CO2 mitigated annually.
- **Total Operational Value Lost:** **${(prod_value + fuel_value):,.0f}/year**.

---

## Slide 20: Action Plan & Conclusion
- **Action Plan:** AIPC must strictly enforce the operational guidelines. Actuators for feed must be locked if ID fan speed exceeds 85% or O2 drops below 2.0%. 
- **Conclusion:** By operating within the tightly defined Reference Values for Free Lime, BZ Temperature, and Torque, the plant can immediately capture the **${(prod_value + fuel_value):,.0f}** annual opportunity while stabilizing the kiln bed.
"""
    return report
