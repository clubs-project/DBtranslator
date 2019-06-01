#!/bin/sh

rm -f /home/sohe01/evaluations/translations.txt &&
rm -f /home/sohe01/evaluations/stats.txt &&

touch /home/sohe01/evaluations/translations.txt &&
touch /home/sohe01/evaluations/stats.txt &&

cp -f /raid/bin/pubpsych_different_evaluation_settings/ZpidQParser.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/ &&


# Mesh_4lex_wikidata_non_diff
cp -f /raid/bin/pubpsych_different_evaluation_settings/mesh_4lex_wikidata_non_diff/QueryFieldRewriter.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/fieldrewriters/ &&
cp -f /raid/bin/pubpsych_different_evaluation_settings/mesh_4lex_wikidata_non_diff/ZpidQParserPlugin.java /raid/bin/PubPsychSolr/src/main/java/de/zpid/pubpsych/search/query/queryparsers/ &&
cp -f /raid/data/sohe01/dicts/evaluation/meshSplit2.solr.non-diff.all-languages.txt /raid/bin/PubPsychSolr/src/main/resources/queryfieldrewriter/ &&
cp -f /raid/data/sohe01/dicts/evaluation/wp.WPcat.untradDEallkeys.dictkeys.wikidata4Labels2.solr.non-diff.all-languages.txt /raid/bin/PubPsychSolr/src/main/resources/queryfieldrewriter/ &&
mvn package -Dmaven.test.skip=true && cp target/solr-backend-3.1.0-jar-with-dependencies.jar /raid/bin/pubpsych/pubpsych-core/lib/ &&

# German
/raid/bin/pubpsych/solr-6.6.5/bin/solr start -m 10g &&
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/"
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/" &&
# need to ensure that the very first query is Solr's built-in warm-up query and NOT the first query sent by the script
sleep 60 &&
python3 /home/sohe01/evaluations/run_50_queries.py /home/sohe01/evaluations/50_queries/queries.de 8983 &&
cp /home/sohe01/evaluations/stats.txt /home/sohe01/evaluations/50_queries/stats.de &&
cp /home/sohe01/evaluations/translations.txt /home/sohe01/evaluations/50_queries/translations.de &&
rm /home/sohe01/evaluations/translations.txt &&
touch /home/sohe01/evaluations/translations.txt &&
/raid/bin/pubpsych/solr-6.6.5/bin/solr stop &&
rm -rf /raid/bin/pubpsych/solr-6.6.5/server/logs/* &&

# English
/raid/bin/pubpsych/solr-6.6.5/bin/solr start -m 10g &&
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/"
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/" &&
# need to ensure that the very first query is Solr's built-in warm-up query and NOT the first query sent by the script
sleep 60 &&
python3 /home/sohe01/evaluations/run_50_queries.py /home/sohe01/evaluations/50_queries/queries.en 8983 &&
cp /home/sohe01/evaluations/stats.txt /home/sohe01/evaluations/50_queries/stats.en &&
cp /home/sohe01/evaluations/translations.txt /home/sohe01/evaluations/50_queries/translations.en &&
rm /home/sohe01/evaluations/translations.txt &&
touch /home/sohe01/evaluations/translations.txt &&
/raid/bin/pubpsych/solr-6.6.5/bin/solr stop &&
rm -rf /raid/bin/pubpsych/solr-6.6.5/server/logs/* &&

# French
/raid/bin/pubpsych/solr-6.6.5/bin/solr start -m 10g &&
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/"
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/" &&
# need to ensure that the very first query is Solr's built-in warm-up query and NOT the first query sent by the script
sleep 60 &&
python3 /home/sohe01/evaluations/run_50_queries.py /home/sohe01/evaluations/50_queries/queries.fr 8983 &&
cp /home/sohe01/evaluations/stats.txt /home/sohe01/evaluations/50_queries/stats.fr &&
cp /home/sohe01/evaluations/translations.txt /home/sohe01/evaluations/50_queries/translations.fr &&
rm /home/sohe01/evaluations/translations.txt &&
touch /home/sohe01/evaluations/translations.txt &&
/raid/bin/pubpsych/solr-6.6.5/bin/solr stop &&
rm -rf /raid/bin/pubpsych/solr-6.6.5/server/logs/* &&

# Spanish
/raid/bin/pubpsych/solr-6.6.5/bin/solr start -m 10g &&
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/"
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/" &&
# need to ensure that the very first query is Solr's built-in warm-up query and NOT the first query sent by the script
sleep 60 &&
python3 /home/sohe01/evaluations/run_50_queries.py /home/sohe01/evaluations/50_queries/queries.es 8983 &&
cp /home/sohe01/evaluations/stats.txt /home/sohe01/evaluations/50_queries/stats.es &&
cp /home/sohe01/evaluations/translations.txt /home/sohe01/evaluations/50_queries/translations.es &&
rm /home/sohe01/evaluations/translations.txt &&
touch /home/sohe01/evaluations/translations.txt &&
/raid/bin/pubpsych/solr-6.6.5/bin/solr stop &&
rm -rf /raid/bin/pubpsych/solr-6.6.5/server/logs/* 
