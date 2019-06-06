#!/bin/sh

./preprocess_for_bleu_scores.sh &&
./run_bleu.sh &&
python3 ../../process_bleu_scores.py bleu-results.txt -sd
