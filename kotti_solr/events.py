from kotti_solr import get_solr


def add_document_handler(event):
    si = get_solr()
    doc = event.object
    si.add(dict(
            id=u'%s-%s' % (doc.type, doc.id),
            title=doc.title,
            description=doc.description,
            text=doc.body,
            last_modified=doc.modification_date.isoformat(),
            ))
    si.optimize()
