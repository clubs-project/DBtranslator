# Data: 12.05.2019
# Author: cristinae
#
# Lowercases sentences with more than 15 letters uppercase 
# Some abstracts in ISOC are completely uppercase
# (I'm taking into account that <abstract> <2en> are always lowercase)

awk 'BEGIN{ FPAT="[a-zA-Z]"; l=u=0 }
     {
         for (i=1; i<=NF; i++) ($i~/[a-z]/)? l++ : u++;
         if (u>15) { print tolower($0);}
         else {print $0;} ;
         l=u=0;
     }'  abstract.es.tc

