import re
import sys
import logging

class TransGetter:
    def __init__(self, trans_path):
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
        self.german = ""
        self.english = ""
        self.french = ""
        self.spanish = ""

    def read_in(self):
        with open(self.path_to_translations, 'r') as f:
            #counter = 0
            for line in f:
            #    counter += 1
            #    if counter == 13:
            #        print("Bla")
                self.german_is_real_translation = False
                self.english_is_real_translation = False
                self.french_is_real_translation = False
                self.spanish_is_real_translation = False
                query_translations = dict()
                original = ""
                self.german = ""
                self.english = ""
                self.french = ""
                self.spanish = ""
                parts = line.split("AU:")
                add_whitespace = False
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

                        self.search_for_translations(rest, original_string, add_whitespace)
                    else:
                        original_string = current_string.split(")")[0]
                        # passed_loop = False
                        # original_strings = list()
                        # while " " in original_string:
                        #     passed_loop = True
                        #     first_original_string = original_string.strip()
                        #     original_strings.append(dict())
                        #     original_strings[0]["org"] = first_original_string
                        #     to_skip += 1
                        #     num_following_aus = 1
                        #     next_string_org = parts[i+num_following_aus].split(")")[0]
                        #     original_strings.append(dict())
                        #     original_strings[num_following_aus]["org"] = next_string_org
                        #     while " " in next_string_org:
                        #         num_following_aus +=1
                        #         next_string_org = parts[i+num_following_aus].split(")")[0]
                        #         original_strings.append(dict())
                        #         original_strings[num_following_aus]["org"] = next_string_org
                        #     next_string = parts[i+num_following_aus].replace(next_string_org + ")", "")
                        #
                        #
                        # if not passed_loop:
                        original += original_string
                        rest = current_string.replace(original + ")", "", 1)
                        self.search_for_translations(rest, original_string, add_whitespace)
                no_real_translation = True
                if self.german_is_real_translation:
                    no_real_translation = False
                    query_translations["de"] = self.german
                if self.english_is_real_translation:
                    no_real_translation = False
                    query_translations["en"] = self.english
                if self.french_is_real_translation:
                    no_real_translation = False
                    query_translations["fr"] = self.french
                if self.spanish_is_real_translation:
                    no_real_translation = False
                    query_translations["es"] = self.spanish

                if no_real_translation:
                    query_translations["org"] = original

                self.translations.append(query_translations)

    @staticmethod
    def search_for_translation(rest_string, regex, la_string, org_string, add_whitespace):
        is_real_translation = False
        if add_whitespace:
            la_string += " "
        if regex.search(rest_string):
            # strip because the regex also matches trailing whitespace since it could also be whitespace
            # in a phrase
            la_string += regex.search(rest_string).group().strip()
            is_real_translation = True
        else:
            la_string += org_string
        return la_string, is_real_translation

    def search_for_translations(self, rest_string, org_string, add_whitespace):
        self.german, current_german_is_real_trans = self.search_for_translation(rest_string, self.re_german, self.german,
                                                                      org_string, add_whitespace)
        self.german_is_real_translation = self.german_is_real_translation | current_german_is_real_trans
        self.english, current_english_is_real_trans = self.search_for_translation(rest_string, self.re_english, self.english,
                                                                       org_string, add_whitespace)
        self.english_is_real_translation = self.english_is_real_translation | current_english_is_real_trans
        self.french, current_french_is_real_trans = self.search_for_translation(rest_string, self.re_french, self.french,
                                                                      org_string, add_whitespace)
        self.french_is_real_translation = self.french_is_real_translation | current_french_is_real_trans
        self.spanish, current_spanish_is_real_trans = self.search_for_translation(rest_string, self.re_spanish, self.spanish,
                                                                       org_string, add_whitespace)
        self.spanish_is_real_translation = self.spanish_is_real_translation | current_spanish_is_real_trans

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
                    if trans == "":
                        logging.warning('Empty translation found in {}-th line'.format(i+1))
                        continue
                    if not first:
                        outp.write(" ")
                    first = False
                    outp.write(code + "::" + trans)
                outp.write("\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 get_complete_translations.py <path_to_translations>")
        sys.exit(1)
    path_to_translations = sys.argv[1]
    # path_to_translations = "server_results/4lex_diff/translations.de"
    extractor = TransGetter(path_to_translations)
    extractor.read_in()
    extractor.write_to_file()