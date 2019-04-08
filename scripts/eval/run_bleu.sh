#!/bin/sh

touch bleu-results.txt &&

# Mesh_4_lex_wikidata
echo "Results of Mesh combined with the concatenation of the quadrilingual dict and the wikidata dictionary:" >> bleu-results.txt

# German source
echo "From de to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-en.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-de-to-en.bleu >> bleu-results.txt
echo "From de to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-en-sw.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-de-to-en-sw.bleu >> bleu-results.txt
echo "From de to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-fr.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-de-to-fr.bleu >> bleu-results.txt
echo "From de to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-fr-sw.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-de-to-fr-sw.bleu >> bleu-results.txt
echo "From de to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-es.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-de-to-es.bleu >> bleu-results.txt
echo "From de to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-es-sw.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-de-to-es-sw.bleu >> bleu-results.txt

# English source
echo "From en to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-de.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-en-to-de.bleu >> bleu-results.txt
echo "From en to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-de-sw.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-en-to-de-sw.bleu >> bleu-results.txt
echo "From en to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-fr.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-en-to-fr.bleu >> bleu-results.txt
echo "From en to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-fr-sw.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-en-to-fr-sw.bleu >> bleu-results.txt
echo "From en to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-es.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-en-to-es.bleu >> bleu-results.txt
echo "From en to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-es-sw.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-en-to-es-sw.bleu >> bleu-results.txt

# French source
echo "From fr to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-de.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-fr-to-de.bleu >> bleu-results.txt
echo "From fr to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-de-sw.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-fr-to-de-sw.bleu >> bleu-results.txt
echo "From fr to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-en.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-fr-to-en.bleu >> bleu-results.txt
echo "From fr to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-en-sw.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-fr-to-en-sw.bleu >> bleu-results.txt
echo "From fr to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-es.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-fr-to-es.bleu >> bleu-results.txt
echo "From fr to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-es-sw.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-fr-to-es-sw.bleu >> bleu-results.txt

# Spanish source
echo "From es to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-de.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-es-to-de.bleu >> bleu-results.txt
echo "From es to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-de-sw.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-es-to-de-sw.bleu >> bleu-results.txt
echo "From es to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-en.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-es-to-en.bleu >> bleu-results.txt
echo "From es to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-en-sw.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-es-to-en-sw.bleu >> bleu-results.txt
echo "From es to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-fr.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-es-to-fr.bleu >> bleu-results.txt
echo "From es to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-fr-sw.bleu < server_results/mesh_4_lex_wikidata/target_qfr-from-es-to-fr-sw.bleu >> bleu-results.txt


# Mesh
echo "\nResults of Mesh:" >> bleu-results.txt

# German source
echo "From de to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-en.bleu < server_results/mesh/target_qfr-from-de-to-en.bleu >> bleu-results.txt
echo "From de to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-en-sw.bleu < server_results/mesh/target_qfr-from-de-to-en-sw.bleu >> bleu-results.txt
echo "From de to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-fr.bleu < server_results/mesh/target_qfr-from-de-to-fr.bleu >> bleu-results.txt
echo "From de to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-fr-sw.bleu < server_results/mesh/target_qfr-from-de-to-fr-sw.bleu >> bleu-results.txt
echo "From de to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-es.bleu < server_results/mesh/target_qfr-from-de-to-es.bleu >> bleu-results.txt
echo "From de to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-es-sw.bleu < server_results/mesh/target_qfr-from-de-to-es-sw.bleu >> bleu-results.txt

# English source
echo "From en to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-de.bleu < server_results/mesh/target_qfr-from-en-to-de.bleu >> bleu-results.txt
echo "From en to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-de-sw.bleu < server_results/mesh/target_qfr-from-en-to-de-sw.bleu >> bleu-results.txt
echo "From en to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-fr.bleu < server_results/mesh/target_qfr-from-en-to-fr.bleu >> bleu-results.txt
echo "From en to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-fr-sw.bleu < server_results/mesh/target_qfr-from-en-to-fr-sw.bleu >> bleu-results.txt
echo "From en to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-es.bleu < server_results/mesh/target_qfr-from-en-to-es.bleu >> bleu-results.txt
echo "From en to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-es-sw.bleu < server_results/mesh/target_qfr-from-en-to-es-sw.bleu >> bleu-results.txt

# French source
echo "From fr to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-de.bleu < server_results/mesh/target_qfr-from-fr-to-de.bleu >> bleu-results.txt
echo "From fr to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-de-sw.bleu < server_results/mesh/target_qfr-from-fr-to-de-sw.bleu >> bleu-results.txt
echo "From fr to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-en.bleu < server_results/mesh/target_qfr-from-fr-to-en.bleu >> bleu-results.txt
echo "From fr to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-en-sw.bleu < server_results/mesh/target_qfr-from-fr-to-en-sw.bleu >> bleu-results.txt
echo "From fr to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-es.bleu < server_results/mesh/target_qfr-from-fr-to-es.bleu >> bleu-results.txt
echo "From fr to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-es-sw.bleu < server_results/mesh/target_qfr-from-fr-to-es-sw.bleu >> bleu-results.txt

# Spanish source
echo "From es to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-de.bleu < server_results/mesh/target_qfr-from-es-to-de.bleu >> bleu-results.txt
echo "From es to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-de-sw.bleu < server_results/mesh/target_qfr-from-es-to-de-sw.bleu >> bleu-results.txt
echo "From es to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-en.bleu < server_results/mesh/target_qfr-from-es-to-en.bleu >> bleu-results.txt
echo "From es to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-en-sw.bleu < server_results/mesh/target_qfr-from-es-to-en-sw.bleu >> bleu-results.txt
echo "From es to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-fr.bleu < server_results/mesh/target_qfr-from-es-to-fr.bleu >> bleu-results.txt
echo "From es to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-fr-sw.bleu < server_results/mesh/target_qfr-from-es-to-fr-sw.bleu >> bleu-results.txt

# 4lex_diff
echo "\nResults of the quadrilingual dictionary (diff version):" >> bleu-results.txt

# German source
echo "From de to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-en.bleu < server_results/4lex_diff/target_qfr-from-de-to-en.bleu >> bleu-results.txt
echo "From de to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-en-sw.bleu < server_results/4lex_diff/target_qfr-from-de-to-en-sw.bleu >> bleu-results.txt
echo "From de to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-fr.bleu < server_results/4lex_diff/target_qfr-from-de-to-fr.bleu >> bleu-results.txt
echo "From de to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-fr-sw.bleu < server_results/4lex_diff/target_qfr-from-de-to-fr-sw.bleu >> bleu-results.txt
echo "From de to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-es.bleu < server_results/4lex_diff/target_qfr-from-de-to-es.bleu >> bleu-results.txt
echo "From de to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-es-sw.bleu < server_results/4lex_diff/target_qfr-from-de-to-es-sw.bleu >> bleu-results.txt

# English source
echo "From en to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-de.bleu < server_results/4lex_diff/target_qfr-from-en-to-de.bleu >> bleu-results.txt
echo "From en to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-de-sw.bleu < server_results/4lex_diff/target_qfr-from-en-to-de-sw.bleu >> bleu-results.txt
echo "From en to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-fr.bleu < server_results/4lex_diff/target_qfr-from-en-to-fr.bleu >> bleu-results.txt
echo "From en to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-fr-sw.bleu < server_results/4lex_diff/target_qfr-from-en-to-fr-sw.bleu >> bleu-results.txt
echo "From en to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-es.bleu < server_results/4lex_diff/target_qfr-from-en-to-es.bleu >> bleu-results.txt
echo "From en to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-es-sw.bleu < server_results/4lex_diff/target_qfr-from-en-to-es-sw.bleu >> bleu-results.txt

# French source
echo "From fr to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-de.bleu < server_results/4lex_diff/target_qfr-from-fr-to-de.bleu >> bleu-results.txt
echo "From fr to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-de-sw.bleu < server_results/4lex_diff/target_qfr-from-fr-to-de-sw.bleu >> bleu-results.txt
echo "From fr to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-en.bleu < server_results/4lex_diff/target_qfr-from-fr-to-en.bleu >> bleu-results.txt
echo "From fr to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-en-sw.bleu < server_results/4lex_diff/target_qfr-from-fr-to-en-sw.bleu >> bleu-results.txt
echo "From fr to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-es.bleu < server_results/4lex_diff/target_qfr-from-fr-to-es.bleu >> bleu-results.txt
echo "From fr to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-es-sw.bleu < server_results/4lex_diff/target_qfr-from-fr-to-es-sw.bleu >> bleu-results.txt

# Spanish source
echo "From es to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-de.bleu < server_results/4lex_diff/target_qfr-from-es-to-de.bleu >> bleu-results.txt
echo "From es to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-de-sw.bleu < server_results/4lex_diff/target_qfr-from-es-to-de-sw.bleu >> bleu-results.txt
echo "From es to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-en.bleu < server_results/4lex_diff/target_qfr-from-es-to-en.bleu >> bleu-results.txt
echo "From es to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-en-sw.bleu < server_results/4lex_diff/target_qfr-from-es-to-en-sw.bleu >> bleu-results.txt
echo "From es to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-fr.bleu < server_results/4lex_diff/target_qfr-from-es-to-fr.bleu >> bleu-results.txt
echo "From es to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-fr-sw.bleu < server_results/4lex_diff/target_qfr-from-es-to-fr-sw.bleu >> bleu-results.txt

# 4lex_non_diff
echo "\nResults of the quadrilingual dictionary (non-diff version):" >> bleu-results.txt

# German source
echo "From de to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-en.bleu < server_results/4lex_non_diff/target_qfr-from-de-to-en.bleu >> bleu-results.txt
echo "From de to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-en-sw.bleu < server_results/4lex_non_diff/target_qfr-from-de-to-en-sw.bleu >> bleu-results.txt
echo "From de to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-fr.bleu < server_results/4lex_non_diff/target_qfr-from-de-to-fr.bleu >> bleu-results.txt
echo "From de to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-fr-sw.bleu < server_results/4lex_non_diff/target_qfr-from-de-to-fr-sw.bleu >> bleu-results.txt
echo "From de to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-es.bleu < server_results/4lex_non_diff/target_qfr-from-de-to-es.bleu >> bleu-results.txt
echo "From de to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-es-sw.bleu < server_results/4lex_non_diff/target_qfr-from-de-to-es-sw.bleu >> bleu-results.txt

# English source
echo "From en to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-de.bleu < server_results/4lex_non_diff/target_qfr-from-en-to-de.bleu >> bleu-results.txt
echo "From en to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-de-sw.bleu < server_results/4lex_non_diff/target_qfr-from-en-to-de-sw.bleu >> bleu-results.txt
echo "From en to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-fr.bleu < server_results/4lex_non_diff/target_qfr-from-en-to-fr.bleu >> bleu-results.txt
echo "From en to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-fr-sw.bleu < server_results/4lex_non_diff/target_qfr-from-en-to-fr-sw.bleu >> bleu-results.txt
echo "From en to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-es.bleu < server_results/4lex_non_diff/target_qfr-from-en-to-es.bleu >> bleu-results.txt
echo "From en to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-es-sw.bleu < server_results/4lex_non_diff/target_qfr-from-en-to-es-sw.bleu >> bleu-results.txt

# French source
echo "From fr to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-de.bleu < server_results/4lex_non_diff/target_qfr-from-fr-to-de.bleu >> bleu-results.txt
echo "From fr to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-de-sw.bleu < server_results/4lex_non_diff/target_qfr-from-fr-to-de-sw.bleu >> bleu-results.txt
echo "From fr to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-en.bleu < server_results/4lex_non_diff/target_qfr-from-fr-to-en.bleu >> bleu-results.txt
echo "From fr to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-en-sw.bleu < server_results/4lex_non_diff/target_qfr-from-fr-to-en-sw.bleu >> bleu-results.txt
echo "From fr to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-es.bleu < server_results/4lex_non_diff/target_qfr-from-fr-to-es.bleu >> bleu-results.txt
echo "From fr to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-es-sw.bleu < server_results/4lex_non_diff/target_qfr-from-fr-to-es-sw.bleu >> bleu-results.txt

# Spanish source
echo "From es to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-de.bleu < server_results/4lex_non_diff/target_qfr-from-es-to-de.bleu >> bleu-results.txt
echo "From es to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-de-sw.bleu < server_results/4lex_non_diff/target_qfr-from-es-to-de-sw.bleu >> bleu-results.txt
echo "From es to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-en.bleu < server_results/4lex_non_diff/target_qfr-from-es-to-en.bleu >> bleu-results.txt
echo "From es to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-en-sw.bleu < server_results/4lex_non_diff/target_qfr-from-es-to-en-sw.bleu >> bleu-results.txt
echo "From es to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-fr.bleu < server_results/4lex_non_diff/target_qfr-from-es-to-fr.bleu >> bleu-results.txt
echo "From es to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-fr-sw.bleu < server_results/4lex_non_diff/target_qfr-from-es-to-fr-sw.bleu >> bleu-results.txt

# wikidata_diff
echo "\nResults of the wikidata dictionary (diff version):" >> bleu-results.txt

# German source
echo "From de to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-en.bleu < server_results/wikidata_diff/target_qfr-from-de-to-en.bleu >> bleu-results.txt
echo "From de to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-en-sw.bleu < server_results/wikidata_diff/target_qfr-from-de-to-en-sw.bleu >> bleu-results.txt
echo "From de to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-fr.bleu < server_results/wikidata_diff/target_qfr-from-de-to-fr.bleu >> bleu-results.txt
echo "From de to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-fr-sw.bleu < server_results/wikidata_diff/target_qfr-from-de-to-fr-sw.bleu >> bleu-results.txt
echo "From de to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-es.bleu < server_results/wikidata_diff/target_qfr-from-de-to-es.bleu >> bleu-results.txt
echo "From de to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-es-sw.bleu < server_results/wikidata_diff/target_qfr-from-de-to-es-sw.bleu >> bleu-results.txt

# English source
echo "From en to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-de.bleu < server_results/wikidata_diff/target_qfr-from-en-to-de.bleu >> bleu-results.txt
echo "From en to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-de-sw.bleu < server_results/wikidata_diff/target_qfr-from-en-to-de-sw.bleu >> bleu-results.txt
echo "From en to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-fr.bleu < server_results/wikidata_diff/target_qfr-from-en-to-fr.bleu >> bleu-results.txt
echo "From en to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-fr-sw.bleu < server_results/wikidata_diff/target_qfr-from-en-to-fr-sw.bleu >> bleu-results.txt
echo "From en to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-es.bleu < server_results/wikidata_diff/target_qfr-from-en-to-es.bleu >> bleu-results.txt
echo "From en to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-es-sw.bleu < server_results/wikidata_diff/target_qfr-from-en-to-es-sw.bleu >> bleu-results.txt

# French source
echo "From fr to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-de.bleu < server_results/wikidata_diff/target_qfr-from-fr-to-de.bleu >> bleu-results.txt
echo "From fr to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-de-sw.bleu < server_results/wikidata_diff/target_qfr-from-fr-to-de-sw.bleu >> bleu-results.txt
echo "From fr to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-en.bleu < server_results/wikidata_diff/target_qfr-from-fr-to-en.bleu >> bleu-results.txt
echo "From fr to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-en-sw.bleu < server_results/wikidata_diff/target_qfr-from-fr-to-en-sw.bleu >> bleu-results.txt
echo "From fr to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-es.bleu < server_results/wikidata_diff/target_qfr-from-fr-to-es.bleu >> bleu-results.txt
echo "From fr to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-es-sw.bleu < server_results/wikidata_diff/target_qfr-from-fr-to-es-sw.bleu >> bleu-results.txt

# Spanish source
echo "From es to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-de.bleu < server_results/wikidata_diff/target_qfr-from-es-to-de.bleu >> bleu-results.txt
echo "From es to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-de-sw.bleu < server_results/wikidata_diff/target_qfr-from-es-to-de-sw.bleu >> bleu-results.txt
echo "From es to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-en.bleu < server_results/wikidata_diff/target_qfr-from-es-to-en.bleu >> bleu-results.txt
echo "From es to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-en-sw.bleu < server_results/wikidata_diff/target_qfr-from-es-to-en-sw.bleu >> bleu-results.txt
echo "From es to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-fr.bleu < server_results/wikidata_diff/target_qfr-from-es-to-fr.bleu >> bleu-results.txt
echo "From es to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-fr-sw.bleu < server_results/wikidata_diff/target_qfr-from-es-to-fr-sw.bleu >> bleu-results.txt

# wikidata_non_diff
echo "\nResults of the wikidata dictionary (non-diff version):" >> bleu-results.txt

# German source
echo "From de to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-en.bleu < server_results/wikidata_non_diff/target_qfr-from-de-to-en.bleu >> bleu-results.txt
echo "From de to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-en-sw.bleu < server_results/wikidata_non_diff/target_qfr-from-de-to-en-sw.bleu >> bleu-results.txt
echo "From de to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-fr.bleu < server_results/wikidata_non_diff/target_qfr-from-de-to-fr.bleu >> bleu-results.txt
echo "From de to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-fr-sw.bleu < server_results/wikidata_non_diff/target_qfr-from-de-to-fr-sw.bleu >> bleu-results.txt
echo "From de to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-es.bleu < server_results/wikidata_non_diff/target_qfr-from-de-to-es.bleu >> bleu-results.txt
echo "From de to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-es-sw.bleu < server_results/wikidata_non_diff/target_qfr-from-de-to-es-sw.bleu >> bleu-results.txt

# English source
echo "From en to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-de.bleu < server_results/wikidata_non_diff/target_qfr-from-en-to-de.bleu >> bleu-results.txt
echo "From en to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-de-sw.bleu < server_results/wikidata_non_diff/target_qfr-from-en-to-de-sw.bleu >> bleu-results.txt
echo "From en to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-fr.bleu < server_results/wikidata_non_diff/target_qfr-from-en-to-fr.bleu >> bleu-results.txt
echo "From en to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-fr-sw.bleu < server_results/wikidata_non_diff/target_qfr-from-en-to-fr-sw.bleu >> bleu-results.txt
echo "From en to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-es.bleu < server_results/wikidata_non_diff/target_qfr-from-en-to-es.bleu >> bleu-results.txt
echo "From en to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-es-sw.bleu < server_results/wikidata_non_diff/target_qfr-from-en-to-es-sw.bleu >> bleu-results.txt

# French source
echo "From fr to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-de.bleu < server_results/wikidata_non_diff/target_qfr-from-fr-to-de.bleu >> bleu-results.txt
echo "From fr to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-de-sw.bleu < server_results/wikidata_non_diff/target_qfr-from-fr-to-de-sw.bleu >> bleu-results.txt
echo "From fr to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-en.bleu < server_results/wikidata_non_diff/target_qfr-from-fr-to-en.bleu >> bleu-results.txt
echo "From fr to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-en-sw.bleu < server_results/wikidata_non_diff/target_qfr-from-fr-to-en-sw.bleu >> bleu-results.txt
echo "From fr to es with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-es.bleu < server_results/wikidata_non_diff/target_qfr-from-fr-to-es.bleu >> bleu-results.txt
echo "From fr to es without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-es-sw.bleu < server_results/wikidata_non_diff/target_qfr-from-fr-to-es-sw.bleu >> bleu-results.txt

# Spanish source
echo "From es to de with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-de.bleu < server_results/wikidata_non_diff/target_qfr-from-es-to-de.bleu >> bleu-results.txt
echo "From es to de without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-de-sw.bleu < server_results/wikidata_non_diff/target_qfr-from-es-to-de-sw.bleu >> bleu-results.txt
echo "From es to en with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-en.bleu < server_results/wikidata_non_diff/target_qfr-from-es-to-en.bleu >> bleu-results.txt
echo "From es to en without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-en-sw.bleu < server_results/wikidata_non_diff/target_qfr-from-es-to-en-sw.bleu >> bleu-results.txt
echo "From es to fr with stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-fr.bleu < server_results/wikidata_non_diff/target_qfr-from-es-to-fr.bleu >> bleu-results.txt
echo "From es to fr without stopwords:" >> bleu-results.txt
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-fr-sw.bleu < server_results/wikidata_non_diff/target_qfr-from-es-to-fr-sw.bleu >> bleu-results.txt
