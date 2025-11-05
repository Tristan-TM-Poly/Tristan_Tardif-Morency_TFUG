// ai7_fw.h -- AI-7 Firmware API (HP-v4)
// SPDX-License-Identifier: MIT
#pragma once
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct { float vmin, vmax; float norm_target; } ai7_clamp_t;
typedef struct { uint16_t row, col; float value; } ai7_prog_t;

int ai7_init(void);
int ai7_set_mask(uint8_t level);
int ai7_set_Df(uint16_t region_id, float Df0, float Df1, float Df2, float Df3);
int ai7_load_Vin(const float* vin, uint16_t len);
int ai7_read_cols(float* buf, uint16_t ncols);
int ai7_program_block(uint16_t tile, const ai7_prog_t* list, uint32_t n);
int ai7_calibrate(uint16_t tile_id);
int ai7_set_clamps(const ai7_clamp_t* cfg);
int ai7_run_mpc(uint32_t horizon_us);  // deadline ≤ 100 µs
int ai7_fallback_lqr(void);

// Telemetry (optional)
typedef struct {
    float snr_db;
    float energy_pj_per_mac;
    float rho_density;
    float drift_residual_pct;
    float vin_mean, vin_std;
} ai7_kpi_t;

int ai7_get_kpis(ai7_kpi_t* out);

#ifdef __cplusplus
}
#endif
