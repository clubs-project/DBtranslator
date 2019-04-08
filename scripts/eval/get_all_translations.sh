#!/bin/sh

python3 get_complete_translations.py server_results/4lex_diff/translations.de
python3 get_complete_translations.py server_results/4lex_diff/translations.en
python3 get_complete_translations.py server_results/4lex_diff/translations.fr
python3 get_complete_translations.py server_results/4lex_diff/translations.es
python3 get_complete_translations.py server_results/4lex_diff/translations.none

python3 get_complete_translations.py server_results/4lex_non_diff/translations.de
python3 get_complete_translations.py server_results/4lex_non_diff/translations.en
python3 get_complete_translations.py server_results/4lex_non_diff/translations.fr
python3 get_complete_translations.py server_results/4lex_non_diff/translations.es
python3 get_complete_translations.py server_results/4lex_non_diff/translations.none

python3 get_complete_translations.py server_results/wikidata_diff/translations.de
python3 get_complete_translations.py server_results/wikidata_diff/translations.en
python3 get_complete_translations.py server_results/wikidata_diff/translations.fr
python3 get_complete_translations.py server_results/wikidata_diff/translations.es
python3 get_complete_translations.py server_results/wikidata_diff/translations.none

python3 get_complete_translations.py server_results/wikidata_non_diff/translations.de
python3 get_complete_translations.py server_results/wikidata_non_diff/translations.en
python3 get_complete_translations.py server_results/wikidata_non_diff/translations.fr
python3 get_complete_translations.py server_results/wikidata_non_diff/translations.es
python3 get_complete_translations.py server_results/wikidata_non_diff/translations.none

python3 get_complete_translations.py server_results/mesh/translations.de
python3 get_complete_translations.py server_results/mesh/translations.en
python3 get_complete_translations.py server_results/mesh/translations.fr
python3 get_complete_translations.py server_results/mesh/translations.es
python3 get_complete_translations.py server_results/mesh/translations.none

python3 get_complete_translations.py server_results/mesh_4_lex_wikidata/translations.de
python3 get_complete_translations.py server_results/mesh_4_lex_wikidata/translations.en
python3 get_complete_translations.py server_results/mesh_4_lex_wikidata/translations.fr
python3 get_complete_translations.py server_results/mesh_4_lex_wikidata/translations.es
python3 get_complete_translations.py server_results/mesh_4_lex_wikidata/translations.none