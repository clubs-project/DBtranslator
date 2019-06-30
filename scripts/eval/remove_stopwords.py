import sys

if len(sys.argv) != 3:
    print("Usage: python3 remove_stopwords.py <path to file to process> <path to file containing stopwords>")
    sys.exit(1)

file_to_process = sys.argv[1]
output_path = file_to_process + ".sw"
stopwords_path = sys.argv[2]

stopwords = set()

with open(stopwords_path, 'r') as f:
    for line in f:
        stopwords.add(line.strip())

with open(file_to_process, 'r') as inp:
    with open(output_path, 'w') as outp:
        for line in inp:
            tokens = line.strip().split()
            indices_to_delete = []
            for i in range(len(tokens)-1, -1, -1):
                if tokens[i] in stopwords:
                    indices_to_delete.append(i)

            for i in indices_to_delete:
                del tokens[i]

            new_line = " ".join(tokens) + "\n"
            outp.write(new_line)
