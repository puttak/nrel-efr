import cantera as ct
import logging
import numpy as np
import matplotlib.pyplot as plt

from SALib.sample import saltelli
from SALib.analyze import sobol


def _run_batch_reactor(y, reactor):
    """
    Run batch reactor for sensitivity analysis.

    Parameters
    ----------
    y : dict
        Initial biomass composition for CELL, GMSW, LIGC, LIGH, LIGO, TANN,
        and TGL.
    reactor : dict
        Reactor parameters.

    Returns
    -------
    tuple
        Final mass fraction of y_gases, y_liquids, and y_solids for a given
        time duration.
    """

    # disable warnings about polynomial mid-point discontinuity in thermo data
    ct.suppress_thermo_warnings()

    # get reactor parameters
    tmax = reactor['time_duration']

    # get reactor parameters
    tmax = reactor['time_duration']
    temp = reactor['temperature']
    press = reactor['pressure']
    energy = reactor['energy']

    # get CTI file for Debiagi 2018 kinetics for softwood
    cti_file = 'efr/debiagi_sw.cti'

    # time vector to evaluate reaction rates [s]
    time = np.linspace(0, tmax, 100)

    gas = ct.Solution(cti_file)

    gas.TPY = temp, press, y

    r = ct.IdealGasReactor(gas, energy=energy)

    sim = ct.ReactorNet([r])
    states = ct.SolutionArray(gas, extra=['t'])

    for tm in time:
        sim.advance(tm)
        states.append(r.thermo.state, t=tm)

    # species representing gases
    sp_gases = ('C2H4', 'C2H6', 'CH2O', 'CH4', 'CO', 'CO2', 'H2')

    # species representing liquids
    sp_liquids = (
        'C2H3CHO', 'C2H5CHO', 'C2H5OH', 'C5H8O4', 'C6H10O5', 'C6H5OCH3', 'C6H5OH',
        'C6H6O3', 'C24H28O4', 'CH2OHCH2CHO', 'CH2OHCHO', 'CH3CHO', 'CH3CO2H',
        'CH3OH', 'CHOCHO', 'CRESOL', 'FURFURAL', 'H2O', 'HCOOH', 'MLINO', 'U2ME12',
        'VANILLIN', 'ACQUA'
    )

    # species representing solids
    sp_solids = (
        'CELL', 'CELLA', 'GMSW', 'HCE1', 'HCE2', 'ITANN', 'LIG', 'LIGC', 'LIGCC',
        'LIGH', 'LIGO', 'LIGOH', 'TANN', 'TGL', 'CHAR', 'GCH2O', 'GCO2', 'GCO',
        'GCH3OH', 'GCH4', 'GC2H4', 'GC6H5OH', 'GCOH2', 'GH2', 'GC2H6'
    )

    # sum of gases, liquids, and solids mass fractions
    y_gases = states(*sp_gases).Y.sum(axis=1)
    y_liquids = states(*sp_liquids).Y.sum(axis=1)
    y_solids = states(*sp_solids).Y.sum(axis=1)

    # return final mass fractions
    return y_gases[-1], y_liquids[-1], y_solids[-1]


def debiagi_sa(reactor, sens_analysis):
    """
    Perform a sensitivity analysis of the Debiagi 2018 pyrolysis kinetics
    using the Sobol method.

    Parameters
    ----------
    reactor : dict
        Reactor parameters.
    sens_analysis : dict
        Sensitivity analysis parameters.

    Notes
    -----
    S1 is the first-order sensitivity indices. S1_conf is the first-order
    confidence (can be interpreted as error). ST is the total-order indices
    while ST_conf is total-order confidence.
    """

    # number of samples to generate for sensitivity analysis
    n = sens_analysis['n_samples']

    # define problem for sensitivity analysis
    problem = {
        'num_vars': sens_analysis['num_vars'],
        'names': sens_analysis['names'],
        'bounds': sens_analysis['bounds']
    }

    # generate samples using Saltelli’s sampling scheme
    param_values = saltelli.sample(problem, n)

    # store outputs from batch reactor where each row of
    # y_out is [y_gases, y_liquids, y_solids]
    y_out = np.zeros([param_values.shape[0], 3])

    for i, p in enumerate(param_values):
        keys = problem['names']
        y = dict(zip(keys, p))
        y_out[i] = _run_batch_reactor(y, reactor)

    # parallel options for Sobol analysis

    # perform Sobol analysis for gas, liquid, and solid phases
    si_gas = sobol.analyze(problem, y_out[:, 0])
    si_liquid = sobol.analyze(problem, y_out[:, 1])
    si_solid = sobol.analyze(problem, y_out[:, 2])

    # log sensitivity analysis parameters to console
    results1 = (
        f'{" Sensitivity analysis of Debiagi 2018 kinetics ":-^80}\n\n'
        f'n         = {n:,}\n'
        f'shape     = {param_values.shape}\n'
        f'samples   = {param_values.shape[0]:,}\n'
    )
    logging.info(results1)

    # log results for gases to console
    results2 = (
        f'Sobol analysis for gases\n\n'
        f'{"Parameter":10} {"S1":>10} {"S1_conf":>10} {"ST":>10} {"ST_conf":>10}'
    )
    logging.info(results2)

    for i, name in enumerate(problem['names']):
        s1 = si_gas['S1'][i]
        s1conf = si_gas['S1_conf'][i]
        st = si_gas['ST'][i]
        stconf = si_gas['ST_conf'][i]
        logging.info(f'{name:10} {s1:10.4f} {s1conf:10.4f} {st:10.4f} {stconf:10.4f}')

    # log results for liquids to console
    results3 = (
        f'\nSobol analysis for liquids\n\n'
        f'{"Parameter":10} {"S1":>10} {"S1_conf":>10} {"ST":>10} {"ST_conf":>10}'
    )
    logging.info(results3)

    for i, name in enumerate(problem['names']):
        s1 = si_liquid['S1'][i]
        s1conf = si_liquid['S1_conf'][i]
        st = si_liquid['ST'][i]
        stconf = si_liquid['ST_conf'][i]
        logging.info(f'{name:10} {s1:10.4f} {s1conf:10.4f} {st:10.4f} {stconf:10.4f}')

    # log results for solids to console
    results4 = (
        f'\nSobol analysis for solids\n\n'
        f'{"Parameter":10} {"S1":>10} {"S1_conf":>10} {"ST":>10} {"ST_conf":>10}'
    )
    logging.info(results4)

    for i, name in enumerate(problem['names']):
        s1 = si_solid['S1'][i]
        s1conf = si_solid['S1_conf'][i]
        st = si_solid['ST'][i]
        stconf = si_solid['ST_conf'][i]
        logging.info(f'{name:10} {s1:10.4f} {s1conf:10.4f} {st:10.4f} {stconf:10.4f}')

    # --- Figure 1 ---
    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(13.5, 8), tight_layout=True)

    # cellulose for rows 0, 1, 2 and column 0
    for i, g in enumerate(['Gases', 'Liquids', 'Solids']):
        hb = axs[i, 0].hexbin(param_values[:, 0], y_out[:, i], gridsize=50, cmap='viridis')
        axs[i, 0].axis([param_values[:, 0].min(), param_values[:, 0].max(), y_out[:, i].min(), y_out[:, i].max()])
        axs[i, 0].set_xlabel('CELL')
        axs[i, 0].set_ylabel(g)
        fig.colorbar(hb, ax=axs[i, 0])     # colorbar represents counts

    # hemicellulose for rows 0, 1, 2 and column 1
    for i, g in enumerate(['Gases', 'Liquids', 'Solids']):
        hb = axs[i, 1].hexbin(param_values[:, 1], y_out[:, i], gridsize=50, cmap='viridis')
        axs[i, 1].axis([param_values[:, 1].min(), param_values[:, 1].max(), y_out[:, i].min(), y_out[:, i].max()])
        axs[i, 1].set_xlabel('GMSW')
        axs[i, 1].set_ylabel(g)
        fig.colorbar(hb, ax=axs[i, 1])

    # lignin-c for rows 0, 1, 2 and column 2
    for i, g in enumerate(['Gases', 'Liquids', 'Solids']):
        hb = axs[i, 2].hexbin(param_values[:, 2], y_out[:, i], gridsize=50, cmap='viridis')
        axs[i, 2].axis([param_values[:, 2].min(), param_values[:, 2].max(), y_out[:, i].min(), y_out[:, i].max()])
        axs[i, 2].set_xlabel('LIGC')
        axs[i, 2].set_ylabel(g)
        fig.colorbar(hb, ax=axs[i, 2])

    # lignin-h for rows 0, 1, 2 and column 3
    for i, g in enumerate(['Gases', 'Liquids', 'Solids']):
        hb = axs[i, 3].hexbin(param_values[:, 3], y_out[:, i], gridsize=50, cmap='viridis')
        axs[i, 3].axis([param_values[:, 3].min(), param_values[:, 3].max(), y_out[:, i].min(), y_out[:, i].max()])
        axs[i, 3].set_xlabel('LIGH')
        axs[i, 3].set_ylabel(g)
        fig.colorbar(hb, ax=axs[i, 3])

    # --- Figure 2 ---
    fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(10, 8), tight_layout=True)

    # lignin-o for rows 0, 1, 2 and column 0
    for i, g in enumerate(['Gases', 'Liquids', 'Solids']):
        hb = axs[i, 0].hexbin(param_values[:, 4], y_out[:, i], gridsize=50, cmap='viridis')
        axs[i, 0].axis([param_values[:, 4].min(), param_values[:, 4].max(), y_out[:, i].min(), y_out[:, i].max()])
        axs[i, 0].set_xlabel('LIGO')
        axs[i, 0].set_ylabel(g)
        fig.colorbar(hb, ax=axs[i, 0])     # colorbar represents counts

    # tann for rows 0, 1, 2 and column 1
    for i, g in enumerate(['Gases', 'Liquids', 'Solids']):
        hb = axs[i, 1].hexbin(param_values[:, 5], y_out[:, i], gridsize=50, cmap='viridis')
        axs[i, 1].axis([param_values[:, 5].min(), param_values[:, 5].max(), y_out[:, i].min(), y_out[:, i].max()])
        axs[i, 1].set_xlabel('TANN')
        axs[i, 1].set_ylabel(g)
        fig.colorbar(hb, ax=axs[i, 1])

    # tgl for rows 0, 1, 2 and column 2
    for i, g in enumerate(['Gases', 'Liquids', 'Solids']):
        hb = axs[i, 2].hexbin(param_values[:, 6], y_out[:, i], gridsize=50, cmap='viridis')
        axs[i, 2].axis([param_values[:, 6].min(), param_values[:, 6].max(), y_out[:, i].min(), y_out[:, i].max()])
        axs[i, 2].set_xlabel('TGL')
        axs[i, 2].set_ylabel(g)
        fig.colorbar(hb, ax=axs[i, 2])

    # --- Figure 3 ---
    x = np.arange(len(problem['names']))
    width = 0.35

    def bar_style(ax):
        ax.grid(True, color='0.9')
        ax.set_axisbelow(True)
        ax.set_frame_on(False)
        ax.tick_params(color='0.9')

    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(13, 4.8), sharey=True, tight_layout=True)

    ax1.bar(x - width / 2, si_gas['S1'], width, label='S1')
    ax1.bar(x + width / 2, si_gas['ST'], width, label='ST')
    ax1.errorbar(x - width / 2, si_gas['S1'], yerr=si_gas['S1_conf'], fmt='k.')
    ax1.errorbar(x + width / 2, si_gas['ST'], yerr=si_gas['ST_conf'], fmt='k.')
    ax1.set_ylabel('Sensitivity')
    ax1.set_title('Gases')
    ax1.set_xticks(x)
    ax1.set_xticklabels(problem['names'])
    bar_style(ax1)

    ax2.bar(x - width / 2, si_liquid['S1'], width, label='S1')
    ax2.bar(x + width / 2, si_liquid['ST'], width, label='ST')
    ax2.errorbar(x - width / 2, si_liquid['S1'], yerr=si_liquid['S1_conf'], fmt='k.')
    ax2.errorbar(x + width / 2, si_liquid['ST'], yerr=si_liquid['ST_conf'], fmt='k.')
    ax2.set_title('Liquids')
    ax2.set_xlabel('Parameter')
    ax2.set_xticks(x)
    ax2.set_xticklabels(problem['names'])
    bar_style(ax2)

    ax3.bar(x - width / 2, si_solid['S1'], width, label='S1')
    ax3.bar(x + width / 2, si_solid['ST'], width, label='ST')
    ax3.errorbar(x - width / 2, si_solid['S1'], yerr=si_solid['S1_conf'], fmt='k.')
    ax3.errorbar(x + width / 2, si_solid['ST'], yerr=si_solid['ST_conf'], fmt='k.')
    ax3.legend(loc='best')
    ax3.set_title('Solids')
    ax3.set_xticks(x)
    ax3.set_xticklabels(problem['names'])
    bar_style(ax3)
