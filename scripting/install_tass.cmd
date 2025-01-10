@echo off
@echo "CLONING TASS REPOSITORY"
git clone https://github.com/StatCan/tass-ssat.git
cd tass-ssat
@echo "CREATING CONDA ENVIRONMENT"
call conda env create -f environment.yaml
call conda activate tass_ssat-dev
@echo "INSTALLING EDITABLE TASS-REPORT"
pip install -e tass-report
@echo "INSTALLING EDITABLE TASS-BASE"
pip install -e tass-base
@echo "INSTALLING EDITABLE TASS-CONVERTER"
pip install -e tass-converter
@echo "INSTALLING EDITABLE TASS-ORCHESTRATOR"
pip install -e tass-orchestrator
@echo "INSTALLATION COMPLETED"
