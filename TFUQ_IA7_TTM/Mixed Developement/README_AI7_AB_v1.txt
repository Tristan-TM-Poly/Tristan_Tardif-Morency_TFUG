AI-7 (RRAM + TFUG/TFUQ + LC/cavity) — A+B Deliverables
======================================================
This folder contains:
1) LC_cavity_HP_v4_SPICE_v3.cir  — Netlist for AC/TRAN with notch EMI tuned at FCLK, sweeps over {Df,Q1,Q2,g0,g1,g2}.
2) ai7_fw.h                      — Firmware API header (C) for clamps/normalization, MPC/LQR, calibration.
3) controller_fw.c               — Loop skeleton (fast/medium/slow), deadline watchdog with fallback to LQR.
4) hp_v4_timeseries.csv          — KPI time series template.
5) hp_v4_summary.json            — KPI summary template.

Next steps:
- Set FCLK to your actual board clock in .cir, run AC/TRAN, export Bode/TRAN.
- Replace HAL stubs in controller_fw.c with board drivers (RRAM, timers, DMA).
- Fill CSV/JSON with your runs; thresholds are in the plan.
