"""Converts the trads files in manualEvaluation into a format suitable for evaluation with BLEU"""
import re
import logging
import argparse
from convert_target_into_bleu_format import Converter


class ConvertTrads(Converter):
    def __init__(self, input_path, stopwords=None):
        super().__init__(input_path, stopwords)
        self.copy_regex_start = re.compile(r'(?<=cp::)[^:]+(?=\s\w{2}::)')
        self.copy_regex_end = re.compile(r'(?<=cp::)[^:]+')

        self.interesting_regex = re.compile(r'(en|de|fr|es)::.*')

        self.german_strings = []
        self.english_strings = []
        self.french_strings = []
        self.spanish_strings = []

    def read_in(self):
        with open(self.input_path, 'r') as inp:
            for line in inp:

                self.german_strings = []
                self.english_strings = []
                self.french_strings = []
                self.spanish_strings = []

                # possible query formattings:
                # Q19696	[' en::questionnaire es::cuestionario fr::questionnaire', ' cp::zum', ' cp::fruhstucksverhalten']
                # Q327011	[' cp::forderbedarf', ' en::self concept es::autoimagen fr::concept du soi']
                # Q147478	[' cp::hochsensible en::personality es::personalidad fr::personnalite']

                split = line.strip().split("', '")
                for part in split:
                    match_cp_start = self.copy_regex_start.search(part)
                    if match_cp_start:
                        match_cp_start = match_cp_start.group()
                        self.add_string_to_all(match_cp_start)

                    else:
                        match_cp_end = self.copy_regex_end.search(part)
                        if match_cp_end:
                            match_cp_end = match_cp_end.group()
                            if match_cp_end.endswith("']"):
                                match_cp_end = match_cp_end[:-2]
                            self.add_string_to_all(match_cp_end)
                            # this part only contained cp:: (otherwise, self.copy_regex_start would have matched)
                            continue


                    # if the start cp regex matched or none of the cp regexes matched, we know that there are
                    # exactly 3 entries like en::operational in the interesting part
                    interesting_part = self.interesting_regex.search(part)
                    if interesting_part:
                        interesting_part = interesting_part.group()
                        subparts = interesting_part.split("::")
                        self.add_string_to_string_collection(subparts[0], subparts[1][:-2].strip())
                        self.add_string_to_string_collection(subparts[1][-2:], subparts[2][:-2].strip())
                        # no other la code nor newline character follows, but there might be ']
                        self.add_string_to_string_collection(subparts[2][-2:], subparts[3].replace("']", "").strip())
                    else:
                        logging.error("Empty match of interesting_regex in line: " + line)

                for la_code in self.valid_la_codes:
                    self.append_strings(la_code)

    def add_string_to_all(self, string):
        # split string to remove substrings that are stopwords in any language
        string = self.preprocess_string(string)
        if string:
            for x in [self.german_strings, self.english_strings, self.french_strings, self.spanish_strings]:
                x.append(string)

    def preprocess_string(self, string):
        string = string.replace("'", " ").replace("-", " ").replace(",", " ")
        string = self.remove_substring_stopwords(string)
        string = self.whitespace_regex.sub(' ', string)
        return string

    def add_string_to_string_collection(self, la_code, string):
        if la_code == "de":
            string_collection = self.german_strings
        elif la_code == "en":
            string_collection = self.english_strings
        elif la_code == "fr":
            string_collection = self.french_strings
        elif la_code == "es":
            string_collection = self.spanish_strings
        else:
            logging.error("Invalid language code:", la_code)
        string = self.preprocess_string(string)

        if string:
            string_collection.append(string)

    def append_strings(self, la_code):
        if la_code == "de":
            string_collection = self.german_strings
        elif la_code == "en":
            string_collection = self.english_strings
        elif la_code == "fr":
            string_collection = self.french_strings
        elif la_code == "es":
            string_collection = self.spanish_strings
        else:
            logging.error("Unknown language code:", la_code)

        self.translations[la_code].append(" ".join(string_collection))

    def main(self):
        self.read_in()
        self.write_all()


if __name__=="__main__":
    """# Debugging
    converter = ConvertTrads("manualEvaluation/trads.none", "../lexicons/DeEnEsFr-preprocessed.sw")
    converter.main()"""

    argparser = argparse.ArgumentParser(
        description="Converts trads (translation) files sticking to the format ['en:: fr:: es::', 'cp:: ',...]  into "
                    "single-language file suitable for evaluation with the Bleu script")
    argparser.add_argument("input_file", type=str, help="Path to file containing the translations")

    argparser.add_argument("-sw", "--stopword", dest="sw_path", default="",
                           help="Path to DeEnEsFr.sw")
    args = argparser.parse_args()

    converter = ConvertTrads(args.input_file, args.sw_path)

    converter.main()