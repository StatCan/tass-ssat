# TASS-Core

This module contains the core automation engine for the TASS framework.
Automated tests are executed using this module.

Most of the information regarding development and contribution from the [TASS README](../README.md) are applicable and should be followed.

## Installation

For production use, you can install it from the git repository.

For development purposes, you will want an editable installation ```pip install -e ./tass-core``` from the working directory ```tass-ssat```.

## Appium - Partially Implemented

The tass-core module partially supports Appium. Appropriately configured devices and tests can be
executed using basic actions provided by TASS; however, the Action Chain framework is not fully supported
and may be used with caution. Appium is setup to mirror the Selenium actions, with modifications to
ensure functionality on most mobile devices. Given the wide array of mobile devices available, 
functionality is not guaranteed; however, best efforts are made to test Appium functions using 
common Android and Apple mobile phone and tablet sized devices.

## Usage

The module can be executed with CLI using the following commands. By default, when executing a job file
JSON schema validation is required, if the job file does not meet the schema requirements it cannot be executed.
It is not recommended to utilize the `--no-validate` unless you are familiar with the function of the module
and the [JSON schema](../templates/execution-template.json) found in the templates folder.

### Commands

`python -m tass.core -f/--file <path/to/file.ext> [--no-validate]`

### Arguments

- file (required): The path to the JSON job file to be executed. 
- no-validate: Flag used to disable the job file validation.

## Development

Follow the instructions to setup the development environment in the [TASS readme](../README.md). Ensure that you
have the `tass_ssat-dev` conda environment active.