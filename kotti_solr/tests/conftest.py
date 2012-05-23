from mr.laforge import up, waitforports, shutdown
from sunburnt import SolrInterface


settings = {
    'kotti.site_title': 'My Kotti Solr-ized site',
    'kotti.secret': 'qwerty',
    'pyramid.includes': 'kotti_solr',
    'sqlalchemy.url': 'sqlite:///%(here)s/Kotti.db',
    'kotti_solr.solr_url': 'http://localhost:8983/solr',
}


def pytest_funcarg__solr(request):
    def setup():
        up('solr')
        waitforports(8983)      # wait for Solr to start up
        request.addfinalizer(shutdown)
        return SolrInterface(settings['kotti_solr.solr_url'])
    return request.cached_setup(setup=setup, scope='session')
