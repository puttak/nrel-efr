import argparse
import importlib
import logging
import matplotlib.pyplot as plt

from ult_analysis_bases import ult_analysis_bases
from bc_chem_analysis import bc_chem_analysis
from bc_ult_analysis import bc_ult_analysis
from bc_ult_modified import bc_ult_modified
from batch_reactor import batch_reactor
from debiagi_sensitivity import debiagi_sa


def _command_line_args():
    """
    Command line arguments.
    """

    parser = argparse.ArgumentParser(
        description='🚀 Model the Entrained Flow Reactor (EFR)',
        epilog='🤓 Enjoy the program.')

    parser.add_argument(
        'params_path',
        help='path to parameters file')

    parser.add_argument(
        '-bc', '--biocomp',
        choices=['chem', 'ult', 'ultmod'],
        default='chem',
        help='biomass composition method (default: chem)')

    parser.add_argument(
        '-sp', '--show_plots',
        action='store_true',
        help='show plot figures (default: False)')

    parser.add_argument(
        '-sa', '--sensitivity-analysis',
        action='store_true',
        help='sensitivity analysis of the kinetics (default: False)')

    args = parser.parse_args()
    return args


def main():
    """
    Main function to run the program.
    """

    # Configure logging and command line arguments
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    args = _command_line_args()

    # Get file path and module name of parameters file
    file_path = args.params_path
    module_name = args.params_path.split('/')[1]

    # Import parameters as a `params` module
    spec = importlib.util.spec_from_file_location(module_name, file_path)

    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)

    # Ultimate analysis bases
    ult_bases = ult_analysis_bases(params.feedstock)

    # Biomass composition
    if args.biocomp == 'chem':
        bc = bc_chem_analysis(params.feedstock)
    elif args.biocomp == 'ult':
        bc = bc_ult_analysis(ult_bases)
    elif args.biocomp == 'ultmod':
        bc = bc_ult_modified(params.feedstock)

    # Batch reactor yields for given biomass composition
    batch_reactor(params.reactor, bc)

    # Sensitivity analysis of Debiagi 2018 pyrolysis kinetics
    if args.sensitivity_analysis:
        debiagi_sa(params.reactor, params.sensitivity_analysis)

    # Show all plot figures
    if args.show_plots:
        plt.show()


if __name__ == '__main__':
    main()
