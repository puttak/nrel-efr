import logging


def bc_chem_analysis(feedstock):
    """
    Biomass composition based on chemical analysis of the feedstock. Uses the
    chemical analysis data of the feedstock to determine the composition.

    Parameters
    ----------
    feedstock : dict
        Feedstock parameters.

    Returns
    -------
    bc_chem : dict
        Biomass composition.
    """

    # dry ash-free basis
    cell_daf = feedstock['chemical_analysis']['cellulose']
    hemi_daf = feedstock['chemical_analysis']['hemicellulose']
    ligc_daf = feedstock['chemical_analysis']['lignin_c']
    ligh_daf = feedstock['chemical_analysis']['lignin_h']
    ligo_daf = feedstock['chemical_analysis']['lignin_o']
    tann_daf = feedstock['chemical_analysis']['tannins']
    tgl_daf = feedstock['chemical_analysis']['triglycerides']
    sum_daf = cell_daf + hemi_daf + ligc_daf + ligh_daf + ligo_daf + tann_daf + tgl_daf

    # log results to console
    results = (
        f'{" Biomass composition based on chemical analysis (mass %) ":-^80}\n\n'
        f'Using chemical analysis data\n\n'
        f'                     % daf\n'
        f'cellulose         {cell_daf:8.2f}\n'
        f'hemicellulose     {hemi_daf:8.2f}\n'
        f'lignin-c          {ligc_daf:8.2f}\n'
        f'lignin-h          {ligh_daf:8.2f}\n'
        f'lignin-o          {ligo_daf:8.2f}\n'
        f'tannins           {tann_daf:8.2f}\n'
        f'triglycerides     {tgl_daf:8.2f}\n'
        f'sum               {sum_daf:8.2f}'
    )

    logging.info(results)

    # return daf results for use in reactor model
    bc_chem = {
        'cellulose': cell_daf,
        'hemicellulose': hemi_daf,
        'lignin-c': ligc_daf,
        'lignin-h': ligh_daf,
        'lignin-o': ligo_daf,
        'tannins': tann_daf,
        'triglycerides': tgl_daf
    }

    return bc_chem
