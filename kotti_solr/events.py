from sunburnt import SolrInterface
from kotti.util import extract_from_settings


def add_document_handler(event):
    solr_url = extract_from_settings('kotti_solr.').get('solr_url')
    si = SolrInterface(solr_url)
    doc = event.object
    si.add(dict(
            id=u'%s-%s' % (doc.type, doc.id),
            title=doc.title,
            description=doc.description,
            text=doc.body,
            last_modified=doc.modification_date.isoformat(),
            ))
    si.optimize()
