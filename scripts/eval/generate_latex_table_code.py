from generate_latex_table_line import generate_string_from_path

dict_mapping = {"1": "mesh_4_lex_wikidata", "2": "wikidata_non_diff", "3": "wikidata_diff", "4": "4lex_non_diff", "5": "4lex_diff", "6": "mesh"}
la_mapping = {"e": "en", "d": "de", "s": "es", "f": "fr", "n": "none"}

with open("latex-table-code.txt", "w") as f:
    for dict_key in ["1", "2", "3", "4", "5", "6"]:
        for la_key in ["e", "d", "s", "f", "n"]:
            path = "server_results/" + dict_mapping[dict_key] + "/stats." + la_mapping[la_key]
            number_string = generate_string_from_path(path)
            line = dict_key + la_key + " & " + number_string + "\n"
            f.write(line)

