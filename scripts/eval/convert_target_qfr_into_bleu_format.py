from convert_target_into_bleu_format import Converter
import re
import logging
import argparse


class ConvertQFR(Converter):
    def __init__(self, input_path, stopwords=None):
        super().__init__(input_path, stopwords)
        self.german_regex_start = re.compile(r'(?<=de::)[^:]+(?=\s\w{2}::)')
        self.german_regex_end = re.compile(r'(?<=de::)[^:]+')
        self.english_regex_start = re.compile(r'(?<=en::)[^:]+(?=\w{2}::)')
        self.english_regex_end = re.compile(r'(?<=en::)[^:]')
        self.french_regex_start = re.compile(r'(?<=fr::)[^:]+(?=\w{2}::)')
        self.french_regex_end = re.compile(r'(?<=fr::)[^:]+')
        self.spanish_regex_start = re.compile(r'(?<=es::)[^:]+(?=\w{2}::)')
        self.spanish_regex_end = re.compile(r'(?<=es::)[^:]+')

        self.copy_regex = re.compile(r"(?<=org::)[^:]+")


    def read_in(self):
        with open(self.input_path, 'r') as inp:
            print("Reading in translations...")
            for line in inp:
                for la_code in ["org", "de", "en", "fr", "es"]:
                    org_matched = self.get_all_translations(line, la_code)
                    if la_code == "org" and org_matched:
                        break
            print("Done.")

    def get_all_translations(self, line, la_code):
        start_regex_to_use = None
        end_regex_to_use = None
        if la_code == "de":
            start_regex_to_use = self.german_regex_start
            end_regex_to_use = self.german_regex_end
        elif la_code == "en":
            start_regex_to_use = self.english_regex_start
            end_regex_to_use = self.english_regex_end
        elif la_code == "fr":
            start_regex_to_use = self.french_regex_start
            end_regex_to_use = self.french_regex_end
        elif la_code == "es":
            start_regex_to_use = self.spanish_regex_start
            end_regex_to_use = self.spanish_regex_end

        # org marks translations by the QueryFieldRewriter that are entire copies of the original query
        elif la_code == "org":
            start_regex_to_use = self.copy_regex
            start_match = start_regex_to_use.search(line)
            if start_match:
                start_match = start_match.group().strip()
                for la_code in {"de", "en", "fr", "es"}:
                    self.translations[la_code].append(start_match)
                return True
            return False
        else:
            logging.error("Invalid language code: {}".format(la_code))

        start_match = start_regex_to_use.search(line)
        end_match = end_regex_to_use.search(line)
        la_string = ""
        if start_match:
            la_string = start_match.group()
        elif end_match:
            la_string = end_match.group()

        la_string = self.remove_substring_stopwords(la_string)

        self.translations[la_code].append(la_string)
        return


if __name__=="__main__":
    """# Debugging
    converter = ConvertQFR("server_results/4lex_diff/target_qfr.en")
    converter.main()"""

    argparser = argparse.ArgumentParser(
        description="Converts target (translation) files sticking to the format en::translation fr::translation "
                    "es::translation or org::copy into single-language file suitable for evaluation with the Bleu "
                    "script")
    argparser.add_argument("input_file", type=str, help="Path to file containing the translations")

    argparser.add_argument("-sw", "--stopword", dest="sw_path", default="", help="Path to DeEnEsFr-preprocessed.sw")
    args = argparser.parse_args()

    converter = ConvertQFR(args.input_file, args.sw_path)

    converter.main()