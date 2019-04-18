#!/bin/sh
rm -rf bleu-results-first-system.txt &&
touch bleu-results-first-system.txt &&

# German source
echo "From de to en with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-en.bleu < manualEvaluation/trads-from-de-to-en.bleu >> bleu-results-first-system.txt &&
echo "From de to en without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-en-sw.bleu < manualEvaluation/trads-from-de-to-en-sw.bleu >> bleu-results-first-system.txt &&
echo "From de to fr with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-fr.bleu < manualEvaluation/trads-from-de-to-fr.bleu >> bleu-results-first-system.txt &&
echo "From de to fr without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-fr-sw.bleu < manualEvaluation/trads-from-de-to-fr-sw.bleu >> bleu-results-first-system.txt &&
echo "From de to es with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-es.bleu < manualEvaluation/trads-from-de-to-es.bleu >> bleu-results-first-system.txt &&
echo "From de to es without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-de-to-es-sw.bleu < manualEvaluation/trads-from-de-to-es-sw.bleu >> bleu-results-first-system.txt &&

# English source
echo "From en to de with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-de.bleu < manualEvaluation/trads-from-en-to-de.bleu >> bleu-results-first-system.txt &&
echo "From en to de without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-de-sw.bleu < manualEvaluation/trads-from-en-to-de-sw.bleu >> bleu-results-first-system.txt &&
echo "From en to fr with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-fr.bleu < manualEvaluation/trads-from-en-to-fr.bleu >> bleu-results-first-system.txt &&
echo "From en to fr without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-fr-sw.bleu < manualEvaluation/trads-from-en-to-fr-sw.bleu >> bleu-results-first-system.txt &&
echo "From en to es with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-es.bleu < manualEvaluation/trads-from-en-to-es.bleu >> bleu-results-first-system.txt &&
echo "From en to es without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-en-to-es-sw.bleu < manualEvaluation/trads-from-en-to-es-sw.bleu >> bleu-results-first-system.txt &&

# French source
echo "From fr to de with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-de.bleu < manualEvaluation/trads-from-fr-to-de.bleu >> bleu-results-first-system.txt &&
echo "From fr to de without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-de-sw.bleu < manualEvaluation/trads-from-fr-to-de-sw.bleu >> bleu-results-first-system.txt &&
echo "From fr to en with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-en.bleu < manualEvaluation/trads-from-fr-to-en.bleu >> bleu-results-first-system.txt &&
echo "From fr to en without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-en-sw.bleu < manualEvaluation/trads-from-fr-to-en-sw.bleu >> bleu-results-first-system.txt &&
echo "From fr to es with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-es.bleu < manualEvaluation/trads-from-fr-to-es.bleu >> bleu-results-first-system.txt &&
echo "From fr to es without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-fr-to-es-sw.bleu < manualEvaluation/trads-from-fr-to-es-sw.bleu >> bleu-results-first-system.txt &&

# Spanish source
echo "From es to de with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-de.bleu < manualEvaluation/trads-from-es-to-de.bleu >> bleu-results-first-system.txt &&
echo "From es to de without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-de-sw.bleu < manualEvaluation/trads-from-es-to-de-sw.bleu >> bleu-results-first-system.txt &&
echo "From es to en with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-en.bleu < manualEvaluation/trads-from-es-to-en.bleu >> bleu-results-first-system.txt &&
echo "From es to en without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-en-sw.bleu < manualEvaluation/trads-from-es-to-en-sw.bleu >> bleu-results-first-system.txt &&
echo "From es to fr with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-fr.bleu < manualEvaluation/trads-from-es-to-fr.bleu >> bleu-results-first-system.txt &&
echo "From es to fr without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-es-to-fr-sw.bleu < manualEvaluation/trads-from-es-to-fr-sw.bleu >> bleu-results-first-system.txt &&

# None source
echo "From none to de with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-none-to-de.bleu < manualEvaluation/trads-from-none-to-de.bleu >> bleu-results-first-system.txt &&
echo "From none to de without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-none-to-de-sw.bleu < manualEvaluation/trads-from-none-to-de-sw.bleu >> bleu-results-first-system.txt &&
echo "From none to en with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-none-to-en.bleu < manualEvaluation/trads-from-none-to-en.bleu >> bleu-results-first-system.txt &&
echo "From none to en without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-none-to-en-sw.bleu < manualEvaluation/trads-from-none-to-en-sw.bleu >> bleu-results-first-system.txt &&
echo "From none to fr with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-none-to-fr.bleu < manualEvaluation/trads-from-none-to-fr.bleu >> bleu-results-first-system.txt &&
echo "From none to fr without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-none-to-fr-sw.bleu < manualEvaluation/trads-from-none-to-fr-sw.bleu >> bleu-results-first-system.txt &&
echo "From none to es with stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-none-to-es.bleu < manualEvaluation/trads-from-none-to-es.bleu >> bleu-results-first-system.txt &&
echo "From none to es without stopwords:" >> bleu-results-first-system.txt &&
perl multi-bleu.perl translatedQueriesManual/done/target-from-none-to-es-sw.bleu < manualEvaluation/trads-from-none-to-es-sw.bleu >> bleu-results-first-system.txt
