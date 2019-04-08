import sys
import re
import logging


def read_in(path):
    result = dict()
    number_pattern = re.compile("\d+")
    with open(path, "r") as f:
        for line in f:
            number = number_pattern.search(line)
            if number:
                number = number.group()
                key = None
                if line.startswith("Mesh"):
                    if "word" in line:
                        key = "muw"
                    elif "multi" in line:
                        key  = "mum"
                    elif "query" in line:
                        key = "muq"
                    else:
                        logging.error("Wrong format of line", line)
                elif line.startswith("Backoff"):
                    if "word" in line:
                        key = "buw"
                    elif "multi" in line:
                        key = "bum"
                    elif "query" in line:
                        key = "buq"
                    else:
                        logging.error("Wrong format of line", line)
                elif line.startswith("Number"):
                    if "word" in line:
                        key = "cw"
                    elif "multi" in line:
                        key = "cm"
                    elif "query" in line:
                        key = "cq"
                    else:
                        logging.error("Wrong format of line", line)
                elif line.startswith("Singular"):
                    if "word" in line:
                        key = "suw"
                    elif "multi" in line:
                        key = "sum"
                    elif "query" in line:
                        key = "suq"
                    else:
                        logging.error("Wrong format of line", line)
                else:
                    if line.strip():
                        logging.error("Wrong format of line", line)
                result[key] = number
    return result


def generate_string(result):
    value_list = [result[x] for x in ["muw", "mum", "muq", "buw", "bum", "buq", "cw", "cm", "cq", "suw", "sum", "suq"]]
    latex_string = " & ".join(value_list)
    latex_string += "\\\\"
    return latex_string


def generate_string_from_path(path):
    values = read_in(path)
    return generate_string(values)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 generate_latex_table_line.py <path to stats.src file>")
        sys.exit(1)
    values = read_in(sys.argv[1])
    print(generate_string(values))