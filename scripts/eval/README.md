#Scripts for the evaluation of queries

## run\_evaluation.py
- Usage: python3 run\_evaluation.py *path to source.la* _port of Solr instance_
- Sends all queries contained in _source.la_ to the Solr instance with the given core. Note that the instance needs an activated core.
- Translation and statistics outputs are stored in the paths specified by the variables *transPath* and *statsPath* in the ZpidQParser.java file.

## run_single_setting.sh
- Shell script to run the experiments for all _source.la_ files (_.en_, _.de_, _.fr_, _.es_ and _.none_) with an activated Solr instance (thus for one dictionary setting).
- Paths are chosen with respect to the DFKI Turing machine.

## run_all_settings.sh
- Copies the Java source code files for each setting to the right place, builds the whole PubPsychSolr project, copies the target jar to the right place, starts a Solr instance and then calls *run\_single\_setting.sh* for each setting.
- Needs the files that are contained in *server\_java\_backup* in the right place (cf. script).
- Paths are chosen with respect to the DFKI Turing machine.

## get_complete_translations.py
- Usage: python3 get\_complete\_translations.py *path to translations*
- Reads in a *translations.la* file (that contains the string representation of the translated SolrQueries) and compiles a file of the format "en::translation fr::translation es::translation" respectively "org::original query" (if the query could not be translated at all).

