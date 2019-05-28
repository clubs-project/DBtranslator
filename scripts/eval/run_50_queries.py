import sys
from subprocess import DEVNULL, STDOUT, check_call
from time import time
import re
import unicodedata
import string
'''Requires a Solr instance WITH ACTIVATED CORE running on the given port'''


def read_in(query_path):
    '''Reads in queries in the format as provided in the testQueriesIR.csv file:
    311240;psychological therapies AND ptsd;;;'''

    # we need to maintain the order of the queries for the evaluation
    queries = list()

    punctuation_regex = re.compile('[%s]' % re.escape(string.punctuation))
    whitespace_regex = re.compile('\s\s+')

    with open(query_path, 'r') as f:
        for line in f:

            # ignore the first line stating the format: id;query;;;
            if line.startswith("id"):
                continue
            raw_query = line.split(";")[1]
            tokens = raw_query.split()
            raw_tokens = list()
            for token in tokens:
                raw_token = token.strip().strip("\'")

                # do not lowercase Boolean operators
                if raw_token != "AND" and raw_token != "OR":
                    raw_token = raw_token.lower()
                # remove diacritics
                raw_token = unicodedata.normalize('NFKD', raw_token).encode('ASCII', 'ignore').decode()

                raw_token = raw_token.replace("-", " ")
                raw_token = raw_token.replace("'", " ")

                # String.punctuation only knows ASCII punctuation
                raw_token = punctuation_regex.sub(' ', raw_token)
                raw_token = whitespace_regex.sub(' ', raw_token)
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
        #if "\"" in search:
        #     print("Sending query: ", search)
        check_call(['curl', search], stdout=DEVNULL, stderr=STDOUT)
        if counter % 1000 == 0:
            print(counter, "queries are done!")
    print("Done after {:.1f} seconds.".format(time() - starting_time))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 run_50_queries.py <path to testQueriesIR.csv> <port of Solr instance>")
        sys.exit(1)

    queries = sys.argv[1]
    port = sys.argv[2]
    main(queries, port)