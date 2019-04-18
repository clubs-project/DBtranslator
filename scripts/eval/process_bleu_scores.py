import argparse
import logging
from collections import defaultdict


class Processor:
    def __init__(self, path_to_bleu_file, more_than_one_dict=True):
        self.bleu_file = path_to_bleu_file
        self.bleu_scores_without_stopwords = dict()
        self.bleu_scores_with_stopwords = dict()
        self.cur_dict = None
        self.cur_src = None
        self.cur_tgt = None
        self.without_stopwords = False
        self.more_than_one_dict = more_than_one_dict

    def read_in(self):
        with open(self.bleu_file, 'r') as f:
            for line in f:
                if line.startswith("Results"):
                    if "Mesh" in line:
                        if "concatenation" in line:
                            self.cur_dict = "mesh_4lex_wikidata"
                        else:
                            self.cur_dict = "mesh"
                    elif "quadrilingual" in line:
                        if "non-diff" in line:
                            self.cur_dict = "4lex_non_diff"
                        else:
                            self.cur_dict = "4lex_diff"
                    else:
                        if "non-diff" in line:
                            self.cur_dict = "wikidata_non_diff"
                        else:
                            self.cur_dict = "wikidata_diff"
                    self.bleu_scores_with_stopwords[self.cur_dict] = dict()
                    self.bleu_scores_without_stopwords[self.cur_dict] = dict()
                elif line.startswith("From"):
                    self.detect_translation_type(line)
                elif line.startswith("BLEU"):
                    if (self.cur_src is None) | (self.cur_tgt is None):
                        logging.error("No current source or target:", line)
                    elif self.more_than_one_dict and (self.cur_dict is None):
                        logging.error("No current dict:", line)
                    else:
                        self.store_bleu_values(line)

    def detect_translation_type(self, line):
        split = line.split()
        self.cur_src = split[1]
        self.cur_tgt = split[3]
        if split[4] == "with":
            self.without_stopwords = False
        elif split[4] == "without":
            self.without_stopwords = True
        else:
            logging.error("Wrong format of line:", line)

    def store_bleu_values(self, line):
        if self.without_stopwords:
            dict_to_use = self.bleu_scores_without_stopwords
        else:
            dict_to_use = self.bleu_scores_with_stopwords
        if self.more_than_one_dict:
            dict_to_use = dict_to_use[self.cur_dict]

        dict_to_use[self.cur_src] = dict()
        dict_to_use[self.cur_src][self.cur_tgt] = dict()
        split = line.split()
        dict_to_use[self.cur_src][self.cur_tgt]["bleu"] = float(split[2][:-1])
        other_scores = split[3].split("/")
        dict_to_use[self.cur_src][self.cur_tgt]["bleu-1"] = float(other_scores[0])
        dict_to_use[self.cur_src][self.cur_tgt]["bleu-2"] = float(other_scores[1])
        dict_to_use[self.cur_src][self.cur_tgt]["bleu-3"] = float(other_scores[2])
        dict_to_use[self.cur_src][self.cur_tgt]["bleu-4"] = float(other_scores[3])

    def compute_average_scores(self, without_stopwords, dict_key=None):
        result = defaultdict(lambda: 0) # key "bleu", "bleu-1", ...
        counter = 0
        if without_stopwords:
            dict_to_use = self.bleu_scores_without_stopwords
        else:
            dict_to_use = self.bleu_scores_with_stopwords
        if self.more_than_one_dict:
            dict_to_use = dict_to_use[dict_key]

        for source_target_dict in dict_to_use.values():
            for target_dict in source_target_dict.values():
                counter += 1
                for score_key in ["bleu", "bleu-1", "bleu-2", "bleu-3", "bleu-4"]:
                    result[score_key] += target_dict[score_key]
        for score_key in result.keys():
            result[score_key] /= counter
        return result

    def main(self):
        self.read_in()
        output_path = "average-bleu-scores-" + self.bleu_file
        table_with_stopwords = dict()
        table_without_stopwords = dict()
        if self.more_than_one_dict:
            for dict_key in ["mesh_4lex_wikidata", "mesh", "4lex_non_diff", "4lex_diff", "wikidata_non_diff", "wikidata_diff"]:
                table_with_stopwords[dict_key] = self.compute_average_scores(False, dict_key)
                table_without_stopwords[dict_key] = self.compute_average_scores(True, dict_key)
            with open(output_path, "w") as f:
                f.write("With stopwords:\n")
                self.write_table_to_file(table_with_stopwords, f)
                f.write("\n")
                f.write("Without stopwords:\n")
                self.write_table_to_file(table_without_stopwords, f)
        else:
            table_with_stopwords = self.compute_average_scores(False)
            table_without_stopwords = self.compute_average_scores(True)
            with open(output_path, "w") as f:
                f.write("With stopwords:\n")
                self.write_simple_table_to_file(table_with_stopwords, f)
                f.write("\n")
                f.write("Without stopwords:\n")
                self.write_simple_table_to_file(table_without_stopwords, f)


    @staticmethod
    def write_simple_table_to_file(table, file):
        file.write("bleu\tbleu-1\tbleu-2\tbleu-3\tbleu-4\n")
        values = []
        for score_key in ["bleu", "bleu-1", "bleu-2", "bleu-3", "bleu-4"]:
            values.append(str(round(table[score_key], 2)))
        file.write("\t".join(values))
        file.write("\n")

    @staticmethod
    def write_table_to_file(table, file):
        file.write("\tbleu\tbleu-1\tbleu-2\tbleu-3\tbleu-4\n")
        for dict_key in ["mesh_4lex_wikidata", "mesh", "4lex_non_diff", "4lex_diff", "wikidata_non_diff", "wikidata_diff"]:
            file.write(dict_key)
            for score_key in ["bleu", "bleu-1", "bleu-2", "bleu-3", "bleu-4"]:
                file.write("\t" + str(round(table[dict_key][score_key], 2)))
            file.write("\n")


if __name__ == "__main__":
    """# Debugging
    proc = Processor("bleu-results.txt")
    proc.main()"""

    argparser = argparse.ArgumentParser(
        description="Processes Bleu scores generated by running run_bleu.sh or run_bleu_first_system.sh")
    argparser.add_argument("input_file", type=str, help="Path to file containing the bleu scores")

    argparser.add_argument("-sd", "--single-dict", dest="single_dict", action='store_true',
                           help="Set this option when the input file contains bleu scores only for one dictionary. "
                                "By default, the script assumes that there are all the different dictionaries we "
                                "evaluated (cf. documentation 3.1, section 4.4)")
    args = argparser.parse_args()
    proc = Processor(args.input_file, not args.single_dict)
    proc.main()