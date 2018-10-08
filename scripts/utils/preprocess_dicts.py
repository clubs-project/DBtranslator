import unicodedata
import re
import argparse
import string

'''Cleans and merges dictionaries as described in the section 'Cleaning and Quad-lexicon Compilation" of year2/CLUBS_MTcts.pdf'
Usage:
'python3 preprocess_dicts.py  <file containing stopwords in all languages> <dictionaries in priority order> ' 

To establish the whole non-MeSH lexicon, you can use:
'python3 preprocess_dicts.py DeEnEsFr.sw wp.enkey2.txt wp.dekey2.txt wp.frkey2.txt wp.eskey2.txt WP.cat.en WP.cat.de 
WP.cat.fr WP.cat.es untradDEall.keys.en untradDEall.keys.de untradDEall.keys.fr untradDEall.keys.es dict.keys.en 
dict.keys.de dict.keys.fr dict.keys.es'
(adapt paths to your own system).
'''


def rreplace(s, old, new, num_occ):
    '''Replaces the last num_occ occurrences of old by new , taken from 
    https://stackoverflow.com/questions/2556108/rreplace-how-to-replace-the-last-occurrence-of-an-expression-in-a-string#2556252'''
    li = s.rsplit(old, num_occ)
    return new.join(li)


def read_in_non_solr(input_path):
    '''Simply reads in a dictionary, no preprocessing at all'''
    la_dict = dict()
    with open(input_path, "r") as f:
        for line in f:
            entries = line.split("|||")
            source_word = entries[0]

            # remove whole entry if source_ẃord is empty
            if source_word == "":
                continue

            la_dict[source_word] = dict()

            # iterate over translations
            delete_entry = False
            for i in range(1, len(entries)):
                la_code = entries[i].split(":")[0]
                translation = concatenate_string_list(entries[i].split(":")[1:], ":")
                translation = translation.rstrip()

                # remove whole entry if translation is empty
                if translation == "":
                    delete_entry = True
                    break

                la_dict[source_word][la_code] = translation

            if delete_entry:
                la_dict.pop(source_word, None)
    return la_dict


def replace_regex_with_whitespace(word, regex):
    # Solr replaces punctuation signs with whitespaces when parsing queries
    return regex.sub(' ', word)


def read_in_solr(input_path, stopwords):
    '''Reads in a dictionary and cleans it:
    - lowercases the token
    - removes diacritics ('ü' -> 'u')
    - replaces 'ß' with 'ss' 
    - replaces punctuation with whitespace
    - introduces duplicate versions of words containing umlauts ('ü' -> 'ue') and BE/AE spelling (e.g. -ise -> -ize)
    - removes entries containing stopwords
    - removes entries containing empty translations or empty source words
    - deletes [dokumenttyp] annotation
    - if non_solr == False, hyphens will be replaced with whitespaces
    '''
    la_dict = dict()
    punctuation_regex = re.compile('[%s]' % re.escape(string.punctuation))
    whitespace_regex = re.compile('\s\s+')  # at least two whitespace characters
    with open(input_path, "r") as f:
        umlaut_pattern = re.compile('[ÜǘÄäÖö]+')
        for line in f:
            # we want to have duplicates like -ise and -ize (BE/AE) and fuhrung/fuehrung (German), fuhrung is the
            # result of unicodedata.normalize(...) applied to "führung", fuehrung has to be added manually
            duplicate_needed = False
            entries = line.split("|||")

            # lowercase
            source_word = entries[0].lower()

            # stopwords are lowercased, but contain diacritics, thus we have to check this here before removing diacritics
            if source_word in stopwords:
                # remove whole entry if source word is a stopword
                continue

            # ß has to be replaced manually, since unicodedata.normalize simply deletes it instead of replacing it with ss
            source_word = source_word.replace('ß', 'ss')

            # check if it is necessary to introduce duplicates like German ü -> ue (unicode normalization returns u)
            # and different spellings in AE and BE
            # first determine the language of the source word
            translation_languages = set()
            sw_language = ""
            for i in range(1, len(entries)):
                translation_languages.add(entries[i].split(":")[0])
            if "en" not in translation_languages:
                sw_language = "en"
            elif "de" not in translation_languages:
                sw_language = "de"
            elif "fr" not in translation_languages:
                sw_language = "fr"
            else:
                sw_language = "es"

            # introduce duplicates
            source_word_duplicate = None
            if umlaut_pattern.search(source_word):
                duplicate_needed = True
                source_word_duplicate = source_word.replace('ü', 'ue').replace('ö', 'oe').replace('ä', 'ae')
            elif sw_language == "en" and source_word.endswith('ise'):
                duplicate_needed = True
                source_word_duplicate = rreplace(source_word, 'ise', 'ize', 1)
            elif sw_language == "en" and source_word.endswith('ize'):
                duplicate_needed = True
                source_word_duplicate = rreplace(source_word, 'ize', 'ise', 1)
            elif sw_language == "en" and source_word.endswith('isation'):
                duplicate_needed = True
                source_word_duplicate = rreplace(source_word, 'isation', 'ization', 1)
            elif sw_language == "en" and source_word.endswith('ization'):
                duplicate_needed = True
                source_word_duplicate = rreplace(source_word, 'ization', 'isation', 1)
            elif sw_language == "en" and source_word.endswith('our'):
                duplicate_needed = True
                source_word_duplicate = rreplace(source_word, 'our', 'or', 1)
            elif sw_language == "en" and source_word.endswith('or'):
                duplicate_needed = True
                source_word_duplicate = rreplace(source_word, 'or', 'our', 1)

            # remove diacritics
            source_word = unicodedata.normalize('NFKD', source_word).encode('ASCII', 'ignore').decode()

            # String.punctuation only knows ASCII punctuation
            source_word = replace_regex_with_whitespace(source_word, punctuation_regex)

            # Replace whitespace that consists of at least two characters with one ws character
            source_word = replace_regex_with_whitespace(source_word, whitespace_regex)

            # delete unnecessary annotation
            source_word = source_word.replace('[dokumenttyp]', '').strip()

            # source word might be empty after all these normalization steps -> remove whole entry
            if source_word.strip() == "":
                continue

            la_dict[source_word] = dict()

            if duplicate_needed:
                source_word_duplicate = unicodedata.normalize('NFKD', source_word_duplicate).encode('ASCII', 'ignore').decode()
                source_word_duplicate = replace_regex_with_whitespace(source_word_duplicate, punctuation_regex)
                # Replace whitespace that consists of at least two characters with one ws character
                source_word_duplicate = replace_regex_with_whitespace(source_word_duplicate, whitespace_regex)
                source_word_duplicate = source_word_duplicate.replace('[dokumenttyp]', '').strip()
                if source_word_duplicate.strip() == "":
                    duplicate_needed = False
                else:
                    la_dict[source_word_duplicate] = dict()

            # iterate over translations
            delete_entry = False
            for i in range(1, len(entries)):
                la_code = entries[i].split(":")[0]
                translation = concatenate_string_list(entries[i].split(":")[1:], ":")
                translation = translation.rstrip().lower()
                if translation in stopwords:
                    # remove whole entry if translation is a stopword in any language (it doesn't have to be a stopword
                    # in its own language)
                    delete_entry = True
                    break
                translation = translation.replace('ß', 'ss')

                translation = unicodedata.normalize('NFKD', translation).encode(encoding='ASCII', errors='ignore').decode()

                # String.punctuation only knows ASCII punctuation
                translation = replace_regex_with_whitespace(translation, punctuation_regex)

                # Replace whitespace that consists of at least two characters with one ws character
                translation = replace_regex_with_whitespace(translation, whitespace_regex)

                translation = translation.replace('[dokumenttyp]', '').strip()

                # translation might be empty after all these normalization steps -> remove whole entry
                if translation.strip() == "":
                    delete_entry = True
                    break

                la_dict[source_word][la_code] = translation
                if duplicate_needed:
                    la_dict[source_word_duplicate][la_code] = translation

            if delete_entry:
                la_dict.pop(source_word, None)
                la_dict.pop(source_word_duplicate, None)

    return la_dict


def merge_dicts(dict_with_higher_priority, other_dict):
    '''Merge two dicts, prioritizing the first one over the second one'''
    for key in other_dict.keys():
        # if a key of other_dict also is a key in dict_with_higher_priority, we keep the value from dict_with_higher_priority
        # and do not add the value from other_dict
        if key not in dict_with_higher_priority.keys():
            dict_with_higher_priority[key] = other_dict[key]
    return dict_with_higher_priority


def concatenate_string_list(string_list, string_between_strings=" ", add_at_last_string=False):
    '''Concatenates a list of strings into a single string with string_between_strings added between the former elements of the list'''
    result = ""
    for i in range(len(string_list)):
        if i == len(string_list)-1 and not add_at_last_string:
            result += string_list[i].strip()
        else:
            result += string_list[i].strip() + string_between_strings
    return result


def write_to_file(la_dict, path, command):
    '''Writes a dictionary to a file, separating translations with |||'''
    with open(path, "w") as out:
        out.write("<<<This dictionary has been compiled with the following command: " + concatenate_string_list(command)
                  + ">>>\n")
        for key in la_dict.keys():
            out.write(key)
            # always write the la_codes in the same order, then the dictionary is more human-friendly
            for la_code in sorted(la_dict[key].keys()):
                out.write('|||' + la_code + ':' + la_dict[key][la_code])
            out.write("\n")


def read_in_sw_file(sw_file):
    '''Returns a set of all stopwords.
    Input file: one stopword per line, the stopwords are lowercased, but no diacritics have been removed'''
    stopwords = set()
    with open(sw_file, "r") as f:
        for line in f:
            stopword = line.strip()
            stopwords.add(stopword)
    return stopwords


def main(dicts, sw_file, command, la_code, non_solr):
    """ dicts[0] > dicts[1] > ... in terms of priority"""
    stopwords = read_in_sw_file(sw_file)
    main_dict = dict()
    for i in range(len(dicts)):
        print("Reading in dict", str(i+1), "...")
        if i == 0:

            # we can make two different versions of the dicts: a preprocessed one and a non-preprocessed one
            if non_solr:
                main_dict = read_in_non_solr(dicts[0])
            else:
                main_dict = read_in_solr(dicts[0], stopwords)
        else:
            print("Merging previous dict and dict", str(i+1), "...")
            if non_solr:
                main_dict = merge_dicts(main_dict, read_in_non_solr(dicts[i]))
            else:
                main_dict = merge_dicts(main_dict, read_in_solr(dicts[i], stopwords))
    path_prefix = concatenate_string_list(dicts[0].split("/")[:-1], "/", add_at_last_string=True)
    path = path_prefix
    previous_abbr = ""
    for i in range(len(dicts)):
        abbrs = dicts[i].split("/")[-1].split(".")
        abbr = ""

        # iterate over abbrs to get full name of dict
        for j in range(len(abbrs)):
            if j < len(abbrs)-1:
                if not (abbrs[j].startswith("en") or abbrs[j].startswith("de") or abbrs[j].startswith("fr") or abbrs[j].startswith("es")):
                    abbr += abbrs[j]

        if abbr == previous_abbr:
            continue
        path += abbr + "."
        previous_abbr = abbr
    if non_solr:
        path += "non-solr."
    else:
        path += "solr."
    if la_code:
        path += "single-language." + la_code
    else:
        path += "all-languages.txt"
    print("Path:", path)
    print("Writing new dict to file...")
    write_to_file(main_dict, path, command)

if __name__=="__main__":
    argparser = argparse.ArgumentParser(description="Cleans and merges different dictionaries, sticking to a given order")
    argparser.add_argument("sw_file", type=str, help="Path to file containing stopwords in all languages (mandatory)")
    # nargs='+': we get at least 1 argument, but there can be finitely many more
    argparser.add_argument("dicts", type=str, nargs='+', help="Paths to dictionaries, priority will be the order in the command ")

    argparser.add_argument("-lc", "--language-code", dest="la_code", default="",
                           help="If you want to merge dictionaries of the same language, give the language code, "
                                "since otherwise the files will be named just like a merged version of the first dict in"
                                "different languages (which might replace existing dictionaries of that kind).")
    argparser.add_argument("-ns", "--non-solr", dest="non_solr", action="store_true", help="If this option is set, the "
                                                                                           "dictionaries will only be "
                                                                                           "pasted together and no "
                                                                                           "preprocessing (e.g. removal"
                                                                                           " of diacritics) willbe "
                                                                                           "performed. If a word is a "
                                                                                           "source word in more than one"
                                                                                           " dictionary, the entry of "
                                                                                           "the dictionary with higher "
                                                                                           "priority will be kept, "
                                                                                           "the other one(s) will be "
                                                                                           "deleted.")
    args = argparser.parse_args()

    command = ["preprocess_dicts.py", args.sw_file] + args.dicts
    if args.la_code:
        command += ["-lc " + args.la_code]
    if args.non_solr:
        command += ["--non-solr"]

    main(args.dicts, args.sw_file, command, args.la_code, args.non_solr)

