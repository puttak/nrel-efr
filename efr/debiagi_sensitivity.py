import cantera as ct
import logging
import numpy as np
import matplotlib.pyplot as plt

from SALib.sample import saltelli
from SALib.analyze import sobol


def _run_batch_reactor(y, tmax):
    """
    here
    """

    # disable warnings about polynomial mid-point discontinuity in thermo data
    ct.suppress_thermo_warnings()

    # time vector to evaluate reaction rates [s]
    time = np.linspace(0, tmax, 100)

    gas = ct.Solution('efr/debiagi_sw.cti')

    gas.TPY = 773.15, 101325.0, y

    r = ct.IdealGasReactor(gas, energy='off')

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


def debiagi_sa(reactor):
    """
    Sensitivity analysis of Debiagi 2018 pyrolysis kinetics.

    Parameters
    ----------
    reactor : dict
        Reactor parameters.
    """
    problem = {
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

    # number of samples to generate for sensitivity analysis
    n = 10

    # get reactor parameters
    tmax = reactor['time_duration']

    # generate samples from model inputs defined in `problem`
    param_values = saltelli.sample(problem, n)

    # store outputs
    y_out = np.zeros([param_values.shape[0], 3])

    for i, p in enumerate(param_values):
        keys = problem['names']
        y = dict(zip(keys, p))
        y_out[i] = _run_batch_reactor(y, tmax)

    # perform sobol analysis for gas, liquid, and solid phase
    si_gas = sobol.analyze(problem, y_out[:, 0])
    si_liquid = sobol.analyze(problem, y_out[:, 1])
    si_solid = sobol.analyze(problem, y_out[:, 2])

    # log results to console
    results1 = (
        f'{" Sensitivity analysis of Debiagi 2018 kinetics ":-^80}\n\n'
        f'n         = {n}\n'
        f'shape     = {param_values.shape}\n'
        f'samples   = {param_values.shape[0]}\n'
    )
    logging.info(results1)

    results2 = (
        f'{" Sobol analysis (gases) ":-^80}\n\n'
        f'{"Parameter":10} {"S1":>10} {"S1_conf":>10} {"ST":>10} {"ST_conf":>10}'
    )
    logging.info(results2)

    for i, name in enumerate(problem['names']):
        s1 = si_gas['S1'][i]
        s1conf = si_gas['S1_conf'][i]
        st = si_gas['ST'][i]
        stconf = si_gas['ST_conf'][i]
        logging.info(f'{name:10} {s1:10.4f} {s1conf:10.4f} {st:10.4f} {stconf:10.4f}')

    results3 = (
        f'\n{" Sobol analysis (liquids) ":-^80}\n\n'
        f'{"Parameter":10} {"S1":>10} {"S1_conf":>10} {"ST":>10} {"ST_conf":>10}'
    )
    logging.info(results3)

    for i, name in enumerate(problem['names']):
        s1 = si_liquid['S1'][i]
        s1conf = si_liquid['S1_conf'][i]
        st = si_liquid['ST'][i]
        stconf = si_liquid['ST_conf'][i]
        logging.info(f'{name:10} {s1:10.4f} {s1conf:10.4f} {st:10.4f} {stconf:10.4f}')

    results4 = (
        f'\n{" Sobol analysis (solids) ":-^80}\n\n'
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

    # cellulose
    axs[0, 0].scatter(param_values[:, 0], y_out[:, 0], s=20, alpha=0.5, color='C0', edgecolors='none')
    axs[0, 0].set_xlabel('CELL')
    axs[0, 0].set_ylabel('Gas')

    axs[1, 0].scatter(param_values[:, 0], y_out[:, 1], s=20, alpha=0.5, color='C0', edgecolors='none')
    axs[1, 0].set_xlabel('CELL')
    axs[1, 0].set_ylabel('Liquid')

    axs[2, 0].scatter(param_values[:, 0], y_out[:, 2], s=20, alpha=0.5, color='C0', edgecolors='none')
    axs[2, 0].set_xlabel('CELL')
    axs[2, 0].set_ylabel('Solid')

    # hemicellulose
    axs[0, 1].scatter(param_values[:, 1], y_out[:, 0], s=20, alpha=0.5, color='C1', edgecolors='none')
    axs[0, 1].set_xlabel('GMSW')
    axs[0, 1].set_ylabel('Gas')

    axs[1, 1].scatter(param_values[:, 1], y_out[:, 1], s=20, alpha=0.5, color='C1', edgecolors='none')
    axs[1, 1].set_xlabel('GMSW')
    axs[1, 1].set_ylabel('Liquid')

    axs[2, 1].scatter(param_values[:, 1], y_out[:, 2], s=20, alpha=0.5, color='C1', edgecolors='none')
    axs[2, 1].set_xlabel('GMSW')
    axs[2, 1].set_ylabel('Solid')

    # lignin-c
    axs[0, 2].scatter(param_values[:, 2], y_out[:, 0], s=20, alpha=0.5, color='C2', edgecolors='none')
    axs[0, 2].set_xlabel('LIGC')
    axs[0, 2].set_ylabel('Gas')

    axs[1, 2].scatter(param_values[:, 2], y_out[:, 1], s=20, alpha=0.5, color='C2', edgecolors='none')
    axs[1, 2].set_xlabel('LIGC')
    axs[1, 2].set_ylabel('Liquid')

    axs[2, 2].scatter(param_values[:, 2], y_out[:, 2], s=20, alpha=0.5, color='C2', edgecolors='none')
    axs[2, 2].set_xlabel('LIGC')
    axs[2, 2].set_ylabel('Solid')

    # lignin-h
    axs[0, 3].scatter(param_values[:, 3], y_out[:, 0], s=20, alpha=0.5, color='C3', edgecolors='none')
    axs[0, 3].set_xlabel('LIGH')
    axs[0, 3].set_ylabel('Gas')

    axs[1, 3].scatter(param_values[:, 3], y_out[:, 1], s=20, alpha=0.5, color='C3', edgecolors='none')
    axs[1, 3].set_xlabel('LIGH')
    axs[1, 3].set_ylabel('Liquid')

    axs[2, 3].scatter(param_values[:, 3], y_out[:, 2], s=20, alpha=0.5, color='C3', edgecolors='none')
    axs[2, 3].set_xlabel('LIGH')
    axs[2, 3].set_ylabel('Solid')

    # --- Figure 2 ---
    fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(10, 8), tight_layout=True)

    # lignin-o
    axs[0, 0].scatter(param_values[:, 4], y_out[:, 0], s=20, alpha=0.5, color='C4', edgecolors='none')
    axs[0, 0].set_xlabel('LIGO')
    axs[0, 0].set_ylabel('Gas')

    axs[1, 0].scatter(param_values[:, 4], y_out[:, 1], s=20, alpha=0.5, color='C4', edgecolors='none')
    axs[1, 0].set_xlabel('LIGO')
    axs[1, 0].set_ylabel('Liquid')

    axs[2, 0].scatter(param_values[:, 4], y_out[:, 2], s=20, alpha=0.5, color='C4', edgecolors='none')
    axs[2, 0].set_xlabel('LIGO')
    axs[2, 0].set_ylabel('Solid')

    # tann
    axs[0, 1].scatter(param_values[:, 5], y_out[:, 0], s=20, alpha=0.5, color='C5', edgecolors='none')
    axs[0, 1].set_xlabel('TANN')
    axs[0, 1].set_ylabel('Gas')

    axs[1, 1].scatter(param_values[:, 5], y_out[:, 1], s=20, alpha=0.5, color='C5', edgecolors='none')
    axs[1, 1].set_xlabel('TANN')
    axs[1, 1].set_ylabel('Liquid')

    axs[2, 1].scatter(param_values[:, 5], y_out[:, 2], s=20, alpha=0.5, color='C5', edgecolors='none')
    axs[2, 1].set_xlabel('TANN')
    axs[2, 1].set_ylabel('Solid')

    # tgl
    axs[0, 2].scatter(param_values[:, 6], y_out[:, 0], s=20, alpha=0.5, color='C6', edgecolors='none')
    axs[0, 2].set_xlabel('TGL')
    axs[0, 2].set_ylabel('Gas')

    axs[1, 2].scatter(param_values[:, 6], y_out[:, 1], s=20, alpha=0.5, color='C6', edgecolors='none')
    axs[1, 2].set_xlabel('TGL')
    axs[1, 2].set_ylabel('Liquid')

    axs[2, 2].scatter(param_values[:, 6], y_out[:, 2], s=20, alpha=0.5, color='C6', edgecolors='none')
    axs[2, 2].set_xlabel('TGL')
    axs[2, 2].set_ylabel('Solid')

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
    ax1.set_ylabel('Sensitivity')
    ax1.set_title('Gas')
    ax1.set_xticks(x)
    ax1.set_xticklabels(problem['names'])
    bar_style(ax1)

    ax2.bar(x - width / 2, si_liquid['S1'], width, label='S1')
    ax2.bar(x + width / 2, si_liquid['ST'], width, label='ST')
    ax2.set_title('Liquid')
    ax2.set_xlabel('Parameter')
    ax2.set_xticks(x)
    ax2.set_xticklabels(problem['names'])
    bar_style(ax2)

    ax3.bar(x - width / 2, si_solid['S1'], width, label='S1')
    ax3.bar(x + width / 2, si_solid['ST'], width, label='ST')
    ax3.legend(loc='best')
    ax3.set_title('Solid')
    ax3.set_xticks(x)
    ax3.set_xticklabels(problem['names'])
    bar_style(ax3)
