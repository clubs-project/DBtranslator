import sys
import logging
from collections import defaultdict


class Processor:
    def __init__(self, path_to_bleu_file):
        self.bleu_file = path_to_bleu_file
        self.bleu_scores_without_stopwords = dict()
        self.bleu_scores_with_stopwords = dict()
        self.cur_dict = None
        self.cur_src = None
        self.cur_tgt = None
        self.without_stopwords = False

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
                    split = line.split()
                    self.cur_src = split[1]
                    self.cur_tgt = split[3]
                    if split[4] == "with":
                        self.without_stopwords = False
                    elif split[4] == "without":
                        self.without_stopwords = True
                    else:
                        logging.error("Wrong format of line:", line)
                elif line.startswith("BLEU"):
                    if (self.cur_dict is None) | (self.cur_src is None) | (self.cur_tgt is None):
                        logging.error("No current dict, source or target:", line)
                    else:
                        self.store_bleu_values(line)

    def store_bleu_values(self, line):
        if self.without_stopwords:
            dict_to_use = self.bleu_scores_without_stopwords
        else:
            dict_to_use = self.bleu_scores_with_stopwords
        dict_to_use[self.cur_dict][self.cur_src] = dict()
        dict_to_use[self.cur_dict][self.cur_src][self.cur_tgt] = dict()
        split = line.split()
        dict_to_use[self.cur_dict][self.cur_src][self.cur_tgt]["bleu"] = float(split[2][:-1])
        other_scores = split[3].split("/")
        dict_to_use[self.cur_dict][self.cur_src][self.cur_tgt]["bleu-1"] = float(other_scores[0])
        dict_to_use[self.cur_dict][self.cur_src][self.cur_tgt]["bleu-2"] = float(other_scores[1])
        dict_to_use[self.cur_dict][self.cur_src][self.cur_tgt]["bleu-3"] = float(other_scores[2])
        dict_to_use[self.cur_dict][self.cur_src][self.cur_tgt]["bleu-4"] = float(other_scores[3])

    def compute_average_scores(self, dict_key, without_stopwords):
        result = defaultdict(lambda: 0) # key "bleu", "bleu-1", ...
        counter = 0
        if without_stopwords:
            dict_to_use = self.bleu_scores_without_stopwords
        else:
            dict_to_use = self.bleu_scores_with_stopwords
        for source_target_dict in dict_to_use[dict_key].values():
            for target_dict in source_target_dict.values():
                counter += 1
                for score_key in ["bleu", "bleu-1", "bleu-2", "bleu-3", "bleu-4"]:
                    result[score_key] += target_dict[score_key]
        for score_key in result.keys():
            result[score_key] /= counter
        return result

    def main(self):
        self.read_in()
        table_with_stopwords = dict()
        table_without_stopwords = dict()
        for dict_key in ["mesh_4lex_wikidata", "mesh", "4lex_non_diff", "4lex_diff", "wikidata_non_diff", "wikidata_diff"]:
            table_with_stopwords[dict_key] = self.compute_average_scores(dict_key, False)
            table_without_stopwords[dict_key] = self.compute_average_scores(dict_key, True)
        with open("average-bleu-scores.txt", "w") as f:
            f.write("With stopwords:\n")
            self.write_table_to_file(table_with_stopwords, f)
            f.write("\n")
            f.write("Without stopwords:\n")
            self.write_table_to_file(table_without_stopwords, f)

    @staticmethod
    def write_table_to_file(table, file):
        file.write("\tbleu\tbleu-1\tbleu-2\tbleu-3\tbleu-4\n")
        for dict_key in ["mesh_4lex_wikidata", "mesh", "4lex_non_diff", "4lex_diff", "wikidata_non_diff", "wikidata_diff"]:
            file.write(dict_key)
            for score_key in ["bleu", "bleu-1", "bleu-2", "bleu-3", "bleu-4"]:
                file.write("\t" + str(round(table[dict_key][score_key], 2)))
            file.write("\n")


if __name__ == "__main__":
    # Debugging
    proc = Processor("bleu-results.txt")
    proc.main()

    """if len(sys.argv) != 2:
        print("Usage: python3 process_bleu_scores.py <path to file created with run_bleu.sh>")
        sys.exit(1)
    proc = Processor(sys.argv[1])
    proc.main()"""