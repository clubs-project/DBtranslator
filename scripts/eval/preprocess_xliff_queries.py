import re
import html
import argparse
import unicodedata
import string


class XLIFFer:

    # path_to_files: e.g. XLIFF_queries/translations/de/1_Anja/query_
    # number of queries n: will read in all files from query_1.xliff until query_n.xliff
    # la_code: {"de", "es", "fr"}
    def __init__(self, path_to_files, number_of_queries, generate_source=False):
        self.path = path_to_files
        self.num_queries = number_of_queries
        self.generate_source = generate_source
        if generate_source:
            self.source = []
            self.source_re = re.compile("(?<=<source>).+(?=</source)")
        self.target = []
        self.target_re = re.compile("(?<=target state=\"translated\">).+(?=</target)")
        punctuation_to_remove = string.punctuation.replace(":", "").replace("<", "").replace(">", "").replace("=", "").replace("\"", "")
        self.punctuation_regex = re.compile('[%s]' % re.escape(punctuation_to_remove))
        self.whitespace_regex = re.compile('\s\s+')

    def read_in(self):
        # we are interested in lines like <source>Psychosocial needs "Cancer patients" (Palliative OR care) PY&gt;=2006
        # PY&lt;=2016</source> <target state="translated">Psychosoziale Bedürfnisse "Krebspatienten" (palliativ OR Pflege)
        # PY&gt;=2006 PY&lt;=2016</target> </trans-unit>
        print("Reading in queries...")
        for i in range(1, self.num_queries+1):
            file_path = self.path + str(i) + ".xliff"
            with open(file_path, "r") as f:
                for line in f:
                    if self.generate_source:
                        self.get_match(line, False)

                    target_match_found = self.get_match(line)
                    if target_match_found:
                        # only one target per file -> don't have to read in the remaining lines
                        break
        print("Done.")

    def get_match(self, line, target=True):
        if target:
            regex = self.target_re
            collection = self.target
        else:
            regex = self.source_re
            collection = self.source
        match = regex.search(line)
        if match:
            match = match.group()
            match = html.unescape(match)
            # replace 'ß' with 'ss' since unicode.normalize simply deletes the whole character
            match = match.replace("ß", "ss")

            # remove diacritics
            match = unicodedata.normalize('NFKD', match).encode('ASCII', 'ignore').decode()

            # String.punctuation only knows ASCII punctuation
            match = self.punctuation_regex.sub(' ', match)
            match = self.whitespace_regex.sub(' ', match)
            collection.append(match)
            return True

    def write_to_file(self):
        tgt_path = self.path[:-1] + ".tgt"
        print("Writing target to path " + tgt_path + "...")
        with open(tgt_path, "w") as f:
            for target_line in self.target:
                f.write(target_line + "\n")
        print("Done.")
        if self.generate_source:
            src_path = self.path[:-1] + ".src"
            print("Writing source to path " + src_path + "...")
            with open(src_path, "w") as g:
                for src_line in self.source:
                    g.write(src_line + "\n")
            print("Done.")

    def run(self):
        self.read_in()
        self.write_to_file()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Converts the XLIFF queries into a file containing one translated query per line. Removes "
                    "punctuation and diacritics")
    argparser.add_argument("path_to_files", type=str, help="Path to XLIFF files, e.g. "
                                                           "XLIFF_queries/translations/de/1_Anja/query_")
    argparser.add_argument("number_of_queries", type=int, help="If this argument is n, the script will try to read in "
                                                               "all files from query_1.xliff until query_n.xliff")

    argparser.add_argument("-s", "--source", dest="generate_source", action='store_true',
                           help="If this option is set, the script will not only generate a target (translated) file, "
                                "but also one containing the source queries")
    args = argparser.parse_args()

    converter = XLIFFer(args.path_to_files, args.number_of_queries, args.generate_source)
    converter.run()