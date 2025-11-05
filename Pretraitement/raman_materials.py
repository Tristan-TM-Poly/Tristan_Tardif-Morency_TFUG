"""
raman_materials.py — Analytical Raman spectra for multiple materials
--------------------------------------------------------------------
Educational template for Si, Ge, diamond, H2O, NaCl.
Values are typical literature averages (room temperature).
"""

import numpy as np
import matplotlib.pyplot as plt
from raman_analytic import raman_analytic  # bloc précédent

# paramètres typiques (cm⁻¹)
MATERIAL_MODES = {
    "Si": [
        {"A": 1.0, "nu": 520.7, "sigma": 4.5, "gamma": 2.0, "beta": 0.3},
    ],
    "Ge": [
        {"A": 1.0, "nu": 300.3, "sigma": 5.0, "gamma": 2.5, "beta": 0.25},
    ],
    "Diamond": [
        {"A": 1.0, "nu": 1332.0, "sigma": 3.0, "gamma": 1.2, "beta": 0.2},
    ],
    "H2O_liquid": [
        {"A": 0.4, "nu": 1640.0, "sigma": 20.0, "gamma": 8.0, "beta": 0.3},
        {"A": 0.8, "nu": 3270.0, "sigma": 70.0, "gamma": 25.0, "beta": 0.4},
    ],
    "NaCl": [
        {"A": 0.6, "nu": 230.0, "sigma": 6.0, "gamma": 3.0, "beta": 0.2},
        {"A": 0.5, "nu": 285.0, "sigma": 8.0, "gamma": 4.0, "beta": 0.3},
    ],
}

def generate_material_spectrum(material, nu_axis, Df=1.0, lam=1.0, T=300):
    if material not in MATERIAL_MODES:
        raise ValueError(f"Material '{material}' not defined.")
    modes = MATERIAL_MODES[material]
    return raman_analytic(nu_axis, modes, Df=Df, lam=lam, T=T)

def demo_all_materials():
    nu = np.linspace(100, 3600, 4000)
    plt.figure(figsize=(10,6))
    for m in MATERIAL_MODES:
        I = generate_material_spectrum(m, nu)
        plt.plot(nu, I/np.max(I), label=m)
    plt.xlabel("Raman shift (cm⁻¹)")
    plt.ylabel("Normalized intensity")
    plt.title("Analytical Raman spectra — typical room-temperature examples")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    demo_all_materials()
