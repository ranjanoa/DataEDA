# Adana Kiln 4 — OYAK Cement AIPC Process Optimization
## Presentation Summary & Slide Deck Draft

This document outlines the slide deck structure for presenting the Kiln 4 Process Optimization Report to the Adana Plant Manager and Lead Process Engineers. It directly connects the historical dataset statistics to the OYAK Cement AIPC design parameters and principles.

---

### 🖥️ Slide 1: Title & Presentation Objective
* **Slide Title**: Process Optimization & AIPC Performance Audit (Rotary Kiln 4)
* **Subtitle**: Validating AIPC Operating Principles against Historical Plant Data
* **Slide Bullet Points**:
  * **Objective**: Audit historical Kiln 4 operation to identify production gaps, thermal losses, and fuel efficiency opportunities.
  * **Methodology**: Analysis of 72,291 data rows (July 2025 – March 2026) compared to OYAK Cement AIPC project specifications.
  * **Focus**: Sintering zone heat recovery, preheater draft reserves, and alternative fuel (RDF) substitution margins.

---

### 🖥️ Slide 2: Operational Mappings (PDF Guidelines vs. Data Sensors)
* **Slide Title**: Mapping OYAK AIPC Design Guidelines to Data Variables
* **Slide Bullet Points**:
  * **Sintering Quality (Priority 1)**: Assessed using **`C3S_XRD_Total`** (mean 64.0%) as the primary clinker mineralogy proxy.
  * **Sintering Heat (Priority 2 & 4)**: Monitored via **`Secondary_Air_Temperature`** (mean 1018.9°C) representing cooler recovery back to the kiln.
  * **Combustion Efficiency (Priority 5)**: Audited using **`O2_(Downcomer)`** (mean 6.36%) and **`CO_(Downcomer)`** (mean 453.9 ppm).
  * **Kiln Load & Flow (Priority 6)**: Proxied by drive motor current **`Current_y`** (mean 246.2 A).
* **PDF Link**: Verifies the PDF's 6 operational priorities by linking raw process sensors to clinker quality and thermal balance.

---

### 🖥️ Slide 3: Production Performance & RPM Synchronization
* **Slide Title**: Production Capability Gap & Stable Bed Load Control
* **Slide Bullet Points**:
  * **Production Status**: Mean clinker production is **186.02 t/h** vs peak achieved rate of **210.62 t/h** (Gap = 24.60 t/h).
  * **AIPC Principle 1 (Stable Bed)**: Kiln speed tracks feed rate with a near-perfect correlation (**`Kiln_RPM_Actual` vs `Raw_Meal_Feeding` = +0.973**).
  * **Engineering Benefit**: Constant fill degree is successfully maintained, preventing material bed surges.
* **Visual Chart Recommendation**: 2D Scatter Plot `Raw_Meal_Feeding` vs `Clinker_Production` (colored by Specific Fuel Consumption).

---

### 🖥️ Slide 4: Sintering Zone Heat Deficit & C3S Quality Loss
* **Slide Title**: Sintering Zone Deficit — Operating Below Design Limits
* **Slide Bullet Points**:
  * **Thermal Deficit**: Mean Secondary Air Temperature (**1018.90°C**) is **31.10°C below the 1050°C minimum constraint** (Target: 1150°C).
  * **Quality Impact**: Lower secondary air heat recovery reduces sintering zone temperature, limiting tricalcium silicate formation (**C3S mean is 64.0%** vs target >66.0%).
  * **Fuel Cost**: Cooler fails to return heat to primary air, forcing higher coal consumption at the main burner (`Consumption_Hood_Total_Coal` mean 4.12 t/h).
* **Visual Chart Recommendation**: 2D Scatter Plot `Secondary_Air_Temperature` vs `Clinker_Production` (colored by SFC).

---

### 🖥️ Slide 5: Combustion Diagnostics & Downcomer Excess Air
* **Slide Title**: Draft System Losses — High Downcomer Oxygen Carryover
* **Slide Bullet Points**:
  * **Excess Air Penalty**: Mean downcomer oxygen (**`O2_(Downcomer)`**) is **6.36% vs the 3.0% AIPC objective**.
  * **Energy Impact**: Excess air acts as a heat sink, carrying thermal energy out of the preheater and increasing Specific Fuel Consumption.
  * **CO Spike Risk**: Downcomer CO (**`CO_(Downcomer)`**) averages **453.87 ppm**; CO spikes begin increasing rapidly when downcomer O2 drops below 3.0%.
* **Visual Chart Recommendation**: 2D Scatter Plot `O2_(Downcomer)` vs `CO_(Downcomer)` (colored by Production).

---

### 🖥️ Slide 6: Preheater Fan Capacity & Draft Reserves
* **Slide Title**: Capacity Constraints — Preheater Draft Fan Reserve Ceiling
* **Slide Bullet Points**:
  * **Draft Status**: Preheater exhaust fan **`Speed_(Fan-5)`** averages **82.37%** (Q3 at 87.35%).
  * **AIPC Principle 5 (Capacity Restriction)**: Do not increase feed capacity if ID fan capacity is tight.
  * **Critical Bottleneck**: Kiln 4 has a narrow **17.6% draft reserve**. Feed increases toward 324 t/h are strictly limited by this fan ceiling.
* **Visual Chart Recommendation**: 2D Scatter Plot `Speed_(Fan-5)` vs `Clinker_Production` (colored by `O2_(Downcomer)`).

---

### 🖥️ Slide 7: Business Case — Value Lost Summary
* **Slide Title**: Quantifying the Financial Value Opportunity
* **Slide Bullet Points**:
  * **Production Opportunity ($6.36M/yr)**: Increasing mean production (186.02 t/h) to Q3 stable performance (201.69 t/h) yields **127,240 extra tons/year** (at $50/t).
  * **Fuel Savings ($2.57M/yr)**: Reducing Specific Fuel Consumption from 0.1381 to 0.1250 t/t saves **21,454 tons of fuel/year** (at $120/t).
  * **Total Conservative Opportunity**: **$8.93 Million / Year**.

| Opportunity Area | Annual Quantity | Financial Value (USD) |
| :--- | :--- | :--- |
| **Production Increase (Conservative)** | +127,240 tons clinker / yr | **$6,362,000 / yr** (at $50/t) |
| **Production Increase (Maximum)** | +199,752 tons clinker / yr | **$9,987,600 / yr** (at $50/t) |
| **Fuel Savings (SFC Reduction)** | −21,454 tons fuel / yr | **$2,574,480 / yr** (at $120/t) |
| **Sintering Quality Improvement** | Avoided C3S adjustments | Reduced clinker rejects |
| **TOTAL CONSERVATIVE VALUE** | | **$8,936,480 / Year** |

---

### 🖥️ Slide 8: Actionable AIPC Recommendations (Prioritized)
* **Slide Title**: Top 5 Actionable Plant Decisions
* **Slide Bullet Points**:
  * **REC-1 | Sintering Thermal Recovery (CRITICAL)**: Adjust cooler grate speed (`Cooler_Speed`) to stabilize bed depth, recovering the **31.10°C secondary air temperature deficit** to improve clinker C3S quality.
  * **REC-2 | Calciner RDF Alternative Fuel Substitution (HIGH)**: Push calciner RDF consumption towards the **15–22 t/h target window** (TSR target 32–40%) to substitute coal, while ensuring CO remains below the 300 ppm spike threshold.
  * **REC-3 | Speed-to-Feed Synchronization (HIGH)**: Maintain strict synchronization of `Kiln_RPM_Actual` tracking `Raw_Meal_Feeding` to preserve stable bed dynamics (**AIPC Principle 1**).
  * **REC-4 | Preheater Fan Speed & Excess Air Draft Control (MEDIUM)**: Adjust preheater exhaust fan `Speed_(Fan-5)` to bring downcomer O2 closer to the 3.0% target (currently running high at 6.36%).
  * **REC-5 | Burner Pipe Air Pressure Optimization (MEDIUM)**: Recalibrate central, peripheral, and turbulence pressures to optimize flame shape and control downcomer NOx emissions.
