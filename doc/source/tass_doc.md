# Testing and Automation Services Suite (TASS)

The Testing and Automation Services Suite (TASS) is a group of tools to
transition the testing activities of the ITTC/SIA team from manual testing
activities and EQATS to a new modular automated testing framework. While
the focus of the TASS framework is automating the testing of Census
related systems, the general approach of the framework allows it to be
used for a variety of web-based technologies.

## Installation

TASS can be installed from the github repository, under [releases]
(https://github.com/StatCan/tass-ssat/releases). We do most of the testing
and use via miniforge, so we recommend using the conda package version of
the framework. The pypi package should work but does not get the same
amount of attention.

## Components of TASS

The framework uses Selenium for web browser automation, json configuration
files to create test cases, and a conversion tool to enable users
unfamiliar with JSON to write their test cases in Excel. The usage of each
of these components will be explained below.

### Selenium

[Selenium](https://www.selenium.dev) is the framework that allows users to
programatically control web browsers.

### JSON Configuration Files

The JSON configuration files stores the test cases, test suites, and test
runs.

### Excel Configuration File Converter

The Excel configuration file can be converted into the correct JSON files
with a direct call or in a script.

Direct call:
TODO: Put in info for direct call.

Script:
```
from tass.tools import conf

my_file = conf.convert('path/to/excel/file.xlsx')
```

## Using TASS

TASS can be used from the commandline directly once installed along with
proper parameters

`python -m tass`

or imported in a script

`import tass`

and last, it will be evaluated for integration in CI/CD.

### Commandline

Using TASS from the commandline is the easiest way to have a more
interactive experience with the framework.

### Script

The framework can be integrated to a script for usage as part of
a comprehensive testing or automation strategy.

### CI/CD Pipeline

TASS has not been tested within a CI/CD pipeline context. TASS is expected
to work within these pipelines, but this section of the documentation will
be updated with more information once we confirm it works.

## Actions

The TASS framework automates browser interactions via actions. 
