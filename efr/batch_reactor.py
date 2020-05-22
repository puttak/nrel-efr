import cantera as ct
import logging
import matplotlib.pyplot as plt
import numpy as np


def _config(ax, xlabel, ylabel):
    """
    Configure and style the plot figure.
    """
    ax.grid(True, color='0.9')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
    ax.set_frame_on(False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(color='0.9')


def _plot_initial_concs(states):
    """
    Plot initial concentrations.
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(states.t, states('CELL').Y[:, 0], label='CELL')
    ax.plot(states.t, states('GMSW').Y[:, 0], label='GMSW')
    ax.plot(states.t, states('LIGC').Y[:, 0], label='LIGC')
    ax.plot(states.t, states('LIGH').Y[:, 0], label='LIGH')
    ax.plot(states.t, states('LIGO').Y[:, 0], label='LIGO')
    ax.plot(states.t, states('TANN').Y[:, 0], label='TANN')
    ax.plot(states.t, states('TGL').Y[:, 0], label='TGL')
    _config(ax, xlabel='Time [s]', ylabel='Mass fraction [-]')


def _plot_solids(states, sp_solids):
    """
    Plot solids concentrations.
    """
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(10, 4.8), tight_layout=True)
    ax1.plot(states.t, states('CELL').Y[:, 0], label='CELL')
    ax1.plot(states.t, states('CELLA').Y[:, 0], label='CELLA')
    ax1.plot(states.t, states('GMSW').Y[:, 0], label='GMSW')
    ax1.plot(states.t, states('HCE1').Y[:, 0], label='HCE1')
    ax1.plot(states.t, states('HCE2').Y[:, 0], label='HCE2')
    ax1.plot(states.t, states('ITANN').Y[:, 0], label='ITANN')
    ax1.plot(states.t, states('LIG').Y[:, 0], label='LIG')
    ax1.plot(states.t, states('LIGC').Y[:, 0], label='LIGC')
    ax2.plot(states.t, states('LIGCC').Y[:, 0], label='LIGCC')
    ax2.plot(states.t, states('LIGH').Y[:, 0], label='LIGH')
    ax2.plot(states.t, states('LIGO').Y[:, 0], label='LIGO')
    ax2.plot(states.t, states('LIGOH').Y[:, 0], label='LIGOH')
    ax2.plot(states.t, states('TANN').Y[:, 0], label='TANN')
    ax2.plot(states.t, states('TGL').Y[:, 0], label='TGL')
    ax2.plot(states.t, states('CHAR').Y[:, 0], label='CHAR')
    _config(ax1, xlabel='Time [s]', ylabel='Mass fraction [-]')
    _config(ax2, xlabel='Time [s]', ylabel='')

    ys = [states(sp).Y[:, 0][-1] for sp in sp_solids]
    ypos = np.arange(len(sp_solids))

    fig, ax = plt.subplots(tight_layout=True)
    ax.barh(ypos, ys, align='center')
    ax.set_xlabel('Mass fraction [-]')
    ax.set_ylim(min(ypos) - 1, max(ypos) + 1)
    ax.set_yticks(ypos)
    ax.set_yticklabels(sp_solids)
    ax.invert_yaxis()
    ax.set_axisbelow(True)
    ax.set_frame_on(False)
    ax.tick_params(color='0.8')
    ax.xaxis.grid(True, color='0.8')


def _plot_metaplastics(states, sp_metaplastics):
    """
    Plot metaplastic concentrations.
    """
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(10, 4.8), tight_layout=True)
    ax1.plot(states.t, states('GCH2O').Y[:, 0], label='GCH2O')
    ax1.plot(states.t, states('GCO2').Y[:, 0], label='GCO2')
    ax1.plot(states.t, states('GCO').Y[:, 0], label='GCO')
    ax1.plot(states.t, states('GCH3OH').Y[:, 0], label='GCH3OH')
    ax1.plot(states.t, states('GCH4').Y[:, 0], label='GCH4')
    ax2.plot(states.t, states('GC2H4').Y[:, 0], label='GC2H4')
    ax2.plot(states.t, states('GC6H5OH').Y[:, 0], label='GC6H5OH')
    ax2.plot(states.t, states('GCOH2').Y[:, 0], label='GCOH2')
    ax2.plot(states.t, states('GH2').Y[:, 0], label='GH2')
    ax2.plot(states.t, states('GC2H6').Y[:, 0], label='GC2H6')
    _config(ax1, xlabel='Time [s]', ylabel='Mass fraction [-]')
    _config(ax2, xlabel='Time [s]', ylabel='')

    ys = [states(sp).Y[:, 0][-1] for sp in sp_metaplastics]
    ypos = np.arange(len(sp_metaplastics))

    fig, ax = plt.subplots(tight_layout=True)
    ax.barh(ypos, ys, align='center')
    ax.set_xlabel('Mass fraction [-]')
    ax.set_ylim(min(ypos) - 1, max(ypos) + 1)
    ax.set_yticks(ypos)
    ax.set_yticklabels(sp_metaplastics)
    ax.invert_yaxis()
    ax.set_axisbelow(True)
    ax.set_frame_on(False)
    ax.tick_params(color='0.8')
    ax.xaxis.grid(True, color='0.8')


def _plot_phases(states, y_gases, y_liquids, y_solids, y_metaplastics):
    """
    Plot phases such as gases, liquids, solids, and metaplastics.
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(states.t, y_gases, label='gases')
    ax.plot(states.t, y_liquids, label='liquids')
    ax.plot(states.t, y_solids, label='solids')
    ax.plot(states.t, y_metaplastics, label='metaplastics')
    _config(ax, xlabel='Time [s]', ylabel='Mass fraction [-]')


def _plot_temperature(states):
    """
    Plot temperature.
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(states.t, states.T)
    ax.grid(True, color='0.9')
    ax.set_frame_on(False)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Temperature [K]')
    ax.tick_params(color='0.9')


def batch_reactor(reactor, bc):
    """
    Batch reactor yields using Debiagi 2018 kinetics for softwood.

    Parameters
    ----------
    reactor : dict
        Reactor parameters.
    bc : dict
        Biomass composition.
    """

    # CTI file for softwood Debiagi 2015 kinetics
    cti_file = 'efr/debiagi_sw.cti'

    # get reactor parameters
    tmax = reactor['time_max']
    temp = reactor['temperature']
    press = reactor['pressure']

    # biomass composition as mass fraction inputs to batch reactor
    y_fracs = {
        'CELL': bc['cellulose'],
        'GMSW': bc['hemicellulose'],
        'LIGC': bc['lignin-c'],
        'LIGH': bc['lignin-h'],
        'LIGO': bc['lignin-o'],
        'TANN': bc['tannins'],
        'TGL': bc['triglycerides']
    }

    # time vector to evaluate reaction rates [s]
    time = np.linspace(0, tmax, 100)

    # disable warnings about discontinuity at polynomial mid-point in thermo data
    # comment this line to show the warnings
    ct.suppress_thermo_warnings()

    gas = ct.Solution(cti_file)

    gas.TPY = temp, press, y_fracs
    r = ct.IdealGasReactor(gas, energy='off')

    sim = ct.ReactorNet([r])
    states = ct.SolutionArray(gas, extra=['t'])

    for tm in time:
        sim.advance(tm)
        states.append(r.thermo.state, t=tm)

    # species representing gases
    sp_gases = ('C2H4', 'C2H6', 'CH2O', 'CH4', 'CO', 'CO2', 'H2')

    # species representing liquids (tars)
    sp_liquids = (
        'C2H3CHO', 'C2H5CHO', 'C2H5OH', 'C5H8O4', 'C6H10O5', 'C6H5OCH3', 'C6H5OH',
        'C6H6O3', 'C24H28O4', 'CH2OHCH2CHO', 'CH2OHCHO', 'CH3CHO', 'CH3CO2H',
        'CH3OH', 'CHOCHO', 'CRESOL', 'FURFURAL', 'H2O', 'HCOOH', 'MLINO', 'U2ME12',
        'VANILLIN', 'ACQUA'
    )

    # species representing solids
    sp_solids = (
        'CELL', 'CELLA', 'GMSW', 'HCE1', 'HCE2', 'ITANN', 'LIG', 'LIGC', 'LIGCC',
        'LIGH', 'LIGO', 'LIGOH', 'TANN', 'TGL', 'CHAR'
    )

    # species representing metaplastics
    sp_metaplastics = (
        'GCH2O', 'GCO2', 'GCO', 'GCH3OH', 'GCH4', 'GC2H4', 'GC6H5OH', 'GCOH2',
        'GH2', 'GC2H6'
    )

    # sum of species mass fractions for gases, liquids, solids, metaplastics
    y_gases = states(*sp_gases).Y.sum(axis=1)
    y_liquids = states(*sp_liquids).Y.sum(axis=1)
    y_solids = states(*sp_solids).Y.sum(axis=1)
    y_metaplastics = states(*sp_metaplastics).Y.sum(axis=1)

    # log results to console
    results = (
        f'{" Batch reactor yields ":-^80}\n\n'
        f'pressure    = {press} Pa\n'
        f'temperature = {temp} K\n'
        f'time max    = {tmax} s\n\n'
        f'              % mass\n'
        f'gases         {y_gases[-1] * 100:.2f}\n'
        f'liquids       {y_liquids[-1] * 100:.2f}\n'
        f'solids        {y_solids[-1] * 100:.2f}\n'
        f'metaplastics  {y_metaplastics[-1] * 100:.2f}\n'
    )

    logging.info(results)

    # plot results
    _plot_initial_concs(states)
    _plot_solids(states, sp_solids)
    _plot_metaplastics(states, sp_metaplastics)
    _plot_phases(states, y_gases, y_liquids, y_solids, y_metaplastics)
    _plot_temperature(states)
