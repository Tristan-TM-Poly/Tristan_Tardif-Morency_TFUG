import os
import numpy as np
import matplotlib.pyplot as plt

def plot_spectrum(wavenumber, intensity, out_png):
    plt.figure()
    plt.plot(wavenumber, intensity)
    plt.xlabel('Wavenumber (cm^-1)')
    plt.ylabel('Intensity (a.u.)')
    plt.title('Raman Spectrum')
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()

def plot_calibration(nominal, empirical, out_png):
    plt.figure()
    plt.plot(nominal, empirical, marker='o')
    plt.plot([0,1],[0,1], linestyle='--')
    plt.xlabel('Nominal coverage')
    plt.ylabel('Empirical coverage')
    plt.title('Uncertainty Calibration')
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()
