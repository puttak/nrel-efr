"""
Blend3 feedstock parameters.

ultimate_analysis : list
    Elements listed as [C, H, O, N, S, ash, moisture]

chemical_analysis : dict
    Biomass composition determined from chemical analysis data. These values
    are used for the pyrolysis kinetics. Values are given as mass fraction (-)
    on dry ash-free basis (% daf).
"""

feedstock = {
    'name': 'Blend3',

    'ultimate_analysis': [49.52, 5.28, 38.35, 0.15, 0.02, 0.64, 6.04],

    'chemical_analysis': {
        'cellulose': 39.19,
        'hemicellulose': 23.26,
        'lignin_c': 9.89,
        'lignin_h': 9.89,
        'lignin_o': 9.89,
        'tannins': 7.88,
        'triglycerides': 0.00
    },

    'biomass_characterization': {
        'yc': 0.51,
        'yh': 0.06,
        'alpha': 0.56,
        'beta': 0.6,
        'gamma': 0.6,
        'delta': 0.78,
        'epsilon': 0.88
    }
}

"""
Entrained flow reactor (EFR) parameters.

energy : str
    Used by the Cantera reactor model. If set to `off` then disable the energy
    equation. If `on` then enable the energy and use the provided thermo data
    for the reactions.
"""

reactor = {
    'name': 'Entrained flow reactor (EFR)',
    'pressure': 101_325.0,
    'temperature': 773.15,
    'time_duration': 10.0,
    'energy': 'on'
}

"""
Sensitivity analysis parameters for the Debiagi 2018 kinetics.
"""

sensitivity_analysis = {
    'n_samples': 10,
    'num_vars': 7,
    'names': ['CELL', 'GMSW', 'LIGC', 'LIGH', 'LIGO', 'TANN', 'TGL'],
    'bounds': [[0.01, 0.99],
               [0.01, 0.99],
               [0.01, 0.99],
               [0.01, 0.99],
               [0.01, 0.99],
               [0.01, 0.99],
               [0.01, 0.99]]
}
