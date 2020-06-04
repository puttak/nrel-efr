"""
Functions for creating batch reactor figures.
"""

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


def plot_sw_biocomp(states):
    """
    Plot concentrations representing the softwood biomass composition.
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


def plot_solids(states, sp_solids):
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


def plot_metaplastics(states, sp_metaplastics):
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


def plot_phases(states, y_gases, y_liquids, y_solids, y_metaplastics):
    """
    Plot phases such as gases, liquids, solids, and metaplastics.
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(states.t, y_gases, label='gases')
    ax.plot(states.t, y_liquids, label='liquids')
    ax.plot(states.t, y_solids, label='solids')
    ax.plot(states.t, y_metaplastics, label='metaplastics')
    _config(ax, xlabel='Time [s]', ylabel='Mass fraction [-]')


def plot_temperature(states):
    """
    Plot batch reactor temperature.
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(states.t, states.T)
    ax.grid(True, color='0.9')
    ax.set_frame_on(False)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Temperature [K]')
    ax.tick_params(color='0.9')
