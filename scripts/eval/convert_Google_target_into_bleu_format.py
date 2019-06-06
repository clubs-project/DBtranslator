from convert_target_into_bleu_format import Converter
import string
import re
import argparse
import sys

"""Removes diacritics, punctuation and capitalization, can also remove stopwords. Expects a simple string per line 
(no language code annotation etc.)"""


class simpleConverter(Converter):
    def __init__(self, input_path, source_la_code, target_la_code, stopwords=None):
        super().__init__(input_path, stopwords)

        self.translations = list()
        self.punctuation_regex = re.compile('[%s]' % re.escape(string.punctuation))

        self.src_la_code = source_la_code
        self.valid_la_codes.add("none")
        if self.src_la_code not in self.valid_la_codes:
            print("Invalid source language code:", self.src_la_code)
            print("Valid language codes:", self.valid_la_codes)
            sys.exit(1)
        self.tgt_la_code = target_la_code
        if self.tgt_la_code not in self.valid_la_codes:
            print("Invalid target language code:", self.tgt_la_code)
            print("Valid language codes:", self.valid_la_codes)
            sys.exit(1)

    def read_in(self):
        with open(self.input_path, 'r') as inp:
            print("Reading in translations...")
            for line in inp:
                line = line.lower().strip()
                self.punctuation_regex.sub(' ', line)
                line = self.remove_stopwords([line])
                line = line.replace("'", " ").replace("-", " ").replace(",", " ").replace('"', " ").replace(".", " ")
                line = self.whitespace_regex.sub(' ', line)
                line = line.strip()
                self.translations.append(line)

    def write_to_file(self):
        print("Writing translations to file...")
        output_path = "from-" + self.src_la_code + "-to-" + self.tgt_la_code
        if self.stopwords:
            output_path += "-sw"
        output_path += ".bleu"
        with open(output_path, "w") as outp:
            for line in self.translations:
                outp.write(line)
                outp.write("\n")

    def main(self):
        self.read_in()
        self.write_to_file()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Converts target (translation) files which contain a single-language string per line (no language "
                    "annotation etc.) into a file suitable for evaluation with the Bleu script")
    argparser.add_argument("input_file", type=str, help="Path to file containing the translations")

    argparser.add_argument("source_la_code", type=str, help="Source language code. Valid language codes: de, en, es, fr")
    argparser.add_argument("target_la_code", type=str, help="Target language code. Valid language codes: de, en, es, fr")


    argparser.add_argument("-sw", "--stopword", dest="sw_path", default="",
                           help="Path to DeEnEsFr.sw")
    args = argparser.parse_args()

    converter = simpleConverter(args.input_file, args.source_la_code, args.target_la_code, args.sw_path)
    converter.main()