#!/bin/sh

./get_all_translations.sh &&
./prepare_evaluation.sh &&
./run_bleu.sh &&
python3 process_bleu_scores.py bleu-results.txt
