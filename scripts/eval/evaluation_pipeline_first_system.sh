#!/bin/sh

./prepare_evaluation_first_system.sh &&
./run_bleu_first_system.sh &&
python3 process_bleu_scores.py bleu-results-first-system.txt -sd
