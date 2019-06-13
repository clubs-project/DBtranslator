import sys
from subprocess import DEVNULL, STDOUT, check_call
from time import time
import re
import unicodedata
import string
'''Requires a Solr instance WITH ACTIVATED CORE running on the given port'''


def read_in(query_path):
    '''Reads in queries in the format as provided in the query.src file generated from the XLIFF queries with
    preprocess_xliff_queries.py:
    Psychosocial needs "Cancer patients" Palliative OR care PY>=2006 PY<=2016'''

    # we need to maintain the order of the queries for the evaluation
    queries = list()

    # Some punctuation has to be maintained in order to mark fields etc.
    punctuation_to_delete = string.punctuation.replace(":", "").replace("<", "").replace("=", "").replace(">", "").replace("\"", "")
    punctuation_regex = re.compile('[%s]' % re.escape(punctuation_to_delete))
    whitespace_regex = re.compile('\s\s+')

    with open(query_path, 'r') as f:
        for line in f:

            tokens = line.split()
            raw_tokens = list()
            for token in tokens:
                raw_token = token.strip()

                # remove diacritics
                raw_token = unicodedata.normalize('NFKD', raw_token).encode('ASCII', 'ignore').decode()

                # String.punctuation only knows ASCII punctuation
                raw_token = punctuation_regex.sub(' ', raw_token)
                raw_token = whitespace_regex.sub(' ', raw_token)
                raw_token = raw_token.strip()

                # ensure that token is not empty after all the preprocessing
                if raw_token:
                    raw_token = raw_token.replace(" ", "%20")
                    raw_tokens.append(raw_token)

            # %20 for whitespace (assuming "%" is not used in the source files)
            query = "%20".join(raw_tokens)
            queries.append(query)

    return queries


def main(query_path, port):
    print("Reading in queries...")
    queries = read_in(query_path)
    print("Number of queries:", len(queries))
    print("Passing queries to Solr instance on port " + port + "...")
    starting_time = time()
    counter = 0
    for query in queries:
        counter += 1

        search = 'http://localhost:' + port + '/solr/pubpsych-core/select?q=' + query
        #print("Sending query: ", search)
        check_call(['curl', search], stdout=DEVNULL, stderr=STDOUT)
    print("Done after {:.1f} seconds.".format(time() - starting_time))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 run_xliff.py <path to query.src> <port of Solr instance>")
        sys.exit(1)

    queries = sys.argv[1]
    port = sys.argv[2]
    main(queries, port)