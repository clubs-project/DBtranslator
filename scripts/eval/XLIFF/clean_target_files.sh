#!/bin/sh

sed 's/OR//g' query.tgt > query_man.tgt &&
sed 's/AND//g' query_man.tgt > query_man2.tgt &&

# filter Irma's Spanish translations of OR and AND...
sed -E 's/\sO\s/ /g' query_man2.tgt > query_man.tgt &&
sed -E 's/\sY\s/ /g' query_man.tgt > query_man2.tgt &&

# filter publication year
sed -E 's/PY(<|>)?=\"?[0-9]{4}\"?//g' query_man2.tgt > query_man.tgt &&

# remove field names of translated fields
sed -E 's/(TI|SW|ti|sw|SH)\s?(=|:)\s?//g' query_man.tgt > query_man2.tgt &&
sed -E 's/(AU|JT|DB|LA|DT|CM)(=|:)\s?"[^"]+"//g' query_man2.tgt > query_man.tgt &&
# do JT manually because there are journal titles that are longer than one token which are not enclosed by quotation marks
sed -E 's/(AU|DB|LA|DT|CM|db)\s?(=|:)\s?\S+//g' query_man.tgt > query_man2.tgt &&

# remove double whitespace
sed -E 's/\s\s/ /g' query_man2.tgt > query_man.tgt &&
# remove empty lines
sed '/^\s*$/d' query_man.tgt > query_man2.tgt &&
# remove leading whitespace
sed -E 's/^\s+//g' query_man2.tgt > query_man.tgt &&

# delete lines only containing journal titles
sed -i '37d' query_man.tgt &&
sed -i '72d' query_man.tgt

# lowercase everything
tr '[:upper:]' '[:lower:]' < query_man.tgt > query_man2.tgt
