==========
kotti_solr
==========

.. image:: https://pypip.in/version/kotti_solr/badge.svg
    :target: https://pypi.python.org/pypi/kotti_solr/
    :alt: Latest Version

This is an extension for `Kotti`_ that provides integration with
`Solr`_ search engine.

When this extension is active, it will automatically post updates to a Solr instance when documents are added, modified, or deleted. It will also make a search in Kotti query the Solr instance. 

Setup
-----

1. `pip install kotti_solr`. 
2. Set the Solr instance URL with the ``kotti_solr.solr_url`` configuration setting. 
3. Add `kotti_solr.kotti_configure` to `kotti.configurators`. 


.. _Kotti: http://pypi.python.org/pypi/Kotti
.. _Solr: http://lucene.apache.org/solr/
