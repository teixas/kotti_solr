import sqlalchemy.event
from sqlalchemy.orm import mapper
from pyramid.request import Request
from pyramid.threadlocal import get_current_request

from kotti.events import notify
from kotti.events import ObjectEvent
from kotti_solr import get_solr

_WIRED_SQLALCHMEY = False


class ObjectAfterInsert(ObjectEvent):
    pass


def _after_insert(mapper, connection, target):
    notify(ObjectAfterInsert(target, get_current_request()))


def wire_sqlalchemy():  # pragma: no cover
    global _WIRED_SQLALCHMEY
    if _WIRED_SQLALCHMEY:
        return
    else:
        _WIRED_SQLALCHMEY = True
    sqlalchemy.event.listen(mapper, 'after_insert', _after_insert)


def add_document_handler(event):
    si = get_solr()
    doc = event.object
    request = event.request
    data = {}
    for field in si.schema.fields:
        value = getattr(doc, field, None)
        if value is not None:
            data[field] = value
    data['id'] = u'%s-%s' % (doc.type, doc.id)      # TODO: discuss! :)
    if request is None:
        request = Request.blank('/')
    data['path'] = request.resource_path(doc)
    si.add(data)
    si.optimize()


def update_document_handler(event):
    # Since when a document with the same ID is overrided we don't
    # need to delete by hand or else we just use code below:
    #
    # si = get_solr()
    # doc = event.object
    # si.delete(doc.id)
    #
    add_document_handler(event)


def delete_document_handler(event):
    si = get_solr()
    doc = event.object
    si.delete(u'%s-%s' % (doc.type, doc.id))
    si.optimize()
