'''Merges four dictionaries that have been concatenated with preprocess.py'''
import sys
from preprocess_dicts import merge_dicts, write_to_file, concatenate_string_list


def read_in(input_path):
    ret_dict = dict()
    with open(input_path, "r") as f:
        for line in f:
            # first line is always of the kind <<<This dictionary has been compiled with <command>>>>
            if line.startswith("<<<"):
                continue
            entries = line.split("|||")
            source_word = entries[0]
            ret_dict[source_word] = dict()
            for i in range(1, len(entries)):
                la_code = entries[i].split(":")[0]
                translation = concatenate_string_list(entries[i].split(":")[1:], ":")
                translation = translation.rstrip().lower()
                ret_dict[source_word][la_code] = translation
    return ret_dict


def main(dict1_path, dict2_path, dict3_path, dict4_path, command):
    """dict1 > dict2 > dict3 > dict4 in terms of priority"""
    print("Reading in first dictionary...")
    dict1 = read_in(dict1_path)
    print("Reading in second dictionary...")
    dict2 = read_in(dict2_path)
    print("Reading in third dictionary...")
    dict3 = read_in(dict3_path)
    print("Reading in fourth dictionary...")
    dict4 = read_in(dict4_path)
    print("Merging results...")
    main_dict = merge_dicts(dict1, dict2)
    main_dict = merge_dicts(main_dict, dict3)
    main_dict = merge_dicts(main_dict, dict4)
    path_prefix = concatenate_string_list(dict1_path.split("/")[:-1], "/", add_at_last_string=True)
    print("Path prefix:", path_prefix)
    path = path_prefix + dict1_path.split("/")[-1].split(".")[0] + "." + dict2_path.split("/")[-1].split(".")[0] + "." \
           + dict3_path.split("/")[-1].split(".")[0] + "." + dict4_path.split("/")[-1].split(".")[0] + ".merged.txt"
    print("Path:", path)
    print("Writing new dict to file...")
    write_to_file(main_dict, path, command)

if __name__=="__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 merge_concatenated_dicts.py <path to dict with highest priority> <path to dict with 2nd "
              "highest priority> <path to dict with 3rd highest priority>" "<path to dict with least priority>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv)
