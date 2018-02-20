# DBtranslator

Scripts to download the information from the DB and translate it using our pre-trained models

## Title & Abstract Translation
The script ```tradTitlesAbstracts.sh``` runs the full pipeline for the translation of titles or abstracts. Before running it for the first time, you need to install the Marian decoder and download the pre-trained models as explained at the end of the section.

### Translation pipeline
Run the following command to execute the translation pipeline for titles or abstracts:
```
user@machine:~/home/DBtranslator/scripts/$ bash tradTitlesAbstracts.sh -h
   bash tradTitlesAbstracts.sh -t # -f tit|abs [-a ABHR|ABNHR] [-h] 
   where:
    -h  show this help text
    -t  number of threads
    -f  field to translate [tit|abs]
    -a  type of abstract [ABHR|ABNHR]
```
```
Example for titles:
    bash tradTitlesAbstracts.sh -t 8 -f tit
Example for abstracts:
    bash tradTitlesAbstracts.sh -t 8 -f abs -a ABHR
```

You must specify the field to be translated (tit vs. abs), and, in the second case, also the specific name of the field (ABHR vs. ABNHR). Defaults are **-f tit** and **-a ABHR**. For titles, the label **T_[lang]** is assumed. In order to change or add a new label you must modify
* `preproTits4trad.py` for title labels
* `preproAbst4trad.py` for abstract labels

The script automatically downloads all the titles or abstracts into one folder per sub-DB within PubPshyc, and each folder contains one file per language with all the titles/abstracts. These files are 
1.  pre-processed (cleaning+tokenisation+truecasing), 
2.  BPEd and tagged to match the training models (target language and procedence), 
3.  translated with Marian (amun), 
4.  post-processed (detokenisation+detruecasing), and 
5.  converted into a format ready for importing the translations into the index:
    ID\sFIELD\t<2LANG>\tTEXT

The output is one file per folder and language with the translations into the other three languages, one element per line
as seen in the example for file ```DBtranslator/titles/PMID/titles.en.trad```:

```
PMID_9819920 TI_E        <2es>        Estrategias de afrontamiento para personas que atienden a personas con enfermedad mental crónica
PMID_9819920 TI_E        <2de>        Copingstrategien für Menschen mit chronischem psychischen Erkrankungen
PMID_9819920 TI_E        <2fr>        Stratégies de coping pour les personnes souffrant de maladie mentale chronique
```

If you want to use the script only on a subset of the database, please, modify the query accordingly in `preproTits4trad.py` and/or `preproAbst4trad.py`.

### Pre-trained Models

### Marian Installation
In a Linux machine
```
   sudo apt-get install libboost-all-dev
   git clone https://github.com/marian-nmt/marian.git
```

```cd marian
   mkdir build && cd build
   cmake .. 
   make -j 
```

In case you only want the CPU version, compile with the following flag instead:
```cmake .. -DCUDA=off
```

If you need the bindings
```
   make python
```
For other OS or necessities refer to the Marian web page:
```https://github.com/marian-nmt/marian```


## Controlled Terms Translation
The script ```tradCTs.sh``` runs the full pipeline for the translation of controlled terms and related fields. 

### Translation pipeline
Run the following command to execute the translation pipeline for any of the four available fields:
```
user@machine:~/home/DBtranslator/scripts/$  bash tradCTs.sh -h
tradCTs.sh -f CTH|CTL|ITH|ITL [-h] 

where:
    -h  show this help text
    -f  field to translate [CTH|CTL|ITH|ITL]
```
```
Example:
    bash tradCTs.sh -f CTH
```

If you want to consider a new field, add it to `preproField4trad.py`
