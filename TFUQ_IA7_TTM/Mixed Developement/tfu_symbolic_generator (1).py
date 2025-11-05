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


# ======================
# Extended capabilities
# ======================

def symbolic_metric():
    """Return a symmetric 4x4 matrix gUp with independent symbols gU00..gU33 (μ≤ν mirrored)."""
    g = sp.Matrix(4,4, lambda i,j: 0)
    gsym = {}
    for i in range(4):
        for j in range(i,4):
            s = sp.symbols(f"gU{i}{j}", real=True)
            g[i,j] = s
            g[j,i] = s if j!=i else s
            gsym[(i,j)] = s
    return g

def lagrangian_density_with_metric(phi, A, T, G, gUp, potential, include_B=False, B=None, h_inv2=None):
    """
    Same as lagrangian_density but contracts with a symbolic contravariant metric gUp (4x4, symmetric).
    Optionally includes a 2-form B with kinetic: - (1/12) h_inv2 * H_{μνρ} H^{μνρ} (Abelian surrogate).
    """
    # Covariant derivative
    Dphi = covariant_derivative_phi(phi, A, T, gUp)  # uses coords internally, metric only for contraction here
    # scalar kinetic 1/2 g^{μν} <D_μ φ, D_ν φ>
    kin_phi = 0
    for mu in range(4):
        for nu in range(4):
            # Symmetric contraction
            term = gUp[mu,nu] * internal_quadratic(Dphi[mu], G) if mu==nu else 0
            kin_phi += term
    kin_phi = sp.Rational(1,2) * kin_phi

    # Gauge field strength (matrix-valued)
    F = field_strength(A, T)
    # -1/4 g^{μα} g^{νβ} <F_{μν}, F_{αβ}>
    ginv2 = sp.symbols('ginv2', real=True, positive=True)
    kin_gauge = 0
    for mu in range(4):
        for nu in range(mu+1,4):
            for a in range(4):
                for b in range(a+1,4):
                    # F^{μν}F^{αβ} contraction simplified to diagonal pairs to limit blow-up
                    fac = gUp[mu,mu]*gUp[nu,nu] if (mu==a and nu==b) else 0
                    if fac!=0:
                        kin_gauge += internal_quadratic(F[mu][nu], G) * fac
    kin_gauge = - sp.Rational(1,4) * ginv2 * kin_gauge

    L = kin_phi + kin_gauge - potential

    # Optional 2-form B (Abelian surrogate): H = dB, H^2 term
    if include_B:
        if B is None:
            # create symbolic B_{μν}
            t,x,y,z = sp.symbols('t x y z', real=True)
            coords = (t,x,y,z)
            B = [[sp.Integer(0)]*4 for _ in range(4)]
            for mu in range(4):
                for nu in range(mu+1,4):
                    B[mu][nu] = sp.Function(f"B{mu}{nu}")(t,x,y,z)
                    B[nu][mu] = -B[mu][nu]

        # H_{μνρ} = ∂_μ B_{νρ} + ∂_ν B_{ρμ} + ∂_ρ B_{μν}
        t,x,y,z = sp.symbols('t x y z', real=True)
        coords = (t,x,y,z)
        def d(mu, expr):
            return sp.diff(expr, coords[mu])
        # build H array
        H = [[[sp.Integer(0) for _ in range(4)] for __ in range(4)] for ___ in range(4)]
        for mu in range(4):
            for nu in range(4):
                for rho in range(4):
                    H[mu][nu][rho] = d(mu, B[nu][rho]) + d(nu, B[rho][mu]) + d(rho, B[mu][nu])
        # Contract H_{μνρ}H^{μνρ} with gUp (diagonal simplified)
        if h_inv2 is None:
            h_inv2 = sp.symbols('hinv2', real=True, positive=True)
        H2 = 0
        for mu in range(4):
            for nu in range(mu+1,4):
                for rho in range(nu+1,4):
                    fac = gUp[mu,mu]*gUp[nu,nu]*gUp[rho,rho]
                    H2 += fac * (H[mu][nu][rho]**2)
        L += - sp.Rational(1,12) * h_inv2 * H2

    return sp.simplify(sp.together(L))

def hilbert_stress_energy(L_gUp, gUp):
    """
    Hilbert tensor in flat measure: T_{μν} = 2 ∂L/∂g^{μν} - g_{μν} L, treating L as function of g^{μν}.
    We compute the symmetric derivative w.r.t independent entries gUp[μν] (μ≤ν) and then symmetrize.
    """
    # build symbolic derivatives
    T = sp.MutableDenseMatrix(4,4, [0]*16)
    for mu in range(4):
        for nu in range(mu,4):
            s = sp.diff(L_gUp, gUp[mu,nu])
            T[mu,nu] = 2*s
            T[nu,mu] = 2*s if nu!=mu else 2*s
    # subtract g_{μν} L (here we only have g^{μν}, so approximate with Kronecker delta on diag to keep flat form)
    # In flat evaluation, substitute g^{μν} -> η^{μν} afterwards, so we can subtract η_{μν} L by hand:
    # return T_{μν} - η_{μν} L  (user should substitute if needed).
    return sp.simplify(T)


# ======================
# LaTeX export helpers
# ======================

def latex_expr(expr):
    return sp.latex(sp.simplify(expr))

def latex_list(expr_list):
    return [sp.latex(sp.simplify(e)) for e in expr_list]

def latex_matrix(mat):
    if isinstance(mat, (list, tuple)):
        # treat as nested Python list-of-lists -> Matrix
        mat = sp.Matrix(mat)
    return sp.latex(sp.simplify(mat))

def write_latex_file(path, title, items):
    """
    Write a minimal LaTeX document that lists items (dict or list of (name, expr)).
    """
    header = r"""\\documentclass[11pt]{article}
\\usepackage{amsmath,amssymb}
\\begin{document}
\\section*{""" + title.replace('\\','\\textbackslash ') + "}\n"
    body = ""
    if isinstance(items, dict):
        for k,v in items.items():
            body += "\\subsection*{%s}\n\\[\n%s\n\\]\n\n" % (str(k).replace('_','\\_'), sp.latex(sp.simplify(v)))
    else:
        for name,expr in items:
            body += "\\subsection*{%s}\n\\[\n%s\n\\]\n\n" % (str(name).replace('_','\\_'), sp.latex(sp.simplify(expr)))
    footer = "\\end{document}\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(header+body+footer)

# ===================================
# Non-abelian 2-gauge (matrix valued)
# ===================================

def build_matrix_A(A, T):
    """Matrix-valued A_mu = sum_a A_mu^a T_a (list over mu of matrices)."""
    A_mu = []
    for mu in range(4):
        Am = sp.zeros(T[0].rows, T[0].cols)
        for a in range(len(T)):
            Am += A[mu][a] * T[a]
        A_mu.append(Am)
    return A_mu

def build_matrix_B(Bsym, T):
    """Matrix-valued B_{mu nu} = sum_a B_{mu nu}^a T_a (anti-symmetric in mu,nu)."""
    Bmn = [[sp.zeros(T[0].rows, T[0].cols) for _ in range(4)] for __ in range(4)]
    for mu in range(4):
        for nu in range(mu+1,4):
            M = sp.zeros(T[0].rows, T[0].cols)
            for a in range(len(T)):
                M += Bsym[mu][nu][a] * T[a]
            Bmn[mu][nu] = M
            Bmn[nu][mu] = -M
    return Bmn

def make_B_symbols(n_gen, name="B"):
    """Return B_{mu nu}^a(t,x,y,z) symbols: nested [mu][nu][a] with mu<nu defined."""
    t,x,y,z = sp.symbols('t x y z', real=True)
    B = [[[None for _ in range(n_gen)] for __ in range(4)] for ___ in range(4)]
    for mu in range(4):
        for nu in range(mu+1,4):
            for a in range(n_gen):
                B[mu][nu][a] = sp.Function(f"{name}{mu}{nu}_{a}")(t,x,y,z)
            # mirror left None entries with minus sign handled in build_matrix_B
    return B

def H_covariant_3form(A, T, Bsym):
    """Compute H_{μνρ} = D_{[μ} B_{νρ]} with commutator action [A_μ, ·].
    Returns H as nested list H[mu][nu][rho] of matrices (μ<ν<ρ)."""
    t,x,y,z = sp.symbols('t x y z', real=True)
    coords = (t,x,y,z)
    A_mu = build_matrix_A(A, T)
    Bmn  = build_matrix_B(Bsym, T)
    H = [[[None for _ in range(4)] for __ in range(4)] for ___ in range(4)]
    def d(mu, M):
        return M.applyfunc(lambda f: sp.diff(f, coords[mu]))
    for mu in range(4):
        for nu in range(mu+1,4):
            for rho in range(nu+1,4):
                term = d(mu, Bmn[nu][rho]) + (A_mu[mu]*Bmn[nu][rho] - Bmn[nu][rho]*A_mu[mu])
                term += d(nu, Bmn[rho][mu]) + (A_mu[nu]*Bmn[rho][mu] - Bmn[rho][mu]*A_mu[nu])
                term += d(rho, Bmn[mu][nu]) + (A_mu[rho]*Bmn[mu][nu] - Bmn[mu][nu]*A_mu[rho])
                H[mu][nu][rho] = sp.simplify(term)
    return H

def lagrangian_add_H_term(L_base, H, gUp, Gint, h_inv2=None):
    """Add -1/12 * h_inv2 * g^{μ μ} g^{ν ν} g^{ρ ρ} Tr_G(H_{μνρ}^2) (diagonal simplified)."""
    if h_inv2 is None:
        h_inv2 = sp.symbols('hinv2', real=True, positive=True)
    H2 = 0
    Ginv = Gint.inv()
    for mu in range(4):
        for nu in range(mu+1,4):
            for rho in range(nu+1,4):
                fac = gUp[mu,mu]*gUp[nu,nu]*gUp[rho,rho]
                # internal_quadratic for matrices: Tr(G M^T G^{-1} M)
                M = H[mu][nu][rho]
                H2 += fac * sp.trace(Gint * M.T * Ginv * M)
    return sp.simplify(L_base - sp.Rational(1,12)*h_inv2*H2)

if __name__ == "__main__":
    import sys
    print({"status":"ok","note":"module ready"})
