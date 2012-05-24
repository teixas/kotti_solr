

def test_access_solr_schema(solr):
    assert 'title' in solr.schema.fields


def test_get_solr_helper(solr, db_session):
    from kotti_solr import get_solr
    assert 'title' in get_solr().schema.fields
