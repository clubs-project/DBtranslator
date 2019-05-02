import re
import argparse
import sys
import logging


class TransGetter:
    def __init__(self, trans_path, source_language):
        self.path_to_translations = trans_path
        self.re_german = re.compile('(?<=TI_D:)[^)T]+')
        self.re_english = re.compile('(?<=TI_E:)[^)T]+')
        self.re_french = re.compile('(?<=TI_F:)[^)T]+')
        self.re_spanish = re.compile('(?<=TI_S:)[^)T]+')
        self.translations = list()
        # remember if at least one string in current translation is a real translation (and not just a copy)
        self.german_is_real_translation = False
        self.english_is_real_translation = False
        self.french_is_real_translation = False
        self.spanish_is_real_translation = False
        self.german = []
        self.english = []
        self.french = []
        self.spanish = []
        self.source_language = source_language

    def read_in(self):
        with open(self.path_to_translations, 'r') as f:
            counter = 0
            for line in f:
                counter += 1
                """if counter == 33:
                    print("Bla")"""
                self.german_is_real_translation = False
                self.english_is_real_translation = False
                self.french_is_real_translation = False
                self.spanish_is_real_translation = False
                query_translations = dict()
                original = ""
                self.german = []
                self.english = []
                self.french = []
                self.spanish = []
                parts = line.split("AU:")
                #to_skip = 0
                # ignore parts[0] because it only contains original fields (whose strings are the same as the one at the
                # beginning of parts[1]
                for i in range(1, len(parts)):
                    # if to_skip > 0:
                    #     to_skip -= 1
                    #     continue
                    current_string = parts[i]
                    if i > 1:
                        original += " "
                        add_whitespace = True
                    if current_string.startswith("\""):

                        original_string = "\"" + current_string.split("\"")[1] + "\""
                        original += original_string
                        rest = current_string.replace(original, "", 1)

                        self.search_for_translations(rest, original_string, counter)
                    else:
                        original_string = current_string.split(")")[0]
                        original += original_string
                        rest = current_string.replace(original + ")", "", 1)
                        self.search_for_translations(rest, original_string, counter)

                if self.german_is_real_translation | self.english_is_real_translation | self.french_is_real_translation | self.spanish_is_real_translation:
                    query_translations["de"] = " ".join(self.german)
                    query_translations["en"] = " ".join(self.english)
                    query_translations["fr"] = " ".join(self.french)
                    query_translations["es"] = " ".join(self.spanish)

                else:
                    query_translations["org"] = original

                self.translations.append(query_translations)

    def search_for_translation(self, rest_string, regex, collection_to_append, org_string):
        if regex.search(rest_string):
            # strip because the regex also matches trailing whitespace since it could also be whitespace
            # in a phrase
            la_string = " ".join(regex.findall(rest_string))
            collection_to_append.append(la_string)
            return True
        elif self.source_language == "none":
            collection_to_append.append(org_string)
        return False

    def check_source_language(self, la_code, current_is_real_trans):
        wrong_source_language = False
        if self.source_language == la_code and current_is_real_trans:
            wrong_source_language = True
        if la_code == "de":
            self.german_is_real_translation = self.german_is_real_translation | current_is_real_trans
        elif la_code == "en":
            self.english_is_real_translation = self.english_is_real_translation | current_is_real_trans
        elif la_code == "fr":
            self.french_is_real_translation = self.french_is_real_translation | current_is_real_trans
        elif la_code == "es":
            self.spanish_is_real_translation = self.spanish_is_real_translation | current_is_real_trans
        else:
            logging.warn("Invalid language code:", la_code)
        return wrong_source_language

    def search_for_translations(self, rest_string, org_string, counter):
        wrong_source_language = False
        current_german_is_real_trans = self.search_for_translation(rest_string, self.re_german, self.german, org_string)
        wrong_source_language = wrong_source_language | self.check_source_language("de", current_german_is_real_trans)

        current_english_is_real_trans = self.search_for_translation(rest_string, self.re_english, self.english, org_string)
        wrong_source_language = wrong_source_language | self.check_source_language("en", current_english_is_real_trans)

        current_french_is_real_trans = self.search_for_translation(rest_string, self.re_french, self.french, org_string)
        wrong_source_language = wrong_source_language | self.check_source_language("fr", current_french_is_real_trans)

        current_spanish_is_real_trans = self.search_for_translation(rest_string, self.re_spanish, self.spanish, org_string)
        wrong_source_language = wrong_source_language | self.check_source_language("es", current_spanish_is_real_trans)

        # for none source, tokens are already copied in search_for_translation if there is no real translation
        if self.source_language != "none":
            # if there is no real translation at all, org_string should be copied (this is needed for cases where a
            # translation consists of less tokens than the source)
            if not current_german_is_real_trans and not current_english_is_real_trans and not current_french_is_real_trans and not current_spanish_is_real_trans:
                self.german.append(org_string)
                self.english.append(org_string)
                self.french.append(org_string)
                self.spanish.append(org_string)
            elif wrong_source_language:
                self.add_copy_to_wrong_source_language(current_german_is_real_trans, current_english_is_real_trans,
                                                       current_french_is_real_trans, current_spanish_is_real_trans,
                                                       org_string, rest_string, counter)

    def add_copy_to_wrong_source_language(self, current_german_is_real_trans, current_english_is_real_trans,
                                          current_french_is_real_trans, current_spanish_is_real_trans, org_string,
                                          rest_string, counter):
        first_la_is_real_trans = None
        second_la_is_real_trans = None
        third_la_is_real_trans = None
        first_la_collection = None
        second_la_collection = None
        third_la_collection = None
        first_name = ""
        second_name = ""
        third_name = ""

        # English source
        if self.source_language == "en":
            first_la_is_real_trans = current_german_is_real_trans
            second_la_is_real_trans = current_french_is_real_trans
            third_la_is_real_trans = current_spanish_is_real_trans
            first_la_collection = self.german
            second_la_collection = self.french
            third_la_collection = self.spanish
            first_name = "German"
            second_name = "French"
            third_name = "Spanish"

        # German source
        elif self.source_language == "de":
            first_la_is_real_trans = current_english_is_real_trans
            second_la_is_real_trans = current_french_is_real_trans
            third_la_is_real_trans = current_spanish_is_real_trans
            first_la_collection = self.english
            second_la_collection = self.french
            third_la_collection = self.spanish
            first_name = "English"
            second_name = "French"
            third_name = "Spanish"

        # French source
        elif self.source_language == "fr":
            first_la_is_real_trans = current_english_is_real_trans
            second_la_is_real_trans = current_german_is_real_trans
            third_la_is_real_trans = current_spanish_is_real_trans
            first_la_collection = self.english
            second_la_collection = self.german
            third_la_collection = self.spanish
            first_name = "English"
            second_name = "German"
            third_name = "Spanish"

        # Spanish source
        else:
            first_la_is_real_trans = current_english_is_real_trans
            second_la_is_real_trans = current_german_is_real_trans
            third_la_is_real_trans = current_french_is_real_trans
            first_la_collection = self.english
            second_la_collection = self.german
            third_la_collection = self.french
            first_name = "English"
            second_name = "German"
            third_name = "French"

        # Find out which language was mistakenly taken to be the source language
        if first_la_is_real_trans:
            if second_la_is_real_trans:
                if third_la_is_real_trans:
                    logging.warn("Line ", counter, ": There seem to be translations in all languages:", org_string,
                                 rest_string)
                else:
                    # the system wrongly assumed the third language to be the source language
                    third_la_collection.append(org_string)
            elif third_la_is_real_trans:
                # the system wrongly assumed the second language to be the source language
                second_la_collection.append(org_string)
            else:
                logging.warn("Line ", counter, ": Both", third_name, "and", second_name, "do not have a real translation, "
                                               "copying token into both languages (which might be wrong):",
                             org_string, rest_string)
                third_la_collection.append(org_string)
                second_la_collection.append(org_string)
        elif second_la_is_real_trans:
            if third_la_is_real_trans:
                # the system wrongly assumed the first language to be the source language
                first_la_collection.append(org_string)
            else:
                logging.warn("Line ", counter, ": Both", third_name, "and", first_name, "do not have a real translation, "
                                               "copying token into both languages (which might be wrong):",
                             org_string, rest_string)
                third_la_collection.append(org_string)
                first_la_collection.append(org_string)
        else:
            if third_la_is_real_trans:
                logging.warn("Line ", counter, ": Both", second_name, "and", first_name ,"do not have a real translation, "
                                               "copying token into both languages (which might be wrong):",
                             org_string, rest_string)
                second_la_collection.append(org_string)
                first_la_collection.append(org_string)
            else:
                logging.warn("Line ", counter, ":", first_name, ",", second_name, "and", third_name, "do not have a real translation, "
                                               "copying token into both languages (which might be wrong):",
                             org_string, rest_string)
                first_la_collection.append(org_string)
                second_la_collection.append(org_string)
                third_la_collection.append(org_string)



    def write_to_file(self):
        path_parts = self.path_to_translations.rsplit("/", 1)
        output_path = path_parts[0] + "/"
        language_code = path_parts[1].split(".")[1]
        output_path += "target_qfr." + language_code
        with open(output_path, "w") as outp:
            for i in range(len(self.translations)):
                query_translations = self.translations[i]
                first = True
                for (code, trans) in query_translations.items():
                    # do not write translations into source_language
                    if code == self.source_language:
                        continue
                    if trans == "":
                        logging.warning('Empty translation found in {}-th line'.format(i+1))
                        continue
                    if not first:
                        outp.write(" ")
                    first = False
                    outp.write(code + "::" + trans)
                outp.write("\n")


if __name__ == "__main__":
    # Debugging
    #extractor = TransGetter("50_queries/translations.txt", "en")

    argparser = argparse.ArgumentParser(
        description="Converts translated Solr queries into the format de::translation fr::translation es::translation")
    argparser.add_argument("input_file", type=str, help="Path to file containing the translations")

    argparser.add_argument("source_language", type=str, help="The language of the source files that have been translate"
                                                             "d. Valid codes: de for German, en for English, fr for "
                                                             "French, es for Spanish and none for none")
    args = argparser.parse_args()

    if args.source_language not in {"de", "en", "es", "fr", "none"}:
        print("Invalid language code:", args.source_language)
        print("Valid codes: de for German, en for English, fr for French, es for Spanish and none for none")
        sys.exit(1)

    extractor = TransGetter(args.input_file, args.source_language)
    extractor.read_in()
    extractor.write_to_file()