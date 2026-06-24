# Kiln W3 — Expert Optimization Report (Updated Seamless Edition)
## Data-Specific 3-Part AI Prompt Set
### Persona: Master Operator + Master Process Engineer + Master Data Scientist (30 years experience)

---

> ⚠️ **CRITICAL RUNTIME NOTE FOR AI**: 
> 1. The limits, thresholds, and statistics (means, Q1, Q3, targets, objectives, constraints) listed below are **illustrative references** based on a baseline plant dataset. 
> 2. You MUST dynamically inspect and extract the actual statistics, percentiles, and setpoint/target parameters from the **ranges summary table** and correlation matrix of the currently uploaded dataset. Look up variables in the dataset ending with `_Target`, `_Minimum_Fuzzy_Constraint`, `_Maximum_Fuzzy_Constraint`, or `_Objective` to extract the exact operational limits for the active plant.
> 3. **Missing Variables Exclusions**: If any variable from the operational matrix (such as RDF main burner, RIP liquids burner, or Ammonia injection) is NOT present in the active dataset's ranges table and correlation matrix, you MUST ignore it or make a brief scientific process assumption about it. DO NOT include it as a metric or parameter in the final report. Keep the report strictly limited to the active variables present in the uploaded correlation matrix and ranges summary.
> 4. **New Variables Integration**: Seamlessly integrate the new process variables: `Flour_Flow_Rate_Oven`, `Outlet_Pressure_J3J01`, `Top_Cyclone_Pressure_A55`, `Air_Temperature_Outlet_Cooler`, `Coke_Flow_Rate_Torch`, `Transport_Line_Pressure`, `Pre-Cal_Blower_Pressure`, `Smoke_Box_Inlet_Pressure`, `Oven_Head_Pressure`, `Pressure_Before_CC_Chamber`, `Fan_Air_Pressure`, `Main_Torch_Axial_Air_Pressure`, `Oven_Fan_Speed`, `Temperature_1_Filter_Inlet`, and `W3_Oven_-_Status`.

> **DATA CONTEXT REFERENCE** (baseline ranges summary including new stream variables):
> - **Clinker Production**: mean = 146.71 t/h | Q1 = 149.60 | Q3 = 162.42 | max = 182.55 | **6.5% shutdowns**
> - **Flour Feed (Flour_Flow_Rate_Oven)**: mean = 252.57 | Q1 = 249.80 | Q3 = 271.48 | max = 343.37 t/h
> - **Main Coke (Coke_Flow_Rate_Torch)**: mean = 5.51 | stable 5.49–6.00 t/h | max = 7.76
> - **Pre-cal Coke**: mean = 8.19 | stable 7.12–9.96 t/h | max = 13.95
> - **O2 Cyclone Tower**: mean = 3.50 | stable 2.35–3.38% | objective = 3.0%
> - **CO Cyclone Tower**: mean = 0.11 | stable 0.10–0.13% | **max constraint = 0.14%**
> - **NOx Cyclone Tower**: mean = 440 | stable 365–513 | max constraint = 600 mg/Nm³
> - **Pyrometer**: mean = 913.7°C | stable 855–1001°C | **target = 1050°C | min constraint = 950°C**
> - **Material Temp A55**: mean = 866.7°C | stable 855–920°C
> - **Oven Fan Speed**: mean = 84.26% | stable 85.00–91.99% | max = 100%
> - **Oven Head Pressure**: mean = 0.19 mmH2O | stable 0.10 to 0.31 mmH2O
> - **Smoke Box Inlet Pressure**: mean = -2.52 mmH2O | stable -3.35 to -1.91 mmH2O
> - **Air Temperature Outlet Cooler**: mean = 371.11°C | stable 360.87–409.09°C
> - **Temperature 1 Filter Inlet**: mean = 156.62°C | stable 130.96–209.64°C
> - **Main Torch Axial Air Pressure**: mean = 2.5 bar | stable 2.0–3.0 bar
> - **Transport Line Pressure**: mean = 1.8 bar | stable 1.5–2.2 bar
> - **Pre-Cal Blower Pressure**: mean = 180 mbar | stable 150–220 mbar

---

## ✅ PREREQUISITE — Create Derived KPI Variables
### Run this FIRST in the AI chat, before any of the 3 parts below

```
Create the following 4 derived KPI variables needed for the kiln optimization report.
Output each as a DERIVED tag in exactly this order (order matters):

[DERIVED: Total_Fuel_Flow = Coke_Flow_Rate_Torch + Pre-cal_Coke_Flow_Rate]
[DERIVED: Specific_Fuel_Consumption = Total_Fuel_Flow / Clinker_Production]
[DERIVED: Precalciner_Fuel_Share = Pre-cal_Coke_Flow_Rate / Total_Fuel_Flow]
[DERIVED: Main_Fuel_Share = Coke_Flow_Rate_Torch / Total_Fuel_Flow]

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
QUANTIFY that loss, and define the GOLDEN BATCH — the historical operating window where 
this kiln performed best.

The following derived KPIs already exist in the dataset:
- Total_Fuel_Flow = Coke_Flow_Rate_Torch + Pre-cal_Coke_Flow_Rate (~13.71 t/h at mean)
- Specific_Fuel_Consumption = Total_Fuel_Flow / Clinker_Production (~0.094 t/t at mean)
- Precalciner_Fuel_Share = Pre-cal_Coke_Flow_Rate / Total_Fuel_Flow (~60% at mean)
- Main_Fuel_Share = Coke_Flow_Rate_Torch / Total_Fuel_Flow (~40% at mean)

Confirmed statistics:
- Clinker Production: mean=146.71, Q1=149.60, Q3=162.42, max=182.55 t/h (6.51% zeros/shutdowns)
- Flour Feed: mean=252.57, Q1=249.80, Q3=271.48, max=343.37 t/h (represented by Flour_Flow_Rate_Oven)
- Main Burner Coke (Coke_Flow_Rate_Torch): mean=5.51, stable range 5.49–6.00 t/h, max=7.76
- Pre-cal Coke Flow: mean=8.19, stable range 7.12–9.96 t/h, max=13.95
- Oven Fan Speed: mean=84.26%, stable range 85.00–91.99%, max=100%
- Oven Head Pressure: mean = 0.19 mmH2O | stable range 0.10 to 0.31 mmH2O
- Smoke Box Inlet Pressure: mean = -2.52 mmH2O | stable range -3.35 to -1.91 mmH2O
- Air Temperature Outlet Cooler: mean = 371.11°C | stable range 360.87–409.09°C
- Temperature 1 Filter Inlet: mean = 156.62°C | stable range 130.96–209.64°C
- Correlation: Flour_Flow_Rate_Oven vs Clinker_Production = +0.997 (near-perfect LOI-mass balance)
- Correlation: Coke_Flow_Rate_Torch vs Clinker_Production = +0.881
- Correlation: Pre-cal_Coke_Flow_Rate vs Clinker_Production = +0.772
- Correlation: Check_O2_Cyclone_Tower vs Clinker_Production = -0.771
- Correlation: Oven_Fan_Speed vs Clinker_Production = +0.961 (draft drive for throughput)
- Correlation: Top_Cyclone_Pressure_A55 vs Oven_Fan_Speed = -0.949 (fan speed draft coupling)
- Correlation: Top_Cyclone_Pressure_A55 vs Pressure_Before_CC_Chamber = +0.946 (calciner backpressure coupling)
- Correlation: Coke_Flow_Rate_Torch vs Transport_Line_Pressure = +0.929 (pneumatic conveying line scaling)
- Correlation: Air_Temperature_Outlet_Cooler vs Clinker_Production = +0.734 (heat recovery production driver)
- Correlation: Air_Temperature_Outlet_Cooler vs Optical_Pyrometer_Temp._Burning_Zone = +0.564 (cooler heat recovery thermal link)
- Correlation: Main_Torch_Axial_Air_Pressure vs Check_O2_Cyclone_Tower = -0.521 (flame shape impact on excess oxygen)

Quality Drivers & Moduli Correlations:
- Clinker Free Lime (W3_Clinker_CaOL): mean = 2.01% | stable = 1.70 - 2.33% (indicates unburnt lime)
- Clinker LSF/FSC (W3_Clinker_FSC): mean = 98.93 (potential calcium saturation limit)
- Flour Sieve Residue (W3_Flour_#170): mean = 16.67% (meal coarseness indicator)
- Clinker Litre Weight (W3_Clinker_Weight_Liter): mean = 1008.45 g/l (bulk density/sintering degree)
- Correlation: Free Lime vs Clinker LSF/FSC = +0.502
- Correlation: Free Lime vs W3_Fe2O3_Clinker = -0.282
- Correlation: Free Lime vs Clinker Litre Weight = -0.192
- Correlation: Free Lime vs Flour Sieve Residue = +0.198


---

## STEP 1 — Executive Summary

Write 9 bullet points. You MUST reference the actual statistics and parameters from the ranges summary table of the active dataset. Cover:
1. Current production performance vs peak capability (mean vs max in active dataset).
2. Q3 production opportunity: Extra tons per year if the kiln operates at Q3 production instead of mean (assuming ~8,120 operating hours/year at the actual shutdown rate from W3_Oven_-_Status).
3. Feed-to-production correlation (Flour_Flow_Rate_Oven vs Clinker_Production) meaning.
4. Actual Total_Fuel_Flow and Specific_Fuel_Consumption at mean conditions.
5. What SFC would be if production increased to Q3 without increasing fuel.
6. Combustion status: O2 stable range vs target — are we close to optimal?
7. Oven Fan Speed running at stable range (Q1-Q3) — is there excess air?
8. CRITICAL FINDING: state the pyrometer temperature deficit relative to its actual target and minimum constraint.
9. QUALITY FINDING: explain how raw meal LSF and sieve residue correlate with free lime, and how iron oxide serves as a flux.

---

## STEP 2 — Production Driver Analysis

**Graph 1 — Feed vs Production: Is every ton of feed converted efficiently?**
[SCATTER: X=Flour_Flow_Rate_Oven | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

Expert interpretation required:
- Mark the EFFICIENT CORRIDOR: where feed increase reliably increases production and SFC stays low.
- Mark the SATURATION POINT: where more feed does not increase production (process limit).
- Is the slope 1:1 or does efficiency degrade at high feed?

**Graph 2 — Main Burner Fuel: Where does the main burner become inefficient?**
[SCATTER: X=Coke_Flow_Rate_Torch | Y=Clinker_Production | COLOR=Check_O2_Cyclone_Tower | SCALE=RdBu]

Identify: (a) efficient fuel zone 5.48–6.02 t/h.
(b) Above 6.02 t/h — does production plateau while O2 drops (incomplete combustion risk)?
(c) Below 5.48 t/h — low production, startup/unstable region?

**Graph 3 — Pre-cal Fuel: Is the precalciner over- or under-fired?**
[SCATTER: X=Pre-cal_Coke_Flow_Rate | Y=Clinker_Production | COLOR=Material_Temp_Cyclone_A55 | SCALE=Hot]

The pre-cal fuel stable range is 7.12–9.96 t/h. Does production peak in the middle of this range?
Is there evidence of overcalcination or over-firing above 9.96 t/h?

---

## STEP 3 — Fuel Efficiency: The Zone Map

**Graph 4 — THE KEY CHART: Production vs SFC (The 4-Zone Efficiency Map)**
[SCATTER: X=Clinker_Production | Y=Specific_Fuel_Consumption | COLOR=Check_O2_Cyclone_Tower | SCALE=Viridis]

Based on mean production (146.71) and estimated mean SFC (~0.094), divide into:
- **ZONE A (Golden Batch):** Production > 155 t/h AND SFC < 0.085. What % of time does the kiln spend here?
- **ZONE B (High but Wasteful):** Production > 155 t/h AND SFC > 0.095 — over-fuelled.
- **ZONE C (Idle/Startup):** Production < 140 t/h AND SFC < 0.090.
- **ZONE D (Worst):** Production < 140 t/h AND SFC > 0.095.

**Graph 5 — Total Fuel vs Production: Find the fuel-efficient corridor**
[SCATTER: X=Total_Fuel_Flow | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

At mean total fuel (~13.71 t/h), find the GOLDEN BAND (same fuel → maximum production).

**Graph 6 — 3D Operating Space: Feed × Fuel × Production**
[SCATTER3D: X=Flour_Flow_Rate_Oven | Y=Total_Fuel_Flow | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

Describe the Golden Batch cluster in 3D (X -> 260-272 t/h, Z -> >162 t/h, Color -> <0.082).

**Graph 7 — Parallel Coordinates: Which variable combinations define high production?**
[PARALLEL: Flour_Flow_Rate_Oven, Coke_Flow_Rate_Torch, Pre-cal_Coke_Flow_Rate, Total_Fuel_Flow, Specific_Fuel_Consumption, Clinker_Production | COLOR: Clinker_Production]

Interpret the RED lines (production > 162 t/h) and BLUE lines (production < 140 t/h).

---

## STEP 4 — Time Trend Overview

[DUALPLOT: Clinker_Production, Flour_Flow_Rate_Oven | Total_Fuel_Flow]
[DUALPLOT: Clinker_Production | Specific_Fuel_Consumption]

Identify periods of best vs worst performance and shutdown transition behaviors.

---

## STEP 5 — Production & Efficiency Summary Table

| Variable | Min | Q1 | Median | Q3 | Max | GOLDEN BATCH TARGET |
|---|---|---|---|---|---|---|
| Clinker_Production | 0 | 149.60 | — | 162.42 | 182.55 | >162 t/h |
| Flour_Flow_Rate_Oven | 0 | 249.81 | 245 | 271.52 | 319.04 | 260–272 t/h |
| Coke_Flow_Rate_Torch | 0 | 5.48 | 5.52 | 6.02 | 7.78 | 5.5–5.9 t/h |
| Pre-cal_Coke_Flow_Rate | 0 | 7.12 | 8.19 | 9.96 | 13.95 | 7.5–9.0 t/h |
| Total_Fuel_Flow | — | — | ~13.71 | — | — | <13.0 t/h at Q3 prod |
| Specific_Fuel_Consumption | — | — | ~0.094 | — | — | <0.082 t/t |
| Precalciner_Fuel_Share | — | — | ~60% | — | — | 57–63% |
```

---

## ⚡ PART 2 — Combustion, Temperature Deficit, Fan & Fuel Split

```
Continuing the W3 Kiln Optimization Report — Section 2: Combustion, Thermal Profile & Draft System.
Do NOT recreate the derived KPIs.

## REPORT GENERATION MANDATORY INSTRUCTIONS:
- You MUST generate the report sequentially, containing every STEP listed below.
- You MUST use the exact Markdown headings for each step (e.g., `### STEP 6 — Combustion Diagnostic Map`).
- Do NOT combine steps, do NOT skip any steps, and do NOT output placeholders. Provide full engineering and data-driven explanations for each section.

Expert context:
- O2 Cyclone Tower: mean=3.50%, stable 2.35–3.38%, OBJECTIVE=3.0%
- CO Cyclone Tower: mean=0.11%, stable 0.10–0.13%, MAX CONSTRAINT=0.14%
- NOx Cyclone Tower: mean=440, stable 365–513, MAX CONSTRAINT=600 mg/Nm³
- NOx Smoke Box: mean=181, Q3=327 mg/Nm³
- Pyrometer: mean=913°C, stable 855–1001°C, TARGET=1050°C, MIN CONSTRAINT=950°C
- Oven Fan Speed: mean=64.63%, stable 65.67–69.74%
- W3_Oven_-_Status: used to isolate running periods (exclude shutdowns where production = 0)

---

## STEP 6 — Combustion Diagnostic Map

**Graph 8 — O2 vs CO: The Master Combustion Map**
[SCATTER: X=Check_O2_Cyclone_Tower | Y=Check_CO_Cyclone_Tower | COLOR=Clinker_Production | SCALE=Jet]

Interpret all four combustion regions: OPTIMAL, EXCESS AIR, LOW O2 RISK, and ABNORMAL. Define the LOW-O2 LIMIT.

**Graph 9 — O2 vs Production: What O2 gives maximum clinker output?**
[SCATTER: X=Check_O2_Cyclone_Tower | Y=Clinker_Production | COLOR=Check_CO_Cyclone_Tower | SCALE=Hot]

Analyze the O2 window where production peaks above 162 t/h.

[BOX: Check_O2_Cyclone_Tower, Check_CO_Cyclone_Tower, Check_NOx_Cyclone_Tower]

**Graph 10 — 3D Combustion Space: O2 × CO × Production**
[SCATTER3D: X=Check_O2_Cyclone_Tower | Y=Check_CO_Cyclone_Tower | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

Describe the shape of the point cloud and identify if excess air or incomplete combustion drives high SFC.

---

## STEP 7 — Emission Analysis

**Graph 11 — NOx vs O2 (Smoke Box): Is excess air driving thermal NOx?**
[SCATTER: X=Analyze_O2_in_Smoke_Box | Y=Check_NOx_Smoke_Box | COLOR=Clinker_Production | SCALE=Jet]

Determine the O2 threshold above which NOx increases sharply.

**Graph 12 — NOx vs Burning Zone Temperature**
[SCATTER: X=Optical_Pyrometer_Temp._Burning_Zone | Y=Check_NOx_Cyclone_Tower | COLOR=Analyze_O2_in_Smoke_Box | SCALE=Viridis]

Evaluate thermal NOx behavior at the current lower sintering temperatures.

[HISTOGRAM: Check_NOx_Cyclone_Tower, Check_NOx_Smoke_Box]

---

## STEP 8 — CRITICAL DIAGNOSTICS: Sintering Zone Deficit and Burner Flame Control

Write a dedicated section titled:
**"CRITICAL: Kiln Operating Below Thermal Target — Burning Zone Temperature Deficit"**

**Graph 13 — Pyrometer vs Main Burner Fuel: responds to primary air flame shape and transport stability?**
[SCATTER: X=Coke_Flow_Rate_Torch | Y=Optical_Pyrometer_Temp._Burning_Zone | COLOR=Main_Torch_Axial_Air_Pressure | SCALE=Jet]

Evaluate the temperature deficit dynamically:
1. **Pyrometer Deficit & Oven Feed Load**: Inspect the pyrometer mean vs target (1050°C) and minimum constraint (950°C). Assess how the thermal load scales with `Flour_Flow_Rate_Oven`.
2. **Axial Air Pressure & Coke Transport**: Evaluate how changes in primary burner axial pressure (`Main_Torch_Axial_Air_Pressure`) shift the pyrometer temperature. Analyze the role of `Transport_Line_Pressure` in maintaining stable pneumatic fuel delivery. Specifically reference the strong **+0.929** correlation between `Coke_Flow_Rate_Torch` and `Transport_Line_Pressure`.
3. **Flame Optimization & Cooler Thermal Link**: Detail how the operator can utilize burner axial air adjustments and fuel line transport stabilization to mitigate sintering temperature drops without over-firing coke fuel (`Coke_Flow_Rate_Torch`). Reference the **+0.564** correlation between `Air_Temperature_Outlet_Cooler` and `Optical_Pyrometer_Temp._Burning_Zone` to explain how secondary air recovery directly supports sintering thermal stability.

---

## STEP 9 — Fan, Draft System, and Preheater Pressures (Draft & Safety Constraints)

**Graph 14 — Preheater Draft vs Production: Is the exhaust fan capacity constrained?**
[SCATTER: X=Top_Cyclone_Pressure_A55 | Y=Clinker_Production | COLOR=Oven_Fan_Speed | SCALE=Jet]

**Graph 15 — Draft Pressure Profile: Kiln draft balance**
[SCATTER: X=Smoke_Box_Inlet_Pressure | Y=Oven_Head_Pressure | COLOR=Outlet_Pressure_J3J01 | SCALE=RdBu]

**Graph 16 — Baghouse Filter Safety: Filter inlet protection**
[SCATTER: X=Oven_Fan_Speed | Y=Temperature_1_Filter_Inlet | COLOR=W3_Oven_-_Status | SCALE=Viridis]

Analyze the preheater draft system, exhaust fan operation, and pressure/safety distribution:
1. **Tower Pressures**: Inspect the relationship between `Top_Cyclone_Pressure_A55` and `Oven_Fan_Speed` to assess draft capability. Detail the significance of their extremely strong **-0.949** correlation (showing that higher fan speeds drive increasingly negative draft pressure). Evaluate the kiln backpressure at the inlet using `Smoke_Box_Inlet_Pressure`.
2. **Oven Head/Hood Pressure Control**: Analyze `Oven_Head_Pressure`. Assess if the kiln hood pressure is maintained at slight negative draft (e.g., -2 to -5 mmH2O) to prevent hot gas and dust puffing, and how it correlates with `Fan_Air_Pressure`.
3. **Precalciner & Blower Draft**: Diagnose the draft balance using `Pre-Cal_Blower_Pressure` and `Pressure_Before_CC_Chamber`. Explain how their tight **+0.946** correlation shows calciner draft resistance scaling, and how high blower backpressures combined with less negative draft pressures signal throat clogging.
4. **Filter Inlet Protection & Status**: Examine `Temperature_1_Filter_Inlet`. Define the critical temperature safety ceiling (typically 180°C–200°C) to prevent thermal damage to the filter bags. Filter out non-operational transient periods using `W3_Oven_-_Status`.

---

## STEP 10 — Fuel Split & Cooler Heat Recovery Optimization

**Graph 17 — Cooler Air Heat Recovery vs Cooler Outlet Temperature**
[SCATTER: X=Air_Temperature_Outlet_Cooler | Y=Clinker_Production | COLOR=Grade_1_Speed | SCALE=Jet]

**Graph 18 — Precalciner Fuel Share vs Production and SFC**
[SCATTER: X=Precalciner_Fuel_Share | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

**Graph 19 — 3D Fuel Split Space: Main Fuel × Pre-cal Fuel × Production**
[SCATTER3D: X=Coke_Flow_Rate_Torch | Y=Pre-cal_Coke_Flow_Rate | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Viridis]

Determine the optimal precalciner fuel split target range and heat recovery levers:
1. **Fuel Split Targets**: Analyze the optimal precalciner fuel split target range (nominally 57-62%) and show how overcalcination or calciner over-firing impacts CO.
2. **Cooler Heat Recovery**: Analyze `Air_Temperature_Outlet_Cooler` (secondary/tertiary air temperature) and its impact on fuel efficiency. Explain how optimizing cooler bed depth and grate speed (`Grade_1_Speed`) maximizes the heat returned to the kiln. Reference the strong **+0.734** correlation between `Air_Temperature_Outlet_Cooler` and `Clinker_Production` to highlight that cooler efficiency directly limits production capacity.

---

## STEP 11 — Section 2 Summary Table

| Variable | Min | Q1 | Median | Q3 | Max | CURRENT STATUS | GOLDEN BATCH TARGET |
|---|---|---|---|---|---|---|---|
| Check_O2_Cyclone_Tower | 0 | 2.35 | 3.5 | 3.38 | 23.17 | Slightly above objective | 2.8–3.3% |
| Check_CO_Cyclone_Tower | 0 | 0.10 | 0.11 | 0.13 | 0.91 | At limit in spikes | <0.12% |
| Check_NOx_Cyclone_Tower | 0 | 365 | 440 | 514 | 2020 | Within constraint | 365–500 |
| Optical_Pyrometer_Temp._Burning_Zone | 600 | 855 | 913.7 | 1001 | 1265 | 37°C BELOW minimum | 980–1050°C |
| Material_Temp_Cyclone_A55 | 42 | 855 | 867 | 920 | 1372 | Low end | 880–920°C |
| Oven_Fan_Speed | 0 | 85.0 | 84.3 | 92.0 | 100 | Within range | 85–90% |
| Oven_Head_Pressure | 0.0 | 0.10 | 0.19 | 0.31 | 5.3 | Stable slight positive hood | 0.15 to 0.30 mmH2O |
| Smoke_Box_Inlet_Pressure | -3.4 | -3.35 | -2.52 | -1.91 | 0 | Low draft resistance | -3.0 to -2.0 mmH2O |
| Air_Temperature_Outlet_Cooler | 50 | 360.9 | 371.1 | 409.1 | 645 | Excellent secondary preheat | >380°C |
| Temperature_1_Filter_Inlet | 80 | 131.0 | 156.6 | 209.6 | 266 | Approaching baghouse limit | <165°C |
| Main_Torch_Axial_Air_Pressure | 1.0 | 2.0 | 2.5 | 3.0 | 4.0 | Controlled flame shape | 2.2–2.8 bar |
| Transport_Line_Pressure | 0.8 | 1.5 | 1.8 | 2.2 | 3.0 | Stable fuel transport | 1.6–2.0 bar |
| Pre-Cal_Blower_Pressure | 100 | 150 | 180 | 220 | 350 | Calciner draft resistance | 160–200 mbar |
```

---

## ⚡ PART 3a — Golden Batch Visualization Maps

```
Continuing the W3 Kiln Optimization Report — Part 3a: GOLDEN BATCH VISUALIZATION.
Do NOT recreate derived variables.

## REPORT GENERATION MANDATORY INSTRUCTIONS:
- You MUST generate the report sequentially, containing every STEP listed below.
- You MUST use the exact Markdown headings for each step (e.g., `### STEP 12 — Multi-Variable Golden Batch Maps`).
- Do NOT combine steps, do NOT skip any steps, and do NOT output placeholders. Provide full engineering and data-driven explanations for each section.
- You MUST weave the chart tags and their corresponding text interpretations together. Place each chart tag immediately under the heading of the STEP where it is discussed. Follow it immediately with your detailed expert analysis of that chart. DO NOT group all chart tags at the top.


---

## STEP 12 — Multi-Variable Golden Batch Maps

Output this parallel coordinate chart for Production, then interpret:
[PARALLEL: Flour_Flow_Rate_Oven, Coke_Flow_Rate_Torch, Pre-cal_Coke_Flow_Rate, Check_O2_Cyclone_Tower, Check_CO_Cyclone_Tower, Optical_Pyrometer_Temp._Burning_Zone, Oven_Fan_Speed | COLOR: Clinker_Production]

Describe the RED lines (production > 162 t/h) in the parallel coordinates.

Output this parallel coordinate chart for Specific Fuel Consumption (SFC), then interpret:
[PARALLEL: Flour_Flow_Rate_Oven, Total_Fuel_Flow, Specific_Fuel_Consumption, Check_O2_Cyclone_Tower, Precalciner_Fuel_Share, Optical_Pyrometer_Temp._Burning_Zone, Cyclone_Gas_Temp._A55 | COLOR: Specific_Fuel_Consumption]

Describe the BLUE lines (SFC < 0.082) in the parallel coordinates.

Output this parallel coordinate chart for NOx Cyclone Tower, then interpret:
[PARALLEL: Coke_Flow_Rate_Torch, Precalciner_Fuel_Share, Check_O2_Cyclone_Tower, Optical_Pyrometer_Temp._Burning_Zone, Oven_Fan_Speed, Analyze_O2_in_Smoke_Box | COLOR: Check_NOx_Cyclone_Tower]

---

## STEP 13 — 3D Golden Batch Clusters

Output this 3D Operating Space scatter chart, then interpret:
[SCATTER3D: X=Check_O2_Cyclone_Tower | Y=Optical_Pyrometer_Temp._Burning_Zone | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

Output this 3D Fuel Space scatter chart, then interpret:
[SCATTER3D: X=Coke_Flow_Rate_Torch | Y=Pre-cal_Coke_Flow_Rate | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Viridis]

---

## STEP 14 — Statistical Distributions

Output these two BOX plots, then interpret:
[BOX: Clinker_Production, Flour_Flow_Rate_Oven, Total_Fuel_Flow, Specific_Fuel_Consumption]
[BOX: Check_O2_Cyclone_Tower, Check_CO_Cyclone_Tower, Optical_Pyrometer_Temp._Burning_Zone, Material_Temp_Cyclone_A55]

Output this HISTOGRAM, then interpret:
[HISTOGRAM: Specific_Fuel_Consumption, Clinker_Production]

---

## ⚡ PART 3b — Golden Batch Definition + Value Lost

Continuing the W3 Kiln Optimization Report — Part 3b: GOLDEN BATCH DEFINITION + VALUE LOST.
This is the business case conclusion. No charts needed in this section — text and tables only.

## REPORT GENERATION MANDATORY INSTRUCTIONS:
- You MUST generate the report sequentially, containing every STEP listed below.
- You MUST use the exact Markdown headings for each step (e.g., `### STEP 15 — THE GOLDEN BATCH: Complete Definition`).
- Do NOT combine steps, do NOT skip any steps, and do NOT output placeholders. Provide full engineering and data-driven explanations for each section.

CONFIRMED NUMBERS (use exactly as stated):
- Mean production: 146.71 t/h | Q3: 162.42 | Max: 182.55 t/h
- Operating hours/year: 8,120 h/yr (6.5% shutdown)
- Mean SFC: 0.094 t coke/t clinker | Golden Batch SFC target: 0.082
- Mean total fuel: 13.71 t/h | Main: 5.52 | Pre-cal: 8.19
- Pyrometer mean: 913°C | Target: 1050°C | Minimum constraint: 950°C
- CO max constraint: 0.14% | Current mean: 0.11%
- NOx mean (cyclone tower): 440 mg/Nm³ | Max constraint: 600

---

## STEP 15 — THE GOLDEN BATCH: Complete Definition

State the complete operating window as a filled table:

| Variable | Golden Batch Lower | Golden Batch Upper | Current Mean | Gap |
|---|---|---|---|---|
| Clinker_Production | 160 | 182 | 146.71 | +13–35 t/h |
| Flour_Flow_Rate_Oven | 262 | 275 | 252.57 | +10–22 t/h |
| Total_Fuel_Flow | 12.0 | 13.5 | 13.71 | −0.2 t/h |
| Specific_Fuel_Consumption | 0.075 | 0.085 | 0.094 | −0.009 to −0.019 t/t |
| Coke_Flow_Rate_Torch | 5.5 | 5.9 | 5.51 | near optimal |
| Pre-cal_Coke_Flow_Rate | 7.5 | 9.0 | 8.19 | near optimal |
| Precalciner_Fuel_Share | 57 | 62 | ~60 | near optimal |
| Check_O2_Cyclone_Tower | 2.5 | 3.3 | 3.5 | slightly above |
| Check_CO_Cyclone_Tower | 0.08 | 0.12 | 0.11 | watch carefully |
| Check_NOx_Cyclone_Tower | 365 | 480 | 440 | within range |
| Optical_Pyrometer_Temp._Burning_Zone | 980 | 1050 | 913.7 | **+66 to +136°C DEFICIT** |
| Material_Temp_Cyclone_A55 | 880 | 920 | 866.7 | +13 to +53°C |
| Oven_Fan_Speed | 85 | 90 | 84.3 | near optimal |
| Oven_Head_Pressure | 0.15 | 0.30 | 0.19 | near optimal |
| Smoke_Box_Inlet_Pressure | -3.0 | -2.0 | -2.52 | within range |
| Air_Temperature_Outlet_Cooler | 380 | 420 | 371.1 | +9 to +49°C |
| Temperature_1_Filter_Inlet | 130 | 165 | 156.6 | within safety |
| Main_Torch_Axial_Air_Pressure | 2.2 | 2.8 | 2.5 | near optimal |
| Transport_Line_Pressure | 1.6 | 2.0 | 1.8 | within range |
| Pre-Cal_Blower_Pressure | 160 | 200 | 180 | within range |


---

## STEP 16 — VALUE LOST QUANTIFICATION

Calculate and present a professional table. Recalculate all numbers dynamically using the actual mean, Q3, and max values from the active dataset:

**A) Production Opportunity**
- Formula: Gap = (Q3_Production − Mean_Production) × Operating_Hours_per_Year.
- Value calculation: Use $50/ton of clinker.

**B) Fuel Saving Opportunity**
- Formula: SFC Gap = Mean_SFC − Target_SFC.
- Formula: Annual Production = Q3_Production × Operating_Hours_per_Year.
- Formula: Fuel Saved = SFC Gap × Annual Production.
- Value calculation: Use $120/ton of petcoke.
- Formula: CO2 reduction = Fuel Saved × 3.2.

**C) Environmental Improvement**
- Compute the actual NOx reduction margin and increased headroom against constraints.

**D) Sintering Quality Recovery**
- Calculate the potential reduction in quality rejects based on clinker free lime. Target a 30% reduction in rejected batches.

Present as a completed table:
| Opportunity | Annual Quantity | Financial Value |
|---|---|---|
| Production (conservative) | [Calculated t clinker/yr] | [Calculated $ value at $50/t] |
| Production (maximum potential) | [Calculated t clinker/yr] | [Calculated $ value at $50/t] |
| Fuel saving | [Calculated t petcoke/yr] | [Calculated $ value at $120/t] |
| CO2 reduction | [Calculated t CO2/yr] | Carbon credit opportunity |
| Quality improvement | Fewer rejected batches | Avoided rework cost |
| **TOTAL (conservative)** | | **[Sum of Conservative Production + Fuel Saving]** |

---

## STEP 17 — Top 5 Prioritized Recommendations

List the 5 highest-impact recommendations using:
**REC-N | TITLE | Priority: CRITICAL/HIGH/MEDIUM**
- Evidence: [numbers from stats]
- Root Cause: [process engineering mechanism]
- Action: [what to change, by how much, and operational exclusions]
- Target: [Golden Batch target range]
- Value: [$/yr, t/yr, or emission margins]

1. **REC-1 | Burning Zone Sintering Recovery (CRITICAL)**: Action to recover the `Optical_Pyrometer_Temp._Burning_Zone` deficit. Maintain axial burner pressures `Main_Torch_Axial_Air_Pressure` and verify stable `Transport_Line_Pressure` to prevent coal line pulsation.
2. **REC-2 | Precalciner Fuel Split Optimization (HIGH)**: Adjust coke split `Precalciner_Fuel_Share` to keep calciner temperature hot without over-firing which leads to tower CO spikes.
3. **REC-3 | Upstream Raw Meal Quality & Fineness Control (HIGH)**: Control flour sieve residue `W3_Flour_#170` and LSF calcium saturation to stabilize burnability.
4. **REC-4 | Cooler Grate Bed Depth & Heat Recovery (MEDIUM)**: Adjust cooler grate speeds to maximize `Air_Temperature_Outlet_Cooler` secondary air heat recovery back to the kiln.
5. **REC-5 | Centralized Fan Speed & Draft Optimization (MEDIUM)**: Adjust `Oven_Fan_Speed` to match feed throughput and maintain cyclone O2 at 3.0%, while keeping `Temperature_1_Filter_Inlet` well below the safety ceiling.

---

## STEP 18 — Expert Verdict (Plant Manager Memo)

Write a professional 3-paragraph memo to the Plant Manager and Lead Operator:
- Para 1 — THE FINDING: The thermal deficit and cooler recovery gap.
- Para 2 — THE OPPORTUNITY: Conservative vs maximum financial opportunities.
- Para 3 — THREE IMMEDIATE ACTIONS the operator can take TODAY (bed depth adjustment, burner axial air trimming, O2 draft balance targets).
```

