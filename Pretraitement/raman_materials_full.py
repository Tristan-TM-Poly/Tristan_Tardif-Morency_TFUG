"""
raman_materials_full.py — Complete analytical Raman spectra for key materials
-----------------------------------------------------------------------------
Includes all main and second-order modes for Si, Ge, Diamond, H2O, NaCl.
"""

import numpy as np
from raman_analytic import raman_analytic

MATERIAL_MODES_FULL = {
    "Si": [
        {"A":1.00,"nu":520.7,"sigma":4.5,"gamma":2.0,"beta":0.25},
        {"A":0.25,"nu":302,"sigma":6,"gamma":3,"beta":0.2},
        {"A":0.20,"nu":435,"sigma":5,"gamma":2,"beta":0.2},
        {"A":0.15,"nu":970,"sigma":10,"gamma":4,"beta":0.3},
        {"A":0.10,"nu":1450,"sigma":15,"gamma":5,"beta":0.35},
        {"A":0.05,"nu":1550,"sigma":18,"gamma":6,"beta":0.4},
    ],
    "Ge": [
        {"A":1.0,"nu":300,"sigma":5,"gamma":2.5,"beta":0.25},
        {"A":0.25,"nu":178,"sigma":6,"gamma":3,"beta":0.2},
        {"A":0.15,"nu":420,"sigma":7,"gamma":3,"beta":0.25},
        {"A":0.10,"nu":590,"sigma":9,"gamma":4,"beta":0.3},
        {"A":0.05,"nu":880,"sigma":12,"gamma":6,"beta":0.35},
    ],
    "Diamond": [
        {"A":1.0,"nu":1332,"sigma":3,"gamma":1.2,"beta":0.2},
        {"A":0.25,"nu":2665,"sigma":5,"gamma":2,"beta":0.25},
        {"A":0.10,"nu":1600,"sigma":12,"gamma":4,"beta":0.3},
        {"A":0.05,"nu":4000,"sigma":8,"gamma":3,"beta":0.35},
    ],
    "H2O": [
        {"A":0.15,"nu":400,"sigma":80,"gamma":20,"beta":0.25},
        {"A":0.6,"nu":1640,"sigma":30,"gamma":10,"beta":0.3},
        {"A":1.0,"nu":3280,"sigma":60,"gamma":20,"beta":0.4},
        {"A":0.9,"nu":3420,"sigma":80,"gamma":25,"beta":0.4},
    ],
    "NaCl": [
        {"A":1.0,"nu":236,"sigma":6,"gamma":3,"beta":0.25},
        {"A":0.8,"nu":284,"sigma":8,"gamma":4,"beta":0.25},
        {"A":0.2,"nu":320,"sigma":10,"gamma":5,"beta":0.3},
        {"A":0.1,"nu":560,"sigma":12,"gamma":6,"beta":0.35},
    ],
}

def generate_full_spectrum(material, nu_axis, Df=1.0, lam=1.0, T=300):
    if material not in MATERIAL_MODES_FULL:
        raise ValueError(f"Material '{material}' not defined.")
    modes = MATERIAL_MODES_FULL[material]
    return raman_analytic(nu_axis, modes, Df=Df, lam=lam, T=T)
