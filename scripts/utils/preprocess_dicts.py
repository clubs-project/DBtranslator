import unicodedata
import re
import argparse


def rreplace(s, old, new, num_occ):
    '''Replaces the last num_occ occurrences of old by new , taken from 
    https://stackoverflow.com/questions/2556108/rreplace-how-to-replace-the-last-occurrence-of-an-expression-in-a-string#2556252'''
    li = s.rsplit(old, num_occ)
    return new.join(li)


def read_in(input_path, stopwords):
    la_dict = dict()
    with open(input_path, "r") as f:
        umlaut_pattern = re.compile('[ÜǘÄäÖö]+')
        for line in f:
            # we want to have duplicates like -ise and -ize (BE/AE) and fuhrung/fuehrung (German), fuhrung is the
            # result of unicodedata.normalize(...) applied to "führung", fuehrung has to be added manually
            duplicate_needed = False
            entries = line.split("|||")
            # lowercase
            source_word = entries[0].lower()
            if source_word == "" or source_word in stopwords:
                # remove whole entry if source is empty or if source word is a stopword
                # debugging/ checking
                #print("Entry removed because of source word:", source_word)
                continue
            # ß has to be replaced manually, since unicodedata.normalize simply deletes it instead of replacing it with ss
            source_word = source_word.replace('ß', 'ss')

            # check if it is necessary to introduce duplicates like German ü -> ue (unicode normalization returns u)
            # and different spellings in AE and BE
            source_word_duplicate = None
            if umlaut_pattern.search(source_word):
                duplicate_needed = True
                source_word_duplicate = source_word.replace('ü', 'ue').replace('ö', 'oe').replace('ä', 'ae')
            elif source_word.endswith('ise'):
                duplicate_needed = True
                source_word_duplicate = rreplace(source_word, 'ise', 'ize', 1)
            elif source_word.endswith('ize'):
                duplicate_needed = True
                source_word_duplicate = rreplace(source_word, 'ize', 'ise', 1)
            elif source_word.endswith('isation'):
                duplicate_needed = True
                source_word_duplicate = rreplace(source_word, 'isation', 'ization', 1)
            elif source_word.endswith('ization'):
                duplicate_needed = True
                source_word_duplicate = rreplace(source_word, 'ization', 'isation', 1)
            elif source_word.endswith('our'):
                duplicate_needed = True
                source_word_duplicate = rreplace(source_word, 'our', 'or', 1)
            elif source_word.endswith('or'):
                duplicate_needed = True
                source_word_duplicate = rreplace(source_word, 'or', 'our', 1)

            # remove diacritics
            source_word = unicodedata.normalize('NFKD', source_word).encode('ASCII', 'ignore').decode()

            source_word = source_word.replace('[dokumenttyp]', '').strip()
            la_dict[source_word] = dict()

            if duplicate_needed:
                if source_word_duplicate is None:
                    print("There is a bug in the source word duplicate generation!")
                source_word_duplicate = unicodedata.normalize('NFKD', source_word_duplicate).encode('ASCII', 'ignore').decode()
                source_word_duplicate = source_word_duplicate.replace('[dokumenttyp]', '').strip()
                la_dict[source_word_duplicate] = dict()

            # iterate over translations
            delete_entry = False
            for i in range(1, len(entries)):
                la_code = entries[i].split(":")[0]
                translation = concatenate_string_list(entries[i].split(":")[1:], ":")
                translation = translation.rstrip().lower()
                if translation == "" or translation in stopwords:
                    # remove whole entry if translation into one language is empty or
                    # translation is a stopword in any language (it doesn't have to be a stopword in its own language)
                    delete_entry = True
                    # debugging/ checking
                    #print("Entry removed because of translation:", translation)
                    break
                translation = translation.replace('ß', 'ss')
                translation = unicodedata.normalize('NFKD', translation).encode('ASCII', 'ignore').decode()
                translation = translation.replace('[dokumenttyp]', '').strip()
                la_dict[source_word][la_code] = translation
                if duplicate_needed:
                    la_dict[source_word_duplicate][la_code] = translation

            if delete_entry:
                la_dict.pop(source_word, None)
                la_dict.pop(source_word_duplicate, None)

    return la_dict


def merge_dicts(dict_with_higher_priority, other_dict):
    for key in other_dict.keys():
        # if a key of other_dict also is a key in dict_with_higher_priority, we eliminate the key of the other_dict
        if key not in dict_with_higher_priority.keys():
            dict_with_higher_priority[key] = other_dict[key]
    return dict_with_higher_priority


def concatenate_string_list(string_list, string_between_strings=" ", add_at_last_string=False):
    result = ""
    for i in range(len(string_list)):
        if i == len(string_list)-1 and not add_at_last_string:
            result += string_list[i].strip()
        else:
            result += string_list[i].strip() + string_between_strings
    return result


def write_to_file(la_dict, path, command):
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
    Input file: one stopword per line, the stopwords are lower-cased, but no diacritics have been removed'''
    stopwords = set()
    with open(sw_file, "r") as f:
        for line in f:
            stopword = line.strip()
            stopwords.add(stopword)
    return stopwords


def main(l1, l2, l3, l4, sw_file, command, la_code):
    """ l1 > l2 > l3 > l4 in terms of priority"""
    stopwords = read_in_sw_file(sw_file)
    print("Reading in L1...")
    l1_dict = read_in(l1, stopwords)
    print("Reading in L2...")
    l2_dict = read_in(l2, stopwords)
    print("Reading in L3...")
    l3_dict = read_in(l3, stopwords)
    print("Reading in L4...")
    l4_dict = read_in(l4, stopwords)
    print("Merging L1 dict with L2 dict...")
    main_dict = merge_dicts(l1_dict, l2_dict)
    print("Merging resulted dict with L3 dict...")
    main_dict = merge_dicts(main_dict, l3_dict)
    print("Merging resulted dict with L4 dict...")
    main_dict = merge_dicts(main_dict, l4_dict)
    path_prefix = concatenate_string_list(l1.split("/")[:-1], "/", add_at_last_string=True)
    if la_code:
        path = path_prefix + l1.split("/")[-1].split(".")[0] + "." + l2.split("/")[-1].split(".")[0] + "." \
           + l3.split("/")[-1].split(".")[0] + "." + l4.split("/")[-1].split(".")[0] + ".merged." + la_code
    else:
        path_middle = l1.split("/")[-1]
        path = path_prefix + path_middle.split(".")[0] + ".concatenated.txt"
    print("Path:", path)
    print("Writing new dict to file...")
    write_to_file(main_dict, path, command)

if __name__=="__main__":
    argparser = argparse.ArgumentParser(description="Preprocess and merge four different dictionaries")
    argparser.add_argument("d1_file", type=str, help="Path to dict [in language] with highest priority (mandatory)")
    argparser.add_argument("d2_file", type=str, help="Path to dict [in language] with 2nd highest priority (mandatory)")
    argparser.add_argument("d3_file", type=str, help="Path to dict [in language] with 3rd highest priority (mandatory)")
    argparser.add_argument("d4_file", type=str, help="Path to dict [in language] with least priority (mandatory)")
    argparser.add_argument("sw_file", type=str, help="path to file containing stopwords in all languages (mandatory)")


    argparser.add_argument("-lc", "--language-code", dest="la_code", default = "",
                           help="If you want to merge four dictionaries of the same language, give the language code, "
                                "since otherwise the files will be named just like a merged version of the first dict in"
                                "four different languages (which might replace existing dictionaries of that kind).")
    args = argparser.parse_args()

    main(args.d1_file, args.d2_file, args.d3_file, args.d4_file, args.sw_file, [args.d1_file, args.d2_file,
                                                                                args.d3_file, args.d4_file,
                                                                                args.sw_file, args.la_code],
         args.la_code)
