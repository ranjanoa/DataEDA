### Run this FIRST in the AI chat, before generating the slides

```
Create the following 4 derived KPI variables needed for the Adana kiln optimization presentation.
Output each as a DERIVED tag in exactly this order (order matters):

[DERIVED: Total_Fuel_Flow = Consumption_Hood_Total_Coal + Consumption_Calciner_Total_Coal + Consumption_Calciner_RDF]
[DERIVED: Specific_Fuel_Consumption = Total_Fuel_Flow / Clinker_Production]
[DERIVED: Precalciner_Fuel_Share = (Consumption_Calciner_Total_Coal + Consumption_Calciner_RDF) / Total_Fuel_Flow]
[DERIVED: Main_Fuel_Share = Consumption_Hood_Total_Coal / Total_Fuel_Flow]

Confirm each was created.
```

---

## ⚡ SLIDE DECK GENERATION PROMPT

Copy and paste the below text into the AI chat to generate the presentation:

```
You are a Senior Process Engineer with 30 years of hands-on expertise in the cement industry and Artificial Intelligence Process Control (AIPC). 
Your task is to create a highly professional, data-oriented executive slide deck (Maximum 20 Slides) analyzing the Adana Plant Kiln dataset. 
The presentation must identify the "Golden Batch" and highlight process issues strictly through the exact priority ranking and AIPC control principles of the Adana plant.

### PARAMETER PRIORITY RANKING (IN ORDER):
1. **Free Lime (`Ck_S.CaO`)**: Primary indicator of quality.
2. **Burning Zone Temperature (`Secondary_Air_Temperature` proxy)**: Directly affects heat input and mineral formation.
3. **Clinker Production Rate (`Clinker_Production`)**: Determines system load and balances.
4. **Tertiary Air / Heat Recuperation (`Secondary_Air_Temperature` proxy)**: Affects cooler efficiency and calciner stability.
5. **Primary Air Pressure (`Primary_Air_Pressure`)**: Affects flame length, mixing, and NOx/CO.
6. **Kiln Torque/Current (`Current_y`)**: Indicates material load and flow regime.

### ADANA AIPC CONTROL PRINCIPLES TO EVALUATE:
1. **Stable Material Bed:** Stable load without fluctuations (`Current_y`).
2. **Stable Oxygen Level:** O2 is fundamental for combustion, CO, NOx, and energy (`O2_(Downcomer)`, `CO_(Downcomer)`).
3. **Controlled Thermal Balance:** Balance heat input to production (`Specific_Fuel_Consumption`).
4. **Feed Continuity:** Gradual changes, stable production (`Raw_Meal_Feeding`).
5. **Sufficient Draft Reserve:** Do not increase capacity if ID Fan is inadequate (`Speed_(Fan-5)`).
6. **Reference-Based Actions:** Decisions rely on Free Lime, Temperatures, O2, Torque.

### INSTRUCTIONS FOR THE DECK:
- Output exactly 20 slides using markdown headers (e.g., `## Slide 1: Title`). Use `---` between slides.
- Do NOT generate [DERIVED: ...] tags, those are already processed.
- You MUST use the provided `[CHART_TAGS]` exactly as written to dynamically render the data.
- **CRITICAL ANALYSIS REQUIREMENT:** As a 30-year veteran, you MUST write an explicit, highly detailed process engineering analysis for EVERY single chart you generate. Do not just leave placeholders like "- Analyze the Golden Batch". You must look at the provided JSON Range Summary and Correlation Matrix and explicitly state WHAT is physically happening in the kiln for that plot. (e.g., "The data shows O2 mean at X%, indicating false air ingress which is correlating negatively with production..."). 

---

## Slide 1: Title Slide
- **Title:** Adana Plant AIPC Optimization & Golden Batch Analysis
- **Subtitle:** Parameter Priority Review & Process Diagnostic
- **Presenter:** Senior Process Engineer

---

## Slide 2: Executive Summary & Estimator Hierarchy
- Summarize the Estimator Priority Ranking (Free Lime > Combustion > Calcination > Kiln Temp > Efficiency > Cooling > Capacity).
- State the baseline operational stats and identify the top 3 deviations from Golden Batch targets.

---

## Slide 3: Priority 1 - Free Lime (Primary Quality Indicator)
- **Objective:** Evaluate final burning quality (`Ck_S.CaO`).
- **Chart:** 
[HISTOGRAM: Ck_S.CaO, C3S_XRD_Total]
- **Analysis:** Identify if Free Lime is too high (underburning risk) or too low (overburning/energy loss risk). Define the Golden Batch target.

---

## Slide 4: Priority 1 & 2 - Free Lime vs Burning Zone Temperature
- **Objective:** How Burning Zone Temp (using Secondary Air as proxy) affects mineral formation.
- **Chart:** 
[SCATTER: X=Secondary_Air_Temperature | Y=Ck_S.CaO | COLOR=Clinker_Production | SCALE=Jet]
- **Analysis:** Identify the temperature threshold required to stabilize Free Lime without wasting fuel.

---

## Slide 5: Priority 3 - Clinker Production Rate (System Load)
- **Objective:** All heat, air, and draft balances tie back to production stability.
- **Chart:** 
[DUALPLOT: Clinker_Production | Specific_Fuel_Consumption]
- **Analysis:** Assess the stability of production. Does Specific Fuel Consumption spike when production drops?

---

## Slide 6: Priority 4 - Heat Recuperation & Calciner Stability
- **Objective:** Evaluate cooler efficiency and its impact on the calciner.
- **Chart:** 
[SCATTER: X=Secondary_Air_Temperature | Y=Consumption_Calciner_Total_Coal | COLOR=Specific_Fuel_Consumption | SCALE=Hot]
- **Analysis:** Assess if high recuperation temperatures lower the necessary calciner fuel rate.

---

## Slide 7: Priority 5 - Primary Air Pressure & Flame Quality
- **Objective:** Primary air affects mixing, flame length, and NOx/CO.
- **Chart:** 
[SCATTER: X=Primary_Air_Pressure | Y=CO_(Downcomer) | COLOR=O2_(Downcomer) | SCALE=RdBu]
- **Analysis:** Determine the optimal Primary Air Pressure range that minimizes CO formation while keeping O2 stable.

---

## Slide 8: Principle 1 - Kiln Torque (Stable Material Bed)
- **Objective:** Torque indicates material load and coating/snowman tendency.
- **Charts:** 
[SCATTER: X=Raw_Meal_Feeding | Y=Current_y | COLOR=Clinker_Production | SCALE=Jet]
[PARALLEL: Raw_Meal_Feeding, Current_y, Clinker_Production | COLOR: Current_y]
- **Analysis:** Identify the efficient corridor for feed vs torque. Assess torque variance as an indicator of bed instability.

---

## Slide 9: Principle 2 - Stable Oxygen & Combustion Master Map
- **Objective:** O2 is fundamental for combustion quality, NOx, and energy.
- **Charts:** 
[SCATTER: X=O2_(Downcomer) | Y=CO_(Downcomer) | COLOR=NO_(Downcomer) | SCALE=Jet]
[PARALLEL: Primary_Air_Pressure, O2_(Downcomer), CO_(Downcomer), NO_(Downcomer) | COLOR: O2_(Downcomer)]
- **Analysis:** Define the Golden Batch O2 range. Identify where CO spikes and NOx drops occur due to unstable combustion.

---

## Slide 10: Principle 3 - Controlled Thermal Balance
- **Objective:** Balance heat input according to production.
- **Charts:** 
[SCATTER: X=Total_Fuel_Flow | Y=Specific_Fuel_Consumption | COLOR=Clinker_Production | SCALE=Viridis]
[PARALLEL: Total_Fuel_Flow, Specific_Fuel_Consumption, Secondary_Air_Temperature, Clinker_Production | COLOR: Specific_Fuel_Consumption]
- **Analysis:** Map the Golden Batch zone: Maximum Production with minimum SFC. 

---

## Slide 11: Principle 3 - Precalciner Combustion Efficiency
- **Objective:** Optimize fuel share and alternative fuels.
- **Chart:** 
[SCATTER3D: X=Consumption_Calciner_Total_Coal | Y=Consumption_Calciner_RDF | Z=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]
- **Analysis:** Evaluate if the calciner efficiently burns RDF. Identify the optimal Precalciner Fuel Share.

---

## Slide 12: Principle 4 - Feed Continuity
- **Objective:** Fluctuations in kiln bed must not be created by sudden feed changes.
- **Charts:** 
[BOX: Raw_Meal_Feeding, Clinker_Production]
[PARALLEL: Raw_Meal_Feeding, Gas_Temperature_(Before_Calciner)_x, Clinker_Production | COLOR: Raw_Meal_Feeding]
- **Analysis:** Evaluate the variance in Raw Meal Feeding. Are capacity changes gradual or sudden?

---

## Slide 13: Principle 5 - Draft Reserve Capacity
- **Objective:** AIPC must not increase capacity if ID fan capacity is inadequate.
- **Charts:** 
[SCATTER: X=Speed_(Fan-5) | Y=O2_(Downcomer) | COLOR=Clinker_Production | SCALE=RdBu]
[PARALLEL: Speed_(Fan-5), O2_(Downcomer), Specific_Fuel_Consumption, Clinker_Production | COLOR: Speed_(Fan-5)]
- **Analysis:** Identify if the fan speed hits a ceiling. Is the fan maxed out just to pull excess false air?

---

## Slide 14: Principle 6 - Quality Reference Control & Thermal Stability
- **Objective:** Evaluate preheater thermal stability and quality references.
- **Charts:** 
[SCATTER: X=Gas_Temperature_(Before_Calciner)_x | Y=Clinker_Production | COLOR=Specific_Fuel_Consumption | SCALE=Jet]
[PARALLEL: Ck_S.CaO, Secondary_Air_Temperature, C3S_XRD_Total, Clinker_Production | COLOR: Ck_S.CaO]
- **Analysis:** Determine the optimal temperature entering the calciner for maximum thermal efficiency and Free Lime stability.

---

## Slide 15: Golden Batch Multi-Variable Map (Quality & Production)
- **Chart:** 
[PARALLEL: Raw_Meal_Feeding, Current_y, Secondary_Air_Temperature, Ck_S.CaO, C3S_XRD_Total, Clinker_Production | COLOR: Clinker_Production]
- **Analysis:** Trace the RED lines (Highest Production). Read explicitly the Golden Batch values for Feed, Torque, Temp, and Lime.

---

## Slide 16: Golden Batch Multi-Variable Map (Combustion & Efficiency)
- **Chart:** 
[PARALLEL: Speed_(Fan-5), Primary_Air_Pressure, O2_(Downcomer), CO_(Downcomer), NO_(Downcomer), Specific_Fuel_Consumption | COLOR: Specific_Fuel_Consumption]
- **Analysis:** Trace the pathways that lead to optimal combustion (lowest SFC) without causing CO/NOx spikes.

---

## Slide 17: Process Issue Identification Summary
- Synthesize findings from Quality, Torque, Combustion, and Draft.
- Detail the risk of overburning/underburning based on the current operational limits.
- State the impact of false air and combustion inefficiencies on the capacity margin.

---

## Slide 18: The Golden Batch Definition
- **Objective:** State the complete operating window based on priority variables.
- **Table:** Present the exact Golden Batch ranges for: `Ck_S.CaO`, `Secondary_Air_Temperature`, `Clinker_Production`, `Primary_Air_Pressure`, `Current_y`, `O2_(Downcomer)`, `Total_Fuel_Flow`, and `Specific_Fuel_Consumption`. Include Current Mean and the required Gap to target.

---

## Slide 19: Value Lost Quantification
- **Objective:** Calculate the financial impact of deviations from the Golden Batch.
- **A) Production Opportunity**: Gap = (Q3_Production (181.42) - Mean_Production (164.07)) * 8120 hrs. Value at $50/ton.
- **B) Fuel Saving Opportunity**: SFC Gap = Mean_SFC (0.156) - Target_SFC (0.145). Annual Prod = Q3 * 8120. Fuel Saved = SFC Gap * Annual Prod. Value at $120/ton. CO2 reduction = Fuel Saved * 3.2.
- **Table:** Present Annual Quantity and Financial Value for Production, Fuel, and CO2.

---

## Slide 20: Action Plan & Conclusion
- **Action Plan:** Outline exactly how AIPC should strictly enforce the operating guidelines based on the Reference Values (e.g., locking feed if draft reserve is < 5%).
- **Conclusion:** Final statement on the financial benefits of operating strictly within the identified Golden Batch parameters.
```
