from kotti import get_settings
from kotti.events import ObjectInsert
from kotti.events import objectevent_listeners
from kotti.resources import Document

from kotti_solr.events import add_document_handler
from sunburnt import SolrInterface


def get_solr(url=None):
    """ return a `SolrInterface` instance using the `solr_url` setting """
    if url is None:
        url = get_settings()['kotti_solr.solr_url']
    return SolrInterface(url)


def includeme(config):
    objectevent_listeners[(ObjectInsert, Document)].append(
        add_document_handler)
