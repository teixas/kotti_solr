from kotti.events import ObjectInsert
from kotti.events import objectevent_listeners
from kotti.resources import Document

from kotti_solr.events import add_document_handler


def includeme(config):
    objectevent_listeners[(ObjectInsert, Document)].append(
        add_document_handler)
