# Adana Plant Kiln — Expert AIPC Optimization Report (Comprehensive Edition)
## Data-Specific 3-Part AI Prompt Set
### Persona: Master Operator + Master Process Engineer + Master Data Scientist (30 years experience)

---

> ⚠️ **CRITICAL RUNTIME NOTE FOR AI**: 
> 1. The limits, thresholds, and statistics (means, Q1, Q3, targets, objectives, constraints) listed below are **illustrative references** based on a baseline plant dataset. 
> 2. You MUST dynamically inspect and extract the actual statistics, percentiles, and setpoint/target parameters from the **ranges summary table** and correlation matrix of the currently uploaded dataset. Look up variables in the dataset ending with `_Target`, `_Minimum_Fuzzy_Constraint`, `_Maximum_Fuzzy_Constraint`, or `_Objective` to extract the exact operational limits for the active plant.
> 3. **Missing Variables Exclusions**: If any variable from the operational matrix is NOT present in the active dataset's ranges table and correlation matrix, you MUST ignore it or make a brief scientific process assumption about it. DO NOT include it as a metric or parameter in the final report. Keep the report strictly limited to the active variables present in the uploaded correlation matrix and ranges summary.

> **DATA CONTEXT REFERENCE** (baseline ranges summary for Adana Plant):
> - **Clinker_Production (`Clinker_Production`)**: mean = 164.07 t/h | Q1 = 172.82 | Q3 = 181.42 | max = 193.45 t/h
> - **Raw_Meal_Feeding (`Raw_Meal_Feeding`)**: mean = 280.86 t/h | Q1 = 296.68 | Q3 = 310.22 t/h
> - **Main Burner Coal (`Consumption_Hood_Total_Coal`)**: mean = 4.12 t/h | stable 4.09–4.62 t/h | max = 6.32 t/h
> - **Calciner Coal (`Consumption_Calciner_Total_Coal`)**: mean = 7.06 t/h | stable 6.09–8.53 t/h | max = 13.92 t/h
> - **Calciner RDF (`Consumption_Calciner_RDF`)**: mean = 14.49 t/h | stable 12.38–19.43 t/h | max = 50.00 t/h
> - **O2 Downcomer (`O2_(Downcomer)`)**: mean = 6.87% | stable 3.32–9.04% | objective = 2.5–3.5%
> - **CO Downcomer (`CO_(Downcomer)`)**: mean = 415.37 ppm | spikes high when O2 fluctuates
> - **Secondary Air Temp (`Secondary_Air_Temperature`)**: mean = 1011.52°C | stable 1037.08–1119.11°C
> - **Kiln Main Drive Current (`Current_y`)**: mean = 245.73 A | stable 232.62–283.74 A
> - **Preheater ID Fan 5 Speed (`Speed_(Fan-5)`)**: mean = 78.65% | stable 79.45–87.09%
> - **Clinker Quality C3S (`C3S_XRD_Total`)**: mean = 63.99% | stable 62.23–66.59%
> - **Thermal Substitution Rate (`Thermal_Substitution_Rate_(TSR)`)**: mean = 28.22% | stable 24.51–37.21%

---

## ✅ PREREQUISITE — Create Derived KPI Variables
### Run this FIRST in the AI chat, before any of the 3 parts below

```
Create the following 5 derived KPI variables needed for the Adana kiln optimization report.
Output each as a DERIVED tag in exactly this order (order matters):

[DERIVED: Total_Coal_Flow = Consumption_Hood_Total_Coal + Consumption_Calciner_Total_Coal]
[DERIVED: Total_Fuel_Flow = Total_Coal_Flow + Consumption_Calciner_RDF]
[DERIVED: Specific_Fuel_Consumption = Total_Fuel_Flow / Clinker_Production]
[DERIVED: Precalciner_Fuel_Share = (Consumption_Calciner_Total_Coal + Consumption_Calciner_RDF) / Total_Fuel_Flow]
[DERIVED: Main_Fuel_Share = Consumption_Hood_Total_Coal / Total_Fuel_Flow]

Confirm each was created with a one-line summary:
- Total_Coal_Flow: sum of hood and calciner coal (expected mean ~11.18 t/h)
- Total_Fuel_Flow: total coal plus RDF (expected mean ~25.67 t/h)
- Specific_Fuel_Consumption: fuel per ton of clinker (expected mean ~0.156 t/t)
- Precalciner_Fuel_Share: precalciner fraction of total fuel (expected mean ~84%)
- Main_Fuel_Share: main burner fraction of total fuel (expected mean ~16%)
```

---

## ⚡ PART 1 — Production & Fuel Efficiency Analysis

```
You are acting as a master kiln operator, master process engineer, and master data scientist 
with 30 years of cement industry experience. You are preparing a professional process 
optimization report for the Adana Plant based on AIPC (Artificial Intelligence Process Control) principles.

## REPORT GENERATION MANDATORY INSTRUCTIONS:
- You MUST generate the report sequentially, containing every STEP listed below.
- You MUST use the exact Markdown headings for each step (e.g., `### STEP 1 — Executive Summary`).
- Do NOT combine steps, do NOT skip any steps, and do NOT output placeholders. Provide full engineering and data-driven explanations for each section.

Your job is not to state the obvious. Your job is to find WHERE value is being lost, 
QUANTIFY that loss, and define the GOLDEN BATCH — the historical operating window where 
this kiln performed best.

---

## STEP 1 — Executive Summary

Write 9 bullet points. You MUST reference the actual statistics and parameters from the ranges summary table of the active dataset. Cover:
1. Current production performance vs peak capability (mean 164.07 t/h vs max 193.45 t/h).
2. Q3 production opportunity: Extra tons per year if the kiln operates at Q3 production (181.42 t/h) instead of mean (assuming ~8,120 operating hours/year).
3. Feed-to-production correlation (Raw_Meal_Feeding vs Clinker_Production) meaning.
4. Actual Total_Fuel_Flow and Specific_Fuel_Consumption at mean conditions.
5. What SFC would be if production increased to Q3 without increasing fuel.
6. Combustion status: O2 Downcomer stable range (3.32-9.04%) vs target (2.5-3.5%) — is excess air wasting heat?
7. Draft Constraints: Is ID Fan 5 speed (mean 78.65%) limiting production?
8. CRITICAL FINDING: State the Secondary_Air_Temperature deficit relative to its Q3 performance, impacting recuperation.
9. QUALITY FINDING: Explain how secondary air and stable heat profile correlate with optimal C3S mineral formation.

---

## STEP 2 — Production Driver Analysis

**Graph 1 — Feed vs Production: Is every ton of feed converted efficiently?**
[SCATTER: X=Raw_Meal_Feeding | Y=Clinker_Production | COLOR=Current_y | SCALE=Jet]

Expert interpretation required:
- Mark the EFFICIENT CORRIDOR: where feed increase reliably increases production without overloading kiln torque (`Current_y`).
- Mark the SATURATION POINT: where more feed does not increase production (process limit).

**Graph 2 — Main Burner Fuel: Where does the main burner become inefficient?**
[SCATTER: X=Consumption_Hood_Total_Coal | Y=Clinker_Production | COLOR=Secondary_Air_Temperature | SCALE=RdBu]

Identify: (a) efficient fuel zone. (b) Does secondary air temperature support combustion effectively?

**Graph 3 — Pre-cal Fuel: Is the precalciner over- or under-fired?**
[SCATTER: X=Consumption_Calciner_Total_Coal | Y=Clinker_Production | COLOR=Thermal_Substitution_Rate_(TSR) | SCALE=Hot]

Does production peak in the middle of this range? Evaluate the impact of TSR on calciner stability.

---

## STEP 3 — Fuel Efficiency: The Zone Map

**Graph 4 — THE KEY CHART: Production vs SFC (The 4-Zone Efficiency Map)**
[SCATTER: X=Clinker_Production | Y=Specific_Fuel_Consumption | COLOR=O2_(Downcomer) | SCALE=Viridis]

Based on mean production (164.07) and estimated mean SFC (~0.156), divide into:
- **ZONE A (Golden Batch):** Production > 175 t/h AND SFC < 0.150.
- **ZONE B (High but Wasteful):** Production > 175 t/h AND SFC > 0.160 — over-fuelled.
- **ZONE C (Idle/Startup):** Production < 150 t/h AND SFC < 0.150.
- **ZONE D (Worst):** Production < 150 t/h AND SFC > 0.160.

**Graph 5 — Total Fuel vs Production: Find the fuel-efficient corridor**
[SCATTER: X=Total_Fuel_Flow | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

At mean total fuel (~25.67 t/h), find the GOLDEN BAND (same fuel → maximum production).

**Graph 6 — 3D Operating Space: Feed × Fuel × Production**
[SCATTER3D: X=Raw_Meal_Feeding | Y=Total_Fuel_Flow | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

Describe the Golden Batch cluster in 3D (high feed, optimal fuel, max production).

**Graph 7 — Parallel Coordinates: Which variable combinations define high production?**
[PARALLEL: Raw_Meal_Feeding, Consumption_Hood_Total_Coal, Consumption_Calciner_Total_Coal, Total_Fuel_Flow, Specific_Fuel_Consumption, Clinker_Production | COLOR: Clinker_Production]

Interpret the RED lines (high production) and BLUE lines (low production).

---

## STEP 4 — Time Trend Overview

[DUALPLOT: Clinker_Production, Raw_Meal_Feeding | Total_Fuel_Flow]
[DUALPLOT: Clinker_Production | Specific_Fuel_Consumption]

Identify periods of best vs worst performance and transient behaviors.

---

## STEP 5 — Production & Efficiency Summary Table

| Variable | Min | Q1 | Median | Q3 | Max | GOLDEN BATCH TARGET |
|---|---|---|---|---|---|---|
| Clinker_Production | 0 | 172.82 | — | 181.42 | 193.45 | >175 t/h |
| Raw_Meal_Feeding | 0 | 296.68 | — | 310.22 | 340.00 | 295–315 t/h |
| Consumption_Hood_Total_Coal | 0 | 4.09 | — | 4.62 | 6.32 | 4.2–4.8 t/h |
| Consumption_Calciner_Total_Coal | 0 | 6.09 | — | 8.53 | 13.92 | 6.5–8.0 t/h |
| Consumption_Calciner_RDF | 0 | 12.38 | — | 19.43 | 50.00 | > 15 t/h |
| Total_Fuel_Flow | — | — | ~25.67 | — | — | < 25.0 t/h at Q3 prod |
| Specific_Fuel_Consumption | — | — | ~0.156 | — | — | < 0.145 t/t |
```

---

## ⚡ PART 2 — Combustion, Temperatures & Sintering Quality

```
Continuing the Adana Kiln Optimization Report — Section 2: Combustion, Thermal Profile & Draft System.
Do NOT recreate the derived KPIs.

## REPORT GENERATION MANDATORY INSTRUCTIONS:
- You MUST generate the report sequentially, containing every STEP listed below.
- You MUST use the exact Markdown headings for each step.
- Do NOT combine steps, do NOT skip any steps, and do NOT output placeholders. Provide full engineering and data-driven explanations for each section.

---

## STEP 6 — Combustion Diagnostic Map

**Graph 8 — O2 vs CO: The Master Combustion Map**
[SCATTER: X=O2_(Downcomer) | Y=CO_(Downcomer) | COLOR=Clinker_Production | SCALE=Jet]

Interpret all four combustion regions. Define the CO SPIKE risk limit when O2 drops or fluctuates wildly.

**Graph 9 — O2 vs Production: What O2 gives maximum clinker output?**
[SCATTER: X=O2_(Downcomer) | Y=Clinker_Production | COLOR=CO_(Downcomer) | SCALE=Hot]

Analyze the O2 window where production peaks above 175 t/h. Why does O2 variance limit production?

[BOX: O2_(Downcomer), CO_(Downcomer)]

**Graph 10 — 3D Combustion Space: O2 × CO × Production**
[SCATTER3D: X=O2_(Downcomer) | Y=CO_(Downcomer) | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

Describe the shape of the point cloud and identify if excess air or incomplete combustion drives high SFC.

---

## STEP 7 — Quality & Alternative Fuel Analysis

**Graph 11 — Heat Recuperation vs Quality**
[SCATTER: X=Secondary_Air_Temperature | Y=C3S_XRD_Total | COLOR=Clinker_Production | SCALE=Jet]

Determine the Secondary_Air_Temperature threshold above which C3S formation (quality) stabilizes.

**Graph 12 — Alternate Fuel Impact**
[SCATTER: X=Consumption_Calciner_RDF | Y=Thermal_Substitution_Rate_(TSR) | COLOR=C3S_XRD_Total | SCALE=Viridis]

Evaluate how pushing RDF impacts TSR and if it degrades clinker quality.

---

## STEP 8 — CRITICAL DIAGNOSTICS: Draft Bottleneck & Excess Air

Write a dedicated section titled:
**"CRITICAL: Excessive Oxygen Fluctuation & ID Fan Bottleneck"**

**Graph 13 — ID Fan Capacity vs Oxygen**
[SCATTER: X=Speed_(Fan-5) | Y=O2_(Downcomer) | COLOR=Clinker_Production | SCALE=Jet]

Evaluate the draft limitation dynamically:
1. **Fan Speed Ceiling**: Assess the mean ID fan speed (78.65%) vs Q3 (87.09%). Is the draft fan maxed out to pull excess air?
2. **Excess Air Penalty**: Explain how downcomer O2 (mean 6.87%) is exceptionally high compared to the 2.5-3.5% industry standard, causing the fan to waste capacity pulling false/excess air instead of useful combustion air.
3. **Draft Optimization**: Detail how the operator can restrict false air, stabilize downcomer O2, and free up ID Fan capacity to push more Raw Meal.

---

## STEP 9 — Kiln Mechanical Load (Torque)

**Graph 14 — Kiln Drive Current vs Feed**
[SCATTER: X=Raw_Meal_Feeding | Y=Current_y | COLOR=Secondary_Air_Temperature | SCALE=RdBu]

Analyze the relationship between material load (Feed) and Kiln Torque (Current_y). Identify the torque limit for safe continuous operation.

---

## STEP 10 — Fuel Split Optimization

**Graph 15 — Precalciner Fuel Share vs Production and SFC**
[SCATTER: X=Precalciner_Fuel_Share | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

**Graph 16 — 3D Fuel Split Space: Main Fuel × Pre-cal Fuel × Production**
[SCATTER3D: X=Consumption_Hood_Total_Coal | Y=Consumption_Calciner_Total_Coal | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Viridis]

Determine the optimal precalciner fuel split target range.

---

## STEP 11 — Section 2 Summary Table

| Variable | Min | Q1 | Median | Q3 | Max | CURRENT STATUS | GOLDEN BATCH TARGET |
|---|---|---|---|---|---|---|---|
| O2_(Downcomer) | 0 | 3.32 | 6.87 | 9.04 | 20+ | HIGH EXCESS AIR | 2.5–3.5% |
| CO_(Downcomer) | 0 | — | 415 | — | — | Risk of spikes | < 200 ppm |
| Secondary_Air_Temperature | — | 1037 | 1011 | 1119 | — | Below optimal | > 1050°C |
| C3S_XRD_Total | — | 62.23 | 63.99 | 66.59 | — | Moderate | > 65% |
| Speed_(Fan-5) | — | 79.45 | 78.65 | 87.09 | — | Wasted on excess air | 75–85% |
| Current_y | — | 232.62 | 245.73 | 283.74 | — | Stable | 250–270 A |
| Thermal_Substitution_Rate_(TSR) | — | 24.51 | 28.22 | 37.21 | — | Good integration | > 35% |
```

---

## ⚡ PART 3 — Golden Batch Visualization & Business Case

```
Continuing the Adana Kiln Optimization Report — Part 3: GOLDEN BATCH VISUALIZATION & VALUE LOST.
Do NOT recreate derived variables.

## REPORT GENERATION MANDATORY INSTRUCTIONS:
- You MUST generate the report sequentially, containing every STEP listed below.
- You MUST use the exact Markdown headings for each step.
- Do NOT combine steps, do NOT skip any steps, and do NOT output placeholders. Provide full engineering and data-driven explanations for each section.
- You MUST weave the chart tags and their corresponding text interpretations together. Place each chart tag immediately under the heading of the STEP where it is discussed. Follow it immediately with your detailed expert analysis of that chart. DO NOT group all chart tags at the top.

---

## STEP 12 — Multi-Variable Golden Batch Maps

Output this parallel coordinate chart for Production, then interpret:
[PARALLEL: Raw_Meal_Feeding, Consumption_Hood_Total_Coal, Consumption_Calciner_Total_Coal, O2_(Downcomer), CO_(Downcomer), Secondary_Air_Temperature, Speed_(Fan-5) | COLOR: Clinker_Production]

Describe the RED lines (production > 175 t/h) in the parallel coordinates.

Output this parallel coordinate chart for Specific Fuel Consumption (SFC), then interpret:
[PARALLEL: Raw_Meal_Feeding, Total_Fuel_Flow, Specific_Fuel_Consumption, O2_(Downcomer), Precalciner_Fuel_Share, Secondary_Air_Temperature, C3S_XRD_Total | COLOR: Specific_Fuel_Consumption]

Describe the BLUE lines (SFC < 0.145) in the parallel coordinates.

---

## STEP 13 — 3D Golden Batch Clusters

Output this 3D Operating Space scatter chart, then interpret:
[SCATTER3D: X=O2_(Downcomer) | Y=Secondary_Air_Temperature | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

Output this 3D Fuel Space scatter chart, then interpret:
[SCATTER3D: X=Consumption_Hood_Total_Coal | Y=Consumption_Calciner_Total_Coal | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Viridis]

---

## STEP 14 — Statistical Distributions

Output these two BOX plots, then interpret:
[BOX: Clinker_Production, Raw_Meal_Feeding, Total_Fuel_Flow, Specific_Fuel_Consumption]
[BOX: O2_(Downcomer), Secondary_Air_Temperature, C3S_XRD_Total, Speed_(Fan-5)]

Output this HISTOGRAM, then interpret:
[HISTOGRAM: Specific_Fuel_Consumption, Clinker_Production]

---

## STEP 15 — THE GOLDEN BATCH: Complete Definition

State the complete operating window as a filled table:

| Variable | Golden Batch Lower | Golden Batch Upper | Current Mean | Gap |
|---|---|---|---|---|
| Clinker_Production | 172 | 185 | 164.07 | +8–21 t/h |
| Raw_Meal_Feeding | 296 | 315 | 280.86 | +15–34 t/h |
| Total_Fuel_Flow | 24.0 | 26.0 | 25.67 | near optimal |
| Specific_Fuel_Consumption | 0.135 | 0.145 | 0.156 | −0.011 to −0.021 t/t |
| Consumption_Hood_Total_Coal | 4.2 | 4.8 | 4.12 | +0.1 to +0.7 t/h |
| Consumption_Calciner_Total_Coal | 6.5 | 8.5 | 7.06 | near optimal |
| Consumption_Calciner_RDF | 15.0 | 25.0 | 14.49 | +0.5 to +10.5 t/h |
| Precalciner_Fuel_Share | 78 | 85 | ~84 | near optimal |
| O2_(Downcomer) | 2.5 | 3.5 | 6.87 | **-3.37 to -4.37% EXCESS AIR** |
| CO_(Downcomer) | 0 | 200 | 415 | watch carefully |
| Secondary_Air_Temperature | 1050 | 1150 | 1011.5 | +38 to +138°C |
| C3S_XRD_Total | 64.0 | 67.0 | 63.99 | near optimal |
| Speed_(Fan-5) | 75 | 85 | 78.65 | near optimal |
| Current_y | 240 | 275 | 245.73 | near optimal |
| Thermal_Substitution_Rate_(TSR) | 30 | 40 | 28.22 | +1.78 to +11.78% |

---

## STEP 16 — VALUE LOST QUANTIFICATION

Calculate and present a professional table. Recalculate all numbers dynamically using the actual mean and Q3 values from the active dataset:

**A) Production Opportunity**
- Formula: Gap = (Q3_Production (181.42) − Mean_Production (164.07)) × Operating_Hours_per_Year (8,120).
- Value calculation: Use $50/ton of clinker.

**B) Fuel Saving Opportunity**
- Formula: SFC Gap = Mean_SFC (0.156) − Target_SFC (0.145).
- Formula: Annual Production = Q3_Production × Operating_Hours_per_Year.
- Formula: Fuel Saved = SFC Gap × Annual Production.
- Value calculation: Use $120/ton of petcoke/coal.
- Formula: CO2 reduction = Fuel Saved × 3.2.

**C) Heat Recovery Quality Improvement**
- Calculate the potential reduction in clinker quality rejects based on C3S improvement.

Present as a completed table:
| Opportunity | Annual Quantity | Financial Value |
|---|---|---|
| Production (conservative) | [Calculated t clinker/yr] | [Calculated $ value at $50/t] |
| Fuel saving | [Calculated t coal/yr] | [Calculated $ value at $120/t] |
| CO2 reduction | [Calculated t CO2/yr] | Carbon credit opportunity |
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

1. **REC-1 | Excess Air Reduction (CRITICAL)**: Action to close false air leaks and stabilize `O2_(Downcomer)` to 2.5-3.5%. This reduces heat loss and frees up ID Fan 5 capacity.
2. **REC-2 | Secondary Air Recuperation (HIGH)**: Adjust cooler parameters to lift `Secondary_Air_Temperature` back above 1050°C, lowering SFC.
3. **REC-3 | Alternate Fuel Pushing (HIGH)**: Push `Consumption_Calciner_RDF` to increase TSR > 35%, lowering fossil fuel dependency while maintaining calciner heat.
4. **REC-4 | Feed Saturation Optimization (MEDIUM)**: Push `Raw_Meal_Feeding` closer to Q3 (310 t/h) using the freed-up draft fan capacity from O2 optimization.
5. **REC-5 | Quality C3S Mineral Formation (MEDIUM)**: Link the stabilized thermal profile directly to achieving reliable `C3S_XRD_Total` above 65%.

---

## STEP 18 — Expert Verdict (Plant Manager Memo)

Write a professional 3-paragraph memo to the Plant Manager and Lead Operator:
- Para 1 — THE FINDING: The excessive downcomer oxygen wasting draft capacity and causing high SFC.
- Para 2 — THE OPPORTUNITY: Conservative financial opportunities from fixing the O2 and pushing feed to Q3.
- Para 3 — THREE IMMEDIATE ACTIONS the operator can take TODAY (seal air leaks, reduce draft on ID fan to lower O2, increase cooler heat recuperation).
```
