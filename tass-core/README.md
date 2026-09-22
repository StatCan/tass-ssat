# TASS-Core

This module contains the core automation engine for the TASS framework.
Automated tests are executed using this module.

Most of the information regarding development and contribution from the [TASS README](../README.md) are applicable and should be followed.

## Installation

For production use, you can install it from the git repository.

For development purposes, you will want an editable installation ```pip install -e ./tass-core``` from the working directory ```tass-ssat```.

## Appium

The tass-core module partially supports Appium. Appropriately configured devices and tests can be
executed using basic actions provided by TASS; however, the Action Chain framework is not fully supported
and may be used with caution. Appium is setup to mirror the Selenium actions, with modifications to
ensure functionality on most mobile devices. Given the wide array of mobile devices available, 
functionality is not guaranteed; however, best efforts are made to test Appium functions using 
common Android and Apple mobile phone and tablet sized devices.

## Selenium and Appium Locator Strategies (v1.2.0)

As of v1.2.0 locator strategies for Selenium and Appium commands that require a locator can be passed as a string
value argument. 3 strategies are provided at this time:

    - The default strategy "find_element" simply searches for the element on the current page based on the provided locator.
    - "wait_element_clickable" uses an explicit wait to wait until the state of the element in question is "clickable" before returning the WebElement
    - "wait_element_visible" uses an explicit wait to wait until the state of the element is "visible" before returning the WebElement

Previously, these alternate strategies were implemented through selenium_wait and appium_wait commands. With this change
either strategy can be used with any of the built-in Selenium/Appium commands by passing the strategy name to the command
using the "find" argument. Ex: find="wait_element_clickable"

### What do I need to change?

At this time, nothing needs to change to retain full functionality. Tests that make use of the old wait implementations
will receive a warning message suggesting a change in implementation. The old wait implementations will be removed after
a future update. Additionally, commands that require a locator will default to using the "find_element" strategy without
user intervention.

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