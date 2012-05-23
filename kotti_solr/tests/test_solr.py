

def test_access_solr_schema(solr):
    assert 'title' in solr.schema.fields
