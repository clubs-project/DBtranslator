#!/bin/sh

python3 get_complete_translations.py server_results/4lex_diff/translations.de &&
python3 get_complete_translations.py server_results/4lex_diff/translations.en &&
python3 get_complete_translations.py server_results/4lex_diff/translations.es &&
python3 get_complete_translations.py server_results/4lex_diff/translations.fr &&
python3 get_complete_translations.py server_results/4lex_diff/translations.none &&

python3 get_complete_translations.py server_results/4lex_non_diff/translations.de &&
python3 get_complete_translations.py server_results/4lex_non_diff/translations.en &&
python3 get_complete_translations.py server_results/4lex_non_diff/translations.es &&
python3 get_complete_translations.py server_results/4lex_non_diff/translations.fr &&
python3 get_complete_translations.py server_results/4lex_non_diff/translations.none &&

python3 get_complete_translations.py server_results/mesh/translations.de &&
python3 get_complete_translations.py server_results/mesh/translations.en &&
python3 get_complete_translations.py server_results/mesh/translations.es &&
python3 get_complete_translations.py server_results/mesh/translations.fr &&
python3 get_complete_translations.py server_results/mesh/translations.none &&

python3 get_complete_translations.py server_results/mesh_4_lex_wikidata/translations.de &&
python3 get_complete_translations.py server_results/mesh_4_lex_wikidata/translations.en &&
python3 get_complete_translations.py server_results/mesh_4_lex_wikidata/translations.es &&
python3 get_complete_translations.py server_results/mesh_4_lex_wikidata/translations.fr &&
python3 get_complete_translations.py server_results/mesh_4_lex_wikidata/translations.none &&

python3 get_complete_translations.py server_results/wikidata_diff/translations.de &&
python3 get_complete_translations.py server_results/wikidata_diff/translations.en &&
python3 get_complete_translations.py server_results/wikidata_diff/translations.es &&
python3 get_complete_translations.py server_results/wikidata_diff/translations.fr &&
python3 get_complete_translations.py server_results/wikidata_diff/translations.none &&

python3 get_complete_translations.py server_results/wikidata_non_diff/translations.de &&
python3 get_complete_translations.py server_results/wikidata_non_diff/translations.en &&
python3 get_complete_translations.py server_results/wikidata_non_diff/translations.es &&
python3 get_complete_translations.py server_results/wikidata_non_diff/translations.fr &&
python3 get_complete_translations.py server_results/wikidata_non_diff/translations.none &&

python3 convert_into_bleu_format.py server_results/4lex_diff/target_qfr.de -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/4lex_diff/target_qfr.de
python3 convert_into_bleu_format.py server_results/4lex_diff/target_qfr.en -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/4lex_diff/target_qfr.en
python3 convert_into_bleu_format.py server_results/4lex_diff/target_qfr.es -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/4lex_diff/target_qfr.es
python3 convert_into_bleu_format.py server_results/4lex_diff/target_qfr.fr -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/4lex_diff/target_qfr.fr
python3 convert_into_bleu_format.py server_results/4lex_diff/target_qfr.none -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/4lex_diff/target_qfr.none

python3 convert_into_bleu_format.py server_results/4lex_non_diff/target_qfr.de -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/4lex_non_diff/target_qfr.de
python3 convert_into_bleu_format.py server_results/4lex_non_diff/target_qfr.en -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/4lex_non_diff/target_qfr.en
python3 convert_into_bleu_format.py server_results/4lex_non_diff/target_qfr.es -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/4lex_non_diff/target_qfr.es
python3 convert_into_bleu_format.py server_results/4lex_non_diff/target_qfr.fr -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/4lex_non_diff/target_qfr.fr
python3 convert_into_bleu_format.py server_results/4lex_non_diff/target_qfr.none -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/4lex_non_diff/target_qfr.none

python3 convert_into_bleu_format.py server_results/mesh/target_qfr.de -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/mesh/target_qfr.de
python3 convert_into_bleu_format.py server_results/mesh/target_qfr.en -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/mesh/target_qfr.en
python3 convert_into_bleu_format.py server_results/mesh/target_qfr.es -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/mesh/target_qfr.es
python3 convert_into_bleu_format.py server_results/mesh/target_qfr.fr -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/mesh/target_qfr.fr
python3 convert_into_bleu_format.py server_results/mesh/target_qfr.none -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/mesh/target_qfr.none

python3 convert_into_bleu_format.py server_results/mesh_4_lex_wikidata/target_qfr.de -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/mesh_4_lex_wikidata/target_qfr.de
python3 convert_into_bleu_format.py server_results/mesh_4_lex_wikidata/target_qfr.en -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/mesh_4_lex_wikidata/target_qfr.en
python3 convert_into_bleu_format.py server_results/mesh_4_lex_wikidata/target_qfr.es -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/mesh_4_lex_wikidata/target_qfr.es
python3 convert_into_bleu_format.py server_results/mesh_4_lex_wikidata/target_qfr.fr -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/mesh_4_lex_wikidata/target_qfr.fr
python3 convert_into_bleu_format.py server_results/mesh_4_lex_wikidata/target_qfr.none -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/mesh_4_lex_wikidata/target_qfr.none

python3 convert_into_bleu_format.py server_results/wikidata_diff/target_qfr.de -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/wikidata_diff/target_qfr.de
python3 convert_into_bleu_format.py server_results/wikidata_diff/target_qfr.en -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/wikidata_diff/target_qfr.en
python3 convert_into_bleu_format.py server_results/wikidata_diff/target_qfr.es -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/wikidata_diff/target_qfr.es
python3 convert_into_bleu_format.py server_results/wikidata_diff/target_qfr.fr -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/wikidata_diff/target_qfr.fr
python3 convert_into_bleu_format.py server_results/wikidata_diff/target_qfr.none -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/wikidata_diff/target_qfr.none

python3 convert_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.de -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.de
python3 convert_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.en -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.en
python3 convert_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.es -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.es
python3 convert_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.fr -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.fr
python3 convert_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.none -sw ../lexicons/DeEnEsFr.sw 
python3 convert_into_bleu_format.py server_results/wikidata_non_diff/target_qfr.none
