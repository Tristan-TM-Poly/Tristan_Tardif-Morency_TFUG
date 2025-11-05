"""
tfu_sc_analytic.py
Analytic TFU/TFUQ superconductivity kernel.

Inputs (per material):
- Base "microscopic" params at Df_ref:
    theta0     : characteristic phonon temperature (K), e.g. Debye or omega_log in K-equivalent
    lambda0    : baseline e-ph coupling (dimensionless)
    mu_star    : Coulomb pseudopotential (dimensionless)
    vF0        : Fermi velocity (m/s)
    mstar0     : effective mass (kg)
    ns0        : superfluid density (m^-3)
    alpha_gap0 : reduced gap factor alpha (BCS=3.52), optional
    Df_ref     : reference fractal parameter (dimensionless)
- Exponents for "power" renormalization vs Df (defaults from our prior TFU runs):
    al  : exponent for lambda_ep
    at  : exponent for theta(=omega_log)
    ans : exponent for ns
    av  : exponent for vF (default +0.10)
    am  : exponent for m* (default -0.10)
    aalpha : exponent for alpha_gap (default 0.0)
- Pinning model (optional):
    pf     : pinning fraction (0..1) (dimensionless)
    beta   : pinning exponent
    Cpin   : prefactor for pinning-limited critical current (A/m^2)

Core outputs:
    Tc, Delta0, xi0_nm, lambdaL_nm, kappa, Hc1_T, Hc2_T, Hc_T, Pc_Jperm3, Jd_Aperm2, Jc_Aperm2

Author: ChatGPT (GPT-5 Thinking)
"""
from __future__ import annotations
import math
from dataclasses import dataclass

# Physical constants
kB  = 1.380649e-23
h   = 6.62607015e-34
hbar= h/(2*math.pi)
e   = 1.602176634e-19
mu0 = 4e-7*math.pi
Phi0= h/(2*e)
me  = 9.10938356e-31

# ---------- Helpers ----------
def _safe_sqrt(x: float) -> float:
    return math.sqrt(max(x, 0.0))

def allen_dynes_Tc(thetaK: float, lam: float, mu_star: float) -> float:
    """Allen–Dynes / McMillan simplified (without f1,f2 factors). Units: K."""
    if lam <= 0.0 or thetaK <= 0.0:
        return 0.0
    denom = lam - mu_star*(1.0 + 0.62*lam)
    if denom <= 1e-16:
        return 0.0
    return (thetaK/1.2) * math.exp(-1.04*(1.0+lam)/denom)

def invert_lambda_from_Tc(Tc: float, thetaK: float, mu_star: float,
                          lam_lo: float=1e-6, lam_hi: float=200.0,
                          iters: int=120) -> float:
    """Numerically invert Allen–Dynes for lambda (bisection)."""
    def f(lam: float) -> float:
        return allen_dynes_Tc(thetaK, lam, mu_star) - Tc
    # Ensure bracket
    flo = f(lam_lo); fhi = f(lam_hi)
    expand = 0
    while flo * fhi > 0 and expand < 8:
        lam_hi *= 2.0
        fhi = f(lam_hi)
        expand += 1
    if flo * fhi > 0:
        return float("nan")
    lo, hi = lam_lo, lam_hi
    for _ in range(iters):
        mid = 0.5*(lo+hi)
        fm  = f(mid)
        if fm == 0.0:
            return mid
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5*(lo+hi)

def delta0_from_Tc(Tc: float, alpha_red: float=3.52) -> float:
    """Superconducting gap @0K: Delta0 = (alpha_red/2) kB Tc (Joules)."""
    return 0.5*alpha_red*kB*Tc

def xi0_from_vF_Delta(vF: float, Delta0: float) -> float:
    """BCS coherence length (meters)."""
    if Delta0 <= 0.0: return float("inf")
    return hbar*vF/(math.pi*Delta0)

def lambdaL_from_m_ns(mstar: float, ns: float) -> float:
    """London penetration depth (meters)."""
    denom = mu0*ns*(2*e)**2
    if denom <= 0.0: return float("inf")
    return _safe_sqrt(mstar/denom)

def fields_from_xi_lambda(xi: float, lamL: float, core_c: float=0.5) -> tuple[float,float,float]:
    """Return (Hc, Hc1, Hc2) in Tesla from xi, lambda (both meters)."""
    if xi<=0 or lamL<=0 or not math.isfinite(xi) or not math.isfinite(lamL):
        return (0.0, 0.0, 0.0)
    kappa = lamL/xi
    Bc  = Phi0/(2*math.sqrt(2)*math.pi*xi*lamL)
    Bc2 = Phi0/(2*math.pi*xi*xi)
    Bc1 = Phi0/(4*math.pi*lamL*lamL)*(math.log(max(kappa,1.0001)) + core_c)
    return (Bc, Bc1, Bc2)  # Tesla

def J_depair(Bc: float, lamL: float) -> float:
    """Depairing current density (A/m^2) ~ 2/(3√3) * Bc / (μ0 λ)."""
    if lamL <= 0.0: return 0.0
    return (2.0/(3.0*math.sqrt(3.0))) * (Bc/(mu0*lamL))

def J_pinning(pf: float, beta: float, ns: float, lamL: float, xi: float, Cpin: float=5e11) -> float:
    """
    Simple pinning-limited Jc model (scaling): Jc_pin = Cpin * pf^beta * sqrt(ns) / (lambda^2 * sqrt(xi)).
    Units: A/m^2. Choose Cpin to keep values in realistic 1e9–1e12 A/m^2 scales.
    """
    pf = max(0.0, min(1.0, pf))
    if lamL<=0 or xi<=0 or ns<=0: return 0.0
    return Cpin * (pf**beta) * (ns**0.5) / (lamL**2 * (xi**0.5))

# ---------- Renormalization vs Df ----------
def power_scale(Df: float, Df_ref: float, a: float) -> float:
    """Return scaling factor (Df/Df_ref)^a."""
    x = max(1e-12, Df)/max(1e-12, Df_ref)
    return x**a

@dataclass
class SCInputs:
    theta0: float
    lambda0: float
    mu_star: float
    vF0: float
    mstar0: float
    ns0: float
    Df_ref: float=1.0
    alpha_gap0: float=3.52
    # exponents
    al: float=0.45
    at: float=0.40
    ans: float=-0.70
    av: float=0.10
    am: float=-0.10
    aalpha: float=0.0
    # pinning
    pf: float=0.10
    beta: float=1.0
    Cpin: float=5e11

def compute_all(Df: float, p: SCInputs) -> dict:
    """Compute all observables for a given Df and material inputs."""
    # renormalize microscopic params by power laws
    lam = p.lambda0 * power_scale(Df, p.Df_ref, p.al)
    theta = p.theta0 * power_scale(Df, p.Df_ref, p.at)
    ns = p.ns0 * power_scale(Df, p.Df_ref, p.ans)
    vF = p.vF0 * power_scale(Df, p.Df_ref, p.av)
    mstar = p.mstar0 * power_scale(Df, p.Df_ref, p.am)
    alpha_gap = p.alpha_gap0 * power_scale(Df, p.Df_ref, p.aalpha)

    Tc = allen_dynes_Tc(theta, lam, p.mu_star)
    Delta0 = delta0_from_Tc(Tc, alpha_gap)
    xi0 = xi0_from_vF_Delta(vF, Delta0)
    lamL = lambdaL_from_m_ns(mstar, ns)
    Hc, Hc1, Hc2 = fields_from_xi_lambda(xi0, lamL, core_c=0.5)
    Jd = J_depair(Hc, lamL)
    Jc_pin = J_pinning(p.pf, p.beta, ns, lamL, xi0, p.Cpin)
    Jc = min(Jd, Jc_pin)
    kappa = lamL/xi0 if (lamL>0 and xi0>0 and math.isfinite(lamL) and math.isfinite(xi0)) else float("inf")
    Pc = (Hc**2)/(2.0*mu0)

    return {
        "Df": Df,
        "lambda_ep": lam,
        "thetaK": theta,
        "Tc_K": Tc,
        "alpha_gap": alpha_gap,
        "Delta0_J": Delta0,
        "xi0_nm": xi0*1e9,
        "lambdaL_nm": lamL*1e9,
        "kappa": kappa,
        "Hc_T": Hc, "Hc1_T": Hc1, "Hc2_T": Hc2,
        "Pc_Jperm3": Pc,
        "Jd_Aperm2": Jd, "Jc_Aperm2": Jc,
    }

def estimate_Df_from_Tc(Tc_target: float, p: SCInputs, Df_min: float=0.05, Df_max: float=5.0,
                        iters: int=64) -> float:
    """
    Invert Tc(Df) -> Df using bisection on the Allen–Dynes relation with power-law scaling.
    Finds Df such that Tc(Df) ~ Tc_target.
    """
    def f(Df):
        lam = p.lambda0 * power_scale(Df, p.Df_ref, p.al)
        theta = p.theta0 * power_scale(Df, p.Df_ref, p.at)
        return allen_dynes_Tc(theta, lam, p.mu_star) - Tc_target
    lo, hi = Df_min, Df_max
    flo, fhi = f(lo), f(hi)
    # expand if needed
    expand = 0
    while flo*fhi > 0 and expand < 8:
        hi *= 1.5
        fhi = f(hi)
        expand += 1
    if flo*fhi > 0:
        return float("nan")
    for _ in range(iters):
        mid = 0.5*(lo+hi); fm = f(mid)
        if fm == 0.0: return mid
        if flo*fm <= 0: hi, fhi = mid, fm
        else: lo, flo = mid, fm
    return 0.5*(lo+hi)
