from datetime import datetime, timedelta
from mock import Mock

from kotti.resources import Document, get_root
from kotti_solr.events import add_document_handler


def test_index_document(solr, db_session):
    now = datetime.now()
    doc = Document(title='foo', body=u'bar!', modification_date=now)
    doc.id = 23     # we don't really add the object yet...
    request = Mock(resource_path=lambda _: '/path/')
    add_document_handler(event=Mock(object=doc, request=request))
    results = list(solr.query(title='foo'))
    assert len(results) == 1
    assert results[0]['id'] == 'document-23'
    assert results[0]['path'] == '/path/'
    # Solr's date values don't take microseconds into account...
    assert abs(results[0]['modification_date'] - now) < timedelta(milliseconds=1)


def test_add_document_triggers_indexing(solr, db_session, request):
    get_root()['doc'] = Document(title=u'foo', body=u'bar!', description=u'foo!')
    db_session.flush()
    results = list(solr.query(title='foo'))
    assert len(results) == 1
    assert results[0]['id'] == u'document-2'
    assert results[0]['description'] == 'foo!'
    assert results[0]['path'] == request.resource_path(get_root()['doc'])


def test_index_document_without_request(solr):
    doc = Document(title='No request', body=u'There is no request',)
    doc.id = 33
    add_document_handler(event=Mock(object=doc, request=None))
    results = list(solr.query(title='No request'))
    assert len(results) == 1
    assert results[0]['id'] == 'document-33'
    assert results[0]['path'] == '/'


def test_populate_triggers_indexing(solr, db_session):
    get_root()['bar'] = Document(title=u'bar', description=u'blah!')
    db_session.flush()
    results = list(solr.query(title='bar'))
    assert len(results) == 1
    assert results[0]['id'] == 'document-2'
    assert results[0]['description'] == u'blah!'
    assert results[0]['path'] == u'/bar/'
