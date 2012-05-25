from datetime import datetime, timedelta
from mock import Mock

from kotti.resources import Document, get_root
from kotti_solr.events import add_document_handler
from kotti_solr.events import delete_document_handler
from kotti_solr.events import update_document_handler


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


def test_update_document(solr, db_session):
    doc = Document(title=u'foo', description=u'foo!')
    doc.id = 3
    request = Mock(resource_path=lambda _: '/path/')
    add_document_handler(event=Mock(object=doc, request=request))
    results = list(solr.query(title='foo'))
    assert len(results) == 1
    assert results[0]['id'] == 'document-3'
    assert results[0]['description'] == u'foo!'
    doc.description = u'bar!'
    update_document_handler(event=Mock(object=doc, request=request))
    results = list(solr.query(title='foo'))
    assert len(results) == 1
    assert results[0]['id'] == 'document-3'
    assert results[0]['description'] == u'bar!'


def test_update_document_triggers_reindexing(solr, db_session, request):
    get_root()['doc'] = Document(title=u'bar', description=u'bar!')
    db_session.flush()
    results = list(solr.query(title='bar'))
    assert len(results) == 1
    assert results[0]['id'] == u'document-2'
    assert results[0]['description'] == 'bar!'
    assert results[0]['path'] == request.resource_path(get_root()['doc'])
    get_root()['doc'].description = u'blah!'
    db_session.flush()
    results = list(solr.query(title='bar'))
    assert len(results) == 1
    assert results[0]['id'] == u'document-2'
    assert results[0]['description'] == 'blah!'
    assert results[0]['path'] == request.resource_path(get_root()['doc'])


def test_delete_document(solr, db_session):
    doc = Document(title=u'delete-me', description=u'foo!')
    doc.id = 3
    request = Mock(resource_path=lambda _: '/path/')
    add_document_handler(event=Mock(object=doc, request=request))
    results = list(solr.query(title='delete-me'))
    assert len(results) == 1
    assert results[0]['id'] == 'document-3'
    assert results[0]['description'] == u'foo!'
    delete_document_handler(event=Mock(object=doc, request=request))
    results = list(solr.query(title='delete-me'))
    assert len(results) == 0


def test_delete_document_triggers_unindexing(solr, db_session, request):
    get_root()['doc'] = Document(title=u'delete-me', description=u'bar!')
    db_session.flush()
    results = list(solr.query(title='delete-me'))
    assert len(results) == 1
    assert results[0]['id'] == u'document-2'
    assert results[0]['description'] == 'bar!'
    del(get_root()['doc'])
    db_session.flush()
    results = list(solr.query(title='delete-me'))
    assert len(results) == 0
