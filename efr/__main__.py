import argparse
import importlib
import logging

from ultimate_analysis_bases import ultimate_analysis_bases
from biocomp_chemical_analysis import biocomp_chemical_analysis


def main():

    # Configure logging
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('params_path', help='path to parameters file')
    args = parser.parse_args()

    # Get file path and module name of parameters file
    file_path = args.params_path
    module_name = args.params_path.split('/')[1]

    # Import parameters as a `params` module
    spec = importlib.util.spec_from_file_location(module_name, file_path)

    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)

    # Ultimate analysis bases
    ultimate_analysis_bases(params.feedstock['ultimate_analysis'])

    # Biomass composition
    biocomp_chemical_analysis(params.feedstock['chemical_analysis'])


if __name__ == '__main__':
    main()
