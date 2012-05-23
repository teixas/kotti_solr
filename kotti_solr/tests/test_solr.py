from sunburnt import SolrInterface


def test_access_solr_schema(solr):
    solr = SolrInterface('http://localhost:8983/solr')
    assert 'title' in solr.schema.fields
