import chemics as cm
import logging


def _bc_chem_analysis(chem):
    """
    Biomass composition based on chemical analysis of the feedstock.

    Parameters
    ----------
    chem : dict
        Chemical analysis data.

    Returns
    -------
    biocomp : dict
        Biomass composition.
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

    # log results to console
    results = (
        f'{" Biomass composition based on chemical analysis (mass %) ":-^80}\n\n'
        f'Using chemical analysis data\n'
        f'cellulose     = glucan\n'
        f'hemicellulose = acetyl + arabinan + galactan + mannan + xylan\n'
        f'lignin-c      = none\n'
        f'lignin-h      = lignin / 2\n'
        f'lignin-o      = lignin / 2\n'
        f'tannins       = none\n'
        f'triglycerides = free fructose + free glucose + sucrose + ethanol extractives + water extractives\n'
        f'ash           = non-structural inorganics + structural inorganics\n\n'
        f'                     % dry    % daf\n'
        f'cellulose         {cell_dry:8.2f} {cell_daf:8.2f}\n'
        f'hemicellulose     {hemi_dry:8.2f} {hemi_daf:8.2f}\n'
        f'lignin-c          {ligc_dry:8.2f} {ligc_daf:8.2f}\n'
        f'lignin-h          {ligh_dry:8.2f} {ligh_daf:8.2f}\n'
        f'lignin-o          {ligo_dry:8.2f} {ligo_daf:8.2f}\n'
        f'tannins           {tann_dry:8.2f} {tann_daf:8.2f}\n'
        f'triglycerides     {tgl_dry:8.2f} {tgl_daf:8.2f}\n'
        f'ash               {ash_dry:8.2f}\n'
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


def _bc_characterization(feedstock):
    """
    Biomass composition based on characterization method discussed in Debiagi
    2015 paper.

    Parameters
    ----------
    feedstock : dict
        Feedstock parameters.

    Returns
    -------
    bc_charact : dict
        Biomass composition.
    """

    yc = feedstock['biomass_characterization']['yc']
    yh = feedstock['biomass_characterization']['yh']
    alpha = feedstock['biomass_characterization']['alpha']
    beta = feedstock['biomass_characterization']['beta']
    gamma = feedstock['biomass_characterization']['gamma']
    delta = feedstock['biomass_characterization']['delta']
    epsilon = feedstock['biomass_characterization']['epsilon']

    bc = cm.biocomp(yc, yh, yo=None, yh2o=0, yash=0, alpha=alpha,
                    beta=beta, gamma=gamma, delta=delta, epsilon=epsilon,
                    printcomp=False)

    # log results to console
    results = (
        f'{" Biomass composition from Debiagi 2015 characterization method (mass %) ":-^80}\n\n'
        f'Using yc, yh, alpha, beta, gamma, delta, epsilon from parameters file\n'
        f'yc = {yc:.2f}\n'
        f'yh = {yh:.2f}\n'
        f'𝜶  = {alpha:.2f}\n'
        f'𝜷  = {beta:.2f}\n'
        f'𝜸  = {gamma:.2f}\n'
        f'𝜹  = {delta:.2f}\n'
        f'𝜺  = {epsilon:.2f}\n\n'
        f'                     % daf\n'
        f'cellulose         {bc["y_daf"][0] * 100:8.2f}\n'
        f'hemicellulose     {bc["y_daf"][1] * 100:8.2f}\n'
        f'lignin-c          {bc["y_daf"][2] * 100:8.2f}\n'
        f'lignin-h          {bc["y_daf"][3] * 100:8.2f}\n'
        f'lignin-o          {bc["y_daf"][4] * 100:8.2f}\n'
        f'tannins           {bc["y_daf"][5] * 100:8.2f}\n'
        f'triglycerides     {bc["y_daf"][6] * 100:8.2f}\n'
    )

    logging.info(results)

    # return daf results for use in reactor model
    bc_charact = {
        'cellulose': bc["y_daf"][0],
        'hemicellulose': bc["y_daf"][1],
        'lignin-c': bc["y_daf"][2],
        'lignin-h': bc["y_daf"][3],
        'lignin-o': bc["y_daf"][4],
        'tannins': bc["y_daf"][5],
        'triglycerides': bc["y_daf"][6]
    }

    return bc_charact


def _bc_ult_analysis(ult_analysis):
    """
    Biomass composition based on characterization method discussed in Debiagi
    2015 paper.

    Parameters
    ----------
    ult_analysis : dict
        Ultimate analysis bases.

    Returns
    -------
    bc_ult : dict
        Biomass composition.
    """

    yc = ult_analysis['dafcho'][0] / 100
    yh = ult_analysis['dafcho'][1] / 100

    bc = cm.biocomp(yc, yh)

    # log results to console
    results = (
        f'{" Biomass composition from Debiagi 2015 characterization method (mass %) ":-^80}\n\n'
        f'Using yc, yh as determined from ultimate analysis\n'
        f'yc = {yc:.4f}\n'
        f'yh = {yh:.4f}\n\n'
        f'                     % daf\n'
        f'cellulose         {bc["y_daf"][0] * 100:8.2f}\n'
        f'hemicellulose     {bc["y_daf"][1] * 100:8.2f}\n'
        f'lignin-c          {bc["y_daf"][2] * 100:8.2f}\n'
        f'lignin-h          {bc["y_daf"][3] * 100:8.2f}\n'
        f'lignin-o          {bc["y_daf"][4] * 100:8.2f}\n'
        f'tannins           {bc["y_daf"][5] * 100:8.2f}\n'
        f'triglycerides     {bc["y_daf"][6] * 100:8.2f}\n'
    )

    logging.info(results)

    # return daf results for use in reactor model
    bc_ult = {
        'cellulose': bc["y_daf"][0],
        'hemicellulose': bc["y_daf"][1],
        'lignin-c': bc["y_daf"][2],
        'lignin-h': bc["y_daf"][3],
        'lignin-o': bc["y_daf"][4],
        'tannins': bc["y_daf"][5],
        'triglycerides': bc["y_daf"][6]
    }

    return bc_ult


def biomass_composition(feedstock, ult_analysis):
    """
    Biomass composition as dry ash-free basis (daf) in terms of cellulose,
    hemicellulose, lignin-c, lignin-h, lignin-o, tannins, and triglycerides.
    Method to determine compostion (from top priority to lowest):

        1. chemical analysis of feedstock

        2. characterization method from Debiagi 2015 using yc, yh, alpha,
        beta, gamma, delta, epsilon from parameters file

        3. characterization method from Debiagi 2015 using C and H from
        ultimate analysis

    Parameters
    ----------
    feedstock : dict
        Feedstock parameters.
    ult : dict
        Ultimate analysis bases.

    Returns
    -------
    bc : dict
        Biomass composition for use in reactor model.
    """

    if 'chemical_analysis' in feedstock:
        chem = feedstock['chemical_analysis']
        bc = _bc_chem_analysis(chem)
    elif 'biomass_characterization' in feedstock:
        bc = _bc_characterization(feedstock)
    else:
        bc = _bc_ult_analysis(ult_analysis)

    return bc
