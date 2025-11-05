# df_hypercore_all_in_one.py
# Noyau math/phys vectorisé pour D_f in {C, H(SU2), O(g2), Cl(3,1)-bivector}
# + Démos batch (LC 60Hz, DBD g2 intermods, SC GL + Jc(theta))
# Auteur: ChatGPT (fusion demandée)
# Licence: MIT

import numpy as np

# =========================
# 0) Utilitaires vectorisés
# =========================
def unit(v, axis=-1, eps=1e-12):
    v = np.asarray(v)
    n = np.linalg.norm(v, axis=axis, keepdims=True)
    return v / np.clip(n, eps, None)

def cross_batch(a, b):
    # a,b shape (...,3)
    a = np.asarray(a); b = np.asarray(b)
    return np.stack([
        a[...,1]*b[...,2]-a[...,2]*b[...,1],
        a[...,2]*b[...,0]-a[...,0]*b[...,2],
        a[...,0]*b[...,1]-a[...,1]*b[...,0]
    ], axis=-1)

# ================================
# 1) LC fractal @60 Hz (U(1), H)
# ================================
def lc_freq_Q_vectorized(L0, C0, R0, D_abs2=None, alpha=0.0, beta=0.0):
    """
    U(1) effectif: C = C0*(1+alpha|D|^2), L = L0*(1+beta|D|^2)
    Entrées:
      L0,C0,R0: scalaires
      D_abs2: array (...) de |D_f|^2 (peut être None -> 0)
    Renvoie:
      f0(...), Q(...)
    """
    if D_abs2 is None:
        D_abs2 = 0.0
    C = C0*(1.0 + alpha*D_abs2)
    L = L0*(1.0 + beta*D_abs2)
    w0 = 1.0/np.sqrt(L*C)
    f0 = w0/(2*np.pi)
    Q  = w0*L/R0
    return f0, Q

def lc_R_eq_anisotropic(R0, nhat, e_paras, rho):
    """
    SU(2) effectif: R_eq = R0*(1 - rho (n·e)^2), avec n,e vecteurs 3D.
    nhat: (...,3), e_paras: (3,), rho in [0,1)
    Renvoie R_eq(...), et gain de Q relatif = 1/(1 - rho (n·e)^2)
    """
    nh = unit(nhat)
    e  = unit(np.asarray(e_paras))
    cos2 = np.sum(nh*e, axis=-1)**2
    scale = 1.0 - rho*cos2
    return R0*scale, 1.0/scale

# ============================================
# 2) Canal EMI "bivecteur" (surrogate Clifford)
# ============================================
def emi_notch_response(freq, fB, zeta=1/np.sqrt(2), gain=1.0):
    """
    Filtre second ordre (notch/peak) centré fB pour canal grade-2.
    freq, fB en Hz. Retourne |H(f)|^2 (linéaire), vectorisé.
    Interprétation: énergie rotationnelle dirigée vers canal bivecteur.
    """
    w  = 2*np.pi*freq
    w0 = 2*np.pi*fB
    num = (w**2 - w0**2)**2
    den = (w**2 - w0**2)**2 + (2*zeta*w0*w)**2
    H2  = 1.0 - gain*( (2*zeta*w0*w)**2 / np.clip(den, 1e-30, None) )
    return np.clip(H2, 0.0, 1.0)

# ======================================================
# 3) Intermodulation non-associative (signature g2/octo)
# ======================================================
def g2_intermod_signature(amps, phases, order='left'):
    """
    Signature d’intermodulation de type χ^(3) non-associative simplifiée.
    Entrées:
      amps: (...,3) amplitudes des trois composantes internes (≃ Im(O))
      phases: (...,3) phases en rad
      order: 'left' (gauche) ou 'right' (droite) pour simuler parenthésage
    Sortie:
      S: (...,) amplitude relative des raies Ω±2Ω dépendant de l’ordre
    """
    a = np.asarray(amps); p = np.asarray(phases)
    z = a*np.exp(1j*p)   # (...,3) phasors
    if order == 'left':
        s = z[...,0]*(z[...,1]*z[...,2])
    else:
        s = (z[...,0]*z[...,1])*z[...,2]
    d = np.abs(s - np.conj(s))  # sensibilité à l’ordre
    return np.real(d)

# ==================================================
# 4) Supraconducteurs GL (U(1)) + anisotropie SU(2)
# ==================================================
def gl_parameters(v, alpha, beta, q, mu0=4e-7*np.pi):
    """
    Paramètres GL: lambda_L, xi, kappa à partir de (v, alpha<0, beta>0).
    v = sqrt(-alpha/beta).
    """
    lam = 1.0/np.sqrt(mu0*q*q*v*v)
    xi  = 1.0/np.sqrt(2.0*abs(alpha))
    kappa = lam/xi
    return lam, xi, kappa

def jc_theta_anisotropy(theta, Jc_par, Jc_perp):
    """
    Loi simple anisotrope: 1/Jc(θ)^2 = cos^2θ/J_parallel^2 + sin^2θ/J_perp^2
    Entrées:
      theta: array (...,) angles (rad), Jc_par, Jc_perp scalaires
    Sortie:
      Jc(theta) (...,)
    """
    c2 = np.cos(theta)**2
    s2 = 1.0 - c2
    inv2 = c2/(Jc_par**2) + s2/(Jc_perp**2)
    return 1.0/np.sqrt(inv2)

# ==========================================
# 5) SU(2) quaternionique (matrices 4x4)
# ==========================================
L_i = np.array([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]], dtype=float)
L_j = np.array([[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]], dtype=float)
L_k = np.array([[0,0,0,-1],[0,0,1,0],[0,-1,0,0],[1,0,0,0]], dtype=float)
T = 0.5*np.stack([L_i, L_j, L_k], axis=0)  # (3,4,4)

def su2_left_act(A_mu, D):
    """
    Dérivée covariante (action gauche) vectorisée:
      A_mu: (...,4,4) matrice su2 (combinaison de T^a) à chaque point mu fixé *ou* (...,3) coeffs vers T^a
      D: (...,4) quaternion (d0,d1,d2,d3)
    Sortie: (...,4) A_mu * D
    """
    A = np.asarray(A_mu)
    D = np.asarray(D)
    if A.shape[-2:] == (4,4):
        return (A @ D[...,None])[...,0]  # (...,4)
    Amat = A[...,0,None,None]*T[0] + A[...,1,None,None]*T[1] + A[...,2,None,None]*T[2]  # (...,4,4)
    return (Amat @ D[...,None])[...,0]

# =====================================
# 6) Démos vectorisées (main inclus)
# =====================================
def demo_lc_module():
    L0, C0, R0 = 17.6, 399e-9, 2.0
    D2 = np.linspace(0.0, 0.2, 2001)  # |D|^2 sweep
    f0, Q = lc_freq_Q_vectorized(L0, C0, R0, D2, alpha=5e-2, beta=0.0)

    # SU(2) anisotropie
    nh = unit(np.random.randn(50000,3), axis=-1)     # 50k orientations
    eP = np.array([0,0,1.0])
    Req, Qgain = lc_R_eq_anisotropic(R0, nh, eP, rho=0.12)

    # Notch EMI (Clifford-like)
    freq = np.logspace(2,5,4000)  # 100 Hz .. 100 kHz
    H2   = emi_notch_response(freq, fB=1200.0, zeta=0.707, gain=0.95)

    out = {
        "f0_Hz_first": float(f0[0]),
        "f0_Hz_last": float(f0[-1]),
        "Q_first": float(Q[0]),
        "Q_last": float(Q[-1]),
        "Q_gain_min": float(Qgain.min()),
        "Q_gain_max": float(Qgain.max()),
        "EMI_min_H2": float(H2.min())
    }
    return out

def demo_g2_intermods():
    A = np.full((200000,3), 1.0)  # 200k phasors
    P = np.random.uniform(0, 2*np.pi, (200000,3))
    S_left  = g2_intermod_signature(A,P,'left')
    S_right = g2_intermod_signature(A,P,'right')
    asym = np.mean(np.abs(S_left - S_right)) / (np.mean(np.abs(S_left))+1e-12)
    out = {
        "g2_intermod_asym": float(asym),
        "S_left_mean": float(np.mean(S_left)),
        "S_right_mean": float(np.mean(S_right))
    }
    return out

def demo_sc_gl():
    alpha, beta, q = -1.0, 1.0, 2.0*1.602e-19
    v = np.sqrt(-alpha/beta)
    lam, xi, kappa = gl_parameters(v, alpha, beta, q)

    theta = np.linspace(0, np.pi, 4001)
    Jc = jc_theta_anisotropy(theta, Jc_par=6e6, Jc_perp=3e6)
    out = {
        "lambda_L": float(lam),
        "xi": float(xi),
        "kappa": float(kappa),
        "Jc_min": float(Jc.min()),
        "Jc_max": float(Jc.max())
    }
    return out

def run_all_demos():
    return {
        "LC_60Hz": demo_lc_module(),
        "g2_intermods": demo_g2_intermods(),
        "SC_GL": demo_sc_gl()
    }

if __name__ == "__main__":
    res = run_all_demos()
    import json
    print(json.dumps(res, indent=2))
