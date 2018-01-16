#!/bin/bash

# #######################################################################
# Translation of PubPhsyc titles and abstracts
# Author: cristinae
# Date: 29.11.2017
#
# NOTE: Everything can be further parallelised at least per language
# #######################################################################

# Initialisation
# Default paths assume this is run from ./scripts
outPath="../"
models="../models"
bins="./thirdparties"
sizeDB=3
#sizeDB=1037540

# Override by command line arguments:
field='tit'
absType='ABHR'
threads=4

# Command line arguments
usage="$(basename "$0") -t # -f tit|abs [-a ABHR|ABNHR] [-h] 

where:
    -h  show this help text
    -t  number of threads
    -f  field to translate [tit|abs]
    -a  type of abstract [ABHR|ABNHR]
"
while getopts ':ht:f:a:' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
    t) threads=$OPTARG
       ;;
    f) field=$OPTARG
       ;;
    a) absType=$OPTARG
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
# A file per subDB and language is created (pre-processing depends on the language)
if [ $field == "tit" ]; then
   outPath=$outPath'titles/'
   python3 preproTits4trad.py $outPath $sizeDB
elif [ $field == "abs" ]; then
   outPath=$outPath'abstracts/'
   #python3 preproAbst4trad.py $outPath $sizeDB $absType
fi

# Extract text (with cuts) and normalise
# (long list of commands because sentences in French behave different)
echo "Normalising text..."
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do cut -f2 $i > $i.cut; cut -f1 $i > $i.head; 
   cat $i.cut | rev | cut -d">" -f2-  | rev > $i.labels; sed -i 's/$/>/' $i.labels;
   cat $i.cut | rev | cut -d">" -f1  | rev > $i.text; 
   cut -d'2' -f2- $i.cut | cut -d' ' -f1 > $i.tmp;  sed 's/^/<2/' $i.tmp > $i.2lang; perl $bins/normalize-punctuation.perl -l $j < $i.text > $i.norm; done; done;
#for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do cut -f2 $i > $i.cut; cut -f1 $i > $i.head; cut -d'2' -f2- $i.cut | cut -d' ' -f1 > $i.tmp;  cut -d' ' -f3- $i.cut > $i.text;  cut -d' ' -f2 $i.cut > $i.2lang; perl $bins/normalize-punctuation.perl -l $j < $i.text > $i.norm; done; done;

# Tokenisation
echo "Tokenising..."
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do perl $bins/tokenizer.perl -q -x -threads $threads -no-escape -l $j < $i.norm > $i.tok; done; done;
rm $outPath/*/*.cut  $outPath/*/*.tmp $outPath/*/*.text

# Truecasing
echo "Truecasing..."
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do perl $bins/truecase.perl --model $models/modelTC.EpWP.$j < $i.tok > $i.tc; done; done;
rm $outPath/*/*.norm

# Cleaning
find . -size 0 -delete
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do paste -d' ' $i.labels $i.tc > $i.tc2; done; done;
rm $outPath/*/*.tok
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do mv $i.tc2 $i.tc; done; done;

# BPE
echo "Applying BPE..."
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do python $bins/apply_bpe.py -c $models/L1L2.allw.bpe < $i.tc > $i.bpe; done; done;

# Running the decoder
echo "Translating..."
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do ../marian/build/amun -m $models/model_L1L2w3_v80k.iter1620000_adaptepoch4.npz $models/model_L1L2w3_v80k.iter1640000_adaptepoch5.npz -s $models/general.tc50shuf.w.bpe.L1.json -t $models/general.tc50shuf.w.bpe.L2.json  --cpu-threads $threads --input-file $i.bpe -b 6 --normalize --mini-batch 64  --maxi-batch 100  --log-progress=off --log-info=off > $i.trad.bpe; done; done;
find . -size 0 -delete

# de-BPE and de-tokenise
echo "Reconstructing translations..."
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do sed 's/\@\@ //g' $i.trad.bpe > $i.trad2; perl $bins/detokenizer.perl -q -u -l $j < $i.trad2 > $i.trad1; done; done;

# Cleaning and upload format?
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do paste $i.head $i.2lang $i.trad1 > $i.trad; done; done;
find . -size 0 -delete
rm $outPath/*/*.tc $outPath/*/*.bpe $outPath/*/*.trad1 $outPath/*/*.trad2
rm $outPath/*/*.2lang $outPath/*/*.labels $outPath/*/*.head

# In case of abstract translation, abstracts must be reconstructed
if [ $field == "abs" ]; then
    for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do python3 postproAbst.py  $i.trad  $i.tradjoint; done; done;
    for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do mv $i.tradjoint $i.trad; done; done;
fi

echo "Ready!"

