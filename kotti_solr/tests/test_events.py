from kotti.resources import Document, get_root
from datetime import datetime
from mock import Mock


class EventRequest(object):
    def resource_path(self, object):
        return '/path/'


class EventMock(Mock):
    def __init__(self, object):
        super(EventMock, self).__init__(object=object)
        self.request = EventRequest()


def test_index_document(solr, db_session):
    doc = Document(title='foo', body=u'bar!', modification_date=datetime.now())
    doc.id = 23     # we don't really add the object yet...
    from kotti_solr.events import add_document_handler
    add_document_handler(event=EventMock(object=doc))
    results = list(solr.query(title='foo'))
    assert len(results) == 1
    assert results[0]['id'] == 'document-23'


def test_add_document_triggers_indexing(solr, db_session):
    get_root()['doc'] = Document(title='foo', body=u'bar!', description='foo!')
    db_session.flush()
    results = list(solr.query(title='foo'))
    assert len(results) == 1
    assert results[0]['description'] == 'foo!'
