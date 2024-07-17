#! /bin/zsh

POSITIONAL=()

while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -e|--environment)
            PACKAGE_ENV="${2}"
            shift
            shift
            ;;
esac
done
set -- "${POSITIONAL[@]}"

if [[ $1 == 'help' || $1 == '-h' || $1 == '--help' ]]
then
    echo "Usage:"
    echo "install_tass.sh"
    echo "Will clone a github repository in current folder and install tass modules."
    exit 0
fi

CWD=$(pwd)

git clone https://github.com/StatCan/tass-ssat.git
cd tass-ssat
conda env create -f environment.yaml
eval "$(conda shell.bash hook)"
conda activate tass_ssat-dev
cd tass-base
pip install -e .
cd ../tass-converter
pip install -e .
