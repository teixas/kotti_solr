from kotti.resources import Document
from datetime import datetime
from mock import Mock


def test_index_document(solr, db_session):
    doc = Document(title='foo', body=u'bar!', modification_date=datetime.now())
    doc.id = 23     # we don't really add the object yet...
    from kotti_solr.events import add_document_handler
    add_document_handler(event=Mock(object=doc))
    results = list(solr.query(title='foo'))
    assert len(results) == 1
    assert results[0]['id'] == 'document-23'
