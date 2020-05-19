import chemics as cm
import logging


def bc_charact_params(feedstock):
    """
    Biomass composition based on characterization method discussed in Debiagi
    2015 paper. Uses the given values for yc, yh, alpha, beta, gamma, delta,
    and epsilon from the parameters file.

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
