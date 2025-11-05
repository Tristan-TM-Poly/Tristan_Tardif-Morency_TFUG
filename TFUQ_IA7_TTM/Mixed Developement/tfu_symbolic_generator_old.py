# tfu_symbolic_generator.py
# SymPy generator for TFU-Ω (associative internal algebras)
# Given: internal metric G (n x n), generator matrices T_a (n x n), spacetime metric eta (4 x 4),
# scalar multiplet phi_i(x), gauge fields A_mu^a(x), and potential U(phi).
# Produces: Lagrangian density L, EOM_phi, EOM_gauge, canonical T^{mu nu}, and Noether currents.
# Author: ChatGPT — MIT License

import sympy as sp

# ------------- Core builders -------------

def minkowski_metric(signature='-+++'):
    if signature == '-+++':
        return sp.diag(-1,1,1,1)
    elif signature == '+---':
        return sp.diag(1,-1,-1,-1)
    else:
        raise ValueError("Unknown signature")

def field_symbols(n, name='phi'):
    """Return component fields phi_i(x) as SymPy Functions of (t,x,y,z)."""
    t,x,y,z = sp.symbols('t x y z', real=True)
    coords = (t,x,y,z)
    phi = [sp.Function(f"{name}{i}")(t,x,y,z) for i in range(n)]
    return phi, coords

def gauge_symbols(n_gen, name='A'):
    """Return gauge fields A_mu^a(x) with mu=0..3, a=0..n_gen-1."""
    t,x,y,z = sp.symbols('t x y z', real=True)
    A = [[sp.Function(f"{name}{mu}_{a}")(t,x,y,z) for a in range(n_gen)] for mu in range(4)]
    return A

def covariant_derivative_phi(phi, A, T, eta):
    """
    D_mu phi = partial_mu phi + sum_a A_mu^a * (T_a * phi)
    phi: list (n)
    A: list over mu=0..3 of list over a
    T: list of SymPy Matrices (n x n)
    eta: spacetime metric (4x4)
    Returns Dphi[mu] as Matrix (n x 1) for mu=0..3
    """
    n = len(phi); n_gen = len(T)
    t,x,y,z = sp.symbols('t x y z', real=True)
    coords = (t,x,y,z)
    phi_vec = sp.Matrix(phi)  # (n,1)
    Dphi = []
    for mu, c in enumerate(coords):
        # partial_mu phi
        dphi = phi_vec.applyfunc(lambda f: sp.diff(f, c))
        # gauge term
        gauge_term = sp.zeros(n,1)
        for a in range(n_gen):
            gauge_term += A[mu][a] * (T[a] * phi_vec)
        Dphi.append(dphi + gauge_term)
    return Dphi  # list of 4 matrices

def field_strength(A, T):
    """
    F_{mu nu}^a = d_mu A_nu^a - d_nu A_mu^a + f^a_{bc} A_mu^b A_nu^c
    Implemented via commutator [A_mu, A_nu] in the representation: [A_mu, A_nu] = sum_a F_{mu nu}^a T_a
    We compute matrix-valued F_{mu nu} = d_mu A_nu - d_nu A_mu + [A_mu, A_nu],
    where A_mu = sum_a A_mu^a T_a.
    Returns: Fmunu_mats[mu][nu] (n x n) SymPy Matrices.
    """
    n_gen = len(T)
    t,x,y,z = sp.symbols('t x y z', real=True)
    coords = (t,x,y,z)

    # Build matrix-valued A_mu
    A_mu = []
    for mu in range(4):
        Am = sp.zeros(T[0].rows, T[0].cols)
        for a in range(n_gen):
            Am += A[mu][a] * T[a]
        A_mu.append(Am)

    # d_mu A_nu
    dA = [[None]*4 for _ in range(4)]
    for mu,c in enumerate(coords):
        for nu in range(4):
            dA[mu][nu] = A_mu[nu].applyfunc(lambda f: sp.diff(f, c))

    F = [[None]*4 for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            comm = A_mu[mu]*A_mu[nu] - A_mu[nu]*A_mu[mu]
            F[mu][nu] = dA[mu][nu] - dA[nu][mu] + comm
    return F

def internal_quadratic(vec_or_mat, G):
    """
    Compute quadratic form with internal metric G.
    - If input is a column vector v (n x 1), return v.T * G * v (scalar)
    - If input is a matrix M (n x n), return Tr(G * M.T * G^{-1} * M) as a gauge-invariant norm surrogate.
    """
    if isinstance(vec_or_mat, sp.Matrix) and vec_or_mat.shape[1] == 1:
        v = vec_or_mat
        return (v.T * G * v)[0]
    M = vec_or_mat
    Ginv = G.inv()
    return sp.trace(G * M.T * Ginv * M)

def lagrangian_density(phi, A, T, G, eta, potential):
    """
    L = 1/2 eta^{mu nu} <D_mu phi, D_nu phi>_G - U(phi) - (1/4g^2) <F_{mu nu}, F^{mu nu}>_G
    Here we leave 1/g^2 factor implicit as a symbol 'ginv2' to be multiplied outside if desired.
    """
    # symbols
    ginv2 = sp.symbols('ginv2', real=True, positive=True)  # equals 1/g^2 if you want
    # Covariant derivative
    Dphi = covariant_derivative_phi(phi, A, T, eta)
    # Kinetic term for phi
    kin_phi = 0
    for mu in range(4):
        for nu in range(4):
            kin_phi += eta[mu,nu] * internal_quadratic(Dphi[mu], G) if mu==nu else 0
    kin_phi = sp.Rational(1,2) * kin_phi

    # Gauge field strength
    F = field_strength(A, T)
    kin_gauge = 0
    for mu in range(4):
        for nu in range(4):
            if mu < nu:
                # F^{mu nu} uses eta to raise indices; here flat so F^{mu nu}=eta^{mu mu} eta^{nu nu} F_{mu nu}
                fac = eta[mu,mu]*eta[nu,nu]
                kin_gauge += internal_quadratic(F[mu][nu], G) * fac
    kin_gauge = - sp.Rational(1,4) * ginv2 * kin_gauge

    L = kin_phi + kin_gauge - potential
    return sp.simplify(L)

# ------------- Variations / EOM -------------

def eom_phi(L, phi, coords):
    """
    Euler–Lagrange for scalar multiplet phi_i:
    d/dx_mu (∂L/∂(∂_mu phi_i)) - ∂L/∂phi_i = 0
    """
    E = []
    for i, f in enumerate(phi):
        # Build derivatives wrt partials
        eq = 0
        for mu,c in enumerate(coords):
            dL_d_dphi = sp.diff(L, sp.diff(f, c))
            eq += sp.diff(dL_d_dphi, c)
        eq -= sp.diff(L, f)
        E.append(sp.simplify(sp.together(eq)))
    return E

def eom_gauge(L, A, coords):
    """
    Gauge EOM: d/dx_nu (∂L/∂(∂_nu A_mu^a)) - ∂L/∂A_mu^a = 0  for each (mu,a)
    """
    E = [[None]*len(A[0]) for _ in range(4)]
    for mu in range(4):
        for a in range(len(A[0])):
            Amua = A[mu][a]
            eq = 0
            for nu,c in enumerate(coords):
                dL_d_dAmuanu = sp.diff(L, sp.diff(Amua, c))
                eq += sp.diff(dL_d_dAmuanu, c)
            eq -= sp.diff(L, Amua)
            E[mu][a] = sp.simplify(sp.together(eq))
    return E

# ------------- Canonical stress-energy (flat) -------------

def canonical_stress_energy(L, phi, A, eta, coords):
    """
    Canonical T^{mu nu} = sum_i ∂L/∂(∂_mu φ_i) ∂^ν φ_i + sum_{μ,a} ∂L/∂(∂_mu A_ρ^a) ∂^ν A_ρ^a - η^{mu ν} L
    NB: This is the canonical (not Belinfante) tensor; adequate for symbolic inspection.
    """
    T = [[None]*4 for _ in range(4)]
    # raise index with eta (flat, diagonal)
    def raise_mu(expr, mu_to_nu):
        # ∂^ν = eta^{ν ν} ∂_ν for diagonal eta
        return eta[mu_to_nu,mu_to_nu] * expr

    for mu in range(4):
        for nu in range(4):
            Tij = 0
            # scalars
            for f in phi:
                dL_d_dphi = sp.diff(L, sp.diff(f, coords[mu]))
                Tij += dL_d_dphi * raise_mu(sp.diff(f, coords[nu]), nu)
            # gauge fields
            n_gen = len(A[0])
            for rho in range(4):
                for a in range(n_gen):
                    Arhoa = A[rho][a]
                    dL_d_dA = sp.diff(L, sp.diff(Arhoa, coords[mu]))
                    Tij += dL_d_dA * raise_mu(sp.diff(Arhoa, coords[nu]), nu)
            Tij -= eta[mu,nu]*L
            T[mu][nu] = sp.simplify(sp.together(Tij))
    return T

# ------------- Noether currents (global internal rotations) -------------

def noether_current_global(L, phi, G, coords, Xi):
    """
    Global internal transformation δphi = Xi * phi  (Xi is an n x n constant matrix).
    J^mu = ∂L/∂(∂_mu phi) · δphi   (sum over components with internal metric G)
    Returns J^mu (mu=0..3).
    """
    n = len(phi)
    phi_vec = sp.Matrix(phi)
    dphi = Xi * phi_vec  # variation
    J = []
    for mu,c in enumerate(coords):
        grad = sp.Matrix([sp.diff(L, sp.diff(phi[i], c)) for i in range(n)])  # ∂L/∂(∂_mu phi_i)
        Jmu = (grad.T * G * dphi)[0]
        J.append(sp.simplify(sp.together(Jmu)))
    return J

# ------------- Demo builder: U(1) and SU(2) -------------

def demo_u1():
    # internal: n=1 real component, T = [0] (Abelian), G = [1]
    n = 1
    G = sp.eye(1)
    T = [sp.zeros(1,1)]  # U(1) acts trivially on a real scalar; for charged complex scalar use 2-comp real form
    eta = minkowski_metric('-+++')
    phi, coords = field_symbols(n)
    # Potential U = λ/4 (phi^T G phi - v^2)^2
    lam, v = sp.symbols('lambda v', positive=True, real=True)
    r = (sp.Matrix(phi).T*G*sp.Matrix(phi))[0]
    U = lam/4 * (r - v**2)**2

    A = gauge_symbols(n_gen=1)
    L = lagrangian_density(phi, A, T, G, eta, U)
    E_phi = eom_phi(L, phi, coords)
    E_A = eom_gauge(L, A, coords)
    Tmunu = canonical_stress_energy(L, phi, A, eta, coords)
    # Noether (global O(1) is trivial here); return structures
    return dict(L=L, E_phi=E_phi, E_A=E_A, T=Tmunu)

def demo_su2():
    # internal: n=3 real multiplet, generators T_a = -epsilon_{a b c} acting on R^3 (adjoint)
    n = 3
    G = sp.eye(3)
    # structure: (T_a)_{bc} = -epsilon_{a b c}
    eps = sp.MutableDenseNDimArray([0]*27, (3,3,3))
    for a in range(3):
        for b in range(3):
            for c in range(3):
                eps[a,b,c] = sp.Eijk(a+1,b+1,c+1)  # Levi-Civita (1..3 indexing)
    T = []
    for a in range(3):
        M = sp.zeros(3,3)
        for b in range(3):
            for c in range(3):
                M[b,c] -= eps[a,b,c]
        T.append(M)

    eta = minkowski_metric('-+++')
    phi, coords = field_symbols(n)
    lam, v = sp.symbols('lambda v', positive=True, real=True)
    r = (sp.Matrix(phi).T*G*sp.Matrix(phi))[0]
    U = lam/4 * (r - v**2)**2
    A = gauge_symbols(n_gen=3)

    L = lagrangian_density(phi, A, T, G, eta, U)
    E_phi = eom_phi(L, phi, coords)
    E_A = eom_gauge(L, A, coords)
    Tmunu = canonical_stress_energy(L, phi, A, eta, coords)

    # Noether current for a global rotation Xi (take Xi = generator T_1 as an example)
    Xi = T[0]
    J = noether_current_global(L, phi, G, coords, Xi)
    return dict(L=L, E_phi=E_phi, E_A=E_A, T=Tmunu, J=J)

# ------------- Notes for non-associative algebras -------------
# For non-associative cases (octonions etc.), one can inject derivations via a faithful
# matrix representation of Der(A) (e.g., g2 in 7D) and keep the matter as an R^n multiplet.
# The commutator structure closes in Der(A), so the above machinery applies with T_a in Der(A).
# A proper 2-gauge extension would add B_{mu nu} and its kinetic term; this is left as an extension.

if __name__ == "__main__":
    import sys
    print({"status":"ok","note":"module ready"})
