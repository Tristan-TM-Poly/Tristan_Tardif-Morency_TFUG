// controller_fw.c -- loops: fast (clamp), medium (MPC), slow (wear)
// SPDX-License-Identifier: MIT
#include "ai7_fw.h"
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>

// ---- HAL stubs (replace with board-specific drivers) ----
static inline uint64_t now_us(void){
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec*1000000ull + ts.tv_nsec/1000ull;
}
static int hal_qp_solve_osqp(float* u, const float* x, uint32_t horizon_us){
    (void)x;
    // pretend we solve within 60 µs
    uint64_t t0=now_us(); while(now_us()-t0<60);
    u[0]*=0.98f; return 0;
}
static int hal_lqr_step(float* u, const float* x){
    // simple proportional fallback
    u[0] = 0.9f*u[0] - 0.1f*x[0]; return 0;
}

// ---- Controller state ----
static ai7_clamp_t g_clamp = { .vmin=-1.10f, .vmax=+1.10f, .norm_target=1.00f };
static float g_last_u = 0.0f;
static ai7_kpi_t g_kpi = {0};

// ---- API impl ----
int ai7_init(void){ memset(&g_kpi,0,sizeof(g_kpi)); return 0; }
int ai7_set_mask(uint8_t level){ (void)level; return 0; }
int ai7_set_Df(uint16_t region_id, float Df0, float Df1, float Df2, float Df3){
    (void)region_id; (void)Df0; (void)Df1; (void)Df2; (void)Df3; return 0; }
int ai7_load_Vin(const float* vin, uint16_t len){ (void)vin; (void)len; return 0; }
int ai7_read_cols(float* buf, uint16_t ncols){ for(uint16_t i=0;i<ncols;i++) buf[i]=0.0f; return 0; }
int ai7_program_block(uint16_t tile, const ai7_prog_t* list, uint32_t n){ (void)tile; (void)list; (void)n; return 0; }
int ai7_set_clamps(const ai7_clamp_t* cfg){ g_clamp = *cfg; return 0; }

int ai7_calibrate(uint16_t tile_id){
    (void)tile_id;
    // Simple normalization: nudge target to measured mean
    float vin_mean = g_kpi.vin_mean;
    if (fabsf(vin_mean) > 1e-6f){
        float corr = g_clamp.norm_target / vin_mean;
        // Apply to internal gain path (placeholder)
        (void)corr;
    }
    // Reset drift residual
    g_kpi.drift_residual_pct = fmaxf(0.0f, g_kpi.drift_residual_pct - 0.5f);
    return 0;
}

int ai7_run_mpc(uint32_t horizon_us){
    float x[4] = {0};     // measured state (placeholder)
    float u[2] = {g_last_u, 0.0f};

    uint64_t t0 = now_us();
    int rc = hal_qp_solve_osqp(u, x, horizon_us);
    uint64_t dt = now_us() - t0;

    if (rc != 0 || dt > horizon_us){
        // deadline miss → fallback to LQR
        hal_lqr_step(u, x);
    }

    // Clamp
    if (u[0] > g_clamp.vmax) u[0] = g_clamp.vmax;
    if (u[0] < g_clamp.vmin) u[0] = g_clamp.vmin;
    g_last_u = u[0];

    // Update KPIs (mock computation)
    g_kpi.snr_db = fmaxf(36.5f, g_kpi.snr_db*0.9f + 37.0f*0.1f);
    g_kpi.energy_pj_per_mac = fminf(58.0f, g_kpi.energy_pj_per_mac*0.9f + 57.0f*0.1f);
    g_kpi.rho_density = fminf(0.18f, g_kpi.rho_density*0.9f + 0.17f*0.1f);
    g_kpi.vin_mean = g_kpi.vin_mean*0.9f + 1.05f*0.1f;
    g_kpi.vin_std  = g_kpi.vin_std*0.9f + 0.01f*0.1f;
    g_kpi.drift_residual_pct = fmaxf(0.0f, g_kpi.drift_residual_pct*0.9f - 0.1f);

    return 0;
}

int ai7_fallback_lqr(void){
    float x[1] = {0};
    float u[1] = {g_last_u};
    return hal_lqr_step(u,x);
}

int ai7_get_kpis(ai7_kpi_t* out){
    if (!out) return -1;
    *out = g_kpi;
    return 0;
}
