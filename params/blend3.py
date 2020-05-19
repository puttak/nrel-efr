"""
Parameters for the Blend3 feedstock in the entrained flow reactor.

`ultimate_analysis` = [C, H, O, N, S, ash, moisture]
"""

# Blend3 feedstock

feedstock = {
    'name': 'Blend3',

    'ultimate_analysis': [49.52, 5.28, 38.35, 0.15, 0.02, 0.64, 6.04],

    'chemical_analysis': {
        'acetyl': 1.59,
        'arabinan': 1.4,
        'ethanol_extractives': 3.49,
        'free_fructose': 0.07,
        'free_glucose': 0.04,
        'galactan': 3.16,
        'glucan': 38.95,
        'lignin': 29.48,
        'mannan': 10.52,
        'nonstructural_inorganics': 0.22,
        'structural_inorganics': 0.41,
        'sucrose': 0.04,
        'water_extractives': 2.75,
        'xylan': 7.89
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

# Entrained flow reactor (EFR)

reactor = {
    'name': 'Entrained flow reactor (EFR)',
    'pressure': 101_325.0,
    'temperature': 773.15,
    'time_max': 10.0
}
