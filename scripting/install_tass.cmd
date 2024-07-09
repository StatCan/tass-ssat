
@echo "CLONE START"
git clone https://github.com/StatCan/tass-ssat.git
@echo "CLONE END"
@echo "CD TO TASS-SSAT"
cd tass-ssat
@echo "SUCCESS CD?"
@echo "CREATE CONDA ENV"
call conda env create -f environment.yaml
@echo "END CREATE CONDA ENV"
@echo "CONDA ACTIVATE"
call conda activate tass_ssat-dev
@echo "END CONDA ACTIVATE"
@echo "CD TASS-BASE"
cd tass-base
@echo "SUCCESS CD?"
@echo "INSTALL EDITABLE TASS-BASE"
pip install -e .
@echo "INSTALL SUCCESS?"
@echo "CD TO TASS CONVERTER"
cd ..\tass-converter
@echo "SUCCESS CD?
@echo "INSTALL EDITABLE TASS-CONVERTER"
pip install -e.
@echo "INSTALL SUCCESS"
