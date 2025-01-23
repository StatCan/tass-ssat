# TASS-Orchestrator

The tool is used to simplify the execution of multiple test case files. It is a simple orchestrator that uses the other TASS modules, and is meant for those without an orchestrator already present.

Most of the information regarding development and contribution from the TASS readme are applicable and should be followed.

## Installation

For production use, you can install it from the git repository.

For development purposes, you will want an editable installation ```pip install -e ./tass-orchestrator``` from the working directory ```tass-ssat```.

## Usage

The workflow file defining the jobs should be written as per the template in the schemas folder. You can then call the orchestrator with ```python -m tass.orchestrator -f /path/to/config/file.json```.

## Development

Make sure you created and activated the ```tass_ssat-dev``` environment. Install the required TASS modules. Running ```python -m tass.orchestrator -f ./tass-orchestrator/tests/data/simple_orch_framework_nix_calls.json``` on a nix based system, or ```python -m tass.orchestrator -f ./tass-orchestrator/tests/data/simple_orch_framework_win_calls.json``` on Windows.