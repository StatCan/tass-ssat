# Testing and Automated Services Suite – Suite et service d’automatisation et de testing

The TASS application assists users in creating and running reproducible
test cases for web applications. TASS uses json configuration files to
define test cases, with each JSON file representing a single "job"
executing the defined tests.

## Getting Started

TASS relies on a conda compatible environment and package manager. The
framework is tested on Windows, and efforts are made for it to be
compatible with Linux/macOS.

### Development

To contribute to the project, please read our best practices:
docs/best_practices.md. Also, create your conda environment via

`conda env create -f environment.yaml`.

The conda environment will contain all the of the dependencies at the
correct versions. To run tests, make sure you have an editable install
with `pip install -e <module>` from the root directory. Where `<module>`
is replaced with the desired component of TASS:

- tass-core
- tass-converter
- tass-report
- tass-orchestrator

You can also download the "install_tass" script appropriate for your
platform from the "scripting" folder and run it to automatically clone the
repository, create the conda environment, and have editable installs of
the tass modules.

#### Build Pypi Package

To build the pypi package, navigate to the root of the directory and type
`python -m build <module>` with `<module>` being replaced by the TASS module
to be built. This will use the `pyproject.toml` file to build the
package. The package will be in the `dist` folder in your repository.

#### Build Conda Package

To build the conda package, navigate to the root of the directory and type
`conda build <module>/conda-recipe`. The package can be found in a folder specified
in the command output. You can always install it via `conda install --use-local <module>`
if you wish to install it in the same environment you built it.

### Installation

The framework can be installed by downloading the appropriate
release and then running the install command.

#### pip

Download the .whl file for the desired release version. Using the CLI
with pip and python >=3.10 enter the command `pip install <path/to/wheel/file>`

#### conda

Download the .tar.bz2 file for the desired release version. Using your conda environment
enter the command `conda install <path/to/tar.bz2/file>`. After this instllation is
successful enter the command `conda install --use-local <module name>` to install
dependencies.

### Utilization

The testing framework can be invoked from your CLI with the commands described in the module README:

- [tass-core](./tass-core/README.md)
- [tass-converter](./tass-converter/README.md)
- [tass-orchestrator](./tass-orchestrator/README.md)

#### Demo

The repository comes with several examples and working demos. To use any of the demos, clone the repository, then
create and activate your conda environment. All the files required for a demo should be provided
in the examples folder.

[EXAMPLES](examples/)


## License/Copyright

The code and all files in this repository are licensed under the Apache
license version 2, unless otherwise specified within the respective file.
In that case, the license specified in the file is applicable.

Copyright © His Majesty the King in Right of Canada, as represented by the
Minister of Statistics Canada, 2023.

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.

## Documentation

Further documentation can be found in the docs folder. The documentation
can be built using the `sphinx-build -b html source build` from the `doc`
folder.
