# Adana Kiln 4 — OYAK Cement AIPC Process Optimization Report Prompt
## Data-Specific 3-Part AI Prompt Set

This document contains the prompt broken down into a **Prerequisite** and **3 sequential parts** for you to copy and paste into the AI chat interface.

---

## ⚡ PREREQUISITE — CREATE DERIVED KPIs
### (Copy and run this FIRST in your AI chat)

```
Create the following 4 derived KPI variables needed for the Adana kiln optimization report.
Output each as a DERIVED tag in exactly this order:

[DERIVED: Clinker_Production = Raw_Meal_Feeding * 0.65]
[DERIVED: Total_Coal_Flow = Consumption_Hood_Total_Coal + Consumption_Calciner_Total_Coal]
[DERIVED: Total_Fuel_Flow = Total_Coal_Flow + Consumption_Calciner_RDF]
[DERIVED: Specific_Fuel_Consumption = Total_Fuel_Flow / Clinker_Production]

Confirm each was created with a one-line summary:
- Clinker_Production: estimated clinker production using standard 0.65 conversion (mean ~186.02 t/h).
- Total_Coal_Flow: sum of hood and calciner coal consumption (mean ~11.17 t/h).
- Total_Fuel_Flow: sum of coal and RDF fuel flows (mean ~25.70 t/h).
- Specific_Fuel_Consumption: total fuel flow per ton of clinker produced (mean ~0.138 t/t).
```

---

## ⚡ PART 1 — Production & Fuel Efficiency Analysis
### (Copy and run this SECOND in your AI chat, after derived KPIs are created)

```
You are acting as a Master Kiln Operator, Master Process Engineer, and Master Data Scientist with 30 years of cement industry experience. You are preparing Section 1 of a professional Process Optimization Report for Rotary Kiln 4 at the OYAK Cement Adana Plant.

Your analysis must strictly align with the operational guidelines defined in the OYAK Cement AIPC project documentation:
- Priority 3: Clinker Production Rate (tph) (Estimated via Clinker_Production = Raw_Meal_Feeding * 0.65)
- Priority 6: Kiln Torque / Current (Proxy: drive current Current_y)

Relevant Data Statistics for Part 1:
- Raw_Meal_Feeding: mean = 286.18 | Q1 = 297.59 | Q3 = 310.29 | max = 324.03 t/h
- Clinker_Production (Estimated): mean = 186.02 | Q1 = 193.43 | Q3 = 201.69 | max = 210.62 t/h
- Consumption_Hood_Total_Coal: mean = 4.12 | stable 4.09–4.62 | max = 6.32 t/h
- Consumption_Calciner_Total_Coal: mean = 7.05 | stable 6.09–8.52 | max = 13.92 t/h
- Consumption_Calciner_RDF: mean = 14.53 | stable 12.45–19.46 | max = 50.00 t/h
- TSR (Thermal Substitution Rate): mean = 0.28 (28%) | stable 0.24–0.36
- Specific_Fuel_Consumption: mean ~0.138 t/t

Write the first part of the report containing the following exact headings:

### STEP 1 — Executive Summary (Part 1)
Write 5 bullet points covering:
1. Production performance gap: Current mean clinker production (186.02 t/h) vs peak capability (210.62 t/h).
2. Q3 production opportunity: Extra tons per year if the kiln operates at Q3 feed rate instead of mean (assuming ~8,120 operating hours/year).
3. Fuel efficiency status: Total fuel flow at mean conditions (25.70 t/h) and Specific Fuel Consumption (mean 0.138 t/t).
4. Alternative fuel utilization: Current RDF feeding mean (14.53 t/h) and TSR substitution level (28%).
5. Speed-to-Feed synchronization: Explain the near-perfect +0.973 correlation between Kiln_RPM_Actual and Raw_Meal_Feeding and how it maintains stable kiln bed load (AIPC Principle 1).

### STEP 2 — Production & Alternative Fuel Analysis
Produce and interpret the following charts using the active dataset:
- [SCATTER: X=Raw_Meal_Feeding | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]
- [SCATTER: X=Consumption_Calciner_RDF | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]
Evaluate the feed-to-production efficiency corridor and identify if there is RDF over-firing or saturation above 20 t/h.

### STEP 3 — Fuel Efficiency & Operating Zones
Produce and interpret the following charts:
- [SCATTER: X=Clinker_Production | Y=Specific_Fuel_Consumption | COLOR=Secondary_Air_Temperature | SCALE=Viridis]
- [PARALLEL: Raw_Meal_Feeding, Consumption_Hood_Total_Coal, Consumption_Calciner_Total_Coal, Total_Fuel_Flow, Specific_Fuel_Consumption, Clinker_Production | COLOR: Clinker_Production]
- [DUALPLOT: Clinker_Production, Raw_Meal_Feeding | Total_Fuel_Flow]
- [DUALPLOT: Clinker_Production | Specific_Fuel_Consumption]

Divide operation into 4 zones based on mean production (186 t/h) and SFC (0.138 t/t). Define the Golden Batch Zone (Zone A: Production > 200 t/h and SFC < 0.125 t/t) and use the parallel coordinate plot to show the batch range across variables (e.g. Raw_Meal_Feeding, coal split, total fuel, and SFC during the high-production red lines). Analyze the fuel split difference and what combination of hood/calciner coal characterizes the highest-production zones.

### STEP 4 — Production & Fuel split Summary Table
Fill in this table with the actual statistics from the ranges summary sheet:
| Variable | Min | Q1 | Median | Q3 | Max | GOLDEN BATCH TARGET |
|---|---|---|---|---|---|---|
| Clinker_Production | | | | | | >200 t/h |
| Raw_Meal_Feeding | | | | | | 297–310 t/h |
| Consumption_Hood_Total_Coal | | | | | | 4.0–4.5 t/h |
| Consumption_Calciner_Total_Coal | | | | | | 6.0–8.0 t/h |
| Total_Fuel_Flow | | | | | | <24.5 t/h at Q3 prod |
| Specific_Fuel_Consumption | | | | | | <0.125 t/t |
```

---

## ⚡ PART 2 — Sintering, Combustion & Draft System
### (Copy and run this THIRD in your AI chat, after Part 1 is complete)

```
Continuing the Adana Kiln 4 Process Optimization Report — Section 2: Sintering, Combustion & Draft System.
Ensure derived KPIs (Clinker_Production, Total_Fuel_Flow, Specific_Fuel_Consumption) are loaded.

Your analysis must strictly align with the OYAK Cement AIPC principles:
- Principle 2 (O2 Control): O2 downcomer and CO downcomer.
- Principle 3 (Controlled Thermal Balance): Dynamic fuel split instead of constant flow.
- Principle 5 (Draft Fan Check): Capacity increase only if sufficient draft reserve exists.
- Principle 6 (Reference Limits): Limits for quality, emissions, and currents.

Relevant Data Statistics for Part 2:
- Secondary_Air_Temperature: mean = 1018.90°C | stable 1038.64–1119.11°C (Target: 1150°C, Min Constraint: 1050°C)
- O2_(Downcomer): mean = 6.36% | stable 3.04–7.65% (AIPC Target: 3.0%)
- CO_(Downcomer): mean = 453.87 | stable 91.93–517.65 | max = 4999.99 ppm
- NO_(Downcomer): mean = 494.95 | stable 308.39–678.64 | max = 5000.00 ppm
- Speed_(Fan-5) (Exhaust Fan): mean = 82.37% | stable 80.29–87.35%
- Kiln Drive Current (Current_y): mean = 246.23 | stable 232.74–283.81 A
- Clinker C3S XRD Total: mean = 64.00% | stable 62.25–66.60%
- Burner Pipe Air Pressures: Central: 442.30 | Peripheral: 221.46 | Turbulence: 344.69
- C4B Cyclone Temperature (Precalciner exit): mean = 866.13°C

Write Section 2 containing the following exact headings:

### STEP 5 — Sintering Zone Thermal Deficit & Quality
Identify the temperature deficit:
- Mean Secondary Air Temperature (1018.90°C) is **31.10°C below the 1050°C minimum limit**.
Produce and interpret:
- [SCATTER: X=Secondary_Air_Temperature | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]
- [DUALPLOT: Secondary_Air_Temperature, C4B_Cyclone_-_Gas_Temperature_(Outlet) | Clinker_Production]
Explain the chemical and process consequences: Low cooler recovery → poor sintering → lower C3S formation (mean 64.0%) and wasted coal in the main burner (hood coal mean 4.12 t/h). Detail how burner pipe pressures (Central, Peripheral, Turbulence) are calibrated to optimize flame shape.

### STEP 6 — Combustion & Emissions Diagnostic
Produce and interpret:
- [SCATTER: X=O2_(Downcomer) | Y=CO_(Downcomer) | COLOR=Clinker_Production | SCALE=Jet]
- [SCATTER: X=Secondary_Air_Temperature | Y=NO_(Downcomer) | COLOR=O2_(Downcomer) | SCALE=Viridis]
Interpret the downcomer combustion window. Why is O2_(Downcomer) at 6.36% mean representing a significant excess air penalty? Identify the O2 threshold where CO starts spiking above the 300 ppm target.

### STEP 7 — Preheater Draft & Fan Reserve Check
Produce and interpret:
- [SCATTER: X=Speed_(Fan-5) | Y=Clinker_Production | COLOR=O2_(Downcomer) | SCALE=RdBu]
Apply OYAK AIPC Principle 5: The preheater exhaust fan Speed_(Fan-5) averages 82.37%, meaning the kiln has a narrow draft reserve (~17.6% capacity margin). Explain why any capacity increase is constrained by this draft ceiling.

### STEP 8 — Combustion & Sintering Summary Table
Fill in this table with the actual statistics from the ranges summary sheet:
| Variable | Min | Q1 | Median | Q3 | Max | CURRENT STATUS | GOLDEN BATCH TARGET |
|---|---|---|---|---|---|---|---|
| O2_(Downcomer) | | | | | | Excess air present | 3.0–4.5% |
| CO_(Downcomer) | | | | | | Spike risk | <300 ppm |
| NO_(Downcomer) | | | | | | Within constraint | 300–600 ppm |
| Secondary_Air_Temperature | | | | | | 31.1°C BELOW minimum | 1080–1150°C |
| C4B_Cyclone_-_Gas_Temperature_(Outlet)| | | | | | Normal | 880–920°C |
| Kiln_RPM_Actual | | | | | | Synchronized | 2.8–3.1 rpm |
| Speed_(Fan-5) | | | | | | High load | 80–85% |
```

---

## ⚡ PART 3 — Business Case, Recommendations & Expert Verdict
### (Copy and run this FOURTH in your AI chat, after Part 2 is complete)

```
Continuing the Adana Kiln 4 Process Optimization Report — Section 3: Business Case, Recommendations & Verdict.
This section integrates multi-variable diagnostic visualization to establish the Golden Batch signature and calculate the financial opportunities.

Relevant Data Statistics for Part 3:
- Mean production: 186.02 t/h | Q3: 201.69 | Max: 210.62 t/h
- Operating hours/year: 8,120 h/yr
- Mean SFC: 0.1381 t/t | Target SFC: 0.1250 t/t
- Secondary Air Temp mean: 1018.90°C | Target: 1150°C | Min: 1050°C
- TSR mean: 27.6% | Target: 35.0%
- O2_(Downcomer) mean: 6.36% | Target: 3.0%

Write Section 3 containing the following exact headings:

### STEP 9 — Golden Batch Multi-Variable Visualizations
Produce and interpret:
- [PARALLEL: Raw_Meal_Feeding, Consumption_Hood_Total_Coal, Consumption_Calciner_Total_Coal, O2_(Downcomer), Secondary_Air_Temperature, Speed_(Fan-5) | COLOR: Clinker_Production]
- [SCATTER3D: X=O2_(Downcomer) | Y=Secondary_Air_Temperature | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]
- [SCATTER3D: X=Consumption_Hood_Total_Coal | Y=Consumption_Calciner_Total_Coal | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Viridis]
- [BOX: Clinker_Production, Raw_Meal_Feeding, Total_Fuel_Flow, Specific_Fuel_Consumption]
- [HISTOGRAM: Specific_Fuel_Consumption, Clinker_Production]

Interpret these multi-variable plots to identify the signature of the Golden Batch (production > 200 t/h, SFC < 0.125 t/t). Focus on:
- Where the high-production red lines cluster in the parallel coordinate chart.
- The location of the efficient cluster in the 3D Operating Space and Fuel Split Space.
- The shape and peaks of the SFC histogram.

### STEP 10 — Golden Batch Complete Definition
State the complete operating window as a filled table:
| Variable | Golden Batch Lower | Golden Batch Upper | Current Mean | Gap |
|---|---|---|---|---|
| Clinker_Production | 195.00 | 210.00 | 186.02 | +9.0–24.0 t/h |
| Raw_Meal_Feeding | 300.00 | 323.00 | 286.18 | +13.8–36.8 t/h |
| Total_Fuel_Flow | 22.00 | 24.50 | 25.70 | −1.20 t/h |
| Specific_Fuel_Consumption | 0.110 | 0.125 | 0.138 | −0.013 to −0.028 t/t |
| Consumption_Hood_Total_Coal | 3.80 | 4.50 | 4.12 | near optimal |
| Consumption_Calciner_Total_Coal | 6.00 | 8.00 | 7.05 | near optimal |
| Consumption_Calciner_RDF | 15.00 | 22.00 | 14.53 | +0.47 to +7.47 t/h |
| O2_(Downcomer) | 3.00 | 4.50 | 6.36 | −1.86 to −3.36% (Excess) |
| CO_(Downcomer) | 80.00 | 300.00 | 453.87 | −153.87 ppm (Spikes) |
| NO_(Downcomer) | 300.00 | 600.00 | 494.95 | within range |
| Secondary_Air_Temperature | 1080.00 | 1150.00 | 1018.90 | **+61.1 to +131.1°C DEFICIT** |
| C4B_Cyclone_-_Gas_Temperature_(Outlet)| 880.00 | 920.00 | 866.13 | +13.8 to +53.8°C |
| Speed_(Fan-5) | 80.00 | 85.00 | 82.37 | near optimal |

### STEP 11 — VALUE LOST QUANTIFICATION
Recalculate all numbers dynamically using the statistics above:
- **Production Opportunity**: Gap = (Q3_Production − Mean_Production) × 8,120 hours/year. Calculate financial value at **$50/ton** of clinker (Conservative: 127,240 t/yr worth $6.36M/yr; Max: 199,752 t/yr worth $9.99M/yr).
- **Fuel Saving Opportunity**: Saved Fuel = (Mean_SFC − Target_SFC) × Q3_Annual_Production. Target SFC is 0.1250 t/t. Calculate savings at **$120/ton** of fuel (21,454 t/yr worth $2.57M/yr).
- Summarize total conservative value: **$8.93M/year**.

Present this completed summary table:
| Opportunity | Annual Quantity | Financial Value |
|---|---|---|
| Production (conservative) | [Calculated t/yr] | [Calculated $ value at $50/t] |
| Production (maximum potential) | [Calculated t/yr] | [Calculated $ value at $50/t] |
| Fuel saving | [Calculated t/yr] | [Calculated $ value at $120/t] |
| Quality & C3S improvement | Better mineralogy | Avoided quality adjustments |
| **TOTAL (conservative)** | | **[Sum of Conservative Production + Fuel Saving]** |

### STEP 12 — Actionable Recommendations (Top 5 Priorities)
List 5 prioritized recommendations using the format: **REC-N | TITLE | Priority: CRITICAL/HIGH/MEDIUM**
- **REC-1 | Cooler Bed Depth & Secondary Air Sintering Recovery (CRITICAL)**: Action to recover the 31.1°C deficit in Secondary_Air_Temperature to improve clinker C3S mineral formation.
- **REC-2 | Calciner RDF & Substitution Optimization (HIGH)**: Increase calciner RDF feeding to substitute coal while keeping downcomer CO below 300 ppm.
- **REC-3 | Stable Bed & RPM Speed-to-Feed Synchronization (HIGH)**: Synchronize Kiln_RPM_Actual tracking Raw_Meal_Feeding to ensure a stable fill degree (AIPC Principle 1).
- **REC-4 | Preheater Fan Speed & Excess Air Draft Control (MEDIUM)**: Adjust Speed_(Fan-5) to bring downcomer O2 closer to the 3.0% target (mean is currently 6.36%).
- **REC-5 | Primary Air & Burner Pipe Calibration (MEDIUM)**: Optimize central/peripheral/turbulence air pressures to shape the flame.

### STEP 13 — Expert Verdict (Plant Manager Memo)
Write a professional 3-paragraph memo to the Plant Manager:
- Para 1: Identify the main issue (cooler thermal deficit & excess air draft loss, causing low C3S quality and high SFC).
- Para 2: State the financial opportunity ($8.93M/year).
- Para 3: Give 3 immediate actions for the operator today (cooling speed optimization, RDF split adjustment, O2 draft reduction target).
```
