#!/bin/sh

touch /home/sohe01/evaluations/translations.txt &&
touch /home/sohe01/evaluations/stats.txt &&

cp -f /raid/bin/pubpsych_different_evaluation_settings/ZpidQParser.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/ &&

cp -f /raid/bin/pubpsych_different_evaluation_settings/mesh_4_lex_wikidata/QueryFieldRewriter.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/fieldrewriters/ &&
cp -f /raid/bin/pubpsych_different_evaluation_settings/mesh_4_lex_wikidata/ZpidQParserPlugin.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/ &&
cp -f /raid/data/sohe01/pubpsych_evaluation/wp.WPcat.untradDEallkeys.dictkeys.wikidata4Labels2.solr.non-diff.all-languages.txt /raid/bin/PubPsychSolr/src/main/resources/queryfieldrewriter/ &&
mvn package -Dmaven.test.skip=true && cp target/solr-backend-3.1.0-jar-with-dependencies.jar /raid/bin/pubpsych/pubpsych-core/lib/ &&
./run_single_setting.sh &&
mkdir /home/sohe01/evaluations/mesh_4_lex_wikidata/
mv /home/sohe01/evaluations/stats.de /home/sohe01/evaluations/mesh_4_lex_wikidata/
mv /home/sohe01/evaluations/stats.en /home/sohe01/evaluations/mesh_4_lex_wikidata/
mv /home/sohe01/evaluations/stats.fr /home/sohe01/evaluations/mesh_4_lex_wikidata/
mv /home/sohe01/evaluations/stats.es /home/sohe01/evaluations/mesh_4_lex_wikidata/
mv /home/sohe01/evaluations/stats.none /home/sohe01/evaluations/mesh_4_lex_wikidata/
mv /home/sohe01/evaluations/translations.de /home/sohe01/evaluations/mesh_4_lex_wikidata/
mv /home/sohe01/evaluations/translations.en /home/sohe01/evaluations/mesh_4_lex_wikidata/
mv /home/sohe01/evaluations/translations.fr /home/sohe01/evaluations/mesh_4_lex_wikidata/
mv /home/sohe01/evaluations/translations.es /home/sohe01/evaluations/mesh_4_lex_wikidata/
mv /home/sohe01/evaluations/translations.none /home/sohe01/evaluations/mesh_4_lex_wikidata/
rm -f /raid/bin/PubPsychSolr/src/main/resources/queryfieldrewriter/wp.WPcat.untradDEallkeys.dictkeys.wikidata4Labels2.solr.non-diff.all-languages.txt

cp -f /raid/bin/pubpsych_different_evaluation_settings/wikidata_non_diff/QueryFieldRewriter.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/fieldrewriters/ &&
cp -f /raid/bin/pubpsych_different_evaluation_settings/wikidata_non_diff/ZpidQParserPlugin.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/ &&
cp -f /raid/data/sohe01/pubpsych_evaluation/wikidata4Labels2.solr.non-diff.all-languages.txt /raid/bin/PubPsychSolr/src/main/resources/queryfieldrewriter/ &&
mvn package -Dmaven.test.skip=true && cp target/solr-backend-3.1.0-jar-with-dependencies.jar /raid/bin/pubpsych/pubpsych-core/lib/ &&
./run_single_setting.sh &&
mkdir /home/sohe01/evaluations/wikidata_non_diff/
mv /home/sohe01/evaluations/stats.de /home/sohe01/evaluations/wikidata_non_diff/
mv /home/sohe01/evaluations/stats.en /home/sohe01/evaluations/wikidata_non_diff/
mv /home/sohe01/evaluations/stats.fr /home/sohe01/evaluations/wikidata_non_diff/
mv /home/sohe01/evaluations/stats.es /home/sohe01/evaluations/wikidata_non_diff/
mv /home/sohe01/evaluations/stats.none /home/sohe01/evaluations/wikidata_non_diff/
mv /home/sohe01/evaluations/translations.de /home/sohe01/evaluations/wikidata_non_diff/
mv /home/sohe01/evaluations/translations.en /home/sohe01/evaluations/wikidata_non_diff/
mv /home/sohe01/evaluations/translations.fr /home/sohe01/evaluations/wikidata_non_diff/
mv /home/sohe01/evaluations/translations.es /home/sohe01/evaluations/wikidata_non_diff/
mv /home/sohe01/evaluations/translations.none /home/sohe01/evaluations/wikidata_non_diff/
rm -f /raid/bin/PubPsychSolr/src/main/resources/queryfieldrewriter/wikidata4Labels2.solr.non-diff.all-languages.txt

cp -f /raid/bin/pubpsych_different_evaluation_settings/wikidata_diff/QueryFieldRewriter.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/fieldrewriters/ &&
cp -f /raid/bin/pubpsych_different_evaluation_settings/wikidata_diff/ZpidQParserPlugin.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/ &&
cp -f /raid/data/sohe01/pubpsych_evaluation/wikidatadiffsLabels2.solr.diff.all-languages.txt /raid/bin/PubPsychSolr/src/main/resources/queryfieldrewriter/ &&
mvn package -Dmaven.test.skip=true && cp target/solr-backend-3.1.0-jar-with-dependencies.jar /raid/bin/pubpsych/pubpsych-core/lib/ &&
./run_single_setting.sh &&
mkdir /home/sohe01/evaluations/wikidata_diff/
mv /home/sohe01/evaluations/stats.de /home/sohe01/evaluations/wikidata_diff/
mv /home/sohe01/evaluations/stats.en /home/sohe01/evaluations/wikidata_diff/
mv /home/sohe01/evaluations/stats.fr /home/sohe01/evaluations/wikidata_diff/
mv /home/sohe01/evaluations/stats.es /home/sohe01/evaluations/wikidata_diff/
mv /home/sohe01/evaluations/stats.none /home/sohe01/evaluations/wikidata_diff/
mv /home/sohe01/evaluations/translations.de /home/sohe01/evaluations/wikidata_diff/
mv /home/sohe01/evaluations/translations.en /home/sohe01/evaluations/wikidata_diff/
mv /home/sohe01/evaluations/translations.fr /home/sohe01/evaluations/wikidata_diff/
mv /home/sohe01/evaluations/translations.es /home/sohe01/evaluations/wikidata_diff/
mv /home/sohe01/evaluations/translations.none /home/sohe01/evaluations/wikidata_diff/
rm -f /raid/bin/PubPsychSolr/src/main/resources/queryfieldrewriter/wikidatadiffsLabels2.solr.diff.all-languages.txt

cp -f /raid/bin/pubpsych_different_evaluation_settings/4lex_diff/QueryFieldRewriter.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/fieldrewriters/ &&
cp -f /raid/bin/pubpsych_different_evaluation_settings/4lex_diff/ZpidQParserPlugin.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/ &&
cp -f /raid/data/sohe01/pubpsych_evaluation/wp.WPcat.untradDEallkeys.dictkeys.solr.diff.all-languages.txt /raid/bin/PubPsychSolr/src/main/resources/queryfieldrewriter/ &&
mvn package -Dmaven.test.skip=true && cp target/solr-backend-3.1.0-jar-with-dependencies.jar /raid/bin/pubpsych/pubpsych-core/lib/ &&
./run_single_setting.sh &&
mkdir /home/sohe01/evaluations/4lex_diff/
mv /home/sohe01/evaluations/stats.de /home/sohe01/evaluations/4lex_diff/
mv /home/sohe01/evaluations/stats.en /home/sohe01/evaluations/4lex_diff/
mv /home/sohe01/evaluations/stats.fr /home/sohe01/evaluations/4lex_diff/
mv /home/sohe01/evaluations/stats.es /home/sohe01/evaluations/4lex_diff/
mv /home/sohe01/evaluations/stats.none /home/sohe01/evaluations/4lex_diff/
mv /home/sohe01/evaluations/translations.de /home/sohe01/evaluations/4lex_diff/
mv /home/sohe01/evaluations/translations.en /home/sohe01/evaluations/4lex_diff/
mv /home/sohe01/evaluations/translations.fr /home/sohe01/evaluations/4lex_diff/
mv /home/sohe01/evaluations/translations.es /home/sohe01/evaluations/4lex_diff/
mv /home/sohe01/evaluations/translations.none /home/sohe01/evaluations/4lex_diff/
rm -f /raid/bin/PubPsychSolr/src/main/resources/queryfieldrewriter/wp.WPcat.untradDEallkeys.dictkeys.solr.diff.all-languages.txt

cp -f /raid/bin/pubpsych_different_evaluation_settings/4lex_non_diff/QueryFieldRewriter.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/fieldrewriters/ &&
cp -f /raid/bin/pubpsych_different_evaluation_settings/4lex_non_diff/ZpidQParserPlugin.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/ &&
cp -f /raid/data/sohe01/pubpsych_evaluation/wp.WPcat.untradDEallkeys.dictkeys.solr.non-diff.all-languages.txt /raid/bin/PubPsychSolr/src/main/resources/queryfieldrewriter/ &&
mvn package -Dmaven.test.skip=true && cp target/solr-backend-3.1.0-jar-with-dependencies.jar /raid/bin/pubpsych/pubpsych-core/lib/ &&
./run_single_setting.sh &&
mkdir /home/sohe01/evaluations/4lex_non_diff/
mv /home/sohe01/evaluations/stats.de /home/sohe01/evaluations/4lex_non_diff/
mv /home/sohe01/evaluations/stats.en /home/sohe01/evaluations/4lex_non_diff/
mv /home/sohe01/evaluations/stats.fr /home/sohe01/evaluations/4lex_non_diff/
mv /home/sohe01/evaluations/stats.es /home/sohe01/evaluations/4lex_non_diff/
mv /home/sohe01/evaluations/stats.none /home/sohe01/evaluations/4lex_non_diff/
mv /home/sohe01/evaluations/translations.de /home/sohe01/evaluations/4lex_non_diff/
mv /home/sohe01/evaluations/translations.en /home/sohe01/evaluations/4lex_non_diff/
mv /home/sohe01/evaluations/translations.fr /home/sohe01/evaluations/4lex_non_diff/
mv /home/sohe01/evaluations/translations.es /home/sohe01/evaluations/4lex_non_diff/
mv /home/sohe01/evaluations/translations.none /home/sohe01/evaluations/4lex_non_diff/
rm -f /raid/bin/PubPsychSolr/src/main/resources/queryfieldrewriter/wp.WPcat.untradDEallkeys.dictkeys.solr.non-diff.all-languages.txt

cp -f /raid/bin/pubpsych_different_evaluation_settings/mesh/QueryFieldRewriter.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/fieldrewriters/ &&
cp -f /raid/bin/pubpsych_different_evaluation_settings/mesh/ZpidQParserPlugin.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/ &&
cp -f /raid/data/sohe01/pubpsych_evaluation/meshSplit2.solr.non-diff.all-languages.txt /raid/bin/PubPsychSolr/src/main/resources/queryfieldrewriter/ &&
mvn package -Dmaven.test.skip=true && cp target/solr-backend-3.1.0-jar-with-dependencies.jar /raid/bin/pubpsych/pubpsych-core/lib/ &&
./run_single_setting.sh &&
mkdir /home/sohe01/evaluations/mesh/
mv /home/sohe01/evaluations/stats.de /home/sohe01/evaluations/mesh/
mv /home/sohe01/evaluations/stats.en /home/sohe01/evaluations/mesh/
mv /home/sohe01/evaluations/stats.fr /home/sohe01/evaluations/mesh/
mv /home/sohe01/evaluations/stats.es /home/sohe01/evaluations/mesh/
mv /home/sohe01/evaluations/stats.none /home/sohe01/evaluations/mesh/
mv /home/sohe01/evaluations/translations.de /home/sohe01/evaluations/mesh/
mv /home/sohe01/evaluations/translations.en /home/sohe01/evaluations/mesh/
mv /home/sohe01/evaluations/translations.fr /home/sohe01/evaluations/mesh/
mv /home/sohe01/evaluations/translations.es /home/sohe01/evaluations/mesh/
mv /home/sohe01/evaluations/translations.none /home/sohe01/evaluations/mesh/
rm -f /raid/bin/PubPsychSolr/src/main/resources/queryfieldrewriter/meshSplit2.solr.non-diff.all-languages.txt
