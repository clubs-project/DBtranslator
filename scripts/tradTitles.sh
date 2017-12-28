#!/bin/bash
# NOTE: Everything can be parallelised
outPath="../titles"
threads=4

# Download the titles from the DB and prepare the format for translation7
# A file per subDB and language is created (pre-processing depends on the language)
# TODO: outPath is hardcoded
python3 preproTits4trad.py

# Extract text (with cuts) and normalise
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do cut -f2 $i > $i.cut; cut -f1 $i > $i.head; cut -d' ' -f-2 $i.cut > $i.labels;  cut -d' ' -f3- $i.cut > $i.text;  cut -d' ' -f2 $i.cut > $i.2lang; perl normalize-punctuation.perl -l $j < $i.text > $i.norm; done; done;

# Tokenisation
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do perl tokenizer.perl -x -threads $threads -no-escape -l $j < $i.norm > $i.tok; done; done;
rm $outPath/*/*.cut
rm $outPath/*/*.text

# Truecasing
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do perl truecase.perl --model ../models/modelTC.EpWP.$j < $i.tok > $i.tc; done; done;
rm $outPath/*/*.norm

# Cleaning
find . -size 0 -delete
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do paste -d' ' $i.labels $i.tc > $i.tc2; done; done;
rm $outPath/*/*.tok
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do mv $i.tc2 $i.tc; done; done;

# BPE
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do python apply_bpe.py -c ../models/L1L2.allw.bpe < $i.tc > $i.bpe; done; done;

# Running the decoder
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; do ../marian/build/amun -m ../models/model_L1L2w3_v80k.iter1620000_adaptepoch4.npz ../models/model_L1L2w3_v80k.iter1640000_adaptepoch5.npz -s ../models/general.tc50shuf.w.bpe.L1.json -t ../models/general.tc50shuf.w.bpe.L2.json  --cpu-threads $threads --input-file $i.bpe -b 6 --normalize --mini-batch 64  --maxi-batch 100  --log-progress 'off' --log-info 'off' > $i.trad.bpe; done; done;
find . -size 0 -delete

# Cleaning and upload format?
#
for j in "en" "de" "fr" "es"; do for i in $outPath/*/*.$j; sed 's/\@\@ //g' $i.trad.bpe > $i.trad2;  paste $i.head $i.2lang $i.trad2 > $i.trad ; done; done;
find . -size 0 -delete
rm $outPath/*/*.tc
rm $outPath/*/*.bpe
rm $outPath/*/*.trad2
rm $outPath/*/*.2lang
rm $outPath/*/*.labels
rm $outPath/*/*.head


