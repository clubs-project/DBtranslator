#!/bin/sh

python3 convert_trads_into_bleu_format.py manualEvaluation/trads.de -sw ../lexicons/DeEnEsFr-preprocessed.sw
python3 convert_trads_into_bleu_format.py manualEvaluation/trads.de
python3 convert_trads_into_bleu_format.py manualEvaluation/trads.en -sw ../lexicons/DeEnEsFr-preprocessed.sw
python3 convert_trads_into_bleu_format.py manualEvaluation/trads.en
python3 convert_trads_into_bleu_format.py manualEvaluation/trads.fr -sw ../lexicons/DeEnEsFr-preprocessed.sw
python3 convert_trads_into_bleu_format.py manualEvaluation/trads.fr
python3 convert_trads_into_bleu_format.py manualEvaluation/trads.es -sw ../lexicons/DeEnEsFr-preprocessed.sw
python3 convert_trads_into_bleu_format.py manualEvaluation/trads.es
python3 convert_trads_into_bleu_format.py manualEvaluation/trads.none -sw ../lexicons/DeEnEsFr-preprocessed.sw
python3 convert_trads_into_bleu_format.py manualEvaluation/trads.none
