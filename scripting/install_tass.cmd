@echo off
@echo "CLONING TASS REPOSITORY"
git clone https://github.com/StatCan/tass-ssat.git
cd tass-ssat
@echo "CREATING CONDA ENVIRONMENT"
call conda env create -f environment.yaml
call conda activate tass_ssat-dev
cd tass-base
@echo "INSTALLING EDITABLE TASS-BASE"
pip install -e .
cd ..\tass-converter
@echo "INSTALLING EDITABLE TASS-CONVERTER"
pip install -e.
@echo "INSTALLATION COMPLETED"
