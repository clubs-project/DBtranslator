#!/bin/sh
rm -rf bleu-results.txt &&
touch bleu-results.txt &&

# English source
echo "From en to de with stopwords:" >> bleu-results.txt
perl ../multi-bleu.perl Goldstandard/de.1 Goldstandard/de.2 < final_system_translations/target_qfr_man2-from-txt-to-de.bleu >> bleu-results.txt
echo "From en to de without stopwords:" >> bleu-results.txt
perl ../multi-bleu.perl Goldstandard/de_sw.1 Goldstandard/de_sw.2 < final_system_translations/target_qfr_man2-from-txt-to-de-sw.bleu >> bleu-results.txt
echo "From en to fr with stopwords:" >> bleu-results.txt
perl ../multi-bleu.perl Goldstandard/fr.1 < final_system_translations/target_qfr_man2-from-txt-to-fr.bleu >> bleu-results.txt
echo "From en to fr without stopwords:" >> bleu-results.txt
perl ../multi-bleu.perl Goldstandard/fr_sw.1 < final_system_translations/target_qfr_man2-from-txt-to-fr-sw.bleu >> bleu-results.txt
echo "From en to es with stopwords:" >> bleu-results.txt
perl ../multi-bleu.perl Goldstandard/es.1 Goldstandard/es.2 < final_system_translations/target_qfr_man2-from-txt-to-es.bleu >> bleu-results.txt
echo "From en to es without stopwords:" >> bleu-results.txt
perl ../multi-bleu.perl Goldstandard/es_sw.1 Goldstandard/es_sw.2 < final_system_translations/target_qfr_man2-from-txt-to-es-sw.bleu >> bleu-results.txt
