import sys
from subprocess import DEVNULL, STDOUT, check_call
from time import time
import re
import unicodedata
import string
'''Requires a Solr instance WITH ACTIVATED CORE running on the given port'''


def concatenate_string_list(string_list, string_between_strings=" ", add_at_last_string=False):
    '''Concatenates a list of strings into a single string with string_between_strings added between the former elements of the list'''
    result = ""
    for i in range(len(string_list)):
        # last element of string list and we don't want to add string_between_strings to the last string
        if i == len(string_list)-1 and not add_at_last_string:
            result += string_list[i].strip()

        # we want to add string_between_String
        else:
            result += string_list[i].strip() + string_between_strings
    return result


def read_in(query_path):
    '''Reads in queries in the format as provided in the source.la files:
    Q327011	['forderbedarf', 'selbstkonzept'] will be stored as "forderbedarf selbstkonzept" '''

    # we need to maintain the order of the queries for the evaluation
    queries = list()

    # match the part between the two embracing brackets
    tokens_re = re.compile('(?<=\[)[^\[\]]+(?=\])')

    punctuation_regex = re.compile('[%s]' % re.escape(string.punctuation))
    with open(query_path, 'r') as f:
        for line in f:
            tokens = tokens_re.search(line).group()
            tokens = tokens.split(",")
            raw_tokens = list()
            for token in tokens:
                raw_token = token.strip().strip("\'")
                raw_token = raw_token.lower()
                # remove diacritics
                raw_token = unicodedata.normalize('NFKD', raw_token).encode('ASCII', 'ignore').decode()

                # String.punctuation only knows ASCII punctuation
                raw_token = punctuation_regex.sub(' ', raw_token)
                raw_token = raw_token.replace(" ", "%20")
                raw_tokens.append(raw_token)

            # %20 for whitespace (assuming "%" is not used in the source files)
            query = concatenate_string_list(raw_tokens, "%20")
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

if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 run_evaluation.py <path to source.la> <port of Solr instance>")
        sys.exit(1)

    queries = sys.argv[1]
    port = sys.argv[2]
    main(queries, port)

