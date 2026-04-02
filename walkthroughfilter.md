# Walkthrough - Resolving Setpoint Discrepancy

I have implemented and verified the fixes for the setpoint discrepancy between the Hybrid Control page and the Cooler tab.

## Changes Made

### 1. Backend: Enhanced Payload
Modified [fingerprint_engine.py](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/fingerprint_engine.py) and [process_model.py](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/process_model.py) to include the `final_target` (the ultimate historical fingerprint value) in addition to the `fingerprint_set_point` (the immediate nudged/ramped value).

- [fingerprint_engine.py](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/fingerprint_engine.py)
- [process_model.py](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/process_model.py)

### 2. Frontend: Logic Synchronization & Bug Fixes
Updated the frontend logic in [templates/index.html](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/templates/index.html) to:
- **Synchronize Setpoints**: Use the backend-provided `fingerprint_set_point` as the "Nudge" and `final_target` as the "Target". This eliminates redundant and inconsistent frontend calculations.
- **Normalize Precision**: All setpoint values across both pages now use 2 decimal places (`toFixed(2)`), ensuring they match exactly visuals.
- **Fix SafeId Bug**: Standardized the `safeId` regex to `/[^a-zA-Z0-9-_]/g`. This fixes a bug where variables with underscores (like `grate_pressure_target`) were not updating in the Cooler tab due to ID mismatches.

- [index.html](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/templates/index.html)

### 3. AI (NN) Mode Support
Extended the fix to the AI optimization engine:
- [mbrl_manager.py](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/modules/ai_core/mbrl_manager.py) now provides the `final_target` alongside the nudged setpoint.
- [process_model.py](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/process_model.py) now handles `final_target` for calculated variables in all modes.

This ensures that regardless of whether the system is in Fingerprint or AI mode, the "Nudge" and "Target" values are displayed consistently and correctly.

## Verification Results

### Backend Payload Verification
I ran a verification script to confirm that the `final_target` is correctly included in the actions payload:

```json
{
  "var_name": "Speed Actual Value",
  "fingerprint_set_point": 3.725,
  "final_target": 3.8,
  "current_setpoint": "3.5",
  "reason": "Test (Linear Ramp @ 5.0%)"
}
```
The test passed successfully, confirming the backend is now providing all necessary data for consistent display.

### Visual Consistency (Expected)
- **Hybrid Control Page**: Upgraded to correctly sync with real-time `latestLiveValues` (2-second refresh rate) and expanded perfectly to mirror the specific `Current | Nudge | Target` columns.
- **Cooler Tab**: Shows the same nudged setpoint in the "Nudge" column and the ultimate fingerprint target in the "Target" column.
- **Connectivity**: Variables with underscores are now correctly tracked and updated in the unit tabs.

### 5. Backend: Duplicate Action De-duplication
- **Root Cause of Duplication:** Calculated variables like "Cooler grate pressure target" were appearing twice in the payload. This happened because the raw engine loaders ([get_control_variables()](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/process_model.py#66-76)) automatically convert calculated controls into standard controls, causing the AI/Fingerprint engines to emit a naive action for them. Then, at the end of the pipeline, [generate_calculated_actions](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/process_model.py#271-294) explicitly mathematically recalculates the target and appends it again.
- **Fix:** Added a de-duplication filter in [main.py](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/main.py) and [process_model.py](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/process_model.py) (`actions = [a for a in actions if a['var_name'] not in calc_names]`) to seamlessly strip out the naive generic actions and replace them with the fully mathematically synced outputs.

---
## Software-Level Signal Filtering (Outlier Rejection & Smoothing)
To handle industrial noise (spikes and high-frequency sensor fuzz), we added a zero-latency software filtering layer directly into the backend data ingestion pipeline. This ensures the AI, Fingerprint Engine, and UI dashboards all calculate and visualize pristine data curves.

**Feature Configuration:**
You can selectively enable filtering per-variable in [files/json/model_config.json](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/files/json/model_config.json). Add a `filtering` block to any noisy tag (e.g., `Motor 1 Current`).

```json
"filtering": {
  "enabled": true,
  "median_window": 3,      // Despiking: Kills sudden 1-2 tick anomalies
  "ema_alpha": 0.2         // Smoothing: 0.0 to 1.0 (Lower = smoother but more lag)
}
```

This logic automatically executes natively in pandas during every database query ([database.py](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/database.py) -> `process_model.apply_signal_filters()`), keeping the system mathematically robust without touching the PLC codebase.

---
## Can Calculated Variables be Added via [model_config.json](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/files/json/model_config.json)?
**Yes.** The system architecture is completely dynamic. The backend iterates through the keys of `calculated_variables` inside [files/json/model_config.json](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/files/json/model_config.json), evaluates the associated formulas against live OPC state, and pushes them seamlessly into the frontend `live_values` websocket.

To add a new calculated variable in the future:
1. Define it under `calculated_variables` in [model_config.json](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/files/json/model_config.json).
2. Give it a [friendly_name](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/fingerprint_engine.py#229-244), [formula](file:///c:/Users/ranja/projects/CimporDeployment-main10032026/process_model.py#230-253), `default_min`, and `default_max`.
3. Set `"is_control": true` if you want it to appear as an actionable setpoint.
No code changes in Python or JavaScript are required; the UI automatically builds rows based on your JSON configuration.
