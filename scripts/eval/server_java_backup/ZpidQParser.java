package de.zpid.pubpsych.search.query.queryparsers;

import de.zpid.pubpsych.search.query.queryparsers.fieldrewriters.FieldRewriteInterface;
import de.zpid.pubpsych.search.query.queryparsers.fieldrewriters.QueryFieldRewriter;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import org.apache.lucene.search.*;
import org.apache.solr.common.params.SolrParams;
import org.apache.solr.request.SolrQueryRequest;
import org.apache.solr.search.ExtendedDismaxQParser;
import org.apache.solr.search.SyntaxError;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;

/**
 * ZPID extensions of the Solr default edismax parser
 */
public class ZpidQParser extends ExtendedDismaxQParser {

    private static final Logger LOG = LoggerFactory.getLogger(ZpidQParser.class);

    private ArrayList<FieldRewriteInterface> fieldRewriters = null;
    
    // get the file reference
    private Path transPath = Paths.get("/home/sohe01/evaluations/translations.txt");
    private Path statsPath = Paths.get("/home/sohe01/evaluations/stats.txt");

    ZpidQParser(String qstr, SolrParams localParams, SolrParams params, SolrQueryRequest req, ArrayList<FieldRewriteInterface> fieldRewriters) {
        super(qstr, localParams, params, req);
        this.fieldRewriters = fieldRewriters;
        LOG.debug("Original query: " + qstr);
    }
        
    @Override
    public Query parse() throws SyntaxError {
        Query query = super.parse();
        LOG.debug("Parsed query: " + query.toString("text"));
        for (FieldRewriteInterface curRewriter: this.fieldRewriters) {
            LOG.debug("Applying FieldRewriter {} on query {}.", curRewriter.getClass().getSimpleName(), query.toString());
            query = curRewriter.manipulateQuery(query);
            if (curRewriter.getClass().getSimpleName().equals("QueryFieldRewriter")){
                QueryFieldRewriter qfr = ((QueryFieldRewriter) curRewriter);
                
                /*Reset seenStrings, since we only want to ignore reoccurring 
                strings within in the same query, not between queries. */
                qfr.resetSeenStrings();
                
                // ignore warm-up query
                if (! qfr.hasSeenFstQuery()){
                    qfr.setHasSeenFirstQuery();
                }
                
                else {
                    //Use try-with-resource to get auto-closeable writer instance

                    try (BufferedWriter writer = Files.newBufferedWriter(transPath,
                            StandardCharsets.UTF_8, StandardOpenOption.APPEND))
                        {
                            LOG.debug("Writing translation to file: " + query.toString());
                            writer.write(query.toString());
                            writer.write("\n");
                        } catch (IOException ex) {
                        LOG.warn("Couldn't write translation to file, exception:", ex);
                    }

                    /* Since we do not know which query will be the last one, we'll 
                    just write the gathered statistics to file after each query.*/
                    try (BufferedWriter writer = Files.newBufferedWriter(statsPath))
                        {
                            LOG.debug("Writing statistics to file: " + query.toString());
                            writer.write("Mesh usage word level: " + 
                                    Integer.toString(qfr.getMeshUsageWordLevel()) + "\n");
                            writer.write("Mesh usage string level: " + 
                                    Integer.toString(qfr.getMeshUsageStringLevel()) + "\n");
                            writer.write("Mesh usage query level: " + 
                                    Integer.toString(qfr.getMeshUsageQueryLevel()) + "\n");
                            writer.write("Backoff usage word level: " + 
                                    Integer.toString(qfr.getBackoffUsageWordLevel()) + "\n");
                            writer.write("Backoff usage string level: " + 
                                    Integer.toString(qfr.getBackoffUsageStringLevel()) + "\n");
                            writer.write("Backoff usage query level: " + 
                                    Integer.toString(qfr.getBackoffUsageQueryLevel()) + "\n");
                            writer.write("Number of entire copies at query level:" + 
                                    Integer.toString(qfr.getNumEntireCopyQueryLevel()) + "\n");
                            writer.write("Number of entire copies at string level: " + 
                                    Integer.toString(qfr.getNumEntireCopyStringLevel()) + "\n");
                            writer.write("Number of partial copies at string level: " + 
                                    Integer.toString(qfr.getNumPartialCopyStringLevel()) + "\n");
                            writer.write("Number of copies at word level: " + 
                                    Integer.toString(qfr.getNumCopyWordLevel()) + "\n");
                            writer.write("Singular usage word level: " + 
                                    Integer.toString(qfr.getSingularUsageWordLevel()) + "\n");
                            writer.write("Singular usage string level: " + 
                                    Integer.toString(qfr.getSingularUsageStringLevel()) + "\n");
                            writer.write("Singular usage query level: " + 
                                    Integer.toString(qfr.getSingularUsageQueryLevel()) + "\n"); 
                        } catch (IOException ex) {
                        LOG.warn("Couldn't write statistics to file, exception:", ex);
                    }
                }
            }
        }
        return query;
    }


}
