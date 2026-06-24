# W3 Kiln — Parallel Coordinate Plots Generation Prompt
### Run the Prerequisite FIRST, then copy the prompt block below to generate and export the parallel plots.

---

## ✅ PREREQUISITE — Create Derived KPI Variables
### (Run this first if you haven't already in this session)

```
Create the following 4 derived KPI variables:
[DERIVED: Total_Fuel_Flow = Coke_Flow_Rate_Torch + Pre-cal_Coke_Flow_Rate]
[DERIVED: Specific_Fuel_Consumption = Total_Fuel_Flow / Clinker_Production]
[DERIVED: Precalciner_Fuel_Share = Pre-cal_Coke_Flow_Rate / Total_Fuel_Flow]
[DERIVED: Main_Fuel_Share = Coke_Flow_Rate_Torch / Total_Fuel_Flow]
```

---

## 📊 Prompt to Render Parallel Plots:

```markdown
You are a Process Optimization Assistant. I need to export the four key parallel coordinates plots for my report. 
Please **ONLY** output the following four parallel coordinate chart tags and a single sentence explaining the process signature of each. 
Do **NOT** write any other summaries, text, tables, or recommendations.

[PARALLEL: Flour_Flow_Rate_Oven, Coke_Flow_Rate_Torch, Pre-cal_Coke_Flow_Rate, Total_Fuel_Flow, Specific_Fuel_Consumption, Clinker_Production | COLOR: Clinker_Production]
*This chart maps the fuel efficiency split signature across production bands.*

[PARALLEL: Flour_Flow_Rate_Oven, Coke_Flow_Rate_Torch, Pre-cal_Coke_Flow_Rate, Check_O2_Cyclone_Tower, Check_CO_Cyclone_Tower, Optical_Pyrometer_Temp._Burning_Zone, Oven_Fan_Speed | COLOR: Clinker_Production]
*This chart isolates the draft and thermal profiles during peak production periods.*

[PARALLEL: Flour_Flow_Rate_Oven, Total_Fuel_Flow, Specific_Fuel_Consumption, Check_O2_Cyclone_Tower, Precalciner_Fuel_Share, Optical_Pyrometer_Temp._Burning_Zone, Cyclone_Gas_Temp._A55 | COLOR: Specific_Fuel_Consumption]
*This chart maps the operating parameters associated with optimal Specific Fuel Consumption (SFC).*

[PARALLEL: Coke_Flow_Rate_Torch, Precalciner_Fuel_Share, Check_O2_Cyclone_Tower, Optical_Pyrometer_Temp._Burning_Zone, Oven_Fan_Speed, Analyze_O2_in_Smoke_Box | COLOR: Check_NOx_Cyclone_Tower]
*This chart highlights the combustion and emission drivers for cyclone tower NOx.*
```

---

### How to Export to HTML:
1. Paste the prompt above into the **Cognitive Intelligence Module (AI Box)** on the dashboard and click **Generate**.
2. Once the AI finishes rendering, a green **🌐 Export Charts HTML** button will appear in the controls area.
3. Click the **🌐 Export Charts HTML** button to instantly download all generated plots as standalone interactive HTML files.
4. *(Alternative)*: You can still hover over any individual chart and click the **Export HTML** icon (the document/page icon) in the chart's top-right hover menu to export that specific chart.

