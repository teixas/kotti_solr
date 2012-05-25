from kotti import get_settings

from sunburnt import SolrInterface


def get_solr(url=None):
    """ return a `SolrInterface` instance using the `solr_url` setting """
    if url is None:
        url = get_settings()['kotti_solr.solr_url']
    return SolrInterface(url)


def get_default_results(search_term=u'', request=None):
    return list(get_solr().query(default=search_term))


def kotti_configure(settings):
    settings['kotti.search_content'] = 'kotti_solr.get_default_results'


def includeme(config):
    from kotti.events import objectevent_listeners
    from kotti.events import ObjectDelete
    from kotti.events import ObjectUpdate
    from kotti.resources import Document

    from kotti_solr.events import ObjectAfterInsert
    from kotti_solr.events import add_document_handler
    from kotti_solr.events import delete_document_handler
    from kotti_solr.events import update_document_handler
    from kotti_solr.events import wire_sqlalchemy

    wire_sqlalchemy()
    objectevent_listeners[(ObjectAfterInsert, Document)].append(
        add_document_handler)
    objectevent_listeners[(ObjectUpdate, Document)].append(
        update_document_handler)
    objectevent_listeners[(ObjectDelete, Document)].append(
        delete_document_handler)
