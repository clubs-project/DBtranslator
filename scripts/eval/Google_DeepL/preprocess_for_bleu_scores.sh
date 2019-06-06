#!/bin/sh

# German source
python3 ../../convert_Google_target_into_bleu_format.py from-de-to-en.txt de en
python3 ../../convert_Google_target_into_bleu_format.py from-de-to-en.txt de en -sw ../../../lexicons/DeEnEsFr.sw 
python3 ../../convert_Google_target_into_bleu_format.py from-de-to-es.txt de es
python3 ../../convert_Google_target_into_bleu_format.py from-de-to-es.txt de es -sw ../../../lexicons/DeEnEsFr.sw 
python3 ../../convert_Google_target_into_bleu_format.py from-de-to-fr.txt de fr
python3 ../../convert_Google_target_into_bleu_format.py from-de-to-fr.txt de fr -sw ../../../lexicons/DeEnEsFr.sw 

# English source
python3 ../../convert_Google_target_into_bleu_format.py from-en-to-de.txt en de
python3 ../../convert_Google_target_into_bleu_format.py from-en-to-de.txt en de -sw ../../../lexicons/DeEnEsFr.sw 
python3 ../../convert_Google_target_into_bleu_format.py from-en-to-es.txt en es
python3 ../../convert_Google_target_into_bleu_format.py from-en-to-es.txt en es -sw ../../../lexicons/DeEnEsFr.sw 
python3 ../../convert_Google_target_into_bleu_format.py from-en-to-fr.txt en fr
python3 ../../convert_Google_target_into_bleu_format.py from-en-to-fr.txt en fr -sw ../../../lexicons/DeEnEsFr.sw 

# French source
python3 ../../convert_Google_target_into_bleu_format.py from-fr-to-de.txt fr de
python3 ../../convert_Google_target_into_bleu_format.py from-fr-to-de.txt fr de -sw ../../../lexicons/DeEnEsFr.sw 
python3 ../../convert_Google_target_into_bleu_format.py from-fr-to-es.txt fr es
python3 ../../convert_Google_target_into_bleu_format.py from-fr-to-es.txt fr es -sw ../../../lexicons/DeEnEsFr.sw 
python3 ../../convert_Google_target_into_bleu_format.py from-fr-to-en.txt fr en
python3 ../../convert_Google_target_into_bleu_format.py from-fr-to-en.txt fr en -sw ../../../lexicons/DeEnEsFr.sw 

# Spanish source
python3 ../../convert_Google_target_into_bleu_format.py from-es-to-de.txt es de
python3 ../../convert_Google_target_into_bleu_format.py from-es-to-de.txt es de -sw ../../../lexicons/DeEnEsFr.sw 
python3 ../../convert_Google_target_into_bleu_format.py from-es-to-fr.txt es fr
python3 ../../convert_Google_target_into_bleu_format.py from-es-to-fr.txt es fr -sw ../../../lexicons/DeEnEsFr.sw 
python3 ../../convert_Google_target_into_bleu_format.py from-es-to-en.txt es en
python3 ../../convert_Google_target_into_bleu_format.py from-es-to-en.txt es en -sw ../../../lexicons/DeEnEsFr.sw 

# none source
python3 ../../convert_Google_target_into_bleu_format.py from-none-to-de.txt none de
python3 ../../convert_Google_target_into_bleu_format.py from-none-to-de.txt none de -sw ../../../lexicons/DeEnEsFr.sw 
python3 ../../convert_Google_target_into_bleu_format.py from-none-to-fr.txt none fr
python3 ../../convert_Google_target_into_bleu_format.py from-none-to-fr.txt none fr -sw ../../../lexicons/DeEnEsFr.sw 
python3 ../../convert_Google_target_into_bleu_format.py from-none-to-en.txt none en
python3 ../../convert_Google_target_into_bleu_format.py from-none-to-en.txt none en -sw ../../../lexicons/DeEnEsFr.sw 
python3 ../../convert_Google_target_into_bleu_format.py from-none-to-es.txt none es
python3 ../../convert_Google_target_into_bleu_format.py from-none-to-es.txt none es -sw ../../../lexicons/DeEnEsFr.sw 
