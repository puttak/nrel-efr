import logging


def biocomp_chemical_analysis(chem):
    """
    Biomass composition based on chemical analysis.
    """

    # dry basis
    # assume all extractives are TGL for Blend3 feedstock
    cell_dry = chem['glucan']
    hemi_dry = chem['acetyl'] + chem['arabinan'] + chem['galactan'] + chem['mannan'] + chem['xylan']
    ligc_dry = 0.0
    ligh_dry = chem['lignin'] / 2
    ligo_dry = chem['lignin'] / 2
    tann_dry = 0.0
    tgl_dry = chem['free_fructose'] + chem['free_glucose'] + chem['sucrose'] + chem['ethanol_extractives'] + chem['water_extractives']
    ash_dry = chem['nonstructural_inorganics'] + chem['structural_inorganics']
    sum_dry = cell_dry + hemi_dry + ligc_dry + ligh_dry + ligo_dry + tann_dry + tgl_dry + ash_dry

    # dry ash-free basis
    cell_daf = 100 * cell_dry / (sum_dry - ash_dry)
    hemi_daf = 100 * hemi_dry / (sum_dry - ash_dry)
    ligc_daf = 100 * ligc_dry / (sum_dry - ash_dry)
    ligh_daf = 100 * ligh_dry / (sum_dry - ash_dry)
    ligo_daf = 100 * ligo_dry / (sum_dry - ash_dry)
    tann_daf = 100 * tann_dry / (sum_dry - ash_dry)
    tgl_daf = 100 * tgl_dry / (sum_dry - ash_dry)

    # log results
    results = (
        f'{" Biomass composition based on chemical analysis (mass %) ":-^80}\n\n'
        f'cellulose     = glucan\n'
        f'hemicellulose = acetyl + arabinan + galactan + mannan + xylan\n'
        f'lignin-c      = none\n'
        f'lignin-h      = lignin / 2\n'
        f'lignin-o      = lignin / 2\n'
        f'tann          = none\n'
        f'tgl           = free fructose + free glucose + sucrose + ethanol extractives + water extractives\n'
        f'ash           = non-structural inorganics + structural inorganics\n\n'
        f'                     % dry    % daf\n'
        f'cellulose         {cell_dry:8.2f} {cell_daf:8.2f}\n'
        f'hemicellulose     {hemi_dry:8.2f} {hemi_daf:8.2f}\n'
        f'lignin-c          {ligc_dry:8.2f} {ligc_daf:8.2f}\n'
        f'lignin-h          {ligh_dry:8.2f} {ligh_daf:8.2f}\n'
        f'lignin-o          {ligo_dry:8.2f} {ligo_daf:8.2f}\n'
        f'tann              {tann_dry:8.2f} {tann_daf:8.2f}\n'
        f'tgl               {tgl_dry:8.2f} {tgl_daf:8.2f}\n'
        f'ash               {ash_dry:8.2f}\n'
    )

    logging.info(results)
