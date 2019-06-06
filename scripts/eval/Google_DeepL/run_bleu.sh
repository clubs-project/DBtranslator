#!/bin/sh
rm -rf bleu-results.txt &&
touch bleu-results.txt &&

# German source
echo "From de to en with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-de-to-en.bleu < from-de-to-en.bleu >> bleu-results.txt
echo "From de to en without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-de-to-en-sw.bleu < from-de-to-en-sw.bleu >> bleu-results.txt
echo "From de to fr with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-de-to-fr.bleu < from-de-to-fr.bleu >> bleu-results.txt
echo "From de to fr without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-de-to-fr-sw.bleu < from-de-to-fr-sw.bleu >> bleu-results.txt
echo "From de to es with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-de-to-es.bleu < from-de-to-es.bleu >> bleu-results.txt
echo "From de to es without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-de-to-es-sw.bleu < from-de-to-es-sw.bleu >> bleu-results.txt

# English source
echo "From en to de with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-en-to-de.bleu < from-en-to-de.bleu >> bleu-results.txt
echo "From en to de without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-en-to-de-sw.bleu < from-en-to-de-sw.bleu >> bleu-results.txt
echo "From en to fr with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-en-to-fr.bleu < from-en-to-fr.bleu >> bleu-results.txt
echo "From en to fr without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-en-to-fr-sw.bleu < from-en-to-fr-sw.bleu >> bleu-results.txt
echo "From en to es with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-en-to-es.bleu < from-en-to-es.bleu >> bleu-results.txt
echo "From en to es without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-en-to-es-sw.bleu < from-en-to-es-sw.bleu >> bleu-results.txt

# French source
echo "From fr to de with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-fr-to-de.bleu < from-fr-to-de.bleu >> bleu-results.txt
echo "From fr to de without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-fr-to-de-sw.bleu < from-fr-to-de-sw.bleu >> bleu-results.txt
echo "From fr to en with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-fr-to-en.bleu < from-fr-to-en.bleu >> bleu-results.txt
echo "From fr to en without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-fr-to-en-sw.bleu < from-fr-to-en-sw.bleu >> bleu-results.txt
echo "From fr to es with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-fr-to-es.bleu < from-fr-to-es.bleu >> bleu-results.txt
echo "From fr to es without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-fr-to-es-sw.bleu < from-fr-to-es-sw.bleu >> bleu-results.txt

# Spanish source
echo "From es to de with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-es-to-de.bleu < from-es-to-de.bleu >> bleu-results.txt
echo "From es to de without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-es-to-de-sw.bleu < from-es-to-de-sw.bleu >> bleu-results.txt
echo "From es to en with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-es-to-en.bleu < from-es-to-en.bleu >> bleu-results.txt
echo "From es to en without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-es-to-en-sw.bleu < from-es-to-en-sw.bleu >> bleu-results.txt
echo "From es to fr with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-es-to-fr.bleu < from-es-to-fr.bleu >> bleu-results.txt
echo "From es to fr without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-es-to-fr-sw.bleu < from-es-to-fr-sw.bleu >> bleu-results.txt

# None source
echo "From none to de with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-none-to-de.bleu < from-none-to-de.bleu >> bleu-results.txt
echo "From none to de without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-none-to-de-sw.bleu < from-none-to-de-sw.bleu >> bleu-results.txt
echo "From none to en with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-none-to-en.bleu < from-none-to-en.bleu >> bleu-results.txt
echo "From none to en without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-none-to-en-sw.bleu < from-none-to-en-sw.bleu >> bleu-results.txt
echo "From none to fr with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-none-to-fr.bleu < from-none-to-fr.bleu >> bleu-results.txt
echo "From none to fr without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-none-to-fr-sw.bleu < from-none-to-fr-sw.bleu >> bleu-results.txt
echo "From none to es with stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-none-to-es.bleu < from-none-to-es.bleu >> bleu-results.txt
echo "From none to es without stopwords:" >> bleu-results.txt
perl ../../multi-bleu.perl ../../translatedQueriesManual/done/target-from-none-to-es-sw.bleu < from-none-to-es-sw.bleu >> bleu-results.txt
