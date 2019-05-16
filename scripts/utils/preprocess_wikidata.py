import sys
from time import time

'''Compiles language-specific versions of a dictionary containing lines like
en::Belgium|||de::Belgien|||es::Bélgica|||fr::Belgique
The result will be four files each containing one of the lines:
Belgium|||de:Belgien|||es:Bélgica|||fr:Belgique
Belgien|||en:Belgium|||es:Bélgica|||fr:Belgique
Belgique|||en::Belgium|||de::Belgien|||es::Bélgica
Bélgica|||en::Belgium|||de::Belgien|||fr::Belgique
'''


def read_in(path_to_dict):
    dicts = dict()
    first = True
    num_entries = 0

    with open(path_to_dict, 'r') as f:
        for line in f:

            entries = line.rstrip().split("|||")
            entries_with_languages = dict()

            # set up a dictionary for each language
            for entry in entries:
                split_ = entry.split("::")
                la_code = split_[0]
                term = split_[1].replace(":", " ").strip()
                entries_with_languages[la_code] = term

            if first:
                first = False
                for la_code in entries_with_languages.keys():
                    dicts[la_code] = dict()

            for (la_code, term) in entries_with_languages.items():
                la_dict = dicts[la_code]

                # do not overwrite existing entries
                if term in la_dict:
                    continue
                la_dict[term] = dict()
                for (trans_la_code, translation) in entries_with_languages.items():
                    if trans_la_code == la_code:
                        continue
                    la_dict[term][trans_la_code] = translation

            num_entries += 1
            if num_entries % 100000 == 0:
                print("Read in {} entries".format(num_entries))

        return dicts


def write_to_file(path_to_dict, dicts):
    num_entries = 0
    for (la_code, la_dict) in dicts.items():
        output_path = path_to_dict + "." + la_code
        print("Writing dict for language code ", la_code)
        with open(output_path, 'w') as outp:
            for (term, translations) in la_dict.items():
                outp.write(term)
                for (trans_la_code, translation) in translations.items():
                    outp.write("|||" + trans_la_code + ":" + translation)
                outp.write("\n")
                num_entries += 1
                if num_entries % 100000 == 0:
                    print("Written {} entries".format(num_entries))
        print("Written dict for language code ", la_code)


if __name__=="__main__":
    if len(sys.argv) != 2:
         print("Usage: python3 preprocess_wikidata.py <path to wikidata>")
         sys.exit(1)
    path = sys.argv[1]
    start = time()
    print("Reading in dictionary...")
    dicts = read_in(path)
    print("Done after {0:.1f} seconds".format(time()-start))
    start = time()
    print("Compiling new dictionaries...")
    write_to_file(path, dicts)
    print("Done after {0:.1f} seconds".format(time()-start))


    # debug
    # path = "../../../lexicons/wikidata.diffsLabels2"
    # dicts = read_in(path)
    # write_to_file(path, dicts)