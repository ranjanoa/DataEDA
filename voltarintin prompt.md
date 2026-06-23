# Kiln W3 — Expert Optimization Report
## Data-Specific 3-Part AI Prompt Set
### Persona: Master Operator + Master Process Engineer + Master Data Scientist (30 years experience)

---

> ⚠️ **CRITICAL RUNTIME NOTE FOR AI**: 
> 1. The limits, thresholds, and statistics (means, Q1, Q3, targets, objectives, constraints) listed below are **illustrative references** based on a baseline plant dataset. 
> 2. You MUST dynamically inspect and extract the actual statistics, percentiles, and setpoint/target parameters from the **ranges summary table** and correlation matrix of the currently uploaded dataset. Look up variables in the dataset ending with `_Target`, `_Minimum_Fuzzy_Constraint`, `_Maximum_Fuzzy_Constraint`, or `_Objective` (e.g. `Pyrometer_-_Target`, `O2_Oven_-_Target`) to extract the exact operational limits for the active plant.
> 3. **Missing Variables Exclusions**: If any variable from the operational matrix (such as RDF main burner, RIP liquids burner, or Ammonia injection) is NOT present in the active dataset's ranges table and correlation matrix, you MUST ignore it or make a brief scientific process assumption about it. DO NOT include it as a metric or parameter in the final report. Keep the report strictly limited to the active variables present in the uploaded correlation matrix and ranges summary.

> **DATA CONTEXT REFERENCE** (baseline ranges summary):
> - **Clinker Production**: mean = 146.71 t/h | Q1 = 149.60 | Q3 = 162.42 | max = 182.55 | **6.5% shutdowns**
> - **Flour Feed**: mean = 245 | Q1 = 249.81 | Q3 = 271.52 | max = 319.04 t/h
> - **Main Coke**: mean = 5.52 | stable 5.48–6.02 t/h | max = 7.78
> - **Pre-cal Coke**: mean = 8.19 | stable 7.12–9.96 t/h | max = 13.95
> - **O2 Cyclone Tower**: mean = 3.50 | stable 2.35–3.38% | objective = 3.0%
> - **CO Cyclone Tower**: mean = 0.11 | stable 0.10–0.13% | **max constraint = 0.14%**
> - **NOx Cyclone Tower**: mean = 440 | stable 365–513 | max constraint = 600 mg/Nm³
> - **NOx Smoke Box**: mean = 181 | Q3 = 327 mg/Nm³
> - **Pyrometer**: mean = 913°C | stable 855–1001°C | **target = 1050°C | min constraint = 950°C** ← CRITICAL GAP
> - **Material Temp A55**: mean = 867°C | stable 855–920°C
> - **Fan Speeds**: all running ~65–74%

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

> ⚠️ **You will see green "Created" chips appear in the AI response for each variable.**
> If any show red "Failed": check the exact column name in the variable selector dropdown and confirm your CSV is uploaded and processed before running this prompt.
> Once all 4 show green ✅ — proceed to Part 1.

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
- Total_Fuel_Flow = Main_Mass_Coke_Flow_Rate + Pre-cal_Coke_Flow_Rate (~13.71 t/h at mean)
- Specific_Fuel_Consumption = Total_Fuel_Flow / Clinker_Production (~0.094 t/t at mean)
- Precalciner_Fuel_Share = Pre-cal_Coke_Flow_Rate / Total_Fuel_Flow (~60% at mean)
- Main_Fuel_Share = Main_Mass_Coke_Flow_Rate / Total_Fuel_Flow (~40% at mean)

Confirmed statistics:
- Clinker Production: mean=146.71, Q1=149.60, Q3=162.42, max=182.55 t/h (6.5% zeros/shutdowns)
- Flour Feed: mean=245, Q1=249.81, Q3=271.52, max=319.04 t/h
- Main Coke Flow: mean=5.52, stable range 5.48–6.02 t/h, max=7.78
- Pre-cal Coke Flow: mean=8.19, stable range 7.12–9.96 t/h, max=13.95
- Correlation: Flour_Feed vs Clinker_Production = +0.997 (near-perfect LOI-mass balance)
- Correlation: Main_Mass_Coke_Flow_Rate vs Clinker_Production = +0.881
- Correlation: Pre-cal_Coke_Flow_Rate vs Clinker_Production = +0.772
- Correlation: Check_O2_Cyclone_Tower vs Clinker_Production = -0.771

Quality Drivers & Moduli Correlations:
- Clinker Free Lime (W3_Clinker_CaOL): mean = 2.01% | stable = 1.70 - 2.33% (indicates unburnt lime)
- Clinker LSF/FSC (W3_Clinker_FSC): mean = 98.93 (potential calcium saturation limit)
- Flour Sieve Residue (W3_Flour_#170): mean = 16.67% (meal coarseness indicator)
- Clinker Litre Weight (W3_Clinker_Weight_Liter): mean = 1008.45 g/l (bulk density/sintering degree)
- Correlation: Free Lime vs Clinker LSF/FSC = +0.502 (chemical drive for excess calcium free lime)
- Correlation: Free Lime vs W3_Fe2O3_Clinker = -0.282 (fluxing effect of iron oxide on liquid phase combination)
- Correlation: Free Lime vs Clinker Litre Weight = -0.192 (higher bulk density / sintering reduces free lime)
- Correlation: Free Lime vs Flour Sieve Residue = +0.198 (coarser raw meal degrades burnability and raises free lime)

---

## STEP 1 — Executive Summary (as an expert, not a textbook)

Write 9 bullet points. You MUST reference the actual statistics and parameters from the ranges summary table of the active dataset (the baseline numbers listed above are for reference only). Cover:
1. Current production performance vs peak capability (mean vs max in active dataset) — what is the gap?
2. If the kiln could operate at Q3 production instead of mean, how many extra tons per year (assuming ~8,120 operating hours/year at the actual shutdown rate from the active dataset)?
3. What does feed-to-production correlation (e.g. Flour_Feed vs Clinker_Production) mean for the operator — is production feed-limited?
4. What is the actual Total_Fuel_Flow at mean conditions in your dataset? What is the Specific_Fuel_Consumption at mean?
5. What would SFC be if production increased to Q3 without increasing fuel?
6. Combustion status: O2 stable range (Q1-Q3) vs. the actual O2 objective/target — are we close to optimal?
7. Fan speeds running at their stable range (Q1-Q3) — at what production level do they operate and is there excess air?
8. CRITICAL FINDING: state the pyrometer temperature deficit relative to its actual target and minimum constraint.
9. QUALITY FINDING: explain how raw meal LSF and coarseness sieve residue correlate with clinker quality (free lime) in the active dataset, and how iron oxide serves as a fluxing countermeasure.

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
| Clinker_Production | 0 | 149.60 | — | 162.42 | 182.55 | >162 t/h |
| Flour_Feed | 0 | 249.81 | 245 | 271.52 | 319.04 | 260–272 t/h |
| Main_Mass_Coke_Flow_Rate | 0 | 5.48 | 5.52 | 6.02 | 7.78 | 5.5–5.9 t/h |
| Pre-cal_Coke_Flow_Rate | 0 | 7.12 | 8.19 | 9.96 | 13.95 | 7.5–9.0 t/h |
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
- O2 Cyclone Tower: mean=3.50%, stable 2.35–3.38%, OBJECTIVE=3.0% 
- CO Cyclone Tower: mean=0.11%, stable 0.10–0.13%, MAX CONSTRAINT=0.14%
- NOx Cyclone Tower: mean=440, stable 365–513, MAX CONSTRAINT=600 mg/Nm³
- NOx Smoke Box: mean=181, Q3=327 mg/Nm³
- O2 Smoke Box: mean=1.35%, stable 0.0–2.46% (kiln inlet exit O2)
- CO Smoke Box: mean=0.02%, max observed=2.12% (kiln inlet exit CO)
- Pyrometer Burning Zone: mean=913°C, stable 855–1001°C
  → TARGET=1050°C, MIN FUZZY CONSTRAINT=950°C ← OPERATING 37°C BELOW MINIMUM!
  *Note: Physically, clinkerization requires clinker bed temperatures of 1350-1450°C. 
   The pyrometer's 913°C mean represents an instrumentation/dust calibration offset, 
   though it is used as a valid relative signal for targets and constraints.
- Material Temp A55: mean=867°C, stable 855–920°C
- Cyclone Temp A55: mean=883°C, stable 877–912°C
- Cyclone Temp A54: mean=799°C, stable 806–813°C
- Cyclone Temp A53: mean=728°C, stable 728–740°C
- Fan Speed 5: mean=64.63%, stable 65.67–69.74% (strongest prod correlation: 0.902)
- Fan Speed 4: mean=64.95%, stable 65.99–70.02%
- Correlation: NOx Smoke Box vs O2 Smoke Box = +0.592
- Fan Speed Scaling: All process fans (Speed 1 to 5) scale synchronously (correlation > 0.92), 
  indicating a centralized draft scheme tracking feed rate rather than independent loops.

Operational Matrix Constraints & Exclusions:
1. Gas Probe Maintenance & Cleaning (`W3_Probe_Inserted`): When the gas probe status `W3_Probe_Inserted` is 0 (indicating the probe is pulled out for maintenance or cleaning), the gas analyzer readings at the smoke box (`Analyze_O2_in_Smoke_Box`, `Check_NOx_Smoke_Box`, `Check_CO_in_Smoke_Box`) are corrupted by ambient false air and MUST be ignored.
2. Shutdown Exclusions: All process parameters (coke flows, fan speeds, temperatures) drop during shutdowns. Zeros in `Clinker_Production` and `Flour_Feed` (representing ~6.5% of the data) must be isolated so they do not skew the stable operating range stats.

---

## STEP 6 — Combustion Diagnostic Map

**Graph 6 — O2 vs CO: The Master Combustion Map**
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

**Graph 7 — O2 vs Production: What O2 gives maximum clinker output?**

[SCATTER: X=Check_O2_Cyclone_Tower | Y=Clinker_Production | COLOR=Check_CO_Cyclone_Tower | SCALE=Hot]

Find: (a) O2 range where production peaks above 162 t/h (Q3) — is this in the 2.35–3.38% window?
(b) At O2 below 2.35%, does production drop or stay high with high CO risk?
(c) At O2 above 3.38%, does production drop due to excess air cooling?

[BOX: Check_O2_Cyclone_Tower, Check_CO_Cyclone_Tower, Check_NOx_Cyclone_Tower]

**Graph — 3D Combustion Space: O2 × CO × Production**
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

**Graph — Parallel Coordinates: Combustion & Production Fingerprint**
(Find the combination of O2, CO, NOx, and pyrometer that defines best production)

[PARALLEL: Check_O2_Cyclone_Tower, Check_CO_Cyclone_Tower, Check_NOx_Cyclone_Tower, Optical_Pyrometer_Temp._Burning_Zone, Fan_Speed_5, Clinker_Production | COLOR: Clinker_Production]

For RED lines (production > 162 t/h):
- O2: in the 2.5–3.3% window or higher?
- CO: below 0.12% in all high-production periods?
- NOx: what range (365–480 as per Golden Batch target)?
- Pyrometer: above or below 950°C? This is the critical question.
- Fan 5: what speed gives both high production AND good O2?

For BLUE lines (production < 140 t/h):
- Is O2 consistently out of range, or is it mainly pyrometer that's cold?
- This PARALLEL chart distinguishes whether low production is a combustion problem or a thermal management problem.

---

## STEP 7 — Emission Analysis

**Graph 8 — NOx vs O2 (Smoke Box): Is excess air driving thermal NOx?**
(Current correlation: +0.592 — significant)

[SCATTER: X=Analyze_O2_in_Smoke_Box | Y=Check_NOx_Smoke_Box | COLOR=Clinker_Production | SCALE=Jet]

The NOx max constraint at the tower is 600 mg/Nm³. Current mean NOx at cyclone tower is 440.
At what smoke box O2 level does NOx at the tower risk exceeding 500 mg/Nm³?
Is there a smoke box O2 threshold above which NOx increases sharply?

**Graph 9 — NOx vs Burning Zone Temperature: Is high temperature driving NOx?**

[SCATTER: X=Optical_Pyrometer_Temp._Burning_Zone | Y=Check_NOx_Cyclone_Tower | COLOR=Analyze_O2_in_Smoke_Box | SCALE=Viridis]

Note: pyrometer mean (913°C) is BELOW the minimum fuzzy constraint (950°C).
Does NOx actually increase in the 913–1001°C range? Is thermal NOx a real concern at these temperatures,
or is the kiln running cool enough that NOx is primarily from raw material nitrogen?
At what temperature does NOx risk exceeding the 500 mg/Nm³ objective?

[HISTOGRAM: Check_NOx_Cyclone_Tower, Check_NOx_Smoke_Box]

---

## STEP 8 — CRITICAL FINDING: The Temperature Deficit

This is the most important finding of Part 2. Write a dedicated section titled:

**"CRITICAL: Kiln Operating Below Thermal Target — Burning Zone Temperature Deficit"**

The pyrometer target and minimum fuzzy constraints must be extracted from the active dataset (e.g. from `Pyrometer_-_Target` and `Pyrometer_-_Minimum_Fuzzy_Constraint` or their equivalent metrics). Calculate the temperature deficit dynamically:
- What is the actual pyrometer mean vs. its target and minimum constraint?
- If the baseline is mean = 913°C vs. min constraint = 950°C (giving a 37°C deficit), compute the exact deficit and percentage for the active dataset.

[DUALPLOT: Optical_Pyrometer_Temp._Burning_Zone, Material_Temp_Cyclone_A55 | Clinker_Production]
[SCATTER: X=Optical_Pyrometer_Temp._Burning_Zone | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

Answer these expert questions using the active dataset's actual ranges and statistics:
1. What % of historical time is the pyrometer below the minimum constraint? (Calculate based on the stable range Q1-Q3 relative to the constraint).
2. Does production increase when pyrometer is within the target range vs below the minimum constraint?
3. Does SFC decrease (better efficiency) when pyrometer is above the minimum constraint?
4. MECHANISM: explain what happens when burning zone temperature is too low:
   - Incomplete calcination → higher free lime (W3_Clinker_CaOL or equivalent) → rejected clinker
   - Lower clinker quality (using actual free lime stats: mean and max)
   - Operator response: add more fuel → wasted fuel
   - Or: reduce feed to stabilize → lost production
5. What is the RECOMMENDED pyrometer target range based on the active dataset's targets?

**Graph — Cyclone Temperature Profile vs Production**

[SCATTER: X=Cyclone_Gas_Temp._A55 | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]
[DUALPLOT: Cyclone_Gas_Temp._A53, Cyclone_Gas_Temp._A54, Cyclone_Gas_Temp._A55 | Material_Temp_Cyclone_A55]

The cyclone stable ranges: A53=728–740°C, A54=806–813°C, A55=877–912°C.
Is there a temperature gradient inversion anywhere in the preheater that would indicate false air?

**Graph — 3D Thermal Space: Pyrometer × Cyclone A55 × Production**
(Does production increase ONLY when BOTH burning zone AND preheater are at the right temperature?)

[SCATTER3D: X=Optical_Pyrometer_Temp._Burning_Zone | Y=Cyclone_Gas_Temp._A55 | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

The Golden Thermal Cluster should show:
- X (Pyrometer) → 950–1050°C (above the 950°C minimum constraint)
- Y (Cyclone A55) → 880–912°C (within stable range)
- Z (Production) → above 162 t/h
- Color (SFC) → blue/green

Key question: Does Z (production) increase ONLY when X (pyrometer) is above 950°C? Or can high production occur at cold pyrometer temperatures too? This directly answers whether the temperature deficit is CAUSING low production or is just correlated.

**Graph — Parallel Coordinates: Full Thermal Chain + Emissions**
(Map the complete preheater temperature profile during high vs low production)

[PARALLEL: Cyclone_Gas_Temp._A53, Cyclone_Gas_Temp._A54, Cyclone_Gas_Temp._A55, Material_Temp_Cyclone_A55, Optical_Pyrometer_Temp._Burning_Zone, Check_NOx_Cyclone_Tower, Clinker_Production | COLOR: Clinker_Production]

For RED lines (highest production):
- Is the entire thermal chain (A53→A54→A55→Pyrometer) uniformly hotter?
- Or does the pattern show high preheater temps but cold pyrometer (indicating heat loss between preheater and burning zone)?
- What is the NOx level when pyrometer is above 950°C and production is high?

This parallel chart reveals whether temperature management is one coordinated action or requires independent control at multiple points in the preheater chain.

---

## STEP 9 — Fan & Draft System

**Graph — Fan 5 (strongest corr 0.902): Is fan speed always optimally matched to production?**

[SCATTER: X=Fan_Speed_5 | Y=Clinker_Production | COLOR=Check_O2_Cyclone_Tower | SCALE=RdBu]
[SCATTER: X=Fan_Speed_5 | Y=Check_O2_Cyclone_Tower | COLOR=Clinker_Production | SCALE=Jet]

Fan 5 stable range is 65.67–69.74%. 
- At what fan speed does O2 go above 3.38% (excess air territory)?
- Is there evidence of fan over-speed driving excess air at the same production level?
- What fan speed gives O2 = 3.0% (objective) at Q3 production (162 t/h)?

[BOX: Fan_Speed_1, Fan_Speed_2, Fan_Speed_3, Fan_Speed_4, Fan_Speed_5]

Expert assessment: The system controller has an O2 objective of 3.0% and uses a fuzzy constraint 
range of 1.5–4.4%. With current mean O2 at 3.5% (slightly above objective), is there evidence 
the draft system is running slightly hot? What is the fan speed reduction opportunity?

---

## STEP 10 — Fuel Split Optimization

**Graph — Precalciner Fuel Share vs Production and SFC**

[SCATTER: X=Precalciner_Fuel_Share | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]
[SCATTER: X=Precalciner_Fuel_Share | Y=Check_CO_Cyclone_Tower | COLOR=Check_O2_Cyclone_Tower | SCALE=RdBu]
[SCATTER: X=Precalciner_Fuel_Share | Y=Check_NOx_Cyclone_Tower | COLOR=Optical_Pyrometer_Temp._Burning_Zone | SCALE=Viridis]

Pre-cal mean share ≈ 8.19/(8.19+5.52) = 59.7% of total fuel.
Main burner share ≈ 40.3%.
- Is the optimal precalciner share above or below 60%?
- Does too much precalciner fuel (>65%) cause CO problems in the tower?
- Does too little precalciner fuel (<55%) cause burning zone over-heating and higher NOx?
- What fuel split minimizes SFC while keeping CO and NOx within constraints?

**Graph — 3D Fuel Split Space: Main Fuel × Pre-cal Fuel × Production**
(Shows the full fuel combination space and which split achieves maximum production with minimum SFC)

[SCATTER3D: X=Main_Mass_Coke_Flow_Rate | Y=Pre-cal_Coke_Flow_Rate | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Viridis]

The optimal fuel split zone should appear as a ridge in the 3D surface where:
- X (Main fuel) → 5.5–5.9 t/h
- Y (Pre-cal fuel) → 7.5–9.0 t/h
- Z (Production) → peak values > 162 t/h
- Color → dark purple/blue (lowest SFC)

**Graph — Parallel Coordinates: Fuel Split + Combustion + Emissions**
(Shows how fuel split choice propagates through to combustion quality and NOx)

[PARALLEL: Main_Mass_Coke_Flow_Rate, Pre-cal_Coke_Flow_Rate, Precalciner_Fuel_Share, Check_O2_Cyclone_Tower, Check_CO_Cyclone_Tower, Check_NOx_Cyclone_Tower, Specific_Fuel_Consumption | COLOR: Clinker_Production]

For RED lines (highest production):
- Does Precalciner_Fuel_Share cluster tightly (e.g., 57–62%) or is it spread?
- Does good combustion (O2 in range, CO below 0.12%) always accompany optimal fuel split?
- What is NOx doing when fuel split is optimal?

For BLUE lines (worst operation):
- Is the precalciner being over-fuelled (>65% share) causing CO problems?
- Or under-fuelled (<55%) causing burning zone over-temperature and NOx spikes?
This chart reveals the OPTIMAL FUEL SPLIT WINDOW with all its downstream effects.

---

## STEP 11 — Section 2 Summary Table

| Variable | Min | Q1 | Median | Q3 | Max | CURRENT STATUS | GOLDEN BATCH TARGET |
|---|---|---|---|---|---|---|---|
| Check_O2_Cyclone_Tower | 0 | 2.35 | 3.5 | 3.38 | 23.17 | Slightly above objective | 2.8–3.3% |
| Check_CO_Cyclone_Tower | 0 | 0.10 | 0.11 | 0.13 | 0.91 | At limit in spikes | <0.12% |
| Check_NOx_Cyclone_Tower | 0 | 365 | 440 | 514 | 2020 | Within constraint | 365–500 |
| Check_NOx_Smoke_Box | 0 | 1 | 181 | 327 | 2123 | High spread | <250 |
| Optical_Pyrometer_Temp._Burning_Zone | 600 | 855 | 913 | 1001 | 1265 | 37°C BELOW minimum | 980–1050°C |
| Material_Temp_Cyclone_A55 | 42 | 855 | 867 | 920 | 1372 | Low end | 880–920°C |
| Cyclone_Gas_Temp._A55 | 164 | 877 | 883 | 912 | 1372 | Within stable | 880–910°C |
| Fan_Speed_5 | 0 | 65.7 | 64.6 | 69.7 | 100 | Within range | 65–68% |
| Precalciner_Fuel_Share | — | — | ~60% | — | — | Within range | 57–62% |
```

---

## ⚡ PART 3a — Golden Batch Visualization Maps
### (Integrated Charts & Interpretations)

```
Continuing the W3 Kiln Optimization Report — Part 3a: GOLDEN BATCH VISUALIZATION.
All derived KPIs already in dataset: Total_Fuel_Flow, Specific_Fuel_Consumption,
Precalciner_Fuel_Share, Main_Fuel_Share — do NOT recreate them.

## REPORT GENERATION MANDATORY INSTRUCTIONS:
- You MUST generate the report sequentially, containing every STEP listed below.
- You MUST use the exact Markdown headings for each step (e.g., `### STEP 12 — Multi-Variable Golden Batch Maps`).
- Do NOT combine steps, do NOT skip any steps, and do NOT output placeholders. Provide full engineering and data-driven explanations for each section.
- You MUST weave the chart tags and their corresponding text interpretations together. Place each chart tag immediately under the heading of the STEP where it is discussed. Follow it immediately with your detailed expert analysis of that chart. DO NOT group all chart tags at the top.

Confirmed data: Mean production=146.71, Q3=162.42, max=182.55 t/h.
Mean SFC=0.094 t/t, target SFC=0.082. Pyrometer mean=913°C, target=1050°C, min=950°C.

---

## STEP 12 — Multi-Variable Golden Batch Maps

Output this parallel coordinate chart for Production, then interpret:
[PARALLEL: Flour_Feed, Main_Mass_Coke_Flow_Rate, Pre-cal_Coke_Flow_Rate, Check_O2_Cyclone_Tower, Check_CO_Cyclone_Tower, Optical_Pyrometer_Temp._Burning_Zone, Fan_Speed_5 | COLOR: Clinker_Production]

Describe the RED lines (production > 162 t/h) in the parallel coordinates:
- What Flour_Feed, O2, CO, Pyrometer, and Fan 5 values characterize highest production?
- Is Pyrometer above or below 950°C in the high-production lines? This is the key question.

Output this parallel coordinate chart for Specific Fuel Consumption (SFC), then interpret:
[PARALLEL: Flour_Feed, Total_Fuel_Flow, Specific_Fuel_Consumption, Check_O2_Cyclone_Tower, Precalciner_Fuel_Share, Optical_Pyrometer_Temp._Burning_Zone, Cyclone_Gas_Temp._A55 | COLOR: Specific_Fuel_Consumption]

Describe the BLUE lines (SFC < 0.082) in the parallel coordinates:
- What Total_Fuel_Flow, Pyrometer, and O2 values give the best fuel efficiency?

Output this parallel coordinate chart for NOx Cyclone Tower, then interpret:
[PARALLEL: Main_Mass_Coke_Flow_Rate, Precalciner_Fuel_Share, Check_O2_Cyclone_Tower, Optical_Pyrometer_Temp._Burning_Zone, Fan_Speed_5, Analyze_O2_in_Smoke_Box | COLOR: Check_NOx_Cyclone_Tower]

Describe the RED lines (NOx > 500) in the parallel coordinates:
- Is high NOx driven by high Pyrometer (thermal NOx) or high O2 (excess air NOx)?

---

## STEP 13 — 3D Golden Batch Clusters

Output this 3D Operating Space scatter chart, then interpret:
[SCATTER3D: X=Check_O2_Cyclone_Tower | Y=Optical_Pyrometer_Temp._Burning_Zone | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]

For 3D Map 1:
- Where is the Golden Batch cluster? (Z > 162, Y > 950°C, X in 2.5-3.3%, color blue)
- Estimate what % of historical data falls in this optimal 3D region.

Output this 3D Fuel Space scatter chart, then interpret:
[SCATTER3D: X=Main_Mass_Coke_Flow_Rate | Y=Pre-cal_Coke_Flow_Rate | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Viridis]

For 3D Map 2:
- Where is the optimal fuel split ridge? (Z > 162, color dark blue/purple)
- What Main/Pre-cal combination sits at the peak production + lowest SFC point?

---

## STEP 14 — Statistical Distributions

Output these two BOX plots, then interpret:
[BOX: Clinker_Production, Flour_Feed, Total_Fuel_Flow, Specific_Fuel_Consumption]
[BOX: Check_O2_Cyclone_Tower, Check_CO_Cyclone_Tower, Optical_Pyrometer_Temp._Burning_Zone, Material_Temp_Cyclone_A55]

Output this HISTOGRAM, then interpret:
[HISTOGRAM: Specific_Fuel_Consumption, Clinker_Production]

Key questions to answer:
1. SFC histogram: single mode or bimodal (efficient vs inefficient)? Where is the split?
2. What % of RUNNING time (excluding 6.5% shutdowns) is production above Q3 (162.42)?
3. How much of the Pyrometer box sits below 950°C (the minimum constraint)?
```

---

## ⚡ PART 3b — Golden Batch Definition + Value Lost
### (Business case — run AFTER Part 3a)

```
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

State the complete operating window as a filled table. Use findings from Parts 1, 2, 3a:

| Variable | Golden Batch Lower | Golden Batch Upper | Current Mean | Gap |
|---|---|---|---|---|
| Clinker_Production | 160 | 182 | 146.71 | +13–35 t/h |
| Flour_Feed | 262 | 275 | 245 | +17–30 t/h |
| Total_Fuel_Flow | 12.0 | 13.5 | 13.71 | −0.2 t/h |
| Specific_Fuel_Consumption | 0.075 | 0.085 | 0.094 | −0.009 to −0.019 t/t |
| Main_Mass_Coke_Flow_Rate | 5.5 | 5.9 | 5.52 | near optimal |
| Pre-cal_Coke_Flow_Rate | 7.5 | 9.0 | 8.19 | near optimal |
| Precalciner_Fuel_Share | 57 | 62 | ~60 | near optimal |
| Check_O2_Cyclone_Tower | 2.5 | 3.3 | 3.5 | slightly above |
| Check_CO_Cyclone_Tower | 0.08 | 0.12 | 0.11 | watch carefully |
| Check_NOx_Cyclone_Tower | 365 | 480 | 440 | within range |
| Optical_Pyrometer_Temp._Burning_Zone | 980 | 1050 | 913 | **+67 to +137°C DEFICIT** |
| Material_Temp_Cyclone_A55 | 880 | 920 | 867 | +13 to +53°C |
| Fan_Speed_5 | 65 | 68 | 64.6 | near optimal |

Update any values based on your analysis from Parts 1–3a.

---

## STEP 16 — VALUE LOST QUANTIFICATION

Calculate and present a professional table. You MUST recalculate all of these numbers dynamically using the actual mean, Q3, and max values from the active dataset (the numbers below are for illustration of the formulas):

**A) Production Opportunity**
- Formula: Gap = (Q3_Production − Mean_Production) × Operating_Hours_per_Year (e.g. 8,120 h/yr adjusting for actual shutdown rate).
- Formula: Max Opportunity = (Max_Production − Mean_Production) × Operating_Hours_per_Year.
- Value calculation: Use $50/ton of clinker to compute conservative and maximum financial values.
- Baseline reference: (162.42 − 146.71) × 8,120 = 127,566 t/yr ($6.4M/yr), Max = (182.55 − 146.71) × 8,120 = 291,002 t/yr ($14.6M/yr).

**B) Fuel Saving Opportunity**
- Formula: SFC Gap = Mean_SFC − Target_SFC.
- Formula: Annual Production = Q3_Production × Operating_Hours_per_Year.
- Formula: Fuel Saved = SFC Gap × Annual Production (tons of petcoke/year).
- Value calculation: Use $120/ton of petcoke to compute financial value.
- Formula: CO2 reduction = Fuel Saved × 3.2 (tons of CO2/year).
- Baseline reference: (0.094 − 0.082) × 1,318,850 = 15,826 t/yr ($1.9M/yr saving).

**C) Environmental Improvement**
- Compute the actual NOx reduction margin (e.g., Mean_NOx to Target_NOx) and the increased headroom against the actual plant constraint.

**D) Sintering Quality Recovery**
- Calculate the potential reduction in quality rejects based on the active dataset's free lime (`W3_Clinker_CaOL` or equivalent) stats. Target a reduction in mean and max free lime (assume a $\ge 30\%$ reduction in rejected batches).

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

List the 5 highest-impact recommendations. For each use:
**REC-N | TITLE | Priority: CRITICAL/HIGH/MEDIUM**
- Evidence: [numbers from statistics and correlations]
- Root Cause: [process engineering mechanism, referencing the LSF saturation or draft scaling]
- Action: [what to change, by how much, and what operational exclusions apply]
- Target: [Golden Batch value / range]
- Value: [$/yr, t/yr, or emission margins]

Structure the recommendations as follows, integrating the operational matrix domain rules:
1. **REC-1 | Burning Zone Sintering Recovery (CRITICAL)**: Action to recover the $37^\circ\text{C}$ deficit in `Optical_Pyrometer_Temp._Burning_Zone`. Note that the $913^\circ\text{C}$ mean is a sensor offset (dust attenuation), but the relative temperature must be increased toward the target ($1050^\circ\text{C}$). Check `W3_Clinker_CaOL` (Free Lime) vs. LSF to ensure the issue is thermal and not high raw-mix LSF (which creates chemical free lime independent of temperature).
2. **REC-2 | Precalciner Fuel Split Optimization (HIGH)**: Adjust the coke fuel split (`Precalciner_Fuel_Share`) toward the $57\text{–}62\%$ target. Optimize the split to balance heat between the calciner and the kiln. Avoid over-firing the calciner, which leads to high tower CO (`Check_CO_Cyclone_Tower`) and thermal inefficiency.
3. **REC-3 | Raw Meal Quality Moduli & Fineness Control (HIGH)**: Control raw meal fineness (flour sieve residue `W3_Flour_#170`) and chemical design (calcium saturation LSF/FSC `W3_Flour_FSC` and `W3_Clinker_FSC`). Since LSF and sieve residue show strong positive correlations with Clinker Free Lime (`W3_Clinker_CaOL`), stabilizing these upstream parameters prevents unburnt lime in clinker.
4. **REC-4 | Cooler Grate 1 Speed Control (MEDIUM)**: Adjust cooler grate speed `Grade_1_Speed` to maintain a stable clinker bed depth, optimizing secondary air temperature and heat recovery, while keeping `Cooler_Inlet_Temperature` within safe design limits.
5. **REC-5 | Centralized Fan Speed & Draft Optimization (MEDIUM)**: Control main process fan speed (`Fan_Speed_5`) to track flour feed rate and maintain the cyclone tower oxygen target (`Check_O2_Cyclone_Tower`) at $3.0\%$ objective, avoiding excess air heat losses.

---

## STEP 18 — Expert Verdict (Plant Manager Memo)

Write a professional 3-paragraph memo to the Plant Manager and Lead Operator:

Para 1 — THE FINDING: The single most important discovery in plain language (the thermal deficit and LSF chemistry constraint).
Para 2 — THE OPPORTUNITY: Total value ($8.1M/yr) and what it requires.
Para 3 — THREE IMMEDIATE ACTIONS the operator can take TODAY (with exact target values and explicit cleaning cycle/sensor exclusions).
```,StartLine:633,TargetContent:
```

---

## Usage Notes

| | Detail |
|---|---|
| **Derived KPIs** | Already created — just load your CSV, process it, and run each part |
| **Run order** | Part 1 → Part 2 → Part 3 |
| **If response cut off** | Say *"Continue from Step [N]"* |
| **Adjust prices** | Replace $50/t clinker and $120/t petcoke with actual plant values |
| **Variable names** | Match exactly to your CSV column headers |
| **Key finding pre-confirmed** | Pyrometer mean (913°C) is below 950°C min constraint — build the report around this |
