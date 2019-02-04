/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.zpid.pubpsych.search.query.queryparsers.fieldrewriters;

import java.util.HashMap;
import java.util.Map;
import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.ListIterator;
import java.util.Set;
import java.util.TreeMap;
import org.apache.lucene.index.Term;
import org.apache.lucene.search.BooleanClause;
import org.apache.lucene.search.BooleanQuery;
import org.apache.lucene.search.BoostQuery;
import org.apache.lucene.search.DisjunctionMaxQuery;
import org.apache.lucene.search.PhraseQuery;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.TermQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 *
 * @author sophie
 */
public class QueryFieldRewriter implements FieldRewriteInterface {
    
    /* FIELDS FOR REAL FUNCTIONALITY */

    private static final Logger LOG = LoggerFactory.getLogger(QueryFieldRewriter.class);
    private final Map<String, Map<String, String>> meshDict = new HashMap<>();

    // the second dictionary consisting of the four non-high-quality dictionaries
    private final Map<String, Map<String, String>> mixedDict = new HashMap<>();

    /*a map containing original field names and language-specific field names 
      if they exist (this is not consistent for all the fields, thus we need a map)
    First key: field name, second key: language code (D, E, F, S)*/
    private final Map<String, Map<String, List<String>>> laFieldNames = new TreeMap<>();
    
    /* every QueryNode will receive a unique ID for sorting purposes */
    private int nodeIdCounter = 1;

    /* FIELDS NEEDED FOR COLLECTING THE STATISTICS FOR EVALUATION */
    
    /* remember strings of one query: since a simple text query is parsed as a 
    query of many fields at once, we translate the same string again and again, 
    but the same string in one query should only count once in the statistics
    -  moreover, remember whether the string is an entire copy to be able to 
    increment the counter for entire copies iff the whole query is a copy*/
    private Set<String> seenStrings = new HashSet<>();
    
    /* statistics for evaluation: 
         - number of times mesh is used at word level
         - number of times mesh is used at string level 
            (whole string is found in Mesh)
         - number of times the whole query is translated using only mesh
         - number of times we need to use the low-quality dictionary (backoff) 
            at word level
         - number of times we need to use the low-quality dictionary (backoff) 
            at string level
         - number of times the whole query is translated using only the 
            low-quality dictionary
         - number of times the whole query is just copied
         - number of times the translation of a whole string is an entire copy
         - number of times the translation of a whole string is partly a copy
         - number of times words are copied (difference: if two of three tokens 
            are copied, this counter is increased by 2, whereas isPartialCopy is 
            increased by 1)
         - number of times singular forms are used for the transla-
            tion (for one string, each token-wise usage of a singular form is 
            counted separately)
         - number of strings where at least one singular form is used for the 
            translation
         - number of times the whole query is only translated with the help of 
            singular forms*/
    private int meshUsageWordLevel = 0;
    private int meshUsageStringLevel = 0;
    private int meshUsageQueryLevel = 0;
    private int backoffUsageWordLevel = 0;
    private int backoffUsageStringLevel = 0;
    private int backoffUsageQueryLevel = 0;
    private int entireCopyQueryLevel = 0;
    private int entireCopyStringLevel = 0;
    private int partialCopyStringLevel = 0;
    private int copyWordLevel = 0;
    private int singularUsageWordLevel = 0;
    private int singularUsageStringLevel = 0;
    private int singularUsageQueryLevel = 0;
    
    private boolean meshAtQueryLevel = true;
    private boolean backoffAtQueryLevel = true;
    private boolean entireCopyAtQueryLevel = true;
    private boolean singularAtQueryLevel = true;

    private boolean hasSeenFirstQuery = false;

    public QueryFieldRewriter(String pathToMeshDict, String pashToMixedDict,
            String pathToLaFieldNames) throws FileNotFoundException, IOException {
        readInDictionary(pathToMeshDict, true);
        readInDictionary(pashToMixedDict, false);
        readInFieldNames(pathToLaFieldNames);
    }
    
    public int getMeshUsageWordLevel(){
        return meshUsageWordLevel;
    }
    
    public int getMeshUsageStringLevel(){
        return meshUsageStringLevel;
    }
    
    public int getMeshUsageQueryLevel(){
        return meshUsageQueryLevel;
    }
    
    public int getBackoffUsageWordLevel(){
        return backoffUsageWordLevel;
    }
    
    public int getBackoffUsageStringLevel(){
        return backoffUsageStringLevel;
    }
    
    public int getBackoffUsageQueryLevel(){
        return backoffUsageQueryLevel;
    }
    
    public int getNumEntireCopyQueryLevel(){
        return entireCopyQueryLevel;
    }
    
    public int getNumEntireCopyStringLevel(){
        return entireCopyStringLevel;
    }
    
    public int getNumPartialCopyStringLevel(){
        return partialCopyStringLevel;
    }
    
    public int getNumCopyWordLevel(){
        return copyWordLevel;
    }
    
    public int getSingularUsageWordLevel(){
        return singularUsageWordLevel;
    }
    
    public int getSingularUsageStringLevel(){
        return singularUsageStringLevel;
    }
    
    public int getSingularUsageQueryLevel(){
        return singularUsageQueryLevel;
    }
    
    public void resetSeenStrings(){
        seenStrings = new HashSet<>();
    }

    private void readInFieldNames(String pathToFieldNames) throws FileNotFoundException, IOException {
        /*Expected format of the file: 
            - one line containing the field name
            - next line starts with a language code (D, E, F or S), then all 
                language-specific names follow separated by whitespaces
            - after this is done for all languages for which a language-specific
                version of the current field exists, a blank line follows, then 
                the schema is repeated for the next field
            - comments: lines starting with //*/
        BufferedReader br = new BufferedReader(new InputStreamReader(getClass().getClassLoader().getResourceAsStream(pathToFieldNames), "UTF8"));
        String line;
        String currentField = null;
        LOG.debug("Reading in language-specific field names");
        Map<String, List<String>> innerMap = new HashMap<>();
        boolean first = true;
        while ((line = br.readLine()) != null) {

            // ignore comments
            if (line.startsWith("//")) {
                continue;
            }

            String[] parts = line.split("\\s+");

            //check whether we are in a line only containing the field name
            if (parts.length == 1 && !parts[0].equals("")) {
                LOG.debug("Found field: " + parts[0]);
                if (!first) {
                    laFieldNames.put(currentField, innerMap);
                    innerMap = new HashMap<>();
                }
                first = false;
                currentField = parts[0];

            } //check whether we are in a line containing specific field names for a language
            else if (parts.length > 1) {
                if (currentField == null) {
                    LOG.warn("The file containing the language-specific field names doesn't meet the expected format in line: " + line);
                } else if (!parts[0].equals("D") && !parts[0].equals("E") && !parts[0].equals("F") && !parts[0].equals("S")) {
                    LOG.warn("Only the following language codes are permitted "
                            + "in the field name file: D for German, E for "
                            + "English, F for French, and S for Spanish. "
                            + "Line: " + line);
                } else {
                    List<String> fieldNames = new LinkedList(Arrays.asList(parts));

                    // remove the language code
                    fieldNames.remove(0);

                    innerMap.put(parts[0], fieldNames);
                }
            }
        }
    }

    private void readInDictionary(String pathToDictionary, boolean mesh) throws FileNotFoundException, IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(getClass().getClassLoader().getResourceAsStream(pathToDictionary), "UTF8"));
        String line;
        // read file line by line
        while ((line = br.readLine()) != null) {
            String[] parts = line.split("\\|\\|\\|");
            if (parts.length == 1) {
                // we're in the first line of a dictionary that contains information on how it was compiled
                continue;
            }
            String sourceWord = parts[0].trim();
            Map<String, String> translationMap = new HashMap<>();
            splitEntry(parts[1], translationMap, mesh);
            splitEntry(parts[2], translationMap, mesh);
            splitEntry(parts[3], translationMap, mesh);
            if (mesh) {
                meshDict.put(sourceWord, translationMap);
            } else {
                mixedDict.put(sourceWord, translationMap);
            }
        }
    }

    private void splitEntry(String entry, Map<String, String> translationMap, boolean mesh) {
        String[] laCodeAndTranslation = entry.split(":");
        if (laCodeAndTranslation.length == 1) {
            if (mesh) {
                LOG.warn("An empty translation has been found while reading in the MeSH dictionary:" + laCodeAndTranslation[0]);
            } else {
                LOG.warn("An empty translation has been found while reading in the mixed dictionary:" + laCodeAndTranslation[0]);
            }
            return;
        }
        translationMap.put(laCodeAndTranslation[0].trim(), laCodeAndTranslation[1].trim());
    }

    private Translation matchFieldNamesAndTranslations(Map<String, String> translationMap, String field) {
        /*Gets a map with language codes as key and translations for a whole 
        phrase as values. Returns a map of language-specific field names and 
        corresponding translations. We do not check whether a translation
        equals the original string, since this way, we can search through more 
        fields*/
 /* If a combination of field and language doesn't have a specific field 
        name (as SH and French), we mark this by SH~F to be able to distinguish 
        language-specific field names that exist in the schema and those that 
        we just need in this code to distinguish different languages.
         */

 /* use a TreeMap in order to ensure that the iteration over fields is 
        always performed in the same ordering and thus, the query is always 
        constructed in the same way-> easier testing */
        Map<String, String> fieldsAndTranslations = new TreeMap<>();
        Map<String, Boolean> fieldNamesLASpecific = new HashMap<>();
        if (laFieldNames.containsKey(field)) {
            if (translationMap.containsKey("de")) {
                /* We have to check for every language whether a specific 
                field-name for this language actually exists. For instance, SH 
                has English and German versions (SHE resp. SHD), but no French 
                or Spanish ones. */
                boolean noGermanName = gatherTransInfo(field, "D", "de",
                        fieldsAndTranslations, fieldNamesLASpecific, translationMap);
                if (noGermanName) {
                    addDummyField(translationMap, field, fieldsAndTranslations, fieldNamesLASpecific, "de", "D");
                }
            }
            if (translationMap.containsKey("en")) {
                boolean noEnglishName = gatherTransInfo(field, "E", "en",
                        fieldsAndTranslations, fieldNamesLASpecific, translationMap);
                if (noEnglishName) {
                    addDummyField(translationMap, field, fieldsAndTranslations, fieldNamesLASpecific, "en", "E");
                }
            }
            if (translationMap.containsKey("fr")) {
                boolean noFrenchName = gatherTransInfo(field, "F", "fr",
                        fieldsAndTranslations, fieldNamesLASpecific, translationMap);
                if (noFrenchName) {
                    addDummyField(translationMap, field, fieldsAndTranslations, fieldNamesLASpecific, "fr", "F");
                }
            }
            if (translationMap.containsKey("es")) {
                boolean noSpanishName = gatherTransInfo(field, "S", "es",
                        fieldsAndTranslations, fieldNamesLASpecific, translationMap);
                if (noSpanishName) {
                    addDummyField(translationMap, field, fieldsAndTranslations, fieldNamesLASpecific, "es", "S");
                }
            }
        } else {
            if (translationMap.containsKey("de")) {
                addDummyField(translationMap, field, fieldsAndTranslations, fieldNamesLASpecific, "de", "D");
            }

            if (translationMap.containsKey("en")) {
                addDummyField(translationMap, field, fieldsAndTranslations, fieldNamesLASpecific, "en", "E");
            }

            if (translationMap.containsKey("fr")) {
                addDummyField(translationMap, field, fieldsAndTranslations, fieldNamesLASpecific, "fr", "F");
            }

            if (translationMap.containsKey("es")) {
                addDummyField(translationMap, field, fieldsAndTranslations, fieldNamesLASpecific, "es", "S");
            }

        }
        return new Translation(fieldsAndTranslations, fieldNamesLASpecific, field);
    }

    public Boolean gatherTransInfo(String fieldName, String laFieldCode,
            String laTransCode, Map<String, String> fieldsAndTranslations,
            Map<String, Boolean> fieldNamesLASpecific,
            Map<String, String> translationMap) {
        boolean noLAName = true;
        if (null != laFieldNames.get(fieldName).get(laFieldCode)) {
            for (String laFieldName : laFieldNames.get(fieldName).get(laFieldCode)) {
                fieldsAndTranslations.put(laFieldName, translationMap.get(laTransCode));
                fieldNamesLASpecific.put(laFieldName, true);
                noLAName = false;
            }
        }
        return noLAName;
    }

    private void addDummyField(Map<String, String> translationMap,
            String field, Map<String, String> fieldsAndTranslations,
            Map<String, Boolean> fieldNamesLASpecific, String laTransCode,
            String laFieldCode) {
        String dummyName = field + "~" + laFieldCode;
        fieldsAndTranslations.put(dummyName, translationMap.get(laTransCode));
        fieldNamesLASpecific.put(dummyName, false);
    }

    private String removePluralEnding(String plural, String language) {
        /*Removes -s, -n, -en and -e as plural forms */
        // Implementation follows tradQueries.py in DBTranslator/scripts/utils

        StringBuilder singular = new StringBuilder();
        int lengthPlural = plural.length();
        if (lengthPlural > 1) {
            // Spanish
            if (language.equals("es")) {
                if (plural.endsWith("es")) {
                    return plural.substring(0, lengthPlural - 2);
                }
                if (plural.endsWith("s")) {
                    return plural.substring(0, lengthPlural - 1);
                }
            } //French
            else if (language.equals("fr") && plural.endsWith("s")) {
                return plural.substring(0, lengthPlural - 1);
            } // English
            else if (language.equals("en")) {
                if (lengthPlural > 3 && plural.endsWith("ies")) {
                    singular.append(plural.substring(0, lengthPlural - 3));
                    singular.append("y");
                    return singular.toString();
                }
                if (lengthPlural > 2 && plural.endsWith("es")) {
                    return plural.substring(0, lengthPlural - 2);
                }
                if (lengthPlural > 1 && plural.endsWith("s")) {
                    return plural.substring(0, lengthPlural - 1);
                }
            } // German
            else if (language.equals("de")) {
                if (lengthPlural > 2) {
                    /* in contrast to tradQueries, we don't need to remove 
                    umlauts here, because Solr already do the job for us*/
                    if (plural.endsWith("er")) {
                        return plural.substring(0, lengthPlural - 2);
                    }
                    if (plural.endsWith("n")) {
                        plural = plural.substring(0, lengthPlural - 1);
                    }
                }
                if (plural.endsWith("e") || plural.endsWith("s")) {
                    return plural.substring(0, lengthPlural - 1);
                }
            }
        }

        return plural;
    }
    
    private boolean checkNewString(String original){
        Boolean countInStats = true;
        if (seenStrings.contains(original)){
            countInStats = false;
        }
        else {
            // false as dummy value
            seenStrings.add(original);
        }
        return countInStats;
    }

    private Translation translateWholeString(String original, String field) {
        LOG.debug("Translating string \"" + original + "\" , which is the value of field " + field);
        boolean countInStats = checkNewString(original);
        
        if (meshDict.containsKey(original)) {
            LOG.debug("The whole string is contained in the MeSh dictionary.");
            if (countInStats){
                LOG.debug("translateWholeString: \""+ original + "\" counts towards the statistics.");
                meshUsageStringLevel += 1;
                backoffAtQueryLevel = false;
                singularAtQueryLevel = false;
                entireCopyAtQueryLevel = false;
            } else {
                LOG.debug("translateWholeString: \""+ original + "\" doesn't count towards the "
                        + "statistics.");
            }
            return matchFieldNamesAndTranslations(meshDict.get(original), 
                    field);
        } else if (mixedDict.containsKey(original)) {
            LOG.debug("The whole string is contained in the mixed dictionary.");
            if (countInStats){
                LOG.debug("translateWholeString: \""+ original + "\" counts towards the statistics.");
                backoffUsageStringLevel += 1;
                meshAtQueryLevel = false;
                singularAtQueryLevel = false;
                entireCopyAtQueryLevel = false;
            } else {
                LOG.debug("translateWholeString: \""+ original + "\" doesn't count towards the "
                        + "statistics.");
            }
            
            return matchFieldNamesAndTranslations(mixedDict.get(original),
                    field);
        }
        LOG.debug("No translation for whole string found.");
        return null;
    }

    private boolean checkSingular(String possibleSingular, String laCode, 
            String token, boolean countInStats, boolean isEntireCopy, 
            boolean mesh, Map<String, Map<String, String>> translationByToken){
        if (mesh){
            if (meshDict.containsKey(possibleSingular)) {
                        // TODO: ignore if source language is not laCode (and for other languages)
                        Map<String, String> translationMap = meshDict.get(possibleSingular);

                        /* Check whether the source language is laCode to avoid 
                        mistakes where the possible laCode singular form looks 
                        like a word in another language.*/
                        if (! translationMap.containsKey(laCode)){                        
                            translationByToken.put(token, translationMap);
                            if (countInStats){
                                meshUsageWordLevel += 1;
                                singularUsageWordLevel += 1;
                            }
                            backoffAtQueryLevel = false;
                            isEntireCopy = false;
                            return true;
                        }
            }
        }
        else {
            if (mixedDict.containsKey(possibleSingular)){
                // TODO: ignore if source language is not laCode (and for other languages)
                        Map<String, String> translationMap = mixedDict.get(possibleSingular);

                        /* Check whether the source language is laCode to avoid 
                        mistakes where the possible laCode singular form looks 
                        like a word in another language.*/
                        if (! translationMap.containsKey(laCode)){                        
                            translationByToken.put(token, translationMap);
                            if (countInStats){
                                backoffUsageWordLevel += 1;
                                singularUsageWordLevel += 1;
                            }
                            meshAtQueryLevel = false;
                            isEntireCopy = false;
                            return true;
                        }
            }
        }
        return false;
    }

    private Translation translate(String original, String field) {
        /* check whether we have already seen the string BEFORE calling 
        translateWholeString, because in this method, original will be added 
        to seenStrings, because it is also called at another point in the code 
        where this method isn't used*/
        /* also, ignore warm-up query*/
        Boolean countInStats = true;
        if (seenStrings.contains(original) || ! hasSeenFirstQuery){
            countInStats = false;
            LOG.debug("translate: \""+ original + "\" doesn't count towards the "
                    + "statistics.");            
        } else{
            LOG.debug("translate: \""+ original + "\" counts towards the statistics.");
        }
        
        /* if seenStrings doesn't contain original yet, it will be added in translateWholeString*/
        Translation wholeStringTranslation = translateWholeString(original, field);
        if (wholeStringTranslation != null) {
            return wholeStringTranslation;
        }

        /* split the string and translate token by token*/
        LOG.debug("No translation for whole string found, trying to translate tokens.");
        String[] tokens = original.split("\\s+");
        Map<String, Map<String, String>> translationByToken = new HashMap<>();

        String german = "";
        String english = "";
        String french = "";
        String spanish = "";
        
        /* remember whether the whole string has been translated with the help 
        of singular forms*/
        boolean onlySingular = true;
        boolean isEntireCopy = true;
        boolean isPartialCopy = false;

        // get all token-wise translations
        for (String token : tokens) {
            if (meshDict.containsKey(token)) {
                LOG.debug("MeSH dict contains " + token);
                translationByToken.put(token, meshDict.get(token));
                if (countInStats){
                    meshUsageWordLevel += 1;
                }
                onlySingular = false;
                isEntireCopy = false;
                backoffAtQueryLevel = false;
            } else if (mixedDict.containsKey(token)) {
                LOG.debug("Mixed dict contains " + token);
                translationByToken.put(token, mixedDict.get(token));
                if (countInStats){
                    backoffUsageWordLevel += 1;
                }
                onlySingular = false;
                isEntireCopy = false;
                meshAtQueryLevel = false;
            } else {
                // no translation available: try possible singular forms
                LOG.debug("No translations for \"" + token + "\" found, now searching for possible singular forms.");
                String possibleSingularEn = removePluralEnding(token, "en");
                String possibleSingularDe = removePluralEnding(token, "de");
                String possibleSingularFr = removePluralEnding(token, "fr");
                String possibleSingularEs = removePluralEnding(token, "es");

                // look for possible singular forms in MeshDict, precedence EN > DE > FR > ES
                if (checkSingular(possibleSingularEn, "en", token, 
                        countInStats, isEntireCopy, true, translationByToken)){
                    LOG.debug("Found possible English singular form \"" + 
                            possibleSingularEn + "\" for token " + token + 
                            " in MeSH dict.");

                } else if (checkSingular(possibleSingularDe, "de", token, 
                        countInStats, isEntireCopy, true, translationByToken)){
                    LOG.debug("Found possible German singular form \"" + 
                            possibleSingularDe + "\" for token " + token + 
                            " in MeSH dict.");
                } else if (checkSingular(possibleSingularFr, "fr", token, 
                        countInStats, isEntireCopy, true, translationByToken)){
                    LOG.debug("Found possible French singular form \"" + 
                            possibleSingularFr + "\" for token " + token + 
                            " in MeSH dict.");
                } else if (checkSingular(possibleSingularEs, "es", token, 
                        countInStats, isEntireCopy, true, translationByToken)){
                    LOG.debug("Found possible Spanish singular form \"" + 
                            possibleSingularEs + "\" for token " + token + 
                            " in MeSH dict.");
                }
                // look for possible singular forms in mixedDict, precedence EN > DE > FR > ES
                else if (checkSingular(possibleSingularEn, "en", token, 
                        countInStats, isEntireCopy, false, 
                        translationByToken)){
                    LOG.debug("Found possible English singular form \"" + 
                            possibleSingularEn + "\" for token " + token + 
                            " in mixed dict.");
                } else if (checkSingular(possibleSingularDe, "de", token, 
                        countInStats, isEntireCopy, false, 
                        translationByToken)){
                    LOG.debug("Found possible German singular form \"" + 
                            possibleSingularDe + "\" for token " + token + 
                            " in mixed dict.");
                } else if (checkSingular(possibleSingularFr, "fr", token, 
                        countInStats, isEntireCopy, false, 
                        translationByToken)){
                    LOG.debug("Found possible French singular form \"" + 
                            possibleSingularFr + "\" for token " + token + 
                            " in mixed dict.");
                } else if (checkSingular(possibleSingularEs, "es", token, 
                        countInStats, isEntireCopy, false, 
                        translationByToken)){
                    LOG.debug("Found possible Spanish singular form \"" + 
                            possibleSingularEs + "\" for token " + token + 
                            " in mixed dict.");
                } // singular forms are also not contained in one of the dicts: just copy the token
                else {
                    // TODO: implement counting for statistics
                    LOG.debug("No possible singular form is contained in any of the dicts. The token is now copied as its own translation into all languages.");
                    Map<String, String> dummyMap = new HashMap<>();
                    dummyMap.put("de", token);
                    dummyMap.put("en", token);
                    dummyMap.put("fr", token);
                    dummyMap.put("es", token);
                    translationByToken.put(token, dummyMap);
                    onlySingular = false;
                    isPartialCopy = true;
                    if (countInStats){
                        copyWordLevel += 1;
                    }
                    meshAtQueryLevel = false;
                    backoffAtQueryLevel = false;
                }
            }
        }
        
        if (countInStats){
            if (isEntireCopy) {
                entireCopyStringLevel += 1;
                LOG.debug("Incremented number of entire copies at string:" + 
                        original + " for field: " + field);
                seenStrings.add(original);
                
            } else if (isPartialCopy) {
                partialCopyStringLevel += 1;
                LOG.debug("Incremented number of partial copies at string:" + 
                        original + " for field: " + field);
                entireCopyAtQueryLevel = false;
            } else {
                entireCopyAtQueryLevel = false;
            }

            if (onlySingular) {
                singularUsageStringLevel += 1;
                LOG.debug("Incremented number of singularUsageStringLevel at "
                        + "string:" + original + " for field: " + field);
            }
            else {
                singularAtQueryLevel = false;
            }
        }
        

        boolean firstToken = true;
        for (String token : tokens) {
            if (!firstToken) {
                german += " ";
                english += " ";
                french += " ";
                spanish += " ";
            }
            firstToken = false;
            Map<String, String> translations = translationByToken.get(token);
            if (translations.containsKey("de")) {
                german += translations.get("de");
            }
            if (translations.containsKey("en")) {
                english += translations.get("en");
            }
            if (translations.containsKey("fr")) {
                french += translations.get("fr");
            }
            if (translations.containsKey("es")) {
                spanish += translations.get("es");
            }
        }

        // if one token-based translation is completely identical to the source version, we can drop it
        Map<String, String> translationMap = new HashMap<>();
        if (!german.replaceAll("\\s+", "").equals("") && !german.equals(original)) {
            translationMap.put("de", german);
        }
        if (!english.replaceAll("\\s+", "").equals("") && !english.equals(original)) {
            translationMap.put("en", english);
        }
        if (!french.replaceAll("\\s+", "").equals("") && !french.equals(original)) {
            translationMap.put("fr", french);
        }
        if (!spanish.replaceAll("\\s+", "").equals("") && !spanish.equals(original)) {
            translationMap.put("es", spanish);
        }

        return matchFieldNamesAndTranslations(translationMap, field);
    }

    /*Builds a tree displaying the structure of the query. Instead of 
    manipulating the queries directly when translating, we will manipulate this tree.*/
    public QueryNode buildQueryNode(Query query, BooleanClause.Occur occLvl) {
        /* some code duplication, but it shouldn't be possible to construct a 
        QueryNode without specifying its type, thus we need these case 
        distinctions
         */
        if (query instanceof BooleanQuery) {
            QueryNode qn = new QueryNode(QueryNode.QueryType.BOOLEAN, nodeIdCounter);
            nodeIdCounter++;
            if (occLvl != null) {
                qn.setOccurrenceLevel(occLvl);
            }
            for (BooleanClause clause : ((BooleanQuery) query).clauses()) {
                qn.addChild(buildQueryNode(clause.getQuery(), clause.getOccur()));
            }
            qn.markAsToTranslate();
            return qn;
        } else if (query instanceof DisjunctionMaxQuery) {
            DisjunctionMaxQuery dmq = ((DisjunctionMaxQuery) query);
            QueryNode qn = new QueryNode(QueryNode.QueryType.DISJUNCTIONMAX, nodeIdCounter);
            nodeIdCounter++;
            if (occLvl != null) {
                qn.setOccurrenceLevel(occLvl);
            }
            for (Query disjunct : dmq.getDisjuncts()) {
                qn.addChild(buildQueryNode(disjunct, null));
            }
            qn.setTieBreakerMultiplier(dmq.getTieBreakerMultiplier());
            qn.markAsToTranslate();
            return qn;
        } else if (query instanceof PhraseQuery) {
            PhraseQuery pq = ((PhraseQuery) query);
            QueryNode qn = new QueryNode(QueryNode.QueryType.PHRASE, nodeIdCounter);
            nodeIdCounter++;
            if (occLvl != null) {
                qn.setOccurrenceLevel(occLvl);
            }
            qn.setSlop(pq.getSlop());
            StringBuilder phrase = new StringBuilder();
            String field = "";
            boolean first = true;
            for (Term term : pq.getTerms()) {
                field = term.field(); // a PhraseQuery always only deals with one field
                if (!first) {
                    phrase.append(" ");
                }
                first = false;
                phrase.append(term.text());
            }
            qn.setFieldName(field);
            qn.setText(phrase.toString());

            if (hasToBeTranslated(field)) {
                qn.markAsToTranslate();
            }

            return qn;
        } else if (query instanceof TermQuery) {
            TermQuery tq = ((TermQuery) query);
            QueryNode qn = new QueryNode(QueryNode.QueryType.TERM, nodeIdCounter);
            nodeIdCounter++;
            if (occLvl != null) {
                qn.setOccurrenceLevel(occLvl);
            }
            String field = tq.getTerm().field();
            qn.setFieldName(field);
            qn.setText(tq.getTerm().text());

            if (hasToBeTranslated(field)) {
                qn.markAsToTranslate();
            }

            return qn;
        } else if (query instanceof BoostQuery) {
            BoostQuery bq = ((BoostQuery) query);
            QueryNode qn = new QueryNode(QueryNode.QueryType.BOOST, nodeIdCounter);
            nodeIdCounter++;
            if (occLvl != null) {
                qn.setOccurrenceLevel(occLvl);
            }
            qn.setBoost(bq.getBoost());
            QueryNode child = buildQueryNode(bq.getQuery(), null);
            qn.addChild(child);
            if (child.hasToBeTranslated()) {
                qn.markAsToTranslate();
            }
            return qn;
        } else {
            LOG.warn("Unhandled query instance type "
                    + query.getClass().getSimpleName()
                    + "; now copying old query.");
            QueryNode qn = new QueryNode(QueryNode.QueryType.DUMMY, nodeIdCounter);
            nodeIdCounter++;
            if (occLvl != null) {
                qn.setOccurrenceLevel(occLvl);
            }
            qn.setOriginalQuery(query);
            return qn;
        }
    }

    public QueryNode translateQueryNode(QueryNode old) {
        // check whether this node has to be translated at all
        if (!old.hasToBeTranslated()) {
            return old;
        }

        QueryNode.QueryType oldType = old.getType();
        switch (oldType) {
            case BOOLEAN: {
                Map<String, PreTranslationInfo> fieldsAndPreTransInfo = new HashMap<>();
                List<QueryNode> children = old.getChildren();
                ListIterator<QueryNode> childItr = children.listIterator();
                List<QueryNode> nodesToBeTranslatedAlone = new ArrayList<>();
                List<QueryNode> disjunctionMaxQueries = new ArrayList<>();

                /* concatenate the strings of those subqueries combined with AND*/
                while (childItr.hasNext()) {
                    QueryNode child = childItr.next();

                    if (child.getOccurrenceLevel().equals(BooleanClause.Occur.MUST)) {
                        String fieldName = child.getFieldName();
                        if (fieldName != null) {
                            if (child.hasToBeTranslated()) {
                                /* only concatenate the strings querying the same field*/
                                if (!fieldsAndPreTransInfo.containsKey(fieldName)) {
                                    fieldsAndPreTransInfo.put(fieldName, new PreTranslationInfo());
                                }
                                fieldsAndPreTransInfo.get(fieldName).addString(child.getText() + " ");

                                // we have to use previousIndex() since the iterator already moved on with next()
                                fieldsAndPreTransInfo.get(fieldName).addOriginalNode(childItr.previousIndex(), child);
                            }
                            /* don't do anything with nodes containing fields that 
                            we do not want to translate*/
                        } else if (child.getType().equals(QueryNode.QueryType.DISJUNCTIONMAX)) {
                            disjunctionMaxQueries.add(child);
                        } else {
                            nodesToBeTranslatedAlone.add(child);
                        }
                    } else {
                        // an occurrence level other than MUST means we have to translate the child separately
                        childItr.set(translateQueryNode(child));
                    }
                }

                for (Map.Entry<String, PreTranslationInfo> entry : fieldsAndPreTransInfo.entrySet()) {
                    String fieldName = entry.getKey();
                    PreTranslationInfo transInfo = entry.getValue();
                    String childStrings = transInfo.buildString().trim();
                    if (!childStrings.equals("")) {

                        /* Map<String, String> consists of (language-specific) field 
                        names as keys and corresponding translations as value.
                        The Boolean indicates whether these language-specific field 
                        names actually exist in the schema or if they are just dummy
                        names (if a fi2eld, e.g. "text", doesn't have 
                        language-specific field names, then storing a translation 
                        with the key "text" would overwrite the other translations)*/
                        Translation translationOfWholeString = translateWholeString(childStrings, fieldName);

                        /*it was possible to translate the whole string*/
                        if (translationOfWholeString != null) {

                            // new in-between node with occurrence level MUST, which is the parent node of all translations
                            QueryNode inBetween = new QueryNode(QueryNode.QueryType.BOOLEAN, nodeIdCounter);
                            nodeIdCounter++;
                            inBetween.setOccurrenceLevel(BooleanClause.Occur.MUST);
                            Collection<QueryNode> originalNodes = transInfo.getNodes();

                            /* check whether we have to replace the old children with a new parent node */
                            if (originalNodes.size() > 1) {
                                QueryNode parentOfOldNodes = new QueryNode(QueryNode.QueryType.BOOLEAN, nodeIdCounter);
                                nodeIdCounter++;
                                /* set occurrence level to SHOULD since we want to have
                                a disjunction of all original nodes and translations*/
                                parentOfOldNodes.setOccurrenceLevel(BooleanClause.Occur.SHOULD);
                                for (QueryNode originalNode : transInfo.getNodes()) {
                                    parentOfOldNodes.addChild(originalNode);
                                }

                                /* remove original nodes*/
                                List<Integer> originalIndices = new ArrayList(transInfo.getIntegers());
                                Collections.sort(originalIndices, Collections.reverseOrder());

                                /*indices are in descending order -> we can safely 
                                delete the corresponding nodes without adjusting the indices*/
                                for (int i : originalIndices) {
                                    old.removeChildAtIndex(i);
                                }

                                inBetween.addChild(parentOfOldNodes);
                                inBetween.addChildren(buildNewChildren(translationOfWholeString, QueryNode.QueryType.TERM, true, 0, null));
                            } else {
                                /* there is only one original node for the 
                                translated string -> it suffices to set its 
                                occurrence level to SHOULD to get a disjunction of 
                                the original string and its translations*/
                                for (int i : transInfo.getIntegers()) {
                                    QueryNode oldChild = old.getChildAtIndex(i);
                                    oldChild.setOccurrenceLevel(BooleanClause.Occur.SHOULD);
                                    inBetween.addChild(oldChild);
                                    old.removeChildAtIndex(i);
                                    /* since there is only one original node and thus only one iteration, we can do the following*/
                                    inBetween.addChildren(buildNewChildren(translationOfWholeString, oldChild.getType(), false, 0, null));
                                }
                            }
                            old.addChild(inBetween);
                        } /* the tokens couldn't be translated as a whole -> 
                        translate them token by token */ /* in this case, 
                        children must be Phrase or TermQueries, since they 
                        contain text */ else {
                            for (Map.Entry<Integer, QueryNode> oldNodeEntry : transInfo.getOriginalNodesMap().entrySet()) {
                                old.replaceChildAtIndex(oldNodeEntry.getKey(), translateQueryNode(oldNodeEntry.getValue()));
                            }
                        }
                    } else {
                        /* there are no tokens -> traverse the tree downwards */
                        for (Map.Entry<Integer, QueryNode> oldNodeEntry : transInfo.getOriginalNodesMap().entrySet()) {
                            old.replaceChildAtIndex(oldNodeEntry.getKey(), translateQueryNode(oldNodeEntry.getValue()));
                        }
                    }
                }

                if (disjunctionMaxQueries.size() > 1) {
                    /* if there is more than one DMQ, we have to check whether 
                    there are disjuncts with same field and (if BoostQueries) same 
                    boost */
                    LOG.debug("Trying to match DMQs with same field for " + old.buildQuery().toString());
                    Map<QueryNode, List<QueryNode>> queryNodeGroups = matchDMQsWithSameField(disjunctionMaxQueries);
                    for (Map.Entry<QueryNode, List<QueryNode>> entry : queryNodeGroups.entrySet()) {
                        QueryNode representative = entry.getKey();
                        List<QueryNode> nodesOfSameGroup = entry.getValue();
                        /* check if we have other nodes with the same group*/
                        if (nodesOfSameGroup.isEmpty()) {
                            continue;
                        }
                        
                        LOG.debug("Node " + 
                                representative.buildQuery().toString() 
                                + " has at least one node of the same group");

                        /* there is at least one node of the same group */
                        StringBuilder sb = new StringBuilder();
                        if (representative.getType().equals(QueryNode.QueryType.BOOST)) {
                            sb.append(representative.getChildAtIndex(0).getText());
                        } else {
                            sb.append(representative.getText());
                        }

                        /* store the IDs so that we can assign the new nodes to different DMQs */
                        List<Integer> idsOfDMQs = new ArrayList<>();
                        idsOfDMQs.add(representative.getParentId());

                        boolean boostQuery = false;
                        boolean otherQueryType = false;

                        for (QueryNode node : nodesOfSameGroup) {
                            sb.append(" ");
                            if (node.getType().equals(QueryNode.QueryType.BOOST)) {
                                sb.append(node.getChildAtIndex(0).getText());
                                boostQuery = true;
                            } else {
                                sb.append(node.getText());
                                otherQueryType = true;
                            }
                            idsOfDMQs.add(node.getParentId());
                        }

                        if (boostQuery && otherQueryType) {
                            LOG.warn("Boost and non-boost queries combined in the same group:" + nodesOfSameGroup.toString());
                        }

                        String wholeString = sb.toString();
                        LOG.debug("Whole string of group: " + wholeString);
                        if (meshDict.containsKey(wholeString)) {
                            /* there is a translation for the whole string*/
                            Map<String, String> translationMap = meshDict.get(wholeString);
                            LOG.debug("Found translation for whole string "
                                    + "of group in Mesh.");
                            translateGroup(representative, nodesOfSameGroup,
                                    translationMap, disjunctionMaxQueries, idsOfDMQs);

                        } else if (mixedDict.containsKey(wholeString)) {
                            Map<String, String> translationMap = mixedDict.get(wholeString);
                            LOG.debug("Found translation for whole string "
                                    + "of group in the backoff dict.");
                            translateGroup(representative, nodesOfSameGroup,
                                    translationMap, disjunctionMaxQueries, idsOfDMQs);
                        } else{
                            LOG.debug("No translation for whole string of "
                                    + "group found.");
                        }

                    }

                    /* add all disjunctionMaxQueries to translate single fields or 
                    fields for which there is no translation for the whole string*/
                    nodesToBeTranslatedAlone.addAll(disjunctionMaxQueries);

                } else {
                    /* if there is only one DMQ, we can add it to the nodes without 
                    field, since we do not want to combine it with non-DMQ children 
                    (the children of the DMQ are disjuncts, thus not compulsory)*/
                    nodesToBeTranslatedAlone.addAll(disjunctionMaxQueries);
                }

                /* translate the nodes to be translated on their own (e.g. nodes 
                without field names)*/
                List<QueryNode> childrenAfterChanges = old.getChildren();
                for (QueryNode node : nodesToBeTranslatedAlone) {
                    int index = childrenAfterChanges.indexOf(node);
                    old.replaceChildAtIndex(index, translateQueryNode(node));
                }
                break;
            }
            case DISJUNCTIONMAX: {
                List<QueryNode> newChildren = new ArrayList<>();
                for (QueryNode child : old.getChildren()) {
                    /* check whether child has to be translated*/
                    if (!child.hasToBeTranslated()) {
                        continue;
                    }

                    QueryNode.QueryType childType = child.getType();
                    switch (childType) {
                        case BOOLEAN:
                        case DISJUNCTIONMAX:
                            // translate the node on its own if its a BooleanQuery or a DisjunctionMaxQuery
                            newChildren.add(translateQueryNode(child));
                            break;
                        case BOOST: {
                            LOG.debug("Found BoostQuery: " + child.buildQuery().toString());
                            QueryNode wrappedQuery = child.getChildAtIndex(0);
                            QueryNode.QueryType wqType = wrappedQuery.getType();
                            List<QueryNode> newNodes = translateWrappedQueryOfBoostQuery(wrappedQuery, wqType, child);
                            newChildren.addAll(newNodes);
                            break;
                        }
                        case PHRASE:
                        case TERM: {
                            // copy the original node
                            Translation trans = translate(child.getText(), child.getFieldName());
                            List<QueryNode> newNodes = buildNewChildren(trans, childType, false, 0, null);
                            newChildren.addAll(newNodes);
                            break;
                        }
                        default:
                            LOG.warn("Unhandled Query instance type: " + child.getOriginalQuery().getClass().getSimpleName());
                            break;
                    }
                }
                old.addChildren(newChildren);
                break;
            }
            case BOOST: {
                QueryNode wrappedQuery = old.getChildAtIndex(0);
                List<QueryNode> newNodes = translateWrappedQueryOfBoostQuery(wrappedQuery, wrappedQuery.getType(), old);

                /* newNodes is empty if wrappedQuery was of type Boolean or 
                DisjunctionMaxQuery; then the wrappedQuery of old was directly 
                replaced by its translation*/
                if (newNodes.isEmpty()) {
                    return old;
                }

                /* Otherwise, combine old and new BoostQueries into a BooleanQuery.*/
                QueryNode inBetween = new QueryNode(QueryNode.QueryType.BOOLEAN, nodeIdCounter);
                nodeIdCounter++;
                inBetween.setOccurrenceLevel(old.getOccurrenceLevel());
                old.setOccurrenceLevel(BooleanClause.Occur.SHOULD);
                inBetween.addChild(old);
                inBetween.addChildren(newNodes);
                return inBetween;
            }

            case PHRASE:
            case TERM: {
                Translation trans = translate(old.getText(), old.getFieldName());
                List<QueryNode> newNodes = buildNewChildren(trans, old.getType(), false, 0, null);
                QueryNode inBetween = new QueryNode(QueryNode.QueryType.BOOLEAN, nodeIdCounter);
                nodeIdCounter++;
                inBetween.setOccurrenceLevel(old.getOccurrenceLevel());
                old.setOccurrenceLevel(BooleanClause.Occur.SHOULD);
                inBetween.addChild(old);
                inBetween.addChildren(newNodes);
                return inBetween;
            }

            default:
                LOG.warn("Unhandled QueryNode instance type " + old.getOriginalQuery().getClass().getSimpleName());
        }
        return old;
    }

    private void translateGroup(QueryNode representative, List<QueryNode> group,
            Map<String, String> translationMap, List<QueryNode> disjunctionMaxQueries, List<Integer> idsOfDMQs) {
        QueryNode.QueryType type = representative.getType();
        String fieldName = representative.getFieldName();
        if (type.equals(QueryNode.QueryType.BOOST)) {
            fieldName = representative.getChildAtIndex(0).getFieldName();
            // check whether the child has to be translated at all
            if (!representative.getChildAtIndex(0).hasToBeTranslated()) {
                return;
            }
        } else {
            if (!representative.hasToBeTranslated()) {
                return;
            }
        }

        // 0 if no BoostQuery
        Float boost = representative.getBoost();

        Translation translationsWithCorrectFieldNames = matchFieldNamesAndTranslations(translationMap, fieldName);

        for (Map.Entry<String, String> translation : translationsWithCorrectFieldNames.getTranslations().entrySet()) {
            String translationString = translation.getValue();
            String[] translationTokens = translationString.split("\\s+");
            int numOfCorrespondingDMQs = idsOfDMQs.size();
            for (int i = 0; i < translationTokens.length; i++) {
                String token = translationTokens[i];
                QueryNode newNode = new QueryNode(type, nodeIdCounter);
                nodeIdCounter++;
                if (type.equals(QueryNode.QueryType.BOOST)) {
                    newNode.setBoost(boost);
                    // use TermQuery because we split the translation
                    QueryNode wrappedQuery = new QueryNode(QueryNode.QueryType.TERM, nodeIdCounter);
                    nodeIdCounter++;
                    if (translationsWithCorrectFieldNames.isLanguageSpecificFieldName(translation.getKey())) {
                        wrappedQuery.setFieldName(translation.getKey());
                    } else {
                        wrappedQuery.setFieldName(fieldName);
                    }
                    wrappedQuery.setText(token);
                    newNode.addChild(wrappedQuery);
                } else {
                    if (translationsWithCorrectFieldNames.isLanguageSpecificFieldName(translation.getKey())) {
                        newNode.setFieldName(translation.getKey());
                    } else {
                        newNode.setFieldName(fieldName);
                    }
                    newNode.setText(token);
                }

                // distribute translations across the DMQs
                if (i < numOfCorrespondingDMQs) {
                    disjunctionMaxQueries.get(idsOfDMQs.get(i)).addChild(newNode);
                } else {
                    disjunctionMaxQueries.get(idsOfDMQs.get(numOfCorrespondingDMQs - 1)).addChild(newNode);
                }
            }
        }

        /* everything is translated */
        representative.unmarkToTranslate();
        if (representative.getType().equals(QueryNode.QueryType.BOOST)) {
            representative.getChildAtIndex(0).unmarkToTranslate();
        }

        for (QueryNode node : group) {
            node.unmarkToTranslate();
            if (node.getType().equals(QueryNode.QueryType.BOOST)) {
                node.getChildAtIndex(0).unmarkToTranslate();
            }
        }
    }

    private Map<QueryNode, List<QueryNode>> matchDMQsWithSameField(List<QueryNode> disjunctionMaxQueries) {
        /* key: a QueryNode of some type x, with some field name y or some boost factor z, value: list of 
        all QueryNodes (in other DisjunctionMaxQueries) with x and y or z*/
        // use a TreeMap to maintain the same order all the time [needed for testing]
        QueryNodeComparator qnc = new QueryNodeComparator();
        Map<QueryNode, List<QueryNode>> queryNodeGroups = new TreeMap<>(qnc);

        // need to find the corresponding representative of the group
        // 1st key: QueryType, 2nd key: field name
        Map<QueryNode.QueryType, Map<String, QueryNode>> identificationMap = new HashMap<>();

        /* we need to remember the boost for BoostQueries; 1st key: boost factor, 
        2nd key: field name of wrapped query (only TermQueries and PhraseQueries
        supported, more complicated queries are translated on their own)*/
        Map<Float, Map<String, QueryNode>> identificationMapForBoostQueries = new HashMap<>();
        for (int i = 0; i < disjunctionMaxQueries.size(); i++) {
            QueryNode dmq = disjunctionMaxQueries.get(i);
            for (QueryNode child : dmq.getChildren()) {
                if (child.hasToBeTranslated()) {
                    child.setParentId(i);
                    QueryNode.QueryType queryType = child.getType();

                    switch (queryType) {
                        case BOOST: {
                            // wrapped query, a BoostQuery only has one child
                            QueryNode grandChild = child.getChildAtIndex(0);
                            if ((!grandChild.getType().equals(QueryNode.QueryType.TERM)) && (!grandChild.getType().equals(QueryNode.QueryType.PHRASE))) {
                                // all other query types except for TermQueries and PhraseQueries are too complicated to combine with other disjuncts
                                continue;
                            }
                            float boost = child.getBoost();
                            String fieldName = grandChild.getFieldName();
                            /* check if we have already found a QueryNode with the same
                                type, field and boost*/
                            if (identificationMapForBoostQueries.containsKey(boost)) {
                                Map<String, QueryNode> innerMap = identificationMapForBoostQueries.get(boost);
                                if (innerMap.containsKey(fieldName)) {
                                    QueryNode representative = innerMap.get(fieldName);
                                    // add child to list of respective representative
                                    queryNodeGroups.get(representative).add(child);
                                } else {
                                    // child is the first BoostQuery with this field name -> gets a representative
                                    innerMap.put(fieldName, child);

                                    // make a new list for all nodes with same field and same boost factor
                                    queryNodeGroups.put(child, new ArrayList<>());
                                }
                            } else {
                                /* we don't have a QueryNode with that boost yet*/

 /* set up the identification maps */
                                Map<String, QueryNode> newInnerMap = new HashMap<>();
                                newInnerMap.put(fieldName, child);
                                identificationMapForBoostQueries.put(boost, newInnerMap);

                                /* make a new list for all nodes with the same field and same boost factor */
                                queryNodeGroups.put(child, new ArrayList<>());
                            }
                            break;
                        }
                        case TERM:
                        case PHRASE: {
                            /* all query types except BoostQuery */
                            String fieldName = child.getFieldName();
                            if (identificationMap.containsKey(queryType)) {
                                /* we have already seen a node of this type */
                                Map<String, QueryNode> innerMap = identificationMap.get(queryType);
                                if (innerMap.containsKey(fieldName)) {
                                    /* there is a node with the same field name */
                                    QueryNode representative = innerMap.get(fieldName);

                                    /* add child to list of nodes with same type and field name */
                                    queryNodeGroups.get(representative).add(child);
                                } else {
                                    /* first node with this field name*/
                                    innerMap.put(fieldName, child);
                                    queryNodeGroups.put(child, new ArrayList<>());
                                }
                            } else {
                                Map<String, QueryNode> newInnerMap = new HashMap<>();
                                newInnerMap.put(fieldName, child);
                                identificationMap.put(queryType, newInnerMap);

                                queryNodeGroups.put(child, new ArrayList<>());
                            }
                            break;
                        }
                        default:
                        /* we don't want to match unknown query types*/
                    }
                }
            }
        }
        return queryNodeGroups;
    }

    /*
    * @param trans
    * @param typeOfChildren 
    * @param moreThanOneOriginalNode
    * @param boost the boost factor, only needed for BoostQueries
    * @param typeOfWrappedQuery the type of the wrapped query, only needed for BoostQueries
     */
    private List<QueryNode> buildNewChildren(Translation trans,
            QueryNode.QueryType typeOfChildren, boolean moreThanOneOriginalNode,
            float boost, QueryNode.QueryType typeOfWrappedQuery) {
        // key: field name, value: trans
        Map<String, String> translations = trans.getTranslations();
        String fieldName = trans.getOriginalFieldName();
        List<QueryNode> newNodes = new ArrayList<>();

        for (Map.Entry<String, String> translation : translations.entrySet()) {
            String translationString = translation.getValue();
            String translationFieldName = fieldName;
            if (trans.isLanguageSpecificFieldName(translation.getKey())) {
                translationFieldName = translation.getKey();
            }
            switch (typeOfChildren) {
                case TERM:
                    if (moreThanOneOriginalNode) {
                        String[] tokens = translationString.split("\\s+");
                        if (tokens.length > 1) {
                            /* if we have more than one token, we need an additional
                            parent, since we want the translation itself to have
                            occurrence level SHOULD, but all the tokens then should
                            have occurrence level MUST, because this method is only
                            called for translation of strings concatenated from queries
                            with occurrence level MUST*/
                            QueryNode parentOfNewNodes = new QueryNode(QueryNode.QueryType.BOOLEAN, nodeIdCounter);
                            nodeIdCounter++;
                            parentOfNewNodes.setOccurrenceLevel(BooleanClause.Occur.SHOULD);
                            for (String token : tokens) {
                                QueryNode newNode = buildNewChild(typeOfChildren, translationFieldName, token, BooleanClause.Occur.MUST);
                                parentOfNewNodes.addChild(newNode);
                            }
                            newNodes.add(parentOfNewNodes);
                        } else {
                            QueryNode newNode = buildNewChild(typeOfChildren, translationFieldName, translationString, BooleanClause.Occur.SHOULD);
                            newNodes.add(newNode);
                        }
                    } else {
                        QueryNode newNode = buildNewChild(typeOfChildren, translationFieldName, translationString, BooleanClause.Occur.SHOULD);
                        newNodes.add(newNode);
                    }
                    break;
                case BOOST:
                    if (moreThanOneOriginalNode) {
                        LOG.warn("Translations of BoostQuery nodes are not expected"
                                + " to have more than one original node if the "
                                + "BoostQuery was directly translated.");
                    } else {
                        QueryNode newNode = new QueryNode(typeOfChildren, nodeIdCounter);
                        nodeIdCounter++;
                        newNode.setBoost(boost);
                        QueryNode wrappedQuery = buildNewChild(typeOfWrappedQuery,
                                translationFieldName, translationString, null);
                        newNode.addChild(wrappedQuery);
                        newNodes.add(newNode);
                    }
                    break;
                default:
                    QueryNode newNode = buildNewChild(typeOfChildren, translationFieldName, translationString, BooleanClause.Occur.SHOULD);
                    newNodes.add(newNode);
                    break;
            }
        }
        return newNodes;
    }

    private QueryNode buildNewChild(QueryNode.QueryType typeOfChild, String fieldName, String text, BooleanClause.Occur occLvl) {
        QueryNode newNode = new QueryNode(typeOfChild, nodeIdCounter);
        nodeIdCounter++;
        newNode.setFieldName(fieldName);
        newNode.setText(text);
        newNode.setOccurrenceLevel(occLvl);
        return newNode;
    }

    private boolean hasToBeTranslated(String fieldName) {
        return (laFieldNames.containsKey(fieldName)
                || fieldName.equalsIgnoreCase("text")
                || fieldName.equalsIgnoreCase("SW"));
    }

    public QueryNode simplify(QueryNode toSimplify) {
        if (toSimplify.getType().equals(QueryNode.QueryType.BOOLEAN)) {
            List<QueryNode> oldChildren = toSimplify.getChildren();
            List<Integer> indicesOfChildrenToRemove = new ArrayList<>();
            List<QueryNode> newChildren = new ArrayList<>();
            if (oldChildren.size() > 1) {
                Map<Integer, QueryNode> compulsoryBooleanChildren = new HashMap<>();
                for (int i = 0; i < oldChildren.size(); i++) {
                    QueryNode child = oldChildren.get(i);
                    if (child.getOccurrenceLevel().equals(BooleanClause.Occur.MUST)
                            && child.getType().equals(QueryNode.QueryType.BOOLEAN)) {
                        compulsoryBooleanChildren.put(i, child);
                    }
                }
                for (Map.Entry<Integer, QueryNode> entry : compulsoryBooleanChildren.entrySet()) {
                    int index = entry.getKey();
                    QueryNode compulsoryBooleanChild = entry.getValue();
                    List<QueryNode> grandChildren = compulsoryBooleanChild.getChildren();
                    Map<Integer, QueryNode> compulsoryGrandChildren = new TreeMap<>();
                    for (int i = 0; i < grandChildren.size(); i++) {
                        QueryNode grandChild = grandChildren.get(i);
                        if (grandChild.getOccurrenceLevel().equals(BooleanClause.Occur.MUST)) {
                            compulsoryGrandChildren.put(i, grandChild);
                        }
                    }
                    if (compulsoryGrandChildren.keySet().size() == grandChildren.size()) {
                        // all children are compulsory -> we can delete the parent node
                        indicesOfChildrenToRemove.add(index);
                    } else {
                        /* if we sort the keys in descending order, we can 
                        simply remove the compulsory children from behind, 
                        otherwise we would have to adapt the indices since they
                        change when we remove a preceding element*/
                        List<Integer> keyList = new ArrayList(compulsoryGrandChildren.keySet());
                        Collections.sort(keyList, Collections.reverseOrder());
                        for (Integer indexOfCompulsoryGrandChild : keyList) {
                            compulsoryBooleanChild.removeChildAtIndex(indexOfCompulsoryGrandChild);
                        }
                    }
                    for (QueryNode compulsoryGrandChild : compulsoryGrandChildren.values()) {
                        toSimplify.addChild(simplify(compulsoryGrandChild));
                    }
                }
                Collections.sort(indicesOfChildrenToRemove, Collections.reverseOrder());
                for (Integer indexOfChildToRemove : indicesOfChildrenToRemove) {
                    toSimplify.removeChildAtIndex(indexOfChildToRemove);
                }
            } else {
                QueryNode onlyChild = toSimplify.getChildAtIndex(0);
                toSimplify.replaceChildAtIndex(0, simplify(onlyChild));
            }
        }
        // no simplification for DisjunctionMaxQuery, PhraseQuery, TermQuery and unhandled instance types
        return toSimplify;
    }
    
    /* needed for the tests*/
    public void setHasSeenFirstQuery(){
        hasSeenFirstQuery = true;
    }
    
    public boolean hasSeenFstQuery(){
        return hasSeenFirstQuery;
    }
    
    private void resetAllQueryLevelBits(){
        entireCopyAtQueryLevel = true;
        singularAtQueryLevel = true;
        meshAtQueryLevel = true;
        backoffAtQueryLevel = true;
    }

    @Override
    public Query manipulateQuery(Query query) {        
        
        LOG.debug("Query instance type: " + query.getClass().getSimpleName());
        QueryNode qn = buildQueryNode(query, null);
        QueryNode simplifiedQN = simplify(qn);
        QueryNode newQN = translateQueryNode(simplifiedQN);
                

        
        if (entireCopyAtQueryLevel){
            entireCopyQueryLevel += 1;
        } else if (singularAtQueryLevel){
            singularUsageQueryLevel += 1;
        } else if (meshAtQueryLevel){
            meshUsageQueryLevel += 1;
        } else if (backoffAtQueryLevel){
            backoffUsageQueryLevel += 1;
        }
        
        resetAllQueryLevelBits();        

        return newQN.buildQuery();
    }

    public List<QueryNode> translateWrappedQueryOfBoostQuery(QueryNode wrappedQuery, QueryNode.QueryType wqType, QueryNode bq) {
        List<QueryNode> newChildren = new ArrayList<>();
        switch (wqType) {
            case BOOLEAN:
            case DISJUNCTIONMAX:
                bq.removeChildAtIndex(0);
                bq.addChild(translateQueryNode(wrappedQuery));
                break;
            default:
                LOG.debug("Wrapped query of BoostQuery: " + wrappedQuery.buildQuery().toString());
                Translation trans = translate(wrappedQuery.getText(), wrappedQuery.getFieldName());
                List<QueryNode> newNodes = buildNewChildren(trans, bq.getType(), false, bq.getBoost(), wrappedQuery.getType());
                newChildren.addAll(newNodes);
                break;
        }
        return newChildren;
    }

    public class QueryNodeComparator implements Comparator<QueryNode> {

        public int compare(QueryNode qn1, QueryNode qn2) {
            return qn1.getId() - qn2.getId();
        }
    }

}
