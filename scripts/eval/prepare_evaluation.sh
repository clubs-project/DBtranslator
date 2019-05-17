#!/bin/sh
python3 convert_target_into_bleu_format.py translatedQueriesManual/done/target.de -sw ../lexicons/DeEnEsFr.sw
python3 convert_target_into_bleu_format.py translatedQueriesManual/done/target.de
python3 convert_target_into_bleu_format.py translatedQueriesManual/done/target.en -sw ../lexicons/DeEnEsFr.sw
python3 convert_target_into_bleu_format.py translatedQueriesManual/done/target.en
python3 convert_target_into_bleu_format.py translatedQueriesManual/done/target.fr -sw ../lexicons/DeEnEsFr.sw
python3 convert_target_into_bleu_format.py translatedQueriesManual/done/target.fr
python3 convert_target_into_bleu_format.py translatedQueriesManual/done/target.es -sw ../lexicons/DeEnEsFr.sw
python3 convert_target_into_bleu_format.py translatedQueriesManual/done/target.es
python3 convert_target_into_bleu_format.py translatedQueriesManual/done/target.none -sw ../lexicons/DeEnEsFr.sw
python3 convert_target_into_bleu_format.py translatedQueriesManual/done/target.none

python3 convert_target_qfr_into_bleu_format.py server_results/4lex_diff/target_qfr.de -sw ../lexicons/DeEnEsFr-preprocessed.sw 
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_diff/target_qfr.de
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_diff/target_qfr.en -sw ../lexicons/DeEnEsFr-preprocessed.sw 
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_diff/target_qfr.en
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_diff/target_qfr.es -sw ../lexicons/DeEnEsFr-preprocessed.sw 
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_diff/target_qfr.es
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_diff/target_qfr.fr -sw ../lexicons/DeEnEsFr-preprocessed.sw 
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_diff/target_qfr.fr
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_diff/target_qfr.none -sw ../lexicons/DeEnEsFr-preprocessed.sw 
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_diff/target_qfr.none

python3 convert_target_qfr_into_bleu_format.py server_results/4lex_non_diff/target_qfr.de -sw ../lexicons/DeEnEsFr-preprocessed.sw 
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_non_diff/target_qfr.de
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_non_diff/target_qfr.en -sw ../lexicons/DeEnEsFr-preprocessed.sw 
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_non_diff/target_qfr.en
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_non_diff/target_qfr.es -sw ../lexicons/DeEnEsFr-preprocessed.sw 
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_non_diff/target_qfr.es
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_non_diff/target_qfr.fr -sw ../lexicons/DeEnEsFr-preprocessed.sw 
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_non_diff/target_qfr.fr
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_non_diff/target_qfr.none -sw ../lexicons/DeEnEsFr-preprocessed.sw 
python3 convert_target_qfr_into_bleu_format.py server_results/4lex_non_diff/target_qfr.none

python3 convert_target_qfr_into_bleu_format.py server_results/mesh/target_qfr.de -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh/target_qfr.de
python3 convert_target_qfr_into_bleu_format.py server_results/mesh/target_qfr.en -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh/target_qfr.en
python3 convert_target_qfr_into_bleu_format.py server_results/mesh/target_qfr.es -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh/target_qfr.es
python3 convert_target_qfr_into_bleu_format.py server_results/mesh/target_qfr.fr -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh/target_qfr.fr
python3 convert_target_qfr_into_bleu_format.py server_results/mesh/target_qfr.none -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh/target_qfr.none

python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_wikidata_non_diff/target_qfr.de -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_wikidata_non_diff/target_qfr.de
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_wikidata_non_diff/target_qfr.en -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_wikidata_non_diff/target_qfr.en
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_wikidata_non_diff/target_qfr.es -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_wikidata_non_diff/target_qfr.es
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_wikidata_non_diff/target_qfr.fr -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_wikidata_non_diff/target_qfr.fr
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_wikidata_non_diff/target_qfr.none -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_wikidata_non_diff/target_qfr.none

python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_non_diff/target_qfr.de -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_non_diff/target_qfr.de
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_non_diff/target_qfr.en -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_non_diff/target_qfr.en
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_non_diff/target_qfr.es -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_non_diff/target_qfr.es
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_non_diff/target_qfr.fr -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_non_diff/target_qfr.fr
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_non_diff/target_qfr.none -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/mesh_4lex_non_diff/target_qfr.none

python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_diff/target_qfr.de -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_diff/target_qfr.de
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_diff/target_qfr.en -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_diff/target_qfr.en
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_diff/target_qfr.es -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_diff/target_qfr.es
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_diff/target_qfr.fr -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_diff/target_qfr.fr
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_diff/target_qfr.none -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_diff/target_qfr.none

python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.de -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.de
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.en -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.en
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.es -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.es
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.fr -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.fr
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.none -sw ../lexicons/DeEnEsFr-preprocessed.sw  
python3 convert_target_qfr_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.none
