# Entrained Flow Reactor (EFR)

This repository is for the Entrained Flow Reactor (EFR) at NREL. The reactor operates at fast pyrolysis conditions to thermochemically convert biomass into gaseous products.

⚠️ This project is being actively developed. Use at your own risk.

## Project structure

**data** - Data from experimental measurements and for the pyrolysis kinetics.

**diagrams** - Files for creating diagrams on the [diagrams.net](https://www.diagrams.net) website.

**efr** - Python files for running various models of the entrained flow reactor.

**params** - Parameter files for running the EFR model.

**tex** - LaTeX files for generating the report.

## Installation

The EFR program requires the latest version of Python and several packages as listed in the `requirements.txt` file.

## Usage

The EFR program is run from the command line using Python.

```bash
# run the EFR program with the Blend3 feedstock parameters
$ python efr params/blend3.py

# show all Matplotlib plot figures
$ python efr --show_plots params/blend3.py

# use C and H from ultimate analysis to determine biomass composition
$ python efr --biocomp=ult params/blend3.py

# view all available commands for running the EFR program
$ python efr --help
```

## Report

See the [main.pdf](tex/main.pdf) document in the **tex** folder for the EFR technical report.

## Contributing

If you would like to contribute code to this project, please submit a Pull Request. Questions, comments, and other feedback can be submitted on the Issues page.
