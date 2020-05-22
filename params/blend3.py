"""
Parameters for the Blend3 feedstock in the entrained flow reactor.

`ultimate_analysis` is [C, H, O, N, S, ash, moisture]
`chemical_analysis` is dry ash-free basis (% daf)
"""

# Blend3 feedstock

feedstock = {
    'name': 'Blend3',

    'ultimate_analysis': [49.52, 5.28, 38.35, 0.15, 0.02, 0.64, 6.04],

    'chemical_analysis': {
        'cellulose': 39.19,
        'hemicellulose': 24.71,
        'lignin_c': 0.00,
        'lignin_h': 14.83,
        'lignin_o': 14.83,
        'tannins': 0.00,
        'triglycerides': 6.43
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
    'time_duration': 10.0
}
