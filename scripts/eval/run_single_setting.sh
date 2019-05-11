#!/bin/sh

/raid/bin/pubpsych/solr-6.6.5/bin/solr start -m 10g &&
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/"
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/" &&
# need to ensure that the very first query is Solr's built-in warm-up query and NOT the first query sent by the script
sleep 60 &&
python3 /home/sohe01/evaluations/run_evaluation.py /home/sohe01/evaluations/source.none 8983 &&
cp /home/sohe01/evaluations/stats.txt /home/sohe01/evaluations/stats.none &&
cp /home/sohe01/evaluations/translations.txt /home/sohe01/evaluations/translations.none &&
rm /home/sohe01/evaluations/translations.txt &&
touch /home/sohe01/evaluations/translations.txt &&
/raid/bin/pubpsych/solr-6.6.5/bin/solr stop &&
rm -rf /raid/bin/pubpsych/solr-6.6.5/server/logs/* &&

/raid/bin/pubpsych/solr-6.6.5/bin/solr start -m 10g &&
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/" 
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/" &&
sleep 60 &&
python3 /home/sohe01/evaluations/run_evaluation.py /home/sohe01/evaluations/source.de 8983 &&
cp /home/sohe01/evaluations/stats.txt /home/sohe01/evaluations/stats.de &&
cp /home/sohe01/evaluations/translations.txt /home/sohe01/evaluations/translations.de &&
rm /home/sohe01/evaluations/translations.txt &&
touch /home/sohe01/evaluations/translations.txt &&
/raid/bin/pubpsych/solr-6.6.5/bin/solr stop &&
rm -rf /raid/bin/pubpsych/solr-6.6.5/server/logs/* &&

/raid/bin/pubpsych/solr-6.6.5/bin/solr start -m 10g &&
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/"
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/" &&
sleep 60 &&
python3 /home/sohe01/evaluations/run_evaluation.py /home/sohe01/evaluations/source.en 8983 &&
cp /home/sohe01/evaluations/stats.txt /home/sohe01/evaluations/stats.en &&
cp /home/sohe01/evaluations/translations.txt /home/sohe01/evaluations/translations.en &&
rm /home/sohe01/evaluations/translations.txt &&
touch /home/sohe01/evaluations/translations.txt &&
/raid/bin/pubpsych/solr-6.6.5/bin/solr stop &&
rm -rf /raid/bin/pubpsych/solr-6.6.5/server/logs/* &&

/raid/bin/pubpsych/solr-6.6.5/bin/solr start -m 10g &&
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/"
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/" &&
sleep 60 &&
python3 /home/sohe01/evaluations/run_evaluation.py /home/sohe01/evaluations/source.fr 8983 &&
cp /home/sohe01/evaluations/stats.txt /home/sohe01/evaluations/stats.fr &&
cp /home/sohe01/evaluations/translations.txt /home/sohe01/evaluations/translations.fr &&
rm /home/sohe01/evaluations/translations.txt &&
touch /home/sohe01/evaluations/translations.txt &&
/raid/bin/pubpsych/solr-6.6.5/bin/solr stop &&
rm -rf /raid/bin/pubpsych/solr-6.6.5/server/logs/* &&

/raid/bin/pubpsych/solr-6.6.5/bin/solr start -m 10g &&
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/"
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=pubpsych-core&instanceDir=/raid/bin/pubpsych/pubpsych-core/" &&
sleep 60 &&
python3 /home/sohe01/evaluations/run_evaluation.py /home/sohe01/evaluations/source.es 8983 &&
cp /home/sohe01/evaluations/stats.txt /home/sohe01/evaluations/stats.es &&
cp /home/sohe01/evaluations/translations.txt /home/sohe01/evaluations/translations.es &&
rm /home/sohe01/evaluations/translations.txt &&
touch /home/sohe01/evaluations/translations.txt &&
/raid/bin/pubpsych/solr-6.6.5/bin/solr stop &&
rm -rf /raid/bin/pubpsych/solr-6.6.5/server/logs/*
