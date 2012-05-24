from kotti_solr import get_solr


def add_document_handler(event):
    si = get_solr()
    doc = event.object
    request = event.request
    data = dict(
            id=u'%s-%s' % (doc.type, doc.id),
            title=doc.title,
            description=doc.description,
            text=doc.body,
            last_modified=doc.modification_date,
            )
    if request is not None:
        data['path'] = request.resource_path(doc)
    si.add(data)
    si.optimize()
