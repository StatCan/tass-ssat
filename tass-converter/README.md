# TASS-Converter

This module contains the conversion tools to facilitate the creation of JSON files in the required format for use with TASS.
Automated tests are executed using this module.

Most of the information regarding development and contribution from the [TASS README](../README.md) are applicable and should be followed.

## Installation

For production use, you can install it from the git repository.

For development purposes, you will want an editable installation ```pip install -e ./tass-converter``` from the working directory ```tass-ssat```.

## Usage

The module can be executed with CLI using the following commands. The conversion tool can take a properly formatted Excel
file (.xlsx or .xlsm) and convert it to a properly formatted JSON job file that can be executed by the tass-core module.

### Commands

`python -m tass.converter -s/--source <path/to/file.ext> -t/--target <path/to/folder/file-name>`

### Arguments

- source (required): The file path to the Excel file to be converted. Must be .xlsx or .xlsm file format. 
- target (required): The desired file name. Can include additional folder structure starting from `scenarios` default folder.
ex: `-t simple/test/job1` would create the JSON job file: `./scenarios/simple/test/job1.json`

## Development

Follow the instructions to setup the development environment in the [TASS readme](../README.md). Ensure that you
have the `tass_ssat-dev` conda environment active.