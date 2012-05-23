from mr.laforge import up, waitforports, shutdown
from sunburnt import SolrInterface


def pytest_funcarg__solr(request):
    def setup():
        up('solr')
        waitforports(8983)      # wait for Solr to start up
        request.addfinalizer(shutdown)
        return SolrInterface('http://localhost:8983/solr')
    return request.cached_setup(setup=setup, scope='session')
