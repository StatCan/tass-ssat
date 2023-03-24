# Testing and Automated Services Suite – Suite et service d’automatisation
et de testing

The TASS application assists users in creating and running reproducible
test cases for web applications. TASS uses json configuration files to
define test cases, organize them as test suites and run them via test
runs.

## Getting Started

TASS relies on a conda compatible environment and package manager. The
framework is tested on Windows, and efforts are made for it to be
compatible with Linux/macOS.

### Development

To contribute to the project, please read our best practices:
docs/best_practices.md. Also, create your conda environment via 

`conda env create -f environment.yaml`.

The conda environment will contain all the of the dependencies at the
correct versions.

### Utilization

The testing framework can be invoked from your CLI with the command

`python -m ./path/to/module/tass --file ./path/to/config/file`.

#### Demo

The repository comes with a working demo. Clone the repository, then
create and active your conda environment. Assuming the working
directory is the root of the git repository, you can run the demo with
`python -m ./tass/ --file demo/tass_sample.json`. Please note that the
tass_sample.json file will need to be adjusted if you want to run the demo
with a different browser than Google Chrome.

This short demo will go through some of the actions Selenium actions TASS
supports on a test webpage. The test webpage is locally present in the
repository.

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

Further documentation can be found in the docs folder.
