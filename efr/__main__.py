import argparse
import importlib
import logging

from ult_analysis_bases import ult_analysis_bases
from bc_chem_analysis import bc_chem_analysis
from bc_charact_params import bc_charact_params
from bc_ult_analysis import bc_ult_analysis


def _command_line_args():
    """
    Command line arguments.
    """

    parser = argparse.ArgumentParser(
        description='🚀 Model the Entrained Flow Reactor (EFR)',
        epilog='Enjoy the program 🤓')

    parser.add_argument(
        'params_path',
        help='path to parameters file')

    parser.add_argument(
        '-bc', '--biocomp',
        choices=['chem', 'charact', 'ult'],
        default='chem',
        help='biomass composition method (default: chem)')

    args = parser.parse_args()

    return args


def main():
    """
    Main function.
    """

    # Configure logging
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    # Get command line arguments
    args = _command_line_args()

    # Get file path and module name of parameters file
    file_path = args.params_path
    module_name = args.params_path.split('/')[1]

    # Import parameters as a `params` module
    spec = importlib.util.spec_from_file_location(module_name, file_path)

    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)

    # Ultimate analysis bases
    ult_analysis = ult_analysis_bases(params.feedstock['ultimate_analysis'])

    # Biomass composition
    if args.biocomp == 'chem':
        bc = bc_chem_analysis(params.feedstock['chemical_analysis'])
    elif args.biocomp == 'charact':
        bc = bc_charact_params(params.feedstock)
    elif args.biocomp == 'ult':
        bc = bc_ult_analysis(ult_analysis)

    # Batch reactor yields from biomass composition
    # TODO


if __name__ == '__main__':
    main()
