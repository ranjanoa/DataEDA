# Kiln W3 — Expert Optimization Report (New Variables Edition)
## Data-Specific 3-Part AI Prompt Set
### Persona: Master Operator + Master Process Engineer + Master Data Scientist (30 years experience)

---

> ⚠️ **CRITICAL RUNTIME NOTE FOR AI**: 
> 1. The limits, thresholds, and statistics (means, Q1, Q3, targets, objectives, constraints) listed below are **illustrative references** based on the active plant dataset. 
> 2. You MUST dynamically inspect and extract the actual statistics, percentiles, and setpoint/target parameters from the **ranges summary table** and correlation matrix of the currently uploaded dataset. Look up variables in the dataset ending with `_Target`, `_Minimum_Fuzzy_Constraint`, `_Maximum_Fuzzy_Constraint`, or `_Objective` (e.g. `Pyrometer_-_Target`, `Torque_(AMPS)_-_Target`, `O2_Tower_-_Objective`) to extract the exact operational limits for the active plant.
> 3. **Missing Variables Exclusions**: If any variable from the operational matrix is NOT present in the active dataset's ranges table and correlation matrix, you MUST ignore it or make a brief scientific process assumption about it. DO NOT include it as a metric or parameter in the final report. Keep the report strictly limited to the active variables present in the uploaded correlation matrix and ranges summary.

> **DATA CONTEXT REFERENCE** (new variables ranges summary):
> - **Clinker Production**: mean = 146.71 t/h | Q1 = 149.60 | Q3 = 162.42 | max = 182.55 | **6.51% shutdowns**
> - **Flour Feed**: mean = 245.00 t/h | Q1 = 249.81 | Q3 = 271.52 | max = 319.04
> - **Main Coke**: mean = 5.52 t/h | stable 5.48–6.02 t/h | max = 7.78 (column: `Main_Mass_Coke_Flow_Rate`)
> - **Pre-cal Coke**: mean = 8.19 t/h | stable 7.12–9.96 t/h | max = 13.95 (column: `Pre-cal_Coke_Flow_Rate`)
> - **O2 Cyclone Tower**: mean = 3.50% | stable 2.35–3.38% | objective = 3.0% (column: `Check_O2_Cyclone_Tower`)
> - **CO Cyclone Tower**: mean = 0.11% | stable 0.10–0.13% | **max constraint = 0.14%** (column: `Check_CO_Cyclone_Tower`)
> - **NOx Cyclone Tower**: mean = 439.74 | stable 365.31–513.59 | max constraint = 600 mg/Nm³ (column: `Check_NOx_Cyclone_Tower`)
> - **Pyrometer**: mean = 913.73°C | stable 855.17–1001.25°C | **target = 1050°C | min constraint = 950°C** ← CRITICAL GAP (column: `Optical_Pyrometer_Temp._Burning_Zone`)
> - **Material Temp A55**: mean = 866.68°C | stable 854.60–919.65°C
> - **Kiln Drive Current**: mean = 68.24 A | stable 66.82–75.99 A | **target = 55.00 A | max constraint = 65.00 A** ← CRITICAL OVERLOAD (column: `Furnace_Motor_Current`)
> - **Raw Meal LSF/FSC**: mean = 101.01 | stable 99.90–101.78 (column: `W3_Flour_FSC`)
> - **Raw Meal Silica Modulus**: mean = 2.65 | stable 2.57–2.73 (column: `W3_Flour_MS`)
> - **Raw Meal Sieve Residue**: mean = 16.67% | stable 12.00–20.40% (column: `W3_Flour_#170`)
> - **Clinker Free Lime**: mean = 2.01% | stable 1.70–2.33% (column: `W3_Clinker_CaOL`)
> - **Clinker LSF/FSC**: mean = 98.93 | stable 97.92–99.81 (column: `W3_Clinker_FSC`)
> - **Clinker excess sulfur**: mean = 1150.13 | stable 968.48–1303.96 (column: `W3_-_excess_sulfur`)
> - **Top Cyclone Pressure**: mean = -15.43 mmH2O | stable -17.62 to -14.95 mmH2O (column: `Top_Cyclone_Pressure_A55`)
> - **Exhaust Fan Speed**: mean = 64.63% | stable 65.67–69.74% (column: `Fan_Speed.4`)

---

## ✅ PREREQUISITE — Create Derived KPI Variables
### Run this FIRST in the AI chat, before any of the 3 parts below

```
Create the following 4 derived KPI variables needed for the kiln optimization report.
Output each as a DERIVED tag in exactly this order (order matters — Total_Fuel_Flow must exist before Specific_Fuel_Consumption):

[DERIVED: Total_Fuel_Flow = Main_Mass_Coke_Flow_Rate + Pre-cal_Coke_Flow_Rate]
[DERIVED: Specific_Fuel_Consumption = Total_Fuel_Flow / Clinker_Production]
[DERIVED: Precalciner_Fuel_Share = Pre-cal_Coke_Flow_Rate / Total_Fuel_Flow]
[DERIVED: Main_Fuel_Share = Main_Mass_Coke_Flow_Rate / Total_Fuel_Flow]

Confirm each was created with a one-line summary:
- Total_Fuel_Flow: sum of both coke flows (expected mean ~13.71 t/h)
- Specific_Fuel_Consumption: fuel per ton of clinker (expected mean ~0.094 t/t)
- Precalciner_Fuel_Share: precalciner fraction of total fuel (expected mean ~60%)
- Main_Fuel_Share: main burner fraction of total fuel (expected mean ~40%)
```

---

## ⚡ PART 1 — Production & Fuel Efficiency Analysis

```
You are acting as a master kiln operator, master process engineer, and master data scientist 
with 30 years of cement industry experience. You are preparing a professional process 
optimization report for Kiln W3.

## REPORT GENERATION MANDATORY INSTRUCTIONS:
- You MUST generate the report sequentially, containing every STEP listed below.
- You MUST use the exact Markdown headings for each step (e.g., `### STEP 1 — Executive Summary`).
- Do NOT combine steps, do NOT skip any steps, and do NOT output placeholders. Provide full engineering and data-driven explanations for each section.

Your job is not to state the obvious. Your job is to find WHERE value is being lost, 
QUANTIFY that loss, define the GOLDEN BATCH — the historical operating window where 
this kiln performed best, and analyze the chemical and physical drivers of operation.

The following derived KPIs already exist in the dataset:
- Total_Fuel_Flow = Main_Mass_Coke_Flow_Rate + Pre-cal_Coke_Flow_Rate (~13.71 t/h at mean)
- Specific_Fuel_Consumption = Total_Fuel_Flow / Clinker_Production (~0.094 t/t at mean)
- Precalciner_Fuel_Share = Pre-cal_Coke_Flow_Rate / Total_Fuel_Flow (~60% at mean)
- Main_Fuel_Share = Main_Mass_Coke_Flow_Rate / Total_Fuel_Flow (~40% at mean)

Confirmed statistics:
- Clinker Production: mean=146.71, Q1=149.60, Q3=162.42, max=182.55 t/h (6.51% zeros/shutdowns)
- Flour Feed: mean=245.00, Q1=249.81, Q3=271.52, max=319.04 t/h
- Main Coke Flow: mean=5.52, stable range 5.48–6.02 t/h, max=7.78
- Pre-cal Coke Flow: mean=8.19, stable range 7.12–9.96 t/h, max=13.95
- Kiln Drive Current: mean=68.24, stable range 66.82–75.99 A, max=98.49 A (Target = 55.00 A, Max constraint = 65.00 A)
- Correlation: Flour_Feed vs Clinker_Production = +0.997 (near-perfect LOI-mass balance)
- Correlation: Main_Mass_Coke_Flow_Rate vs Clinker_Production = +0.881
- Correlation: Pre-cal_Coke_Flow_Rate vs Clinker_Production = +0.772
- Correlation: Check_O2_Cyclone_Tower vs Clinker_Production = -0.771
- Correlation: Furnace_Motor_Current vs Clinker_Production = +0.819 (kiln load scales strongly with production)

Quality Drivers & Chemical Moduli Correlations:
- Clinker Free Lime (W3_Clinker_CaOL): mean = 2.01% | stable = 1.70 - 2.33% (indicates unburnt lime)
- Clinker LSF/FSC (W3_Clinker_FSC): mean = 98.93 | stable = 97.92 - 99.81 (potential calcium saturation limit)
- Raw Meal LSF/FSC (W3_Flour_FSC): mean = 101.01 | stable = 99.90 - 101.78
- Raw Meal Silica Modulus (W3_Flour_MS): mean = 2.65 | stable = 2.57 - 2.73
- Raw Meal Sieve Residue (W3_Flour_#170): mean = 16.67% | stable = 12.00 - 20.40% (meal coarseness indicator)
- Clinker Litre Weight (W3_Clinker_Weight_Liter): mean = 1008.45 g/l | stable = 980.00 - 1030.00 g/l (sintering degree)
- Correlation: Free Lime vs Clinker LSF/FSC = +0.502 (chemical drive for excess calcium free lime)
- Correlation: Free Lime vs W3_Flour_FSC = +0.300 (raw meal LSF drive)
- Correlation: Free Lime vs W3_Flour_MS = +0.147 (silica modulus burns harder)
- Correlation: Free Lime vs W3_Fe2O3_Clinker = -0.282 (fluxing effect of iron oxide on liquid phase combination)
- Correlation: Free Lime vs Clinker Litre Weight = -0.192 (higher bulk density / sintering reduces free lime)
- Correlation: Free Lime vs Flour Sieve Residue = +0.198 (coarser raw meal degrades burnability and raises free lime)

---

## STEP 1 — Executive Summary (as an expert, not a textbook)

Write 9 bullet points. You MUST reference the actual statistics and parameters from the ranges summary table of the active dataset. Cover:
1. Current production performance vs peak capability (mean vs max in active dataset) — what is the gap?
2. If the kiln could operate at Q3 production instead of mean, how many extra tons per year (assuming ~8,120 operating hours/year at the actual shutdown rate from the active dataset)?
3. What does feed-to-production correlation (e.g. Flour_Feed vs Clinker_Production) mean for the operator — is production feed-limited?
4. What is the actual Total_Fuel_Flow at mean conditions in your dataset? What is the Specific_Fuel_Consumption at mean?
5. What would SFC be if production increased to Q3 without increasing fuel?
6. Sintering & Quality drivers: explain how raw meal LSF (`W3_Flour_FSC`) and silica modulus (`W3_Flour_MS`) correlate with clinker quality (free lime `W3_Clinker_CaOL`), and how iron oxide (`W3_Fe2O3_Clinker`) acts as a fluxing countermeasure.
7. Meal Fineness: analyze the impact of sieve residue (`W3_Flour_#170`) on the burnability of the raw meal.
8. Kiln Load & Torque: highlight the drive motor current (`Furnace_Motor_Current`) operating at a mean of 68.24 A, which is 3.24 A above its fuzzy maximum constraint of 65.00 A, and discuss the mechanical stress implications.
9. CRITICAL FINDING: state the pyrometer temperature deficit relative to its actual target and minimum constraint.

---

## STEP 2 — Production Driver Analysis

**Graph 1 — Feed vs Production: Is every ton of feed converted efficiently?**
(Color by SFC: blue = efficient, red = fuel-wasteful operation)

[SCATTER: X=Flour_Feed | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

Expert interpretation required:
- Mark the EFFICIENT CORRIDOR: where feed increase reliably increases production AND SFC stays low
- Mark the SATURATION POINT: where more feed does not increase production (process limit)
- Is the slope 1:1 or does efficiency degrade at high feed?
- At max historical feed (319 t/h), what production was achieved and was it efficient?

**Graph 2 — Main Burner Fuel: Where does the main burner become inefficient?**
(Color by O2: red=low O2 risk, blue=excess air)

[SCATTER: X=Main_Mass_Coke_Flow_Rate | Y=Clinker_Production | COLOR=Check_O2_Cyclone_Tower | SCALE=RdBu]

Identify: (a) efficient fuel zone 5.48–6.02 t/h — does production reliably increase here?
(b) Above 6.02 t/h — does production plateau while O2 drops (incomplete combustion risk)?
(c) Below 5.48 t/h — low production, startup/unstable region?

**Graph 3 — Pre-cal Fuel: Is the precalciner over- or under-fired?**

[SCATTER: X=Pre-cal_Coke_Flow_Rate | Y=Clinker_Production | COLOR=Material_Temp_Cyclone_A55 | SCALE=Hot]

The pre-cal fuel stable range is 7.12–9.96 t/h. Does production peak in the middle of this range?
Is there evidence of over-firing above 9.96 t/h (high material temp, no extra production)?

---

## STEP 3 — Fuel Efficiency: The Zone Map

**Graph 4 — THE KEY CHART: Production vs SFC (The 4-Zone Efficiency Map)**

[SCATTER: X=Clinker_Production | Y=Specific_Fuel_Consumption | COLOR=Check_O2_Cyclone_Tower | SCALE=Viridis]

Based on mean production (146.71) and estimated mean SFC (~0.094), divide into:
- **ZONE A (Golden Batch):** Production > 155 t/h AND SFC < 0.085 — these are the best historical points. 
  What % of time does the kiln spend here?
- **ZONE B (High but Wasteful):** Production > 155 t/h AND SFC > 0.095 — over-fuelled
- **ZONE C (Idle/Startup):** Production < 140 t/h AND SFC < 0.090
- **ZONE D (Worst):** Production < 140 t/h AND SFC > 0.095 — unstable, worst possible operation

For each zone, state the approximate O2 color (Viridis scale = purple to yellow). 
What is the SFC in Zone A vs Zone D? Calculate the FUEL COST DIFFERENCE per ton of clinker.

**Graph 5 — Total Fuel vs Production: Find the fuel-efficient corridor**

[SCATTER: X=Total_Fuel_Flow | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

At mean total fuel (~13.71 t/h), what is the spread of production outcomes?
Find the GOLDEN BAND: same fuel → maximum production. 
What operating conditions distinguish high-production vs low-production at the same fuel level?

**Graph 6 — 3D Operating Space: Feed × Fuel × Production**
(The most complete view of the production efficiency space — color = SFC)

[SCATTER3D: X=Flour_Feed | Y=Total_Fuel_Flow | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

The Golden Batch cluster in 3D should sit at:
- X (Flour_Feed) → 260–272 t/h
- Z (Clinker_Production) → above 162 t/h
- Color (SFC) → blue/green (< 0.082 t/t)

Describe where the dense cluster of INEFFICIENT points lies (high fuel, low production). 
How far is the Golden Batch cluster from the average operating point? Is there a clear separation or a continuum?

**Graph 7 — Parallel Coordinates: Which variable combinations define high production?**
(Red = highest production periods → this IS the Golden Batch signature for Part 1)

[PARALLEL: Flour_Feed, Main_Mass_Coke_Flow_Rate, Pre-cal_Coke_Flow_Rate, Total_Fuel_Flow, Specific_Fuel_Consumption, Clinker_Production | COLOR: Clinker_Production]

For the RED lines (production > 162 t/h — the Q3 threshold):
- What Flour_Feed band? (closer to 260 or 272 t/h?)
- What Total_Fuel_Flow? (above or below 13.5 t/h?)
- What SFC? (below 0.085 or above 0.095?)
- What is the spread of Pre-cal vs Main fuel in those high-production periods?

For the BLUE/COLD lines (production < 140 t/h — worst performers):
- Do they show higher Total_Fuel_Flow at lower production (proving SFC is high)?
- Is Flour_Feed low (feed-limited) or is there some other driver?

This parallel chart is your PART 1 GOLDEN BATCH FINGERPRINT — the pattern of red lines defines the target operating window for production and fuel.

---

## STEP 4 — Time Trend Overview

[DUALPLOT: Clinker_Production, Flour_Feed | Total_Fuel_Flow]
[DUALPLOT: Clinker_Production | Specific_Fuel_Consumption]

From the time trends, identify:
- At least 2 periods of best performance (high production, low SFC)
- At least 2 periods of worst performance (high SFC, unstable production)
- Are the shutdown periods (zeros) sudden or gradual? What happens to fuel before shutdown?

---

## STEP 5 — Production & Efficiency Summary Table

Fill using the actual statistics provided + your Zone Map analysis:

| Variable | Min | Q1 | Median | Q3 | Max | GOLDEN BATCH TARGET |
|---|---|---|---|---|---|---|
| Clinker_Production | 0 | 149.60 | 155.93 | 162.42 | 182.55 | >162 t/h |
| Flour_Feed | 0 | 249.81 | 260.54 | 271.52 | 319.04 | 260–272 t/h |
| Main_Mass_Coke_Flow_Rate | 0 | 5.48 | 5.80 | 6.02 | 7.78 | 5.5–5.9 t/h |
| Pre-cal_Coke_Flow_Rate | 0.05 | 7.12 | 8.46 | 9.96 | 13.95 | 7.5–9.0 t/h |
| Total_Fuel_Flow | — | — | ~13.71 | — | — | <13.0 t/h at Q3 prod |
| Specific_Fuel_Consumption | — | — | ~0.094 | — | — | <0.082 t/t |
| Precalciner_Fuel_Share | — | — | ~60% | — | — | 57–63% |
```

---

## ⚡ PART 2 — Combustion, Temperature Deficit, Fan & Fuel Split

```
Continuing the W3 Kiln Optimization Report — Section 2: Combustion, Thermal Profile & Draft System.
Derived KPIs are already in the dataset: Total_Fuel_Flow, Specific_Fuel_Consumption,
Precalciner_Fuel_Share, Main_Fuel_Share — do NOT recreate them.

## REPORT GENERATION MANDATORY INSTRUCTIONS:
- You MUST generate the report sequentially, containing every STEP listed below.
- You MUST use the exact Markdown headings for each step (e.g., `### STEP 6 — Combustion Diagnostic Map`).
- Do NOT combine steps, do NOT skip any steps, and do NOT output placeholders. Provide full engineering and data-driven explanations for each section.

Expert context for this section:
- O2 Cyclone Tower (Check_O2_Cyclone_Tower): mean=3.50%, stable 2.35–3.38%, OBJECTIVE=3.0% 
- CO Cyclone Tower (Check_CO_Cyclone_Tower): mean=0.11%, stable 0.10–0.13%, MAX CONSTRAINT=0.14%
- NOx Cyclone Tower (Check_NOx_Cyclone_Tower): mean=439.74, stable 365.31–513.59, MAX CONSTRAINT=600 mg/Nm³
- NOx Smoke Box (Check_NOx_Smoke_Box): mean=181.11, Q3=327.36 mg/Nm³
- O2 Smoke Box (Analyze_O2_in_Smoke_Box): mean=1.35%, stable 0.00–2.46% (kiln inlet exit O2)
- CO Smoke Box (Check_CO_in_Smoke_Box): mean=0.02%, max observed=2.12% (kiln inlet exit CO)
- Pyrometer Burning Zone (Optical_Pyrometer_Temp._Burning_Zone): mean=913.73°C, stable 855.17–1001.25°C
  → TARGET=1050°C, MIN FUZZY CONSTRAINT=950°C ← OPERATING BELOW MINIMUM!
- Material Temp A55 (Material_Temp_Cyclone_A55): mean=866.68°C, stable 854.60–919.65°C
- Cyclone Temp A55 (Cyclone_Gas_Temp._A55): mean=882.93°C, stable 876.67–911.82°C
- Cyclone Temp A54 (Cyclone_Gas_Temp._A54): mean=798.95°C, stable 805.97–812.86°C
- Cyclone Temp A53 (Cyclone_Gas_Temp._A53): mean=727.83°C, stable 728.18–740.24°C
- Top Cyclone Pressure (Top_Cyclone_Pressure_A55): mean=-15.43, stable -17.62 to -14.95 mmH2O (correlation to production: -0.935)
- Fan Speed 5 (Fan_Speed.4): mean=64.63%, stable 65.67–69.74% (strongest prod correlation: 0.902)
- Fan Speed 4 (Fan_Speed.3): mean=64.95%, stable 65.99–70.02%
- Fan Speed 3 (Fan_Speed.2): mean=61.59%, stable 61.71–66.90%
- Fan Speed 2 (Fan_Speed.1): mean=58.13%, stable 58.08–63.10%
- Fan Speed 1 (Fan_Speed): mean=68.37%, stable 69.02–73.59%
- Correlation: NOx Smoke Box vs O2 Smoke Box = +0.592
- Fan Speed Scaling: All process fans scale synchronously, indicating a centralized draft scheme tracking feed rate.

Operational Matrix Constraints & Exclusions:
1. Gas Probe Maintenance & Cleaning (`W3_Probe_Inserted`): When the gas probe status `W3_Probe_Inserted` is 0 (indicating the probe is pulled out for maintenance or cleaning), the gas analyzer readings at the smoke box (`Analyze_O2_in_Smoke_Box`, `Check_NOx_Smoke_Box`, `Check_CO_in_Smoke_Box`) are corrupted by ambient false air and MUST be ignored.
2. Shutdown Exclusions: All process parameters (coke flows, fan speeds, temperatures) drop during shutdowns. Zeros in `Clinker_Production` and `Flour_Feed` (representing ~6.5% of the data) must be isolated so they do not skew the stable operating range stats.

---

## STEP 6 — Combustion Diagnostic Map

**Graph 8 — O2 vs CO: The Master Combustion Map**
(Production shown as color — find where good combustion + high production overlap)

[SCATTER: X=Check_O2_Cyclone_Tower | Y=Check_CO_Cyclone_Tower | COLOR=Clinker_Production | SCALE=Jet]

As an expert, interpret ALL FOUR combustion regions:
- **OPTIMAL:** O2 2.35–3.38%, CO < 0.13% — target window. What % of points are here?
- **EXCESS AIR:** O2 > 3.38%, CO < 0.13% — fan over-speed, heat loss. What is the production here?
- **LOW O2 RISK:** O2 < 2.35%, CO > 0.13% — incomplete combustion, approaching CO limit (0.14%). 
  How close to the CO max constraint (0.14%)? Is this a daily occurrence or rare?
- **ABNORMAL:** O2 > 3.38%, CO > 0.13% — false air, poor mixing. Any points here?

State the TARGET O2 window for this kiln: between Q1 (2.35%) and Q3 (3.38%), objective 3.0%.
At what O2 does CO start rising above 0.13%? This is the LOW-O2 LIMIT for this kiln.

**Graph 9 — O2 vs Production: What O2 gives maximum clinker output?**

[SCATTER: X=Check_O2_Cyclone_Tower | Y=Clinker_Production | COLOR=Check_CO_Cyclone_Tower | SCALE=Hot]

Find: (a) O2 range where production peaks above 162 t/h (Q3) — is this in the 2.35–3.38% window?
(b) At O2 below 2.35%, does production drop or stay high with high CO risk?
(c) At O2 above 3.38%, does production drop due to excess air cooling?

[BOX: Check_O2_Cyclone_Tower, Check_CO_Cyclone_Tower, Check_NOx_Cyclone_Tower]

**Graph 10 — 3D Combustion Space: O2 × CO × Production**
(The complete combustion operating map in 3 dimensions — color = SFC)

[SCATTER3D: X=Check_O2_Cyclone_Tower | Y=Check_CO_Cyclone_Tower | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

In this 3D space, the GOLDEN COMBUSTION ZONE should appear as a cluster where:
- X (O2) in 2.5–3.3% — neither too low (CO risk) nor too high (excess air)
- Y (CO) below 0.12% — clean combustion
- Z (Production) above 162 t/h
- Color (SFC) blue/green (< 0.085)

Describe the shape of the point cloud:
- Is there a clear ridge of high production at optimal O2? Or is it scattered?
- Where do the red (high SFC) points cluster — low O2 + high CO, or high O2 + excess air?
- This proves whether combustion management or thermal management is the primary driver of SFC.

---

## STEP 7 — Emission & Chemical Moduli Analysis

**Graph 11 — NOx vs O2 (Smoke Box): Is excess air driving thermal NOx?**
(Current correlation: +0.592 — significant)

[SCATTER: X=Analyze_O2_in_Smoke_Box | Y=Check_NOx_Smoke_Box | COLOR=Clinker_Production | SCALE=Jet]

The NOx max constraint at the tower is 600 mg/Nm³. Current mean NOx at cyclone tower is 440.
At what smoke box O2 level does NOx at the tower risk exceeding 500 mg/Nm³?
Is there a smoke box O2 threshold above which NOx increases sharply?

**Graph 12 — Quality Driver: FSC (LSF) vs Clinker Free Lime**
(Current correlation: +0.502 — high LSF drives high Free Lime)

[SCATTER: X=W3_Clinker_FSC | Y=W3_Clinker_CaOL | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

Analyze:
- The impact of LSF saturation on chemical burnability.
- When raw mix LSF (`W3_Flour_FSC`) or clinker LSF (`W3_Clinker_FSC`) exceeds 100, why does free lime spike regardless of burning temperature?
- Sieve residue fineness (`W3_Flour_#170`) impact: how does coarser meal (+0.198 correlation to free lime) prevent complete combination?

---

## STEP 8 — CRITICAL FINDINGS: Thermal Deficit, Sulfur, and Drive Current

This is the most important finding of Part 2. Write a dedicated section titled:

**"CRITICAL DIAGNOSTICS: Burning Zone Temperature Deficit, Drive Current Overload, and Sulfur Balance"**

The pyrometer target and minimum fuzzy constraints must be extracted from the active dataset (e.g. from `Pyrometer_-_Target` and `Pyrometer_-_Minimum_Fuzzy_Constraint`). Calculate the temperature deficit and discuss drive current overload:
- What is the actual pyrometer mean vs. its target and minimum constraint? (Mean 913.73°C vs min constraint 950°C, target 1050°C).
- What is the Kiln Drive Current (`Furnace_Motor_Current`) operating state? (Mean 68.24 A vs Max fuzzy constraint 65.00 A). Why is the drive current running 3.24 A overloaded? Explain that high coating thickness or heavy load inside the kiln drives current up, and how this mechanical stress restricts further feed rate increases.
- Excess Sulfur (`W3_-_excess_sulfur`): mean is 1150.13. Explain that high excess sulfur indicates volatility cycles of sulfur, which risks ring formation in the burning zone and clogging in preheater cyclones.

[DUALPLOT: Optical_Pyrometer_Temp._Burning_Zone, Furnace_Motor_Current | Clinker_Production]
[SCATTER: X=Optical_Pyrometer_Temp._Burning_Zone | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

Answer these expert questions:
1. What % of historical time is the pyrometer below the minimum constraint? (Compare Q1-Q3 relative to 950°C constraint).
2. Does production increase when pyrometer is within the target range vs below the minimum constraint?
3. Does SFC decrease (better efficiency) when pyrometer is above the minimum constraint?
4. MECHANISM: explain what happens when burning zone temperature is too low:
   - Incomplete calcination → higher free lime (W3_Clinker_CaOL) → rejected clinker
   - Avoidable over-firing: operator responds by adding excess fuel → drives up SFC and causes drive current overload due to thermal expansion/coating.
5. Sulfur and cyclone build-up: discuss if `W3_-_excess_sulfur` (mean 1150) correlates with preheater draft drops (e.g. `Top_Cyclone_Pressure_A55` and `Smoke_Box_Inlet_Pressure`).

---

## STEP 9 — Fan, Draft System, and Pressures

**Graph 13 — Top Cyclone Draft vs Production: Is the exhaust fan capacity constrained?**

[SCATTER: X=Top_Cyclone_Pressure_A55 | Y=Clinker_Production | COLOR=Fan_Speed.4 | SCALE=Jet]

- Explain that Top Cyclone Pressure `Top_Cyclone_Pressure_A55` correlates strongly with Clinker Production (`-0.935`). As production increases, pressure becomes more negative (down to -17.62 mmH2O), meaning the draft system must pull harder.
- Fan Speeds: Detail the stable ranges of the five process fans (Fan 1 `Fan_Speed` through Fan 5 `Fan_Speed.4`). Is there draft capacity reserve? (Exhaust fan 5 averages 64.63%, meaning there is still a ~35% draft reserve, which is highly favorable for capacity expansions compared to typical constrained preheaters).

[BOX: Fan_Speed, Fan_Speed.1, Fan_Speed.2, Fan_Speed.3, Fan_Speed.4]

---

## STEP 10 — Fuel Split Optimization

**Graph 14 — Precalciner Fuel Share vs Production and SFC**

[SCATTER: X=Precalciner_Fuel_Share | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]
[SCATTER: X=Precalciner_Fuel_Share | Y=Check_CO_Cyclone_Tower | COLOR=Check_O2_Cyclone_Tower | SCALE=RdBu]

Pre-cal mean share ≈ 8.19/(8.19+5.52) = 59.7% of total fuel. Main burner share ≈ 40.3%.
- Is the optimal precalciner share above or below 60%?
- Does too much precalciner fuel (>65%) cause CO problems in the tower?
- Does too little precalciner fuel (<55%) cause burning zone over-heating and higher NOx?
- What fuel split minimizes SFC while keeping CO and NOx within constraints?

---

## STEP 11 — Section 2 Summary Table

| Variable | Min | Q1 | Median | Q3 | Max | CURRENT STATUS | GOLDEN BATCH TARGET |
|---|---|---|---|---|---|---|---|
| Check_O2_Cyclone_Tower | 0.00 | 2.35 | 2.80 | 3.38 | 23.17 | Slightly above objective | 2.8–3.3% |
| Check_CO_Cyclone_Tower | 0.00 | 0.10 | 0.12 | 0.13 | 0.91 | At limit in spikes | <0.12% |
| Check_NOx_Cyclone_Tower | 0.00 | 365.31 | 436.75 | 513.59 | 2019.60 | Within constraint | 365–500 |
| Check_NOx_Smoke_Box | 0.00 | 1.19 | 9.66 | 327.36 | 2123.09 | High spread | <250 |
| Optical_Pyrometer_Temp._Burning_Zone | 600.00 | 855.17 | 953.47 | 1001.25 | 1265.06 | Below target | 980–1050°C |
| Furnace_Motor_Current | 0.07 | 66.82 | 71.44 | 75.99 | 98.49 | OVERLOADED | 60–65 A |
| W3_Flour_FSC | 95.91 | 99.90 | 101.01 | 101.78 | 106.50 | High LSF | 98.0–100.0 |
| W3_Clinker_CaOL (Free Lime) | 0.82 | 1.70 | 1.95 | 2.33 | 4.82 | Sintering issues | 1.2–1.8% |
| Top_Cyclone_Pressure_A55 | -30.82 | -17.62 | -15.43 | -14.95 | 0.00 | Draft tracks feed | -15 to -18 mmH2O |
| Fan_Speed.4 (Fan 5) | 0.00 | 65.67 | 64.63 | 69.74 | 99.99 | Stable draft | 62–67% |
```

---

## ⚡ PART 3a-1 — Golden Batch Parallel Coordinates

```
Continuing the W3 Kiln Optimization Report — Part 3a-1: GOLDEN BATCH PARALLEL COORDINATES.
All derived KPIs already in dataset: Total_Fuel_Flow, Specific_Fuel_Consumption,
Precalciner_Fuel_Share, Main_Fuel_Share — do NOT recreate them.

## REPORT GENERATION MANDATORY INSTRUCTIONS:
- You MUST generate the report sequentially, containing every STEP listed below.
- You MUST use the exact Markdown headings for each step (e.g., `### STEP 12 — Multi-Variable Golden Batch Maps`).
- Do NOT combine steps, do NOT skip any steps, and do NOT output placeholders. Provide full engineering and data-driven explanations for each section.
- You MUST weave the chart tags and their corresponding text interpretations together.

Confirmed data: Mean production=146.71, Q3=162.42, max=182.55 t/h.
Mean SFC=0.094 t/t, target SFC=0.082. Pyrometer mean=913.73°C, target=1050°C, min=950°C.

---

## STEP 12 — Multi-Variable Golden Batch Maps

Output this parallel coordinate chart for Production, then interpret:
[PARALLEL: Flour_Feed, Main_Mass_Coke_Flow_Rate, Pre-cal_Coke_Flow_Rate, Check_O2_Cyclone_Tower, Check_CO_Cyclone_Tower, Optical_Pyrometer_Temp._Burning_Zone, Furnace_Motor_Current, Fan_Speed.4 | COLOR: Clinker_Production]

Describe the RED lines (production > 162 t/h) in the parallel coordinates:
- What Flour_Feed, O2, CO, Pyrometer, Furnace_Motor_Current, and Fan 5 values characterize highest production?
- How does the drive current Furnace_Motor_Current respond during peak production periods?

Output this parallel coordinate chart for Specific Fuel Consumption (SFC), then interpret:
[PARALLEL: Flour_Feed, Total_Fuel_Flow, Specific_Fuel_Consumption, W3_Flour_FSC, W3_Flour_#170, Optical_Pyrometer_Temp._Burning_Zone, Cyclone_Gas_Temp._A55 | COLOR: Specific_Fuel_Consumption]

Describe the BLUE lines (SFC < 0.082) in the parallel coordinates:
- What chemistry moduli (LSF/FSC, sieve residue) and pyrometer values yield the best fuel efficiency?

Output this parallel coordinate chart for NOx Cyclone Tower, then interpret:
[PARALLEL: Main_Mass_Coke_Flow_Rate, Pre-cal_Coke_Flow_Rate, Check_O2_Cyclone_Tower, Optical_Pyrometer_Temp._Burning_Zone, Furnace_Motor_Current, Analyze_O2_in_Smoke_Box | COLOR: Check_NOx_Cyclone_Tower]

Describe the RED lines (NOx > 500) in the parallel coordinates:
- Is high NOx driven by high Pyrometer (thermal NOx) or high O2 (excess air NOx)?
```

---

## ⚡ PART 3a-2 — 3D Clusters & Distributions

```
Continuing the W3 Kiln Optimization Report — Part 3a-2: 3D CLUSTERS & DISTRIBUTIONS.
All derived KPIs already in dataset: Total_Fuel_Flow, Specific_Fuel_Consumption,
Precalciner_Fuel_Share, Main_Fuel_Share — do NOT recreate them.

## REPORT GENERATION MANDATORY INSTRUCTIONS:
- You MUST generate the report sequentially, containing every STEP listed below.
- You MUST use the exact Markdown headings for each step (e.g., `### STEP 13 — 3D Golden Batch Clusters`).
- Do NOT combine steps, do NOT skip any steps, and do NOT output placeholders. Provide full engineering and data-driven explanations for each section.
- You MUST weave the chart tags and their corresponding text interpretations together.

Confirmed data: Mean production=146.71, Q3=162.42, max=182.55 t/h.
Mean SFC=0.094 t/t, target SFC=0.082. Pyrometer mean=913.73°C, target=1050°C, min=950°C.

---

## STEP 13 — 3D Golden Batch Clusters

Output this 3D Operating Space scatter chart, then interpret:
[SCATTER3D: X=Check_O2_Cyclone_Tower | Y=Optical_Pyrometer_Temp._Burning_Zone | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

For 3D Map 1:
- Where is the Golden Batch cluster? (Z > 162, Y > 950°C, X in 2.5-3.3%, color blue)
- Estimate what % of historical data falls in this optimal 3D region.

Output this 3D Chemistry Space scatter chart, then interpret:
[SCATTER3D: X=W3_Flour_FSC | Y=W3_Flour_#170 | Z=W3_Clinker_CaOL | COLOR=Specific_Fuel_Consumption | SCALE=Viridis]

For 3D Map 2:
- Identify the region of raw meal chemistry and fineness that minimizes both free lime (Z < 1.5%) and SFC (color dark purple).
- Discuss if there is a clear operating sweet spot.

---

## STEP 14 — Statistical Distributions

Output these two BOX plots, then interpret:
[BOX: Clinker_Production, Flour_Feed, Total_Fuel_Flow, Specific_Fuel_Consumption]
[BOX: Check_O2_Cyclone_Tower, W3_Clinker_CaOL, Optical_Pyrometer_Temp._Burning_Zone, Furnace_Motor_Current]

Output this HISTOGRAM, then interpret:
[HISTOGRAM: Specific_Fuel_Consumption, Clinker_Production]

Key questions to answer:
1. SFC histogram: single mode or bimodal? Where is the split?
2. What % of RUNNING time (excluding 6.51% shutdowns) is production above Q3 (162.42)?
3. How much of the pyrometer box sits below 950°C?
4. How much of the drive current box sits above 65.00 A?
```

---

## ⚡ PART 3b-1 — Golden Batch & Value Lost

```
Continuing the W3 Kiln Optimization Report — Part 3b-1: GOLDEN BATCH & VALUE LOST.
This is the business case definition and quantification section. No charts needed — text and tables only.

## REPORT GENERATION MANDATORY INSTRUCTIONS:
- You MUST generate the report sequentially, containing every STEP listed below.
- You MUST use the exact Markdown headings for each step (e.g., `### STEP 15 — THE GOLDEN BATCH: Complete Definition`).
- Do NOT combine steps, do NOT skip any steps, and do NOT output placeholders. Provide full engineering and data-driven explanations for each section.

CONFIRMED NUMBERS (use exactly as stated):
- Mean production: 146.71 t/h | Q3: 162.42 | Max: 182.55 t/h
- Operating hours/year: 8,120 h/yr (6.51% shutdown)
- Mean SFC: 0.094 t coke/t clinker | Golden Batch SFC target: 0.082
- Mean total fuel: 13.71 t/h | Main: 5.52 | Pre-cal: 8.19
- Pyrometer mean: 913.73°C | Target: 1050°C | Minimum constraint: 950°C
- Kiln Drive Current mean: 68.24 A | Max constraint: 65.00 A
- CO max constraint: 0.14% | Current mean: 0.11%
- NOx mean (cyclone tower): 439.74 mg/Nm³ | Max constraint: 600

---

## STEP 15 — THE GOLDEN BATCH: Complete Definition

State the complete operating window as a filled table:

| Variable | Golden Batch Lower | Golden Batch Upper | Current Mean | Gap |
|---|---|---|---|---|
| Clinker_Production | 160 | 182 | 146.71 | +13–35 t/h |
| Flour_Feed | 262 | 275 | 245.00 | +17–30 t/h |
| Total_Fuel_Flow | 12.0 | 13.5 | 13.71 | −0.2 t/h |
| Specific_Fuel_Consumption | 0.075 | 0.085 | 0.094 | −0.009 to −0.019 t/t |
| Main_Mass_Coke_Flow_Rate | 5.5 | 5.9 | 5.52 | near optimal |
| Pre-cal_Coke_Flow_Rate | 7.5 | 9.0 | 8.19 | near optimal |
| Precalciner_Fuel_Share | 57 | 62 | ~60% | near optimal |
| Check_O2_Cyclone_Tower | 2.5 | 3.3 | 3.50 | slightly above |
| Check_CO_Cyclone_Tower | 0.08 | 0.12 | 0.11 | watch carefully |
| Check_NOx_Cyclone_Tower | 365 | 480 | 439.74 | within range |
| Optical_Pyrometer_Temp._Burning_Zone | 980 | 1050 | 913.73 | **+66 to +136°C DEFICIT** |
| Furnace_Motor_Current | 60 | 65 | 68.24 | **−3.24 A OVERLOAD** |
| W3_Flour_FSC (Raw LSF) | 98 | 100 | 101.01 | −1.0 to −3.0 LSF |
| W3_Flour_MS (Raw Silica Mod) | 2.50 | 2.60 | 2.65 | −0.05 to −0.15 |
| W3_Flour_#170 (Sieve) | 12.0% | 15.0% | 16.67% | −1.67% to −4.67% |
| W3_Clinker_CaOL (Free Lime) | 1.2% | 1.8% | 2.01% | −0.21% to −0.81% |
| Top_Cyclone_Pressure_A55 | -18 | -15 | -15.43 | near optimal |
| Fan_Speed.4 (Fan 5) | 65 | 68 | 64.63 | near optimal |

---

## STEP 16 — VALUE LOST QUANTIFICATION

Calculate and present a professional table. You MUST recalculate all of these numbers dynamically using the actual mean, Q3, and max values from the active dataset:

**A) Production Opportunity**
- Formula: Gap = (Q3_Production − Mean_Production) × Operating_Hours_per_Year.
- Formula: Max Opportunity = (Max_Production − Mean_Production) × Operating_Hours_per_Year.
- Value calculation: Use $50/ton of clinker to compute conservative and maximum financial values.
- Baseline reference: (162.42 − 146.71) × 8,120 = 127,566 t/yr ($6.38M/yr), Max = (182.55 − 146.71) × 8,120 = 291,002 t/yr ($14.55M/yr).

**B) Fuel Saving Opportunity**
- Formula: SFC Gap = Mean_SFC − Target_SFC.
- Formula: Annual Production = Q3_Production × Operating_Hours_per_Year.
- Formula: Fuel Saved = SFC Gap × Annual Production (tons of petcoke/year).
- Value calculation: Use $120/ton of petcoke to compute financial value.
- Formula: CO2 reduction = Fuel Saved × 3.2 (tons of CO2/year).
- Baseline reference: (0.094 − 0.082) × 1,318,850 = 15,826 t/yr ($1.90M/yr saving).

**C) Environmental Improvement**
- Compute the actual NOx reduction margin and the increased headroom against the actual plant constraint.

**D) Quality Recovery & Mechanical Stress Relief**
- Calculate the potential reduction in quality rejects based on the clinker free lime stats.
- Compute the potential reduction in drive current overload to prolong gear life.

Present as a completed table:
| Opportunity | Annual Quantity | Financial Value |
|---|---|---|
| Production (conservative) | [Calculated t clinker/yr] | [Calculated $ value at $50/t] |
| Production (maximum potential) | [Calculated t clinker/yr] | [Calculated $ value at $50/t] |
| Fuel saving | [Calculated t petcoke/yr] | [Calculated $ value at $120/t] |
| CO2 reduction | [Calculated t CO2/yr] | Carbon credit opportunity |
| Quality improvement | Fewer rejected batches | Avoided rework cost |
| Drive Current overload | Lower peak currents | Avoided gearbox wear |
| **TOTAL (conservative)** | | **[Sum of Conservative Production + Fuel Saving]** |
```

---

## ⚡ budgetb
```

---

## ⚡ BONUS — Render Parallel Plots for Export

```
Render the three parallel coordinate plots for Kiln W3 in a single response so they can be exported. Do not write any analysis text; only output the titles, the chart tags on their own lines, and a short instruction to the operator to use the built-in "Export HTML" (or "Export as standalone HTML") button located on the plot's upper-right modebar to download the interactive plot as an HTML file.

1. **Production Drivers Parallel Plot**:
[PARALLEL: Flour_Feed, Main_Mass_Coke_Flow_Rate, Pre-cal_Coke_Flow_Rate, Check_O2_Cyclone_Tower, Check_CO_Cyclone_Tower, Optical_Pyrometer_Temp._Burning_Zone, Furnace_Motor_Current, Fan_Speed.4 | COLOR: Clinker_Production]
*Note: Use the "Export HTML" button on this plot's modebar to export as a standalone interactive HTML.*

2. **Specific Fuel Consumption (SFC) Drivers Parallel Plot**:
[PARALLEL: Flour_Feed, Total_Fuel_Flow, Specific_Fuel_Consumption, W3_Flour_FSC, W3_Flour_#170, Optical_Pyrometer_Temp._Burning_Zone, Cyclone_Gas_Temp._A55 | COLOR: Specific_Fuel_Consumption]
*Note: Use the "Export HTML" button on this plot's modebar to export as a standalone interactive HTML.*

3. **NOx Emissions Drivers Parallel Plot**:
[PARALLEL: Main_Mass_Coke_Flow_Rate, Pre-cal_Coke_Flow_Rate, Check_O2_Cyclone_Tower, Optical_Pyrometer_Temp._Burning_Zone, Furnace_Motor_Current, Analyze_O2_in_Smoke_Box | COLOR: Check_NOx_Cyclone_Tower]
*Note: Use the "Export HTML" button on this plot's modebar to export as a standalone interactive HTML.*
```
