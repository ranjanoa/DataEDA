# Data Analysis Report: Bursa_Cimento_with_lab.csv

This document provides a comprehensive summary of the dataset `Bursa_Cimento_with_lab.csv` which compiles high-frequency sensor measurements and hourly laboratory results.

## 1. General Dataset Structure
* **Total Rows**: 4,928,874
* **Total Columns / Variables**: 31
  * `1` Timestamp column (`Timestamp`)
  * `28` High-frequency sensor tag variables
  * `2` Lab variables (`C3S` for Alite and `SCaO` for Free Lime)
* **Sensor Sampling Rate**: **1 second** (exactly 1 Hz). The time delta between consecutive timestamps is consistently exactly 1 second for the entire dataset.

## 2. Duration & Coverage
* **Start Timestamp**: 2026-01-28 16:51:31
* **End Timestamp**: 2026-03-26 17:59:24
* **Total Duration**: 57 days, 1 hour, 7 minutes, and 53 seconds (approx. **1,369.13 hours** or **57.05 days**).

## 3. Kiln Feed Flow Rate Statistics (`351GRP3_FZ1`)
In the CSV file, this column is named **`351GRP3_FZ1`** (corresponding to `351GRP3/FZ1 kiln feed`).
* **Zero Values**: **3,042,156 times** (`61.72%` of the total rows). This suggests that the kiln feed was off/idle for the majority of the duration.
* **Non-Zero Values**: 1,751,333 times (`35.53%` of the total rows)
* **Missing/NaN Values**: 135,385 times (`2.75%` of the total rows). Note that this `2.75%` missing rate is uniform across all 28 sensor columns, indicating a temporary data logging outage during the 57-day window.
* **Key Statistics**:
  * Minimum value: `0.00`
  * Maximum value: `381.96`
  * Mean: `125.27`

## 4. Lab Variables & Alignment Method
* **Lab Variables**:
  * **`C3S` (Alite)**: Represents Alite quality from `POLAB_CLK4_C3S_FIRST_VAL.xlsx`.
  * **`SCaO` (Free Lime)**: Represents Free Lime quality from `POLAB_CLK4_SCAO_FIRST_VAL.xlsx`.
* **Original Sampling Rate**: **Hourly** (every 1 hour).
  * Unique lab records: `6,349` samples.
  * Median interval between successive samples: **1 hour** (`0 days 01:00:00`). 
  * Maximum gap between samples: `2 days, 18 hours` (e.g., weekend/shutdown periods).
* **Fill / Alignment Method**: **Nearest-Neighbor Matching**.
  * The lab data was aligned with the high-frequency (1-second) sensor data using a `pd.merge_asof(..., direction='nearest')` join.
  * This matches each high-frequency (1-second) sensor timestamp with the temporally closest hourly lab measurement.
  * Consequently, there are **0% null values** in the final `C3S` and `SCaO` columns in the merged CSV.

## 5. Active Feed Dataset (Bursa_Cimento_with_lab_filtered.csv)
For operational modeling and machine learning, a filtered version of the dataset has been generated. This subset restricts rows only to active kiln feed conditions up to February 20th, 2026.
* **Filename**: [Bursa_Cimento_with_lab_filtered.csv](file:///c:/Users/z004n00r/Documents/AI%20sales/AG%20PROJECTS/EDA%20MERGE/Bursa_Cimento_with_lab_filtered.csv)
* **Filtering Condition**: `351GRP3_FZ1 > 0` and `Timestamp < '2026-02-21'` (until 20th Feb 2026 only)
* **Total Rows**: `1,728,740` rows (retains `35.07%` of the original dataset; discards the `61.72%` inactive/zero values, the `2.75%` missing/NaN sensor timestamps, and records after February 20th, 2026).
* **Date Range**: `2026-01-30 06:27:56` to `2026-02-20 04:38:44`
* **File Size**: `799.5 MB` (reduced from `1.98 GB` to optimize memory usage during subsequent analysis/modeling).

## 6. Detailed Column-by-Column Statistics

| Column Name | Type | Nulls % | Zeros % | Min Value | Max Value | Mean Value | Description / Characterization |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Timestamp** | object | 0.00% | N/A |        N/A |        N/A |        N/A | High-resolution time-axis (1-second intervals) |
| **331FN100PN01_CO** | float | 2.75% | 47.32% |       0.00 |       4.83 |       0.06 | Mostly zero or near-zero values |
| **331FN100PN01_O** | float | 2.75% | 4.25% |       0.00 |      24.15 |      13.74 | Oxygen levels; mean around 13.74% |
| **331FN100_PZ1** | float | 2.75% | 0.00% |      -5.00 |       4.21 |      -3.17 | Negative pressure indicator |
| **351GRP3_FZ1** | float | 2.75% | 61.72% |       0.00 |     381.96 |     125.27 | Kiln Feed Flow Rate |
| **421CI400PN01_CO** | float | 2.75% | 66.36% |       0.00 |       4.83 |       0.00 | Carbon monoxide levels; primarily zero |
| **421CI400PN01_O** | float | 2.75% | 4.17% |       0.00 |      21.42 |      14.19 | Oxygen levels |
| **421CN110_N04P01** | float | 2.75% | 4.76% |     -46.98 |       0.00 |     -13.64 | Negative pressure |
| **421CN210_N04P01** | float | 2.75% | 4.69% |     -45.52 |       0.00 |     -13.50 | Negative pressure |
| **421CN250_N01T01** | float | 2.75% | 0.00% |     -10.00 |    1200.00 |     363.34 | Temperature (highly dynamic, peak at 1200°C) |
| **421CN250_N04P01** | float | 2.75% | 53.75% |     -26.73 |       0.00 |      -4.94 | Pressure |
| **421DU415_N01_T01** | float | 2.75% | 0.11% |     -10.00 |    1200.00 |     447.05 | Temperature |
| **431KL100PN01_O** | float | 2.75% | 4.39% |       0.00 |      21.42 |      13.32 | Oxygen sensor |
| **431KL100_N01_T02** | float | 2.75% | 0.00% |     550.00 |    1800.00 |    1494.69 | Extremely high temperature (Klinker Zone, mean ~1495°C) |
| **431KL100_N04_P01** | float | 2.75% | 0.02% |      -5.00 |       5.00 |      -0.47 | Pressure |
| **431MD140_M01_IZ1** | float | 2.75% | 1.24% |       0.00 |     689.66 |     119.75 | Motor current/power indicator |
| **431MD140_M01_SZ1** | float | 2.75% | 58.48% |      -0.01 |       3.52 |       1.10 | Speed/status variable |
| **431MD140_M02_IZ1** | float | 2.75% | 1.20% |       0.00 |     761.51 |     116.31 | Motor current/power indicator |
| **441FN590_M01_JZ1** | float | 2.75% | 55.85% |       0.00 |     779.00 |     290.59 | Motor speed / flow metric |
| **441FN590_M01_SZ1** | float | 2.75% | 55.77% |      -6.70 |      90.17 |      25.81 | Motor current/power |
| **441HE500_TZ1** | float | 2.75% | 0.00% |     -10.00 |     470.11 |      94.57 | Preheater/gas temperature |
| **441KH050_N01T01** | float | 2.75% | 0.00% |     -10.00 |    1192.30 |     391.04 | Temperature |
| **441KH050_N01T02** | float | 2.75% | 0.00% |     550.00 |    1800.00 |    1341.99 | High temperature zone (mean ~1342°C) |
| **441KH050_N02P01** | float | 2.75% | 0.00% |      -5.00 |       1.97 |      -0.42 | Pressure |
| **441MD140_A01_S01** | float | 2.75% | 60.46% |       0.00 |       7.37 |       1.60 | Speed / flow metric |
| **465RL570_FZ1** | float | 2.75% | 60.25% |       0.00 |      21.50 |       4.12 | Flow control valve speed/position |
| **465RL620_FZ1** | float | 2.75% | 59.50% |       0.00 |      10.02 |       3.20 | Flow control valve speed/position |
| **ATY_POS230_FLOW** | float | 2.75% | 47.39% |       0.00 |      52.28 |       2.47 | Alternative fuel feed flow rate |
| **NOX_AMMONIA_FLOW** | float | 2.75% | 1.96% |       0.00 |    1000.00 |      39.24 | Ammonia solution flow rate (for NOx reduction) |
| **C3S** | float | 0.00% | 0.00% |      19.50 |      70.60 |      58.95 | Lab Alite content (aligned to nearest sample) |
| **SCaO** | float | 0.00% | 0.00% |       0.13 |      11.72 |       2.17 | Lab Free Lime content (aligned to nearest sample) |
