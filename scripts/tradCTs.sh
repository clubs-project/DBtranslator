#!/bin/bash

# #######################################################################
# Translation of PubPhsyc controlled terms
# Author: cristinae
# Date: 20.02.2018
# #######################################################################

# Initialisation
# Default paths assume this is run from ./scripts
outPath="../"
models="../models"
bins="./thirdparties"
sizeDB=30000
#sizeDB=1037540

# Override by command line arguments:
ctType='CTL'

# Command line arguments
usage="$(basename "$0") -f CTH|CTL|ITH|ITL [-h] 

where:
    -h  show this help text
    -f  field to translate [CTH|CTL|ITH|ITL]
"
while getopts ':hf:' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
    f) ctType=$OPTARG
       ;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done

echo "Translation Pipeline"
# Download the titles from the DB and prepare the format for translation
# A file per subDB and language is created 
if [ $ctType == "CTH" ]; then
   outPath=$outPath'cth/'
elif [ $ctType == "CTL" ]; then
   outPath=$outPath'ctl/'
elif [ $ctType == "ITH" ]; then
   outPath=$outPath'ith/'
elif [ $ctType == "ITL" ]; then
   outPath=$outPath'itl/'
fi
mkdir -p $outPath
python3 preproField4trad.py $outPath $sizeDB $ctType

# Mapping
echo "Translating..."
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do python3 tradCTs.py $i $i.trad; done; done;

echo "Ready!"

