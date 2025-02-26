import numpy as np


# define CSTR model
def cstr(x, t, u, d):
    # Input variables
    Ca, T = x    # States: Concentration of A in CSTR (mol/m^3) & Temperature in CSTR (K)
    Tc = u       # Controls: Temperature of cooling jacket (K)
    Caf, Tf = d  # Disturbances: Feed Concentration (mol/m^3) & Feed Temperature (K)

    # Parameters
    q = 100        # Volumetric Flowrate (m^3/sec)
    V = 100        # Volume of CSTR (m^3)
    rho = 1000     # Density of A-B Mixture (kg/m^3)
    Cp = 0.239     # Heat capacity of A-B Mixture (J/kg-K)
    mdelH = 5e4    # Heat of reaction for A->B (J/mol)
    EoverR = 8750  # Activation energy (J/mol) / Universal Gas Constant = 8.31451 J/mol-K
    k0 = 7.2e10    # Pre-exponential factor (1/sec)
    UA = 5e4       # U - Overall Heat Transfer Coefficient (W/m^2-K) * A - Area (m^2)
    
    rA = k0*np.exp(-EoverR/T)*Ca  # reaction rate
    dCadt = q/V*(Caf - Ca) - rA   # concentration derivative
    dTdt = q/V*(Tf - T) + mdelH/(rho*Cp)*rA + UA/V/rho/Cp*(Tc-T)  # temperature derivative
    xdot = np.array([dCadt, dTdt])  # return xdot

    return xdot
