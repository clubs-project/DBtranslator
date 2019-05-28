package de.zpid.pubpsych.search.query.queryparsers;

import de.zpid.pubpsych.search.query.queryparsers.fieldrewriters.FieldRewriteInterface;
import de.zpid.pubpsych.search.query.queryparsers.fieldrewriters.LaFieldRewriter;
import de.zpid.pubpsych.search.query.queryparsers.fieldrewriters.QueryFieldRewriter;
import java.io.IOException;
import org.apache.solr.common.params.SolrParams;
import org.apache.solr.request.SolrQueryRequest;
import org.apache.solr.search.QParser;
import org.apache.solr.search.QParserPlugin;

import java.util.ArrayList;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * One instance of ZpidQParserPlugin is created when the core is loaded. It creates a QParser object for each incoming request.
 * Loading required resources should happen here to avoid a reload for every request.
 */
public class ZpidQParserPlugin extends QParserPlugin {
    
    private static final Logger LOG = LoggerFactory.getLogger(ZpidQParserPlugin.class);

    ArrayList<FieldRewriteInterface> FieldRewriterList = new ArrayList<>();

    //set up all field rewriters just once
    public ZpidQParserPlugin() {
        FieldRewriterList.add(new LaFieldRewriter());
        LOG.debug("Added LAFieldRewriter");
        try {            
            String meshDict = "queryfieldrewriter/meshSplit2.solr.non-diff."
                    + "all-languages.txt";
            String mixedDict = "queryfieldrewriter/wp.WPcat.untradDEallkeys.dictkeys.solr.non-diff.all-languages.txt";
            String laFieldNamesFile = "queryfieldrewriter/language_specific_fie"
                    + "ld_names.txt";
            FieldRewriterList.add(new QueryFieldRewriter(meshDict, 
                    mixedDict, laFieldNamesFile));
            LOG.debug("Successfully added QueryFieldRewriter to FieldRewriterL"
                    + "ist.");
        } catch (IOException ex) {
            LOG.warn("Could not load dictionary for query translation, thus "
                            + "queries won't be translated", ex);
            LOG.debug("Current directory: " + System.getProperty("user.dir"));
        }
    }

    @Override
    public QParser createParser(String qstr, SolrParams localParams, SolrParams params, SolrQueryRequest req) {
        return new ZpidQParser(qstr, localParams, params, req, FieldRewriterList);
    }
}
