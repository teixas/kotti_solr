from pyramid.request import Request

from kotti_solr import get_solr


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
