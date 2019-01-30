FILE=$1

# Sometimes the language tag is generated as a word
# This should not happen. tags are in the target vocab but have not been seen in training,
# that's the replace UNK
sed -i -e 's/<2es>//g' $FILE
sed -i -e 's/<2en>//g' $FILE
sed -i -e 's/<2fr>//g' $FILE
sed -i -e 's/<2de>//g' $FILE

# French detokeniser is not working properly
# TODO: Check moses file. Inconsistences might exist between my version of tok and detok
sed -i "s/ c '/ c'/g" $FILE
sed -i "s/^c '/c'/g" $FILE
sed -i "s/qu '/qu'/g" $FILE
sed -i "s/ l '/ l'/g" $FILE
sed -i "s/^l '/l'/g" $FILE
sed -i "s/ d '/ d'/g" $FILE
sed -i "s/^d '/d'/g" $FILE
sed -i "s/ s '/ s'/g" $FILE
sed -i "s/^s '/s'/g" $FILE
sed -i "s/ n '/ n'/g" $FILE
sed -i "s/^n '/n'/g" $FILE

# Unacceptable mistakes
sed -i "s/© Derecho/© Copyright/g" $FILE
sed -i "s/Derecho (/Copyright (/g" $FILE
sed -i "s/Autoría (/Copyright (/g" $FILE
sed -i "s/El autor de autor (c)/Copyright (c)/g" $FILE
sed -i "s/El autor de derecho de autor/Copyright/g" $FILE
sed -i "s/© Derecho del autor/© Copyright/g" $FILE
sed -i "s/Le droit d\'auteur/Copyright/g" $FILE
sed -i "s/Le droit d\'auteur/Copyright/g" $FILE
sed -i "s/Rechte (c)/Copyright (c)/g" $FILE
sed -i "s/Rechte 2/Copyright 2/g" $FILE
sed -i "s/Das Recht des Autors/Copyright/g" $FILE
