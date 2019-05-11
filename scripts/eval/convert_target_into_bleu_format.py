import re
import logging
import string
import unicodedata
import argparse

"""Converts target files into a format suitable for evaluation with BLEU, does NOT expect the format as in the
 target_qfr files or in the trads files in manualEvaluation"""


class Converter:
    def __init__(self, input_path, stopwords=None):
        self.translations = dict()
        self.translations["de"] = list()
        self.translations["en"] = list()
        self.translations["fr"] = list()
        self.translations["es"] = list()
        self.german_regex = re.compile('(?<=de::)[^:]+')
        self.english_regex = re.compile('(?<=en::)[^:]+')
        self.french_regex = re.compile('(?<=fr::)[^:]+')
        self.spanish_regex = re.compile('(?<=es::)[^:]+')

        self.whitespace_regex = re.compile('\s\s+')  # at least two whitespace characters

        self.input_path = input_path
        self.valid_la_codes = {"de", "en", "es", "fr"}

        self.stopwords = set()
        if stopwords:
            print("Reading in stopwords...")
            with open(stopwords, 'r') as f:
                for line in f:
                    self.stopwords.add(line.strip())
            print("Done.")

    def read_in(self):
        with open(self.input_path, 'r') as inp:
            print("Reading in translations...")
            for line in inp:
                for la_code in self.valid_la_codes:
                    self.get_all_translations(line, la_code)
            print("Done.")

    def remove_stopwords(self, matching_strings, la_code):
        # Get rid of stopwords if the converter was given a set of them
        indices_to_delete = list()

        # iterate over matching strings in reversed order to be able to delete the stopwords starting with the
        # biggest index (thus no problems with changing indices while manipulating the list)
        for i in range(len(matching_strings) - 1, -1, -1):
            current_string = matching_strings[i]

            current_string = self.remove_substring_stopwords(current_string)

            # remove diacritics (stopwords contain diacritics, thus it has to be done after stopword removal)
            # diacritics have to be removed in any case (also if stopwords aren't removed)

            # ß has to be replaced manually, since unicodedata.normalize simply deletes it instead of replacing it with ss
            current_string = current_string.replace('ß', 'ss')

            current_string = unicodedata.normalize('NFKD', current_string).encode('ASCII', 'ignore').decode()

            current_string = self.whitespace_regex.sub(' ', current_string)
            current_string = current_string.strip()

            matching_strings[i] = current_string
            # check whether the whole string has become empty due to removal of stopwords
            if not current_string:
                indices_to_delete.append(i)

        for index in indices_to_delete:
            del matching_strings[index]

        la_str = " ".join(matching_strings)
        return la_str

    def remove_substring_stopwords(self, string):
        split = string.split()
        sub_indices_to_remove = []
        for j in range(len(split) - 1, -1, -1):
            substring = split[j]
            if substring in self.stopwords:
                sub_indices_to_remove.append(j)

        for index in sub_indices_to_remove:
            del split[index]

        return " ".join(split)

    def get_all_translations(self, line, la_code):
        regex_to_use = None
        if la_code == "de":
            regex_to_use = self.german_regex
        elif la_code == "en":
            regex_to_use = self.english_regex
        elif la_code == "fr":
            regex_to_use = self.french_regex
        elif la_code == "es":
            regex_to_use = self.spanish_regex
        else:
            logging.error("Invalid language code: {}".format(la_code))

        matching_strings = regex_to_use.findall(line)


        for i in range(len(matching_strings)):
            current_string = matching_strings[i].lower().strip()
            if "'," not in current_string:
                # the match is either of type es::actitud de:: (the actual match then is "actitud de") or of
                # type fr::inventaire'] (the actual match then is "inventaire']")
                # -> need to get rid of the last two characters + remove trailing whitespace if necessary
                current_string = current_string.strip()[:-2]
            else:
                # the match is of type fr::attitude', ' es:: (the actual match then is "attitude', ' es")
                current_string = current_string.split("',")[0]

            # remove punctuation and replace double whitespaces with single whitespace
            punctuation_regex = re.compile('[%s]' % re.escape(string.punctuation))

            punctuation_regex.sub(' ', current_string)

            current_string = current_string.replace("'", " ").replace("-", " ").replace(",", " ")

            matching_strings[i] = current_string

        la_str = self.remove_stopwords(matching_strings, la_code)
        self.translations[la_code].append(la_str)

    def write_to_file(self, la_code):
        if la_code not in self.valid_la_codes:
            logging.error("Invalid language code: {}".format(la_code))
        split = self.input_path.split(".")
        output_path = split[0] + "-from-" + split[1] + "-to-" + la_code
        # mark that stopwords have been removed
        if self.stopwords:
            output_path += "-sw"
        output_path += ".bleu"
        with open(output_path, 'w') as outp:
            for line in self.translations[la_code]:
                outp.write(line)
                outp.write("\n")

    def write_all(self):
        print("Writing translations to files...")
        for la_code in self.valid_la_codes:
            self.write_to_file(la_code)
        print("Done.")

    def main(self):
        self.read_in()
        self.write_all()


if __name__=="__main__":
    # Debugging
    """converter = Converter("translatedQueriesManual/done/target.de")
    converter.main()"""

    argparser = argparse.ArgumentParser(
        description="Converts target (translation) files sticking to the format ['en::translation fr::translation "
                    "es::translation', ... '] into single-language file suitable for evaluation with the Bleu script")
    argparser.add_argument("input_file", type=str, help="Path to file containing the translations")


    argparser.add_argument("-sw", "--stopword", dest="sw_path", default="",
                           help="Path to DeEnEsFr.sw")
    args = argparser.parse_args()

    converter = Converter(args.input_file, args.sw_path)

    converter.main()
